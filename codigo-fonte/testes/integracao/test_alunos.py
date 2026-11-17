"""Testes de integração de alunos — RF01, RN05.

IC: GYM-TST-003 · Plano de Testes (GYM-TST-001), seção 4.3 · Caso de teste CT05.
"""

from conftest import API, SENHA_PADRAO, auth, unico


def _novo(**campos):
    corpo = {"nome": "Aluno Novo", "email": f"{unico('aluno')}@teste.local", "senha": SENHA_PADRAO}
    corpo.update(campos)
    return corpo


# TI-ALU-01 — CT05: cadastrar, consultar e editar
def test_cadastrar_consultar_e_editar_aluno(client, instrutor):
    cabecalho = auth(instrutor["token"])
    corpo = _novo(telefone="92999990000", data_nascimento="2000-05-10")

    criado = client.post(f"{API}/alunos", json=corpo, headers=cabecalho)
    assert criado.status_code == 201
    dados = criado.get_json()
    assert dados["perfil"] == "ALUNO"
    assert dados["ativo"] is True
    assert dados["data_nascimento"] == "2000-05-10"

    consultado = client.get(f"{API}/alunos/{dados['id']}", headers=cabecalho)
    assert consultado.status_code == 200
    assert consultado.get_json()["email"] == corpo["email"]

    editado = client.put(f"{API}/alunos/{dados['id']}", json={"nome": "Aluno Editado"}, headers=cabecalho)
    assert editado.status_code == 200
    assert editado.get_json()["nome"] == "Aluno Editado"


# TI-ALU-02 — campo obrigatório ausente
def test_cadastro_sem_nome(client, instrutor):
    resposta = client.post(f"{API}/alunos", json=_novo(nome=""), headers=auth(instrutor["token"]))

    assert resposta.status_code == 400
    assert resposta.get_json()["campo"] == "nome"


def test_email_de_aluno_duplicado(client, instrutor, aluno):
    resposta = client.post(f"{API}/alunos", json=_novo(email=aluno["email"]), headers=auth(instrutor["token"]))
    assert resposta.status_code == 409


# TI-ALU-03 — busca por nome ou e-mail
def test_busca_por_nome_e_por_email(client, instrutor):
    cabecalho = auth(instrutor["token"])
    nome = unico("Buscavel")
    corpo = _novo(nome=nome)
    assert client.post(f"{API}/alunos", json=corpo, headers=cabecalho).status_code == 201

    por_nome = client.get(f"{API}/alunos", query_string={"nome": nome}, headers=cabecalho).get_json()
    por_email = client.get(f"{API}/alunos", query_string={"nome": corpo["email"]}, headers=cabecalho).get_json()

    assert [a["email"] for a in por_nome] == [corpo["email"]]
    assert [a["email"] for a in por_email] == [corpo["email"]]


# TI-ALU-04 — aluno não acessa o cadastro de alunos
def test_aluno_nao_lista_alunos(client, aluno):
    assert client.get(f"{API}/alunos", headers=auth(aluno["token"])).status_code == 403


def test_sem_token_nao_lista_alunos(client):
    assert client.get(f"{API}/alunos").status_code == 401


# TI-ALU-05 — RN05: inativar e reativar
def test_inativar_e_reativar_aluno(client, instrutor, criar_aluno, login):
    cabecalho = auth(instrutor["token"])
    novo = criar_aluno()
    id_aluno = novo["usuario"]["id"]

    inativado = client.delete(f"{API}/alunos/{id_aluno}", headers=cabecalho)
    assert inativado.status_code == 200
    assert inativado.get_json()["ativo"] is False
    assert login(novo["email"], novo["senha"]).status_code == 403

    reativado = client.put(f"{API}/alunos/{id_aluno}", json={"ativo": True}, headers=cabecalho)
    assert reativado.status_code == 200
    assert reativado.get_json()["ativo"] is True
    assert login(novo["email"], novo["senha"]).status_code == 200


# TI-ALU-06 — recurso inexistente
def test_aluno_inexistente(client, instrutor):
    assert client.get(f"{API}/alunos/999999999", headers=auth(instrutor["token"])).status_code == 404


def test_instrutor_nao_e_tratado_como_aluno(client, instrutor, criar_instrutor):
    outro = criar_instrutor()
    resposta = client.get(f"{API}/alunos/{outro['usuario']['id']}", headers=auth(instrutor["token"]))
    assert resposta.status_code == 404
