"""Testes de integração das fichas de treino — RF04, RN01, RN02, RN05, RN06, RN09, RN12.

IC: GYM-TST-003 · Plano de Testes (GYM-TST-001), seção 4.3 · Casos de teste CT13 a CT16, CT18 e CT29.
"""

from conftest import API, auth, unico


def _itens(*exercicios):
    return [{"exercicio_id": e["id"], "series": 3, "repeticoes": 12, "carga_kg": 20, "descanso_s": 60} for e in exercicios]


# TI-FIC-01 — CT13: criar ficha com exercícios para um aluno
def test_criar_ficha(client, instrutor, aluno, criar_exercicio):
    corpo = {
        "nome": unico("Treino A"),
        "aluno_id": aluno["usuario"]["id"],
        "data_inicio": "2026-01-01",
        "exercicios": _itens(criar_exercicio(), criar_exercicio()),
    }
    resposta = client.post(f"{API}/fichas", json=corpo, headers=auth(instrutor["token"]))

    assert resposta.status_code == 201
    ficha = resposta.get_json()
    assert ficha["aluno"]["id"] == aluno["usuario"]["id"]
    assert ficha["instrutor"]["id"] == instrutor["usuario"]["id"]
    assert ficha["ativa"] is True and ficha["vigente"] is True
    assert [item["ordem"] for item in ficha["exercicios"]] == [1, 2]


# TI-FIC-02 — CT14 / RN06: ficha sem exercício (e CT29: séries inválidas)
def test_ficha_sem_exercicio(client, instrutor, aluno):
    corpo = {"nome": unico("Ficha"), "aluno_id": aluno["usuario"]["id"], "data_inicio": "2026-01-01", "exercicios": []}
    resposta = client.post(f"{API}/fichas", json=corpo, headers=auth(instrutor["token"]))

    assert resposta.status_code == 400
    assert resposta.get_json()["campo"] == "exercicios"


def test_ficha_com_series_invalidas(client, instrutor, aluno, criar_exercicio):
    itens = [{"exercicio_id": criar_exercicio()["id"], "series": 0, "repeticoes": 12}]
    corpo = {"nome": unico("Ficha"), "aluno_id": aluno["usuario"]["id"], "data_inicio": "2026-01-01", "exercicios": itens}
    resposta = client.post(f"{API}/fichas", json=corpo, headers=auth(instrutor["token"]))

    assert resposta.status_code == 400
    assert resposta.get_json()["campo"] == "exercicios[0].series"


# TI-FIC-10 — período inválido
def test_data_fim_anterior_ao_inicio(client, instrutor, aluno, criar_exercicio):
    corpo = {
        "nome": unico("Ficha"),
        "aluno_id": aluno["usuario"]["id"],
        "data_inicio": "2026-11-17",
        "data_fim": "2026-11-01",
        "exercicios": _itens(criar_exercicio()),
    }
    resposta = client.post(f"{API}/fichas", json=corpo, headers=auth(instrutor["token"]))
    assert resposta.status_code == 400


# TI-FIC-03 — RN01: aluno não cria ficha
def test_aluno_nao_cria_ficha(client, aluno, criar_exercicio):
    corpo = {
        "nome": unico("Ficha"),
        "aluno_id": aluno["usuario"]["id"],
        "data_inicio": "2026-01-01",
        "exercicios": _itens(criar_exercicio()),
    }
    assert client.post(f"{API}/fichas", json=corpo, headers=auth(aluno["token"])).status_code == 403


# TI-FIC-04 — RN05: aluno inativo não recebe ficha
def test_ficha_para_aluno_inativo(client, instrutor, criar_aluno, criar_exercicio):
    inativo = criar_aluno()
    client.delete(f"{API}/alunos/{inativo['usuario']['id']}", headers=auth(instrutor["token"]))

    corpo = {
        "nome": unico("Ficha"),
        "aluno_id": inativo["usuario"]["id"],
        "data_inicio": "2026-01-01",
        "exercicios": _itens(criar_exercicio()),
    }
    resposta = client.post(f"{API}/fichas", json=corpo, headers=auth(instrutor["token"]))

    assert resposta.status_code == 409
    assert resposta.get_json()["campo"] == "aluno_id"


