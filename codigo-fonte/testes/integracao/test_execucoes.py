"""Testes de integração de execuções e histórico — RF05, RN02, RN07, RN10, RN11, RN12, RN13, RN14.

IC: GYM-TST-003 · Plano de Testes (GYM-TST-001), seção 4.3 · Casos de teste CT16 e CT19 a CT26.
"""

from datetime import date, timedelta

import pytest

from conftest import API, auth


@pytest.fixture
def ficha_do_aluno(aluno, criar_ficha):
    return criar_ficha(aluno["usuario"]["id"], qtd_exercicios=2)


def _iniciar(client, token, ficha_id):
    return client.post(f"{API}/execucoes", json={"ficha_id": ficha_id}, headers=auth(token))


def _registrar(client, token, execucao_id, item_id, repeticoes=12, carga=20):
    return client.post(
        f"{API}/execucoes/{execucao_id}/exercicios",
        json={"ficha_exercicio_id": item_id, "repeticoes": repeticoes, "carga_kg": carga},
        headers=auth(token),
    )


def _finalizar(client, token, execucao_id):
    return client.patch(f"{API}/execucoes/{execucao_id}/finalizar", headers=auth(token))


# TI-EXC-01 — CT19 / CT21 / CT23: iniciar, registrar e finalizar
def test_fluxo_completo_de_execucao(client, aluno, ficha_do_aluno):
    token = aluno["token"]
    iniciada = _iniciar(client, token, ficha_do_aluno["id"])
    assert iniciada.status_code == 201
    execucao = iniciada.get_json()
    assert execucao["fim"] is None

    for item in ficha_do_aluno["exercicios"]:
        assert _registrar(client, token, execucao["id"], item["id"]).status_code == 201

    finalizada = _finalizar(client, token, execucao["id"])
    assert finalizada.status_code == 200
    dados = finalizada.get_json()
    assert dados["fim"] is not None
    assert len(dados["registros"]) == 2


# TI-EXC-02 — CT22 / RN11: registrar de novo corrige o anterior
def test_registrar_de_novo_corrige(client, aluno, ficha_do_aluno):
    token = aluno["token"]
    execucao = _iniciar(client, token, ficha_do_aluno["id"]).get_json()
    item = ficha_do_aluno["exercicios"][0]

    assert _registrar(client, token, execucao["id"], item["id"], carga=20).status_code == 201
    corrigido = _registrar(client, token, execucao["id"], item["id"], carga=22.5)

    assert corrigido.status_code == 200
    registros = corrigido.get_json()["registros"]
    assert len(registros) == 1
    assert registros[0]["carga_kg"] == 22.5


# TI-EXC-03 — RN11: execução finalizada não aceita registro
def test_registro_em_execucao_finalizada(client, aluno, ficha_do_aluno):
    token = aluno["token"]
    execucao = _iniciar(client, token, ficha_do_aluno["id"]).get_json()
    _finalizar(client, token, execucao["id"])

    resposta = _registrar(client, token, execucao["id"], ficha_do_aluno["exercicios"][0]["id"])
    assert resposta.status_code == 409
    assert resposta.get_json()["erro"] == "Execução já finalizada."


# TI-EXC-04 — finalizar duas vezes
def test_finalizar_duas_vezes(client, aluno, ficha_do_aluno):
    token = aluno["token"]
    execucao = _iniciar(client, token, ficha_do_aluno["id"]).get_json()

    assert _finalizar(client, token, execucao["id"]).status_code == 200
    assert _finalizar(client, token, execucao["id"]).status_code == 409


# TI-EXC-05 — CT16 / RN07: não inicia execução em ficha de outro aluno
def test_iniciar_em_ficha_de_outro_aluno(client, criar_aluno, ficha_do_aluno):
    outro = criar_aluno()
    assert _iniciar(client, outro["token"], ficha_do_aluno["id"]).status_code == 403


def test_registrar_em_execucao_de_outro_aluno(client, aluno, criar_aluno, ficha_do_aluno):
    execucao = _iniciar(client, aluno["token"], ficha_do_aluno["id"]).get_json()
    outro = criar_aluno()

    resposta = _registrar(client, outro["token"], execucao["id"], ficha_do_aluno["exercicios"][0]["id"])
    assert resposta.status_code == 403


# TI-EXC-06 — CT20 / RN10: só inicia em ficha vigente
def test_iniciar_em_ficha_encerrada(client, instrutor, aluno, ficha_do_aluno):
    client.put(f"{API}/fichas/{ficha_do_aluno['id']}", json={"ativa": False}, headers=auth(instrutor["token"]))

    resposta = _iniciar(client, aluno["token"], ficha_do_aluno["id"])
    assert resposta.status_code == 409
    assert resposta.get_json()["campo"] == "ficha_id"


def test_iniciar_em_ficha_com_data_fim_vencida(client, aluno, criar_ficha):
    ontem = date.today() - timedelta(days=1)
    ficha = criar_ficha(
        aluno["usuario"]["id"],
        data_inicio=(ontem - timedelta(days=30)).isoformat(),
        data_fim=(ontem - timedelta(days=1)).isoformat(),
    )

    assert ficha["vigente"] is False
    assert _iniciar(client, aluno["token"], ficha["id"]).status_code == 409


# TI-EXC-07 — exercício que não pertence à ficha da execução
def test_registrar_exercicio_de_outra_ficha(client, aluno, criar_ficha, ficha_do_aluno):
    outra_ficha = criar_ficha(aluno["usuario"]["id"], qtd_exercicios=1)
    execucao = _iniciar(client, aluno["token"], ficha_do_aluno["id"]).get_json()

    resposta = _registrar(client, aluno["token"], execucao["id"], outra_ficha["exercicios"][0]["id"])
    assert resposta.status_code == 400
    assert resposta.get_json()["campo"] == "ficha_exercicio_id"


