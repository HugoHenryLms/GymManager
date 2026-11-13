"""Rotas de execução de treino e histórico — UC07 e UC08, RF05.

POST  /execucoes                    ALUNO inicia a execução de uma ficha própria e vigente (RN07)
POST  /execucoes/{id}/exercicios    ALUNO registra repetições e carga; repetir corrige (UC07 FA1)
PATCH /execucoes/{id}/finalizar     ALUNO finaliza; depois disso não aceita registros (UC07 FE3)
GET   /alunos/{id}/historico        histórico e evolução de carga (ALUNO só o próprio — RN02)
"""

from datetime import datetime, time, timedelta

from flask import Blueprint, g, jsonify

from .. import validacao
from ..alunos.rotas import buscar_aluno
from ..auth.seguranca import autenticado, exige_perfil
from ..erros import ErroAPI, acesso_negado, nao_encontrado
from ..extensoes import db
from ..fichas.rotas import buscar_ficha
from ..modelos import Execucao, ExecucaoExercicio, FichaExercicio, agora_utc, iso_datahora, numero

bp = Blueprint("execucoes", __name__)

MSG_FINALIZADA = "Execução já finalizada."


def _execucao_do_aluno(id_execucao: int) -> Execucao:
    execucao = db.session.get(Execucao, id_execucao)
    if execucao is None:
        raise nao_encontrado("Execução")
    if execucao.aluno_id != g.usuario.id:
        raise acesso_negado()  # RN02
    return execucao


@bp.post("/execucoes")
@exige_perfil("ALUNO")
def iniciar():
    dados = validacao.corpo_json()
    ficha = buscar_ficha(validacao.identificador(dados.get("ficha_id"), "ficha_id"))
    if ficha.aluno_id != g.usuario.id:
        raise acesso_negado()  # RN07 / UC07 FE2
    if not ficha.vigente:
        raise ErroAPI("Ficha inativa.", 409, "ficha_id")

    execucao = Execucao(ficha_id=ficha.id, aluno_id=g.usuario.id, inicio=agora_utc())
    db.session.add(execucao)
    db.session.commit()
    return jsonify(execucao.para_dict()), 201


@bp.post("/execucoes/<int:id_execucao>/exercicios")
@exige_perfil("ALUNO")
def registrar_exercicio(id_execucao: int):
    execucao = _execucao_do_aluno(id_execucao)
    if execucao.fim is not None:
        raise ErroAPI(MSG_FINALIZADA, 409)

    dados = validacao.corpo_json()
    item = db.session.get(
        FichaExercicio, validacao.identificador(dados.get("ficha_exercicio_id"), "ficha_exercicio_id")
    )
    if item is None or item.ficha_id != execucao.ficha_id:
        raise ErroAPI("Exercício não pertence à ficha desta execução.", 400, "ficha_exercicio_id")
    repeticoes = validacao.inteiro_positivo(dados.get("repeticoes"), "repeticoes")
    carga = validacao.carga(dados.get("carga_kg"), "carga_kg")

    registro = ExecucaoExercicio.query.filter_by(execucao_id=execucao.id, ficha_exercicio_id=item.id).first()
    criado = registro is None
    if criado:
        registro = ExecucaoExercicio(execucao_id=execucao.id, ficha_exercicio_id=item.id)
        db.session.add(registro)
    registro.repeticoes = repeticoes
    registro.carga_kg = carga
    registro.registrado_em = agora_utc()
    db.session.commit()
    db.session.refresh(execucao)
    return jsonify(execucao.para_dict()), 201 if criado else 200


@bp.patch("/execucoes/<int:id_execucao>/finalizar")
@exige_perfil("ALUNO")
def finalizar(id_execucao: int):
    execucao = _execucao_do_aluno(id_execucao)
    if execucao.fim is not None:
        raise ErroAPI(MSG_FINALIZADA, 409)
    execucao.fim = agora_utc()
    db.session.commit()
    return jsonify(execucao.para_dict())


@bp.get("/alunos/<int:id_aluno>/historico")
@autenticado
def historico(id_aluno: int):
    if g.usuario.perfil == "ALUNO" and g.usuario.id != id_aluno:
        raise acesso_negado()  # RN02 / UC08 FE2
    aluno = buscar_aluno(id_aluno)

    data_inicio = validacao.parametro_data("data_inicio")
    data_fim = validacao.parametro_data("data_fim")
    validacao.periodo(data_inicio, data_fim)
    ficha_id = validacao.parametro_inteiro("ficha_id")

    consulta = Execucao.query.filter(Execucao.aluno_id == aluno.id)
    if data_inicio:
        consulta = consulta.filter(Execucao.inicio >= datetime.combine(data_inicio, time.min))
    if data_fim:
        consulta = consulta.filter(Execucao.inicio < datetime.combine(data_fim + timedelta(days=1), time.min))
    if ficha_id:
        consulta = consulta.filter(Execucao.ficha_id == ficha_id)
    execucoes = consulta.order_by(Execucao.inicio.desc(), Execucao.id.desc()).all()

    # Evolução por exercício, em ordem cronológica (UC08 passo 4)
    evolucao: dict[int, dict] = {}
    for execucao in reversed(execucoes):
        for registro in execucao.registros:
            exercicio = registro.item.exercicio
            serie = evolucao.setdefault(
                exercicio.id, {"exercicio": {"id": exercicio.id, "nome": exercicio.nome}, "pontos": []}
            )
            serie["pontos"].append(
                {
                    "data": iso_datahora(execucao.inicio),
                    "execucao_id": execucao.id,
                    "carga_kg": numero(registro.carga_kg),
                    "repeticoes": registro.repeticoes,
                }
            )

    return jsonify(
        {
            "aluno": aluno.referencia(),
            "execucoes": [e.para_dict() for e in execucoes],
            "evolucao": sorted(evolucao.values(), key=lambda s: s["exercicio"]["nome"].lower()),
        }
    )
