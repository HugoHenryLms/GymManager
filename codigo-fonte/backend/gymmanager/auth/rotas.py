"""Rotas de autenticação — UC01 (Autenticar-se), RF02.

POST /auth/login   autentica e retorna o token de acesso (rota pública)
POST /auth/logout  encerra a sessão atual
"""

from flask import Blueprint, g, jsonify

from .. import validacao
from ..erros import ErroAPI
from ..extensoes import db
from ..modelos import Usuario, iso_datahora
from .seguranca import autenticado, conferir_senha, criar_sessao

bp = Blueprint("auth", __name__)


@bp.post("/auth/login")
def login():
    dados = validacao.corpo_json()
    email = dados.get("email")
    senha = dados.get("senha")
    if not isinstance(email, str) or not email.strip():
        raise ErroAPI("Informe o e-mail.", 400, "email")
    if not isinstance(senha, str) or not senha:
        raise ErroAPI("Informe a senha.", 400, "senha")

    usuario = Usuario.query.filter_by(email=email.strip().lower()).first()
    if not conferir_senha(usuario, senha):
        # UC01 FE1: não indica qual campo está incorreto
        raise ErroAPI("E-mail ou senha inválidos.", 401)
    if not usuario.ativo:
        # UC01 FE2 / RN05
        raise ErroAPI("Usuário inativo.", 403)

    token, sessao = criar_sessao(usuario)
    db.session.commit()
    return jsonify({"token": token, "expira_em": iso_datahora(sessao.expira_em), "usuario": usuario.para_dict()})


@bp.post("/auth/logout")
@autenticado
def logout():
    db.session.delete(g.sessao)
    db.session.commit()
    return "", 204
