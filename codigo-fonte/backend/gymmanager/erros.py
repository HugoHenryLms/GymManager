"""Formato único de erro da API: {"erro": "...", "campo": "..."} (ERS 4.5)."""

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .extensoes import db


class ErroAPI(Exception):
    """Erro de negócio ou de validação com status HTTP definido."""

    def __init__(self, mensagem: str, status: int = 400, campo: str | None = None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status = status
        self.campo = campo

    def para_dict(self) -> dict:
        corpo = {"erro": self.mensagem}
        if self.campo:
            corpo["campo"] = self.campo
        return corpo


def nao_encontrado(recurso: str = "Recurso") -> ErroAPI:
    return ErroAPI(f"{recurso} não encontrado.", 404)


def acesso_negado() -> ErroAPI:
    return ErroAPI("Acesso negado.", 403)


_MENSAGENS_HTTP = {
    400: "Requisição inválida.",
    401: "Não autenticado.",
    403: "Acesso negado.",
    404: "Recurso não encontrado.",
    405: "Método não permitido.",
    409: "Conflito.",
    413: "Requisição muito grande.",
    415: "Envie os dados em JSON.",
}


def registrar_tratadores(app: Flask) -> None:
    @app.errorhandler(ErroAPI)
    def _erro_api(erro: ErroAPI):
        db.session.rollback()
        return jsonify(erro.para_dict()), erro.status

    @app.errorhandler(HTTPException)
    def _erro_http(erro: HTTPException):
        mensagem = _MENSAGENS_HTTP.get(erro.code, erro.name)
        return jsonify({"erro": mensagem}), erro.code

    @app.errorhandler(Exception)
    def _erro_interno(erro: Exception):
        db.session.rollback()
        app.logger.exception("Erro interno não tratado")
        return jsonify({"erro": "Erro interno do servidor."}), 500
