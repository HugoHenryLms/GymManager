"""Rotas de usuários e instrutores — UC02, RF06. Somente ADMIN (RN03).

GET    /usuarios        lista (filtros: nome, email, perfil, ativo)
POST   /usuarios        cadastra usuário ou instrutor
PUT    /usuarios/{id}   atualiza
DELETE /usuarios/{id}   inativa (RN05)
"""

from flask import Blueprint, g, jsonify, request

from .. import validacao
from ..auth.seguranca import exige_perfil
from ..erros import ErroAPI, nao_encontrado
from ..extensoes import db
from ..modelos import Usuario
from .servico import atualizar_usuario, definir_situacao, novo_usuario

bp = Blueprint("usuarios", __name__)

MSG_PROPRIO_USUARIO = "Não é possível inativar ou alterar o perfil do próprio usuário."


def _buscar(id_usuario: int) -> Usuario:
    usuario = db.session.get(Usuario, id_usuario)
    if usuario is None:
        raise nao_encontrado("Usuário")
    return usuario


@bp.get("/usuarios")
@exige_perfil("ADMIN")
def listar():
    consulta = Usuario.query
    if nome := request.args.get("nome", "").strip():
        consulta = consulta.filter(Usuario.nome.ilike(f"%{nome}%"))
    if email := request.args.get("email", "").strip():
        consulta = consulta.filter(Usuario.email.ilike(f"%{email}%"))
    if perfil := request.args.get("perfil", "").strip():
        consulta = consulta.filter(Usuario.perfil == validacao.perfil(perfil))
    ativo = validacao.parametro_booleano("ativo")
    if ativo is not None:
        consulta = consulta.filter(Usuario.ativo == ativo)
    return jsonify([u.para_dict() for u in consulta.order_by(Usuario.nome).all()])


@bp.post("/usuarios")
@exige_perfil("ADMIN")
def criar():
    dados = validacao.corpo_json()
    usuario = novo_usuario(dados, dados.get("perfil"))
    db.session.add(usuario)
    db.session.commit()
    return jsonify(usuario.para_dict()), 201


@bp.put("/usuarios/<int:id_usuario>")
@exige_perfil("ADMIN")
def atualizar(id_usuario: int):
    usuario = _buscar(id_usuario)
    dados = validacao.corpo_json()
    proprio = usuario.id == g.usuario.id

    atualizar_usuario(usuario, dados)
    if "perfil" in dados:
        perfil = validacao.perfil(dados["perfil"])
        if proprio and perfil != "ADMIN":
            raise ErroAPI(MSG_PROPRIO_USUARIO, 409, "perfil")
        usuario.perfil = perfil
    if "ativo" in dados:
        ativo = validacao.booleano(dados["ativo"], "ativo")
        if proprio and not ativo:
            raise ErroAPI(MSG_PROPRIO_USUARIO, 409, "ativo")
        definir_situacao(usuario, ativo)

    db.session.commit()
    return jsonify(usuario.para_dict())


@bp.delete("/usuarios/<int:id_usuario>")
@exige_perfil("ADMIN")
def inativar(id_usuario: int):
    usuario = _buscar(id_usuario)
    if usuario.id == g.usuario.id:
        raise ErroAPI(MSG_PROPRIO_USUARIO, 409)
    definir_situacao(usuario, False)
    db.session.commit()
    return jsonify(usuario.para_dict())
