"""Inicialização do contêiner do backend (GYM-IAC-001).

1. Aguarda o MySQL aceitar conexões.
2. Aplica as migrações pendentes (flask migrar).
3. Cria o administrador inicial, se não existir (flask criar-admin).
4. Substitui o processo pelo gunicorn.
"""

import os
import sys
import time

from sqlalchemy import text

from gymmanager import create_app
from gymmanager.extensoes import db
from gymmanager.migracoes import ErroMigracao, aplicar

TEMPO_MAXIMO_S = int(os.environ.get("ESPERA_BANCO_S", "90"))


def aguardar_banco(app) -> None:
    limite = time.monotonic() + TEMPO_MAXIMO_S
    while True:
        try:
            with app.app_context(), db.engine.connect() as conexao:
                conexao.execute(text("SELECT 1"))
            return
        except Exception as erro:  # noqa: BLE001
            if time.monotonic() > limite:
                print(f"Banco indisponível após {TEMPO_MAXIMO_S}s: {erro}", file=sys.stderr)
                sys.exit(1)
            print("Aguardando o banco de dados...", flush=True)
            time.sleep(3)


def main() -> None:
    app = create_app()
    aguardar_banco(app)

    with app.app_context():
        try:
            aplicar(db.engine, app.config["MIGRACOES_DIR"])
        except ErroMigracao as erro:
            print(f"ERRO de migração: {erro}", file=sys.stderr)
            sys.exit(1)

    runner = app.test_cli_runner()
    resultado = runner.invoke(args=["criar-admin"])
    print(resultado.output.strip(), flush=True)
    if resultado.exit_code != 0:
        print("Aviso: administrador inicial não foi criado.", file=sys.stderr)

    workers = os.environ.get("GUNICORN_WORKERS", "3")
    os.execvp(
        "gunicorn",
        ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", workers, "--access-logfile", "-", "wsgi:app"],
    )


if __name__ == "__main__":
    main()