# TI-FIC-05 — CT16 / RN02: aluno não vê a ficha de outro aluno
def test_aluno_nao_consulta_ficha_de_outro(client, criar_aluno, criar_ficha):
    dono, outro = criar_aluno(), criar_aluno()
    ficha = criar_ficha(dono["usuario"]["id"])

    assert client.get(f"{API}/fichas/{ficha['id']}", headers=auth(dono["token"])).status_code == 200
    assert client.get(f"{API}/fichas/{ficha['id']}", headers=auth(outro["token"])).status_code == 403


# TI-FIC-06 — CT15 / RN02: aluno lista só as próprias fichas
def test_aluno_lista_somente_as_proprias_fichas(client, criar_aluno, criar_ficha):
    dono, outro = criar_aluno(), criar_aluno()
    propria = criar_ficha(dono["usuario"]["id"])
    criar_ficha(outro["usuario"]["id"])

    fichas = client.get(f"{API}/fichas", headers=auth(dono["token"])).get_json()

    assert [f["id"] for f in fichas] == [propria["id"]]
    assert all(f["aluno"]["id"] == dono["usuario"]["id"] for f in fichas)


# TI-FIC-07 — CT18 / RN09: ficha com execuções não muda de aluno
def test_ficha_com_execucao_nao_muda_de_aluno(client, instrutor, criar_aluno, criar_ficha):
    dono, outro = criar_aluno(), criar_aluno()
    ficha = criar_ficha(dono["usuario"]["id"])
    assert client.post(f"{API}/execucoes", json={"ficha_id": ficha["id"]}, headers=auth(dono["token"])).status_code == 201

    resposta = client.put(
        f"{API}/fichas/{ficha['id']}", json={"aluno_id": outro["usuario"]["id"]}, headers=auth(instrutor["token"])
    )
    assert resposta.status_code == 409
    assert resposta.get_json()["campo"] == "aluno_id"


def test_ficha_sem_execucao_pode_mudar_de_aluno(client, instrutor, criar_aluno, criar_ficha):
    dono, outro = criar_aluno(), criar_aluno()
    ficha = criar_ficha(dono["usuario"]["id"])

    resposta = client.put(
        f"{API}/fichas/{ficha['id']}", json={"aluno_id": outro["usuario"]["id"]}, headers=auth(instrutor["token"])
    )
    assert resposta.status_code == 200
    assert resposta.get_json()["aluno"]["id"] == outro["usuario"]["id"]


# TI-FIC-08 — RN09: ficha encerrada só reativa com aluno ativo
def test_reativar_ficha_de_aluno_inativo(client, instrutor, criar_aluno, criar_ficha):
    cabecalho = auth(instrutor["token"])
    dono = criar_aluno()
    ficha = criar_ficha(dono["usuario"]["id"])

    assert client.put(f"{API}/fichas/{ficha['id']}", json={"ativa": False}, headers=cabecalho).status_code == 200
    client.delete(f"{API}/alunos/{dono['usuario']['id']}", headers=cabecalho)

    resposta = client.put(f"{API}/fichas/{ficha['id']}", json={"ativa": True}, headers=cabecalho)
    assert resposta.status_code == 409
    assert resposta.get_json()["campo"] == "ativa"


# TI-FIC-09 — RN12: exercício removido da ficha fica inativo no item
def test_remover_exercicio_da_ficha(client, instrutor, aluno, criar_ficha):
    ficha = criar_ficha(aluno["usuario"]["id"], qtd_exercicios=2)
    mantido, removido = ficha["exercicios"]
    item_mantido = {
        "id": mantido["id"],
        "exercicio_id": mantido["exercicio"]["id"],
        "series": 4,
        "repeticoes": 10,
        "carga_kg": 25,
        "descanso_s": 90,
    }

    resposta = client.put(f"{API}/fichas/{ficha['id']}", json={"exercicios": [item_mantido]}, headers=auth(instrutor["token"]))

    assert resposta.status_code == 200
    itens = resposta.get_json()["exercicios"]
    assert [item["id"] for item in itens] == [mantido["id"]]
    assert itens[0]["series"] == 4
    assert removido["id"] not in [item["id"] for item in itens]
