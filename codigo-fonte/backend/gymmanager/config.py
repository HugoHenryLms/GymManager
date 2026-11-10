"""Configuração lida de variáveis de ambiente (.env), conforme RNF03.

Nenhum segredo tem valor padrão no código: SECRET_KEY e a senha do banco
precisam vir do ambiente (ver .env.example, GYM-CFG-002).
"""

import os
from pathlib import Path
from urllib.parse import quote_plus

# Pasta das migrações: banco-de-dados/migracoes/ na raiz do repositório.
# No contêiner o Dockerfile copia as migrações para /app/migracoes e define MIGRACOES_DIR.
_PASTAS_ACIMA = Path(__file__).resolve().parents
_MIGRACOES_PADRAO = (
    _PASTAS_ACIMA[3] / "banco-de-dados" / "migracoes" if len(_PASTAS_ACIMA) > 3 else Path("migracoes")
)


def _url_mysql() -> str | None:
    usuario = os.environ.get("MYSQL_USER")
    senha = os.environ.get("MYSQL_PASSWORD")
    if not usuario or senha is None:
        return None
    host = os.environ.get("MYSQL_HOST", "localhost")
    porta = os.environ.get("MYSQL_PORT", "3306")
    banco = os.environ.get("MYSQL_DATABASE", "gymmanager")
    return (
        f"mysql+pymysql://{quote_plus(usuario)}:{quote_plus(senha)}"
        f"@{host}:{porta}/{banco}?charset=utf8mb4"
    )


def carregar_configuracao(sobrescritas: dict) -> dict:
    testando = bool(sobrescritas.get("TESTING"))

    config = {
        "SECRET_KEY": os.environ.get("SECRET_KEY"),
        "SQLALCHEMY_DATABASE_URI": os.environ.get("DATABASE_URL") or _url_mysql(),
        "SQLALCHEMY_ENGINE_OPTIONS": {"pool_pre_ping": True, "pool_recycle": 280},
        "SESSAO_HORAS": int(os.environ.get("SESSAO_HORAS", "8")),
        "CORS_ORIGENS": [o.strip() for o in os.environ.get("CORS_ORIGENS", "").split(",") if o.strip()],
        "MIGRACOES_DIR": os.environ.get("MIGRACOES_DIR", str(_MIGRACOES_PADRAO)),
        "CRIAR_TABELAS": False,
        "MAX_CONTENT_LENGTH": 1 * 1024 * 1024,
    }
    config.update(sobrescritas)

    if testando:
        config["SECRET_KEY"] = config["SECRET_KEY"] or "chave-somente-para-testes"
        if config["SQLALCHEMY_DATABASE_URI"] is None:
            config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        if str(config["SQLALCHEMY_DATABASE_URI"]).startswith("sqlite"):
            config["SQLALCHEMY_ENGINE_OPTIONS"] = {}

    if not config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY não definida. Copie .env.example para .env e preencha os valores.")
    if not config["SQLALCHEMY_DATABASE_URI"]:
        raise RuntimeError("Banco não configurado: defina MYSQL_USER/MYSQL_PASSWORD (ou DATABASE_URL).")
    return config
