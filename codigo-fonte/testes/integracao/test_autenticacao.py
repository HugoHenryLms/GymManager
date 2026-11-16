import os
import pytest
from gymmanager import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_login_admin_sucesso(client):
    email = os.getenv("ADMIN_EMAIL", "admin@ci.local")
    senha = os.getenv("ADMIN_SENHA", "ci-senha-admin1")

    resposta = client.post(
        "/api/v1/auth/login",
        json={"email": email, "senha": senha},
    )

    assert resposta.status_code == 200
    dados = resposta.get_json()
    assert "token" in dados
    assert dados["usuario"]["perfil"] == "ADMIN"


def test_login_senha_incorreta(client):
    email = os.getenv("ADMIN_EMAIL", "admin@ci.local")

    resposta = client.post(
        "/api/v1/auth/login",
        json={"email": email, "senha": "senha-errada-123"},
    )

    assert resposta.status_code in (400, 401)
