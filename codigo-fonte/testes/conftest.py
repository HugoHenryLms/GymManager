"""Fixtures compartilhadas dos testes do GymManager.

ICs: GYM-TST-002 (unitários) e GYM-TST-003 (integração) · Plano de Testes (GYM-TST-001), seção 3.2.

Regras (Plano de Testes, seção 3.2):
- O banco do CI não é limpo entre os testes: cada teste cria os próprios dados,
  com e-mails e nomes únicos (uuid4), e não depende da ordem de execução.
- As credenciais do administrador vêm de ADMIN_EMAIL e ADMIN_SENHA, definidas
  no CI (RNF03). Nenhuma senha real é versionada.
"""

import os
import uuid

import pytest

from gymmanager import create_app

API = "/api/v1"
SENHA_PADRAO = "Senha1234"


def unico(prefixo: str = "t") -> str:
    """Sufixo único para nomes e e-mails de teste."""
    return f"{prefixo}-{uuid.uuid4().hex[:10]}"


def auth(token: str) -> dict:
    """Cabeçalho Authorization: Bearer <token>."""
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def app():
    return create_app({"TESTING": True})


@pytest.fixture
def client(app):
    with app.test_client() as cliente:
        yield cliente


@pytest.fixture
def login(client):
    """login(email, senha) -> resposta do POST /auth/login."""

    def _login(email: str, senha: str):
        return client.post(f"{API}/auth/login", json={"email": email, "senha": senha})

    return _login


@pytest.fixture
def token_de(login):
    """token_de(email, senha) -> token (falha o teste se o login não der 200)."""

    def _token(email: str, senha: str) -> str:
        resposta = login(email, senha)
        assert resposta.status_code == 200, resposta.get_json()
        return resposta.get_json()["token"]

    return _token


@pytest.fixture
def admin_credenciais():
    return os.getenv("ADMIN_EMAIL", "admin@ci.local"), os.getenv("ADMIN_SENHA", "ci-senha-admin1")


@pytest.fixture
def token_admin(token_de, admin_credenciais):
    return token_de(*admin_credenciais)


@pytest.fixture
def id_admin(login, admin_credenciais):
    return login(*admin_credenciais).get_json()["usuario"]["id"]


@pytest.fixture
def criar_instrutor(client, token_admin, token_de):
    """criar_instrutor() -> dict com usuario, email, senha e token do instrutor."""

    def _criar() -> dict:
        email = f"{unico('instrutor')}@teste.local"
        resposta = client.post(
            f"{API}/usuarios",
            json={"nome": "Instrutor Teste", "email": email, "senha": SENHA_PADRAO, "perfil": "INSTRUTOR"},
            headers=auth(token_admin),
        )
        assert resposta.status_code == 201, resposta.get_json()
        return {
            "usuario": resposta.get_json(),
            "email": email,
            "senha": SENHA_PADRAO,
            "token": token_de(email, SENHA_PADRAO),
        }

    return _criar


@pytest.fixture
def instrutor(criar_instrutor):
    return criar_instrutor()


@pytest.fixture
def criar_aluno(client, instrutor, token_de):
    """criar_aluno() -> dict com usuario, email, senha e token do aluno."""

    def _criar() -> dict:
        email = f"{unico('aluno')}@teste.local"
        resposta = client.post(
            f"{API}/alunos",
            json={"nome": "Aluno Teste", "email": email, "senha": SENHA_PADRAO},
            headers=auth(instrutor["token"]),
        )
        assert resposta.status_code == 201, resposta.get_json()
        return {
            "usuario": resposta.get_json(),
            "email": email,
            "senha": SENHA_PADRAO,
            "token": token_de(email, SENHA_PADRAO),
        }

    return _criar


@pytest.fixture
def aluno(criar_aluno):
    return criar_aluno()


@pytest.fixture
def criar_exercicio(client, instrutor):
    """criar_exercicio() -> exercício (dict) cadastrado pelo instrutor."""

    def _criar(grupo: str = "Peito") -> dict:
        resposta = client.post(
            f"{API}/exercicios",
            json={"nome": unico("Exercicio"), "grupo_muscular": grupo, "descricao": "Criado nos testes"},
            headers=auth(instrutor["token"]),
        )
        assert resposta.status_code == 201, resposta.get_json()
        return resposta.get_json()

    return _criar


@pytest.fixture
def criar_ficha(client, instrutor, criar_exercicio):
    """criar_ficha(aluno_id, qtd_exercicios=2, **campos) -> ficha (dict) criada pelo instrutor."""

    def _criar(aluno_id: int, qtd_exercicios: int = 2, **campos) -> dict:
        itens = [
            {"exercicio_id": criar_exercicio()["id"], "series": 3, "repeticoes": 12, "carga_kg": 20, "descanso_s": 60}
            for _ in range(qtd_exercicios)
        ]
        corpo = {"nome": unico("Ficha"), "aluno_id": aluno_id, "data_inicio": "2026-01-01", "exercicios": itens}
        corpo.update(campos)
        resposta = client.post(f"{API}/fichas", json=corpo, headers=auth(instrutor["token"]))
        assert resposta.status_code == 201, resposta.get_json()
        return resposta.get_json()

    return _criar
