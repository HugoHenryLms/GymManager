"""GymManager — API REST (Flask).

Fábrica da aplicação. Os módulos de domínio são registrados como blueprints
sob o prefixo ``/api/v1`` (ERS 4.5).

ICs: GYM-SRC-001 a GYM-SRC-005 · Arquitetura: GYM-ARQ-001
"""

from flask import Flask

from .config import carregar_configuracao
from .erros import registrar_tratadores
from .extensoes import db

__version__ = "0.1.0"

PREFIXO_API = "/api/v1"


def create_app(config: dict | None = None) -> Flask:
    """Cria e configura a aplicação.

    ``config`` sobrescreve as configurações lidas do ambiente; usado pelos
    testes (ex.: ``{"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://",
    "CRIAR_TABELAS": True}``).
    """
    app = Flask(__name__)
    app.config.update(carregar_configuracao(config or {}))
    app.json.ensure_ascii = False
    app.json.sort_keys = False

    db.init_app(app)
    registrar_tratadores(app)
    _registrar_blueprints(app)
    _registrar_cors(app)

    from .cli import registrar_comandos

    registrar_comandos(app)

    if app.config.get("CRIAR_TABELAS"):
        with app.app_context():
            from . import modelos  # noqa: F401  (registra as tabelas)

            db.create_all()

    return app


def _registrar_blueprints(app: Flask) -> None:
    from .alunos.rotas import bp as alunos_bp
    from .auth.rotas import bp as auth_bp
    from .exercicios.rotas import bp as exercicios_bp
    from .fichas.rotas import bp as fichas_bp
    from .usuarios.rotas import bp as usuarios_bp

    for bp in (auth_bp, usuarios_bp, alunos_bp, exercicios_bp, fichas_bp):
        app.register_blueprint(bp, url_prefix=PREFIXO_API)


def _registrar_cors(app: Flask) -> None:
    """CORS opcional: só para origens listadas em CORS_ORIGENS.

    Em produção o frontend acessa a API pela mesma origem (proxy do Nginx),
    então a lista normalmente fica vazia.
    """
    origens = app.config["CORS_ORIGENS"]
    if not origens:
        return

    @app.after_request
    def _cors(resposta):
        from flask import request

        origem = request.headers.get("Origin")
        if origem in origens:
            resposta.headers["Access-Control-Allow-Origin"] = origem
            resposta.headers["Vary"] = "Origin"
            resposta.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            resposta.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        return resposta
