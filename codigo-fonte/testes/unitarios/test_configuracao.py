from gymmanager import create_app


def test_criacao_aplicacao_flask():
    app = create_app()
    assert app is not None
    assert "SECRET_KEY" in app.config
