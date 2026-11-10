"""Senhas, tokens de sessão e controle de acesso por perfil.

- Senhas: hash scrypt com sal (RNF01).
- Token: 256 bits aleatórios; o banco guarda só o SHA-256 (tabela ``sessao``).
- Autorização: verificada no backend em toda rota (RNF02). O administrador
  herda as permissões do instrutor (ERS 2.4).
"""

import hashlib
import secrets
from datetime import timedelta
from functools import wraps

from flask import current_app, g, request
from werkzeug.security import check_password_hash, generate_password_hash

from ..erros import ErroAPI, acesso_negado
from ..extensoes import db
from ..modelos import Sessao, Usuario, agora_utc

# Hash fixo usado quando o e-mail não existe, para que o tempo de resposta do
# login não revele se o e-mail está cadastrado.
_HASH_FICTICIO = generate_password_hash("senha-ficticia-0", method="scrypt")


def gerar_hash_senha(senha: str) -> str:
    return generate_password_hash(senha, method="scrypt")


def conferir_senha(usuario: Usuario | None, senha: str) -> bool:
    if usuario is None:
        check_password_hash(_HASH_FICTICIO, senha)
        return False
    return check_password_hash(usuario.senha_hash, senha)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def criar_sessao(usuario: Usuario) -> tuple[str, Sessao]:
    """Cria uma sessão e devolve o token em claro (só é exibido uma vez)."""
    agora = agora_utc()
    Sessao.query.filter(Sessao.usuario_id == usuario.id, Sessao.expira_em <= agora).delete()
    token = secrets.token_urlsafe(32)
    sessao = Sessao(
        usuario_id=usuario.id,
        token_hash=_hash_token(token),
        criado_em=agora,
        expira_em=agora + timedelta(hours=current_app.config["SESSAO_HORAS"]),
    )
    db.session.add(sessao)
    return token, sessao


def encerrar_sessoes(usuario: Usuario) -> None:
    """Remove todas as sessões do usuário (logout global / inativação, RN05)."""
    Sessao.query.filter_by(usuario_id=usuario.id).delete()


def _token_da_requisicao() -> str | None:
    cabecalho = request.headers.get("Authorization", "")
    tipo, _, token = cabecalho.partition(" ")
    if tipo.lower() != "bearer" or not token.strip():
        return None
    return token.strip()


def _sessao_valida() -> Sessao | None:
    token = _token_da_requisicao()
    if not token:
        return None
    sessao = Sessao.query.filter_by(token_hash=_hash_token(token)).first()
    if sessao is None or sessao.expira_em <= agora_utc() or not sessao.usuario.ativo:
        return None
    return sessao


def autenticado(funcao):
    """Exige token válido; disponibiliza ``g.usuario`` e ``g.sessao``."""

    @wraps(funcao)
    def envoltorio(*args, **kwargs):
        sessao = _sessao_valida()
        if sessao is None:
            raise ErroAPI("Não autenticado.", 401)
        g.sessao = sessao
        g.usuario = sessao.usuario
        return funcao(*args, **kwargs)

    return envoltorio


def exige_perfil(*perfis: str):
    """Exige autenticação e um dos perfis informados.

    Se INSTRUTOR for permitido, ADMIN também é (herança de permissões).
    """
    permitidos = set(perfis)
    if "INSTRUTOR" in permitidos:
        permitidos.add("ADMIN")

    def decorador(funcao):
        @wraps(funcao)
        @autenticado
        def envoltorio(*args, **kwargs):
            if g.usuario.perfil not in permitidos:
                raise acesso_negado()
            return funcao(*args, **kwargs)

        return envoltorio

    return decorador


def usuario_atual() -> Usuario:
    return g.usuario