# TI-EXC-08 — valores inválidos
@pytest.mark.parametrize("repeticoes, carga, campo", [(0, 20, "repeticoes"), (10, -5, "carga_kg")])
def test_registro_com_valores_invalidos(client, aluno, ficha_do_aluno, repeticoes, carga, campo):
    execucao = _iniciar(client, aluno["token"], ficha_do_aluno["id"]).get_json()

    resposta = _registrar(
        client, aluno["token"], execucao["id"], ficha_do_aluno["exercicios"][0]["id"], repeticoes, carga
    )
    assert resposta.status_code == 400
    assert resposta.get_json()["campo"] == campo


# TI-EXC-09 — só o aluno inicia execução
def test_instrutor_nao_inicia_execucao(client, instrutor, ficha_do_aluno):
    assert _iniciar(client, instrutor["token"], ficha_do_aluno["id"]).status_code == 403


# TI-EXC-10 — CT25 / RN13: a mesma ficha aceita mais de uma execução em andamento
def test_duas_execucoes_abertas_na_mesma_ficha(client, aluno, ficha_do_aluno):
    primeira = _iniciar(client, aluno["token"], ficha_do_aluno["id"])
    segunda = _iniciar(client, aluno["token"], ficha_do_aluno["id"])

    assert primeira.status_code == 201
    assert segunda.status_code == 201
    assert primeira.get_json()["id"] != segunda.get_json()["id"]


# TI-EXC-11 — CT26 / RN14 (e RN12): registro de item inativado depois do início é aceito e preservado
def test_registro_de_item_inativado_apos_o_inicio(client, instrutor, aluno, ficha_do_aluno):
    mantido, removido = ficha_do_aluno["exercicios"]
    execucao = _iniciar(client, aluno["token"], ficha_do_aluno["id"]).get_json()

    item_mantido = {"id": mantido["id"], "exercicio_id": mantido["exercicio"]["id"], "series": 3, "repeticoes": 12}
    alterada = client.put(
        f"{API}/fichas/{ficha_do_aluno['id']}", json={"exercicios": [item_mantido]}, headers=auth(instrutor["token"])
    )
    assert alterada.status_code == 200

    resposta = _registrar(client, aluno["token"], execucao["id"], removido["id"], carga=30)
    assert resposta.status_code == 201

    historico = client.get(f"{API}/alunos/{aluno['usuario']['id']}/historico", headers=auth(aluno["token"])).get_json()
    registros = [r for e in historico["execucoes"] for r in e["registros"]]
    assert removido["id"] in [r["ficha_exercicio_id"] for r in registros]


# TI-EXC-12 — CT24: aluno consulta o próprio histórico e a evolução de carga
def test_historico_com_evolucao_de_carga(client, aluno, ficha_do_aluno):
    token = aluno["token"]
    item = ficha_do_aluno["exercicios"][0]
    for carga in (20, 25):
        execucao = _iniciar(client, token, ficha_do_aluno["id"]).get_json()
        _registrar(client, token, execucao["id"], item["id"], carga=carga)
        _finalizar(client, token, execucao["id"])

    resposta = client.get(f"{API}/alunos/{aluno['usuario']['id']}/historico", headers=auth(token))

    assert resposta.status_code == 200
    dados = resposta.get_json()
    assert len(dados["execucoes"]) == 2
    serie = next(s for s in dados["evolucao"] if s["exercicio"]["id"] == item["exercicio"]["id"])
    assert [p["carga_kg"] for p in serie["pontos"]] == [20, 25]


def test_instrutor_consulta_historico_do_aluno(client, instrutor, aluno):
    resposta = client.get(f"{API}/alunos/{aluno['usuario']['id']}/historico", headers=auth(instrutor["token"]))
    assert resposta.status_code == 200


# TI-EXC-13 — CT16 / RN02: aluno não vê o histórico de outro
def test_aluno_nao_consulta_historico_de_outro(client, aluno, criar_aluno):
    outro = criar_aluno()
    resposta = client.get(f"{API}/alunos/{outro['usuario']['id']}/historico", headers=auth(aluno["token"]))
    assert resposta.status_code == 403


# TI-EXC-14 — filtros do histórico
def test_historico_filtrado_por_ficha_e_periodo(client, aluno, criar_ficha, ficha_do_aluno):
    token = aluno["token"]
    outra = criar_ficha(aluno["usuario"]["id"], qtd_exercicios=1)
    _iniciar(client, token, ficha_do_aluno["id"])
    _iniciar(client, token, outra["id"])
    url = f"{API}/alunos/{aluno['usuario']['id']}/historico"

    por_ficha = client.get(url, query_string={"ficha_id": outra["id"]}, headers=auth(token)).get_json()
    assert [e["ficha"]["id"] for e in por_ficha["execucoes"]] == [outra["id"]]

    amanha = (date.today() + timedelta(days=1)).isoformat()
    futuro = client.get(url, query_string={"data_inicio": amanha}, headers=auth(token)).get_json()
    assert futuro["execucoes"] == []


def test_historico_com_periodo_invertido(client, aluno):
    resposta = client.get(
        f"{API}/alunos/{aluno['usuario']['id']}/historico",
        query_string={"data_inicio": "2026-11-17", "data_fim": "2026-11-01"},
        headers=auth(aluno["token"]),
    )
    assert resposta.status_code == 400
