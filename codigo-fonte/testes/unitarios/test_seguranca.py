"""Testes unitários de senhas e tokens (auth/seguranca.py) — RNF01 e RNF13.

IC: GYM-TST-002 · Plano de Testes (GYM-TST-001), seções 3.1 e 3.4.
"""

from werkzeug.security import check_password_hash

from gymmanager.auth.seguranca import _hash_token, gerar_hash_senha


# TU-09 — RNF01: hash scrypt com sal
def test_hash_de_senha_nao_guarda_texto_puro():
    senha = "abc12345"
    hash_senha = gerar_hash_senha(senha)
    assert hash_senha != senha
    assert senha not in hash_senha
    assert hash_senha.startswith("scrypt:")
    assert check_password_hash(hash_senha, senha)


def test_hash_de_senha_usa_sal():
    assert gerar_hash_senha("abc12345") != gerar_hash_senha("abc12345")


def test_hash_de_senha_rejeita_senha_errada():
    assert not check_password_hash(gerar_hash_senha("abc12345"), "abc12346")


# TU-10 — RNF13: o banco guarda só o SHA-256 do token
def test_hash_do_token_e_sha256_estavel():
    token = "token-de-exemplo"
    assert _hash_token(token) == _hash_token(token)
    assert _hash_token(token) != token
    assert len(_hash_token(token)) == 64


def test_tokens_diferentes_geram_hashes_diferentes():
    assert _hash_token("a") != _hash_token("b")
