"""Testes de integração da autenticação — RF02, RN05, RNF02, RNF13.

IC: GYM-TST-003 · Plano de Testes (GYM-TST-001), seção 4.3 · Casos de teste CT01, CT02 e CT12.
"""

from conftest import API, auth


# TI-AUTH-01 — CT01: login válido
def test_login_admin_sucesso(login, admin_credenciais):
    resposta = login(*admin_credenciais)

    assert resposta.status_code == 200
    dados = resposta.get_json()
    assert dados["token"]
    assert dados["expira_em"]
    assert dados["usuario"]["perfil"] == "ADMIN"
    assert "senha_hash" not in dados["usuario"]


# TI-AUTH-02 — CT02: senha incorreta (asserção restrita a 401, Plano de Testes 3.2.1)
def test_login_senha_incorreta(login, admin_credenciais):
    email, _ = admin_credenciais
    resposta = login(email, "senha-errada-123")

    assert resposta.status_code == 401
    assert resposta.get_json()["erro"] == "E-mail ou senha inválidos."


def test_login_email_inexistente_mesma_mensagem(login):
    resposta = login("ninguem@teste.local", "Senha1234")

    assert resposta.status_code == 401
    assert resposta.get_json()["erro"] == "E-mail ou senha inválidos."


# TI-AUTH-03 — campos obrigatórios
def test_login_sem_email(client):
    resposta = client.post(f"{API}/auth/login", json={"senha": "Senha1234"})
    assert resposta.status_code == 400


def test_login_sem_senha(client, admin_credenciais):
    resposta = client.post(f"{API}/auth/login", json={"email": admin_credenciais[0]})
    assert resposta.status_code == 400


# TI-AUTH-04 — RN05: usuário inativo não autentica
def test_login_usuario_inativo(client, login, token_admin, criar_instrutor):
    instrutor = criar_instrutor()
    client.delete(f"{API}/usuarios/{instrutor['usuario']['id']}", headers=auth(token_admin))

    resposta = login(instrutor["email"], instrutor["senha"])

    assert resposta.status_code == 403
    assert resposta.get_json()["erro"] == "Usuário inativo."


# TI-AUTH-05 — RNF02: rota protegida sem token
def test_rota_protegida_sem_token(client):
    assert client.get(f"{API}/fichas").status_code == 401


# TI-AUTH-06 — RNF13: token inválido
def test_rota_protegida_com_token_invalido(client):
    assert client.get(f"{API}/fichas", headers=auth("token-inventado")).status_code == 401


# TI-AUTH-07 — RNF13: logout encerra a sessão
def test_logout_invalida_o_token(client, token_de, admin_credenciais):
    token = token_de(*admin_credenciais)
    assert client.get(f"{API}/fichas", headers=auth(token)).status_code == 200

    assert client.post(f"{API}/auth/logout", headers=auth(token)).status_code == 204
    assert client.get(f"{API}/fichas", headers=auth(token)).status_code == 401


# TI-AUTH-08 — RN05/RNF13: inativação encerra as sessões abertas
def test_inativacao_encerra_sessao(client, token_admin, criar_instrutor):
    instrutor = criar_instrutor()
    assert client.get(f"{API}/alunos", headers=auth(instrutor["token"])).status_code == 200

    client.delete(f"{API}/usuarios/{instrutor['usuario']['id']}", headers=auth(token_admin))

    assert client.get(f"{API}/alunos", headers=auth(instrutor["token"])).status_code == 401
