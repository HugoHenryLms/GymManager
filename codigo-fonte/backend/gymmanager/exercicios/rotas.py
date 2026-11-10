"""Rotas do catálogo de exercícios — UC04 (Gerenciar exercícios), RF03.

GET    /exercicios        lista (todos os perfis; filtros: nome, grupo_muscular, ativo)
POST   /exercicios        cadastra (ADMIN, INSTRUTOR)
PUT    /exercicios/{id}   atualiza (ADMIN, INSTRUTOR; ativo=true reativa)
DELETE /exercicios/{id}   inativa — nunca exclui; permanece nas fichas existentes (RN04)
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import func

from .. import validacao
from ..auth.seguranca import autenticado, exige_perfil
from ..erros import ErroAPI, nao_encontrado
from ..extensoes import db
from ..modelos import Exercicio

bp = Blueprint("exercicios", __name__)


def _buscar(id_exercicio: int) -> Exercicio:
    exercicio = db.session.get(Exercicio, id_exercicio)
    if exercicio is None:
        raise nao_encontrado("Exercício")
    return exercicio


def _garantir_nome_unico(nome: str, ignorar_id: int | None = None) -> None:
    consulta = Exercicio.query.filter(func.lower(Exercicio.nome) == nome.lower())
    if ignorar_id is not None:
        consulta = consulta.filter(Exercicio.id != ignorar_id)
    if consulta.first() is not None:
        raise ErroAPI(validacao.MSG_EXERCICIO_DUPLICADO, 409, "nome")


@bp.get("/exercicios")
@autenticado
def listar():
    consulta = Exercicio.query
    if nome := request.args.get("nome", "").strip():
        consulta = consulta.filter(Exercicio.nome.ilike(f"%{nome}%"))
    if grupo := request.args.get("grupo_muscular", "").strip():
        consulta = consulta.filter(func.lower(Exercicio.grupo_muscular) == grupo.lower())
    ativo = validacao.parametro_booleano("ativo")
    if ativo is not None:
        consulta = consulta.filter(Exercicio.ativo == ativo)
    return jsonify([e.para_dict() for e in consulta.order_by(Exercicio.nome).all()])


@bp.post("/exercicios")
@exige_perfil("INSTRUTOR")
def criar():
    dados = validacao.corpo_json()
    exercicio = Exercicio(
        nome=validacao.nome(dados.get("nome")),
        grupo_muscular=validacao.texto_opcional(dados.get("grupo_muscular"), "grupo_muscular", 50),
        descricao=validacao.texto_opcional(dados.get("descricao"), "descricao", 5000),
        ativo=True,
    )
    _garantir_nome_unico(exercicio.nome)
    db.session.add(exercicio)
    db.session.commit()
    return jsonify(exercicio.para_dict()), 201


@bp.put("/exercicios/<int:id_exercicio>")
@exige_perfil("INSTRUTOR")
def atualizar(id_exercicio: int):
    exercicio = _buscar(id_exercicio)
    dados = validacao.corpo_json()
    if "nome" in dados:
        nome = validacao.nome(dados["nome"])
        _garantir_nome_unico(nome, ignorar_id=exercicio.id)
        exercicio.nome = nome
    if "grupo_muscular" in dados:
        exercicio.grupo_muscular = validacao.texto_opcional(dados["grupo_muscular"], "grupo_muscular", 50)
    if "descricao" in dados:
        exercicio.descricao = validacao.texto_opcional(dados["descricao"], "descricao", 5000)
    if "ativo" in dados:
        exercicio.ativo = validacao.booleano(dados["ativo"], "ativo")
    db.session.commit()
    return jsonify(exercicio.para_dict())


@bp.delete("/exercicios/<int:id_exercicio>")
@exige_perfil("INSTRUTOR")
def inativar(id_exercicio: int):
    # UC04 FE2 / RN04: exercício nunca é excluído fisicamente, apenas inativado.
    exercicio = _buscar(id_exercicio)
    exercicio.ativo = False
    db.session.commit()
    return jsonify(exercicio.para_dict())
