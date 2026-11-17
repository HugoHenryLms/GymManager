"""Testes de integração de usuários e instrutores — RF06, RN03, RN08.

IC: GYM-TST-003 · Plano de Testes (GYM-TST-001), seção 4.3 · Casos de teste CT03, CT04 e CT12.
"""

import pytest

from conftest import API, SENHA_PADRAO, auth, unico


def _novo(perfil="INSTRUTOR", **campos):
    corpo = {"nome": "Usuário Teste", "email": f"{unico('usuario')}@teste.local", "senha": SENHA_PADRAO, "perfil": perfil}
    corpo.update(campos)
    return corpo


# TI-USU-01 — CT04: admin cadastra instrutor
def test_admin_cadastra_instrutor(client, token_admin):
    corpo = _novo()
    resposta = client.post(f"{API}/usuarios", json=corpo, headers=auth(token_admin))

    assert resposta.status_code == 201
    dados = resposta.get_json()
    assert dados["perfil"] == "INSTRUTOR"
    assert dados["ativo"] is True
    assert dados["email"] == corpo["email"]
    assert "senha" not in dados and "senha_hash" not in dados


# TI-USU-02 — e-mail duplicado (sem diferenciar maiúsculas)
def test_email_duplicado(client, token_admin):
    corpo = _novo()
    assert client.post(f"{API}/usuarios", json=corpo, headers=auth(token_admin)).status_code == 201

    repetido = dict(corpo, email=corpo["email"].upper())
    resposta = client.post(f"{API}/usuarios", json=repetido, headers=auth(token_admin))

    assert resposta.status_code == 409
    assert resposta.get_json()["campo"] == "email"


# TI-USU-03 — validação
@pytest.mark.parametrize("campos, campo", [({"senha": "fraca"}, "senha"), ({"perfil": "GERENTE"}, "perfil"), ({"nome": ""}, "nome")])
def test_dados_invalidos(client, token_admin, campos, campo):
    resposta = client.post(f"{API}/usuarios", json=_novo(**campos), headers=auth(token_admin))

    assert resposta.status_code == 400
    assert resposta.get_json()["campo"] == campo


# TI-USU-04 — RN03: instrutor não cadastra usuários
def test_instrutor_nao_cadastra_usuario(client, instrutor):
    resposta = client.post(f"{API}/usuarios", json=_novo(), headers=auth(instrutor["token"]))
    assert resposta.status_code == 403


# TI-USU-05 — RN03: aluno não lista usuários
def test_aluno_nao_lista_usuarios(client, aluno):
    assert client.get(f"{API}/usuarios", headers=auth(aluno["token"])).status_code == 403


# TI-USU-06 — RN08: admin não inativa a própria conta
def test_admin_nao_inativa_a_si_mesmo(client, token_admin, id_admin):
    assert client.delete(f"{API}/usuarios/{id_admin}", headers=auth(token_admin)).status_code == 409


# TI-USU-07 — RN08: admin não altera o próprio perfil
def test_admin_nao_altera_o_proprio_perfil(client, token_admin, id_admin):
    resposta = client.put(f"{API}/usuarios/{id_admin}", json={"perfil": "INSTRUTOR"}, headers=auth(token_admin))
    assert resposta.status_code == 409


# TI-USU-08 — edição, inativação e reativação
def test_editar_inativar_e_reativar_instrutor(client, token_admin, criar_instrutor, login):
    instrutor = criar_instrutor()
    id_usuario = instrutor["usuario"]["id"]

    editado = client.put(f"{API}/usuarios/{id_usuario}", json={"nome": "Nome Editado"}, headers=auth(token_admin))
    assert editado.status_code == 200
    assert editado.get_json()["nome"] == "Nome Editado"

    inativado = client.delete(f"{API}/usuarios/{id_usuario}", headers=auth(token_admin))
    assert inativado.status_code == 200
    assert inativado.get_json()["ativo"] is False

    reativado = client.put(f"{API}/usuarios/{id_usuario}", json={"ativo": True}, headers=auth(token_admin))
    assert reativado.status_code == 200
    assert reativado.get_json()["ativo"] is True
    assert login(instrutor["email"], instrutor["senha"]).status_code == 200


def test_usuario_inexistente(client, token_admin):
    assert client.put(f"{API}/usuarios/999999999", json={"nome": "X Y"}, headers=auth(token_admin)).status_code == 404
