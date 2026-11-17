"""Testes de integração do catálogo de exercícios — RF03, RN04.

IC: GYM-TST-003 · Plano de Testes (GYM-TST-001), seção 4.3 · Caso de teste CT06.
"""

from conftest import API, auth, unico


# TI-EXE-01 — CT06: cadastrar exercício
def test_instrutor_cadastra_exercicio(client, instrutor):
    corpo = {"nome": unico("Supino"), "grupo_muscular": "Peito", "descricao": "Barra reta"}
    resposta = client.post(f"{API}/exercicios", json=corpo, headers=auth(instrutor["token"]))

    assert resposta.status_code == 201
    dados = resposta.get_json()
    assert dados["nome"] == corpo["nome"]
    assert dados["grupo_muscular"] == "Peito"
    assert dados["ativo"] is True


def test_exercicio_sem_nome(client, instrutor):
    resposta = client.post(f"{API}/exercicios", json={"nome": ""}, headers=auth(instrutor["token"]))
    assert resposta.status_code == 400


# TI-EXE-02 — nome duplicado (sem diferenciar maiúsculas)
def test_nome_duplicado(client, instrutor, criar_exercicio):
    existente = criar_exercicio()
    resposta = client.post(
        f"{API}/exercicios", json={"nome": existente["nome"].upper()}, headers=auth(instrutor["token"])
    )

    assert resposta.status_code == 409
    assert resposta.get_json()["campo"] == "nome"


# TI-EXE-03 — aluno não cadastra exercício
def test_aluno_nao_cadastra_exercicio(client, aluno):
    resposta = client.post(f"{API}/exercicios", json={"nome": unico("Rosca")}, headers=auth(aluno["token"]))
    assert resposta.status_code == 403


# TI-EXE-04 — todos os perfis consultam o catálogo
def test_aluno_lista_exercicios(client, aluno, criar_exercicio):
    criado = criar_exercicio()
    resposta = client.get(f"{API}/exercicios", query_string={"nome": criado["nome"]}, headers=auth(aluno["token"]))

    assert resposta.status_code == 200
    assert [e["id"] for e in resposta.get_json()] == [criado["id"]]


# TI-EXE-05 — RN04: exercício usado em ficha é apenas inativado
def test_excluir_exercicio_usado_em_ficha_apenas_inativa(client, instrutor, aluno, criar_ficha):
    ficha = criar_ficha(aluno["usuario"]["id"], qtd_exercicios=1)
    id_exercicio = ficha["exercicios"][0]["exercicio"]["id"]

    resposta = client.delete(f"{API}/exercicios/{id_exercicio}", headers=auth(instrutor["token"]))
    assert resposta.status_code == 200
    assert resposta.get_json()["ativo"] is False

    ficha_depois = client.get(f"{API}/fichas/{ficha['id']}", headers=auth(instrutor["token"])).get_json()
    assert [item["exercicio"]["id"] for item in ficha_depois["exercicios"]] == [id_exercicio]
    assert ficha_depois["exercicios"][0]["exercicio"]["ativo"] is False


# TI-EXE-06 — RN04: exercício inativo não entra em ficha nova
def test_exercicio_inativo_nao_entra_em_ficha_nova(client, instrutor, aluno, criar_exercicio):
    exercicio = criar_exercicio()
    client.delete(f"{API}/exercicios/{exercicio['id']}", headers=auth(instrutor["token"]))

    corpo = {
        "nome": unico("Ficha"),
        "aluno_id": aluno["usuario"]["id"],
        "data_inicio": "2026-01-01",
        "exercicios": [{"exercicio_id": exercicio["id"], "series": 3, "repeticoes": 10}],
    }
    resposta = client.post(f"{API}/fichas", json=corpo, headers=auth(instrutor["token"]))

    assert resposta.status_code == 400
    assert resposta.get_json()["campo"] == "exercicios[0].exercicio_id"


def test_reativar_exercicio(client, instrutor, criar_exercicio):
    exercicio = criar_exercicio()
    cabecalho = auth(instrutor["token"])
    client.delete(f"{API}/exercicios/{exercicio['id']}", headers=cabecalho)

    resposta = client.put(f"{API}/exercicios/{exercicio['id']}", json={"ativo": True}, headers=cabecalho)
    assert resposta.status_code == 200
    assert resposta.get_json()["ativo"] is True
