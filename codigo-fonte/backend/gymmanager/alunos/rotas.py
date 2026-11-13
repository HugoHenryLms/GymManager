"""Rotas de alunos — UC03 (Gerenciar alunos), RF01. Perfis ADMIN e INSTRUTOR.

GET    /alunos        lista (filtros: nome — também busca no e-mail —, ativo)
POST   /alunos        cadastra aluno (perfil ALUNO, ativo)
GET    /alunos/{id}   consulta
PUT    /alunos/{id}   atualiza (ativo=true reativa)
DELETE /alunos/{id}   inativa: não autentica nem recebe fichas; histórico mantido (RN05)
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import or_

from .. import validacao
from ..auth.seguranca import exige_perfil
from ..erros import nao_encontrado
from ..extensoes import db
from ..modelos import Usuario
from ..usuarios.servico import atualizar_usuario, definir_situacao, novo_usuario

bp = Blueprint("alunos", __name__)


def buscar_aluno(id_aluno: int) -> Usuario:
    aluno = db.session.get(Usuario, id_aluno)
    if aluno is None or aluno.perfil != "ALUNO":
        raise nao_encontrado("Aluno")
    return aluno


@bp.get("/alunos")
@exige_perfil("INSTRUTOR")
def listar():
    consulta = Usuario.query.filter(Usuario.perfil == "ALUNO")
    if termo := request.args.get("nome", "").strip():
        consulta = consulta.filter(or_(Usuario.nome.ilike(f"%{termo}%"), Usuario.email.ilike(f"%{termo}%")))
    ativo = validacao.parametro_booleano("ativo")
    if ativo is not None:
        consulta = consulta.filter(Usuario.ativo == ativo)
    return jsonify([a.para_dict() for a in consulta.order_by(Usuario.nome).all()])


@bp.post("/alunos")
@exige_perfil("INSTRUTOR")
def criar():
    aluno = novo_usuario(validacao.corpo_json(), "ALUNO")
    db.session.add(aluno)
    db.session.commit()
    return jsonify(aluno.para_dict()), 201


@bp.get("/alunos/<int:id_aluno>")
@exige_perfil("INSTRUTOR")
def consultar(id_aluno: int):
    return jsonify(buscar_aluno(id_aluno).para_dict())


@bp.put("/alunos/<int:id_aluno>")
@exige_perfil("INSTRUTOR")
def atualizar(id_aluno: int):
    aluno = buscar_aluno(id_aluno)
    dados = validacao.corpo_json()
    atualizar_usuario(aluno, dados)
    if "ativo" in dados:
        definir_situacao(aluno, validacao.booleano(dados["ativo"], "ativo"))
    db.session.commit()
    return jsonify(aluno.para_dict())


@bp.delete("/alunos/<int:id_aluno>")
@exige_perfil("INSTRUTOR")
def inativar(id_aluno: int):
    aluno = buscar_aluno(id_aluno)
    definir_situacao(aluno, False)
    db.session.commit()
    return jsonify(aluno.para_dict())
