"""Comandos de linha (``flask --app wsgi <comando>``).

flask migrar       aplica as migrações pendentes (GYM-DB-001)
flask criar-admin  cria o primeiro administrador a partir do .env (ERS 2.6)
"""

import os

import click
from flask import Flask, current_app

from .erros import ErroAPI
from .extensoes import db
from .migracoes import ErroMigracao, aplicar


def registrar_comandos(app: Flask) -> None:
    @app.cli.command("migrar")
    def migrar():
        """Aplica as migrações SQL pendentes."""
        try:
            aplicar(db.engine, current_app.config["MIGRACOES_DIR"], log=click.echo)
        except ErroMigracao as erro:
            raise click.ClickException(str(erro)) from None

    @app.cli.command("criar-admin")
    def criar_admin():
        """Cria o administrador inicial, se ainda não existir nenhum."""
        from .modelos import Usuario
        from .usuarios.servico import novo_usuario

        if Usuario.query.filter_by(perfil="ADMIN").first() is not None:
            click.echo("Já existe administrador cadastrado; nada a fazer.")
            return
        dados = {
            "nome": os.environ.get("ADMIN_NOME", "Administrador"),
            "email": os.environ.get("ADMIN_EMAIL"),
            "senha": os.environ.get("ADMIN_SENHA"),
        }
        if not dados["email"] or not dados["senha"]:
            raise click.ClickException("Defina ADMIN_EMAIL e ADMIN_SENHA no .env para criar o administrador.")
        try:
            admin = novo_usuario(dados, "ADMIN")
        except ErroAPI as erro:
            raise click.ClickException(f"Administrador não criado: {erro.mensagem} ({erro.campo})") from None
        db.session.add(admin)
        db.session.commit()
        click.echo(f"Administrador {admin.email} criado.")
