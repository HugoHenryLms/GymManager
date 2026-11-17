"""Testes unitários das regras de validação (validacao.py) — ERS 4.3.

IC: GYM-TST-002 · Plano de Testes (GYM-TST-001), seção 3.1.
Não usam banco nem requisição HTTP.
"""

from datetime import date
from decimal import Decimal

import pytest

from gymmanager import validacao
from gymmanager.erros import ErroAPI


def _rejeita(funcao, *args):
    with pytest.raises(ErroAPI) as erro:
        funcao(*args)
    assert erro.value.status == 400
    return erro.value


# TU-01 — senha: mínimo de 8 caracteres, com letras e números
def test_senha_valida():
    assert validacao.senha("abc12345") == "abc12345"


@pytest.mark.parametrize("senha", ["abc1234", "abcdefgh", "12345678", "", None, 12345678])
def test_senha_fraca_rejeitada(senha):
    assert _rejeita(validacao.senha, senha).mensagem == validacao.MSG_SENHA


# TU-02 — e-mail
def test_email_valido_normalizado():
    assert validacao.email("  Fulano@Teste.COM ") == "fulano@teste.com"


@pytest.mark.parametrize("email", ["sem-arroba", "a@b", "a b@c.com", "", None])
def test_email_invalido(email):
    _rejeita(validacao.email, email)


# TU-03 — nome (2 a 100 caracteres)
def test_nome_valido_sem_espacos_extras():
    assert validacao.nome("  Maria  ") == "Maria"


@pytest.mark.parametrize("nome", ["", "   ", "A", "x" * 101, None])
def test_nome_invalido(nome):
    assert _rejeita(validacao.nome, nome).mensagem == validacao.MSG_NOME


# TU-04 — perfil
@pytest.mark.parametrize("perfil", ["ADMIN", "INSTRUTOR", "ALUNO"])
def test_perfil_valido(perfil):
    assert validacao.perfil(perfil) == perfil


@pytest.mark.parametrize("perfil", ["GERENTE", "admin", "", None])
def test_perfil_invalido(perfil):
    _rejeita(validacao.perfil, perfil)


# TU-05 — séries e repetições: inteiros maiores que zero
def test_inteiro_positivo_valido():
    assert validacao.inteiro_positivo(10, "series") == 10


@pytest.mark.parametrize("valor", [0, -1, "10", 1.5, True, 70000])
def test_inteiro_positivo_invalido(valor):
    _rejeita(validacao.inteiro_positivo, valor, "series")


# TU-06 — carga: >= 0, até 2 casas decimais
@pytest.mark.parametrize("valor, esperado", [(0, Decimal("0.00")), (22.5, Decimal("22.50")), ("10.25", Decimal("10.25"))])
def test_carga_valida(valor, esperado):
    assert validacao.carga(valor) == esperado


@pytest.mark.parametrize("valor", [-1, "abc", 10.123, True, None, 10000])
def test_carga_invalida(valor):
    _rejeita(validacao.carga, valor)


# TU-07 — descanso em segundos (>= 0)
def test_descanso_valido():
    assert validacao.descanso(0) == 0
    assert validacao.descanso(90) == 90


@pytest.mark.parametrize("valor", [-1, "60", 1.5])
def test_descanso_invalido(valor):
    _rejeita(validacao.descanso, valor)


# TU-08 — datas e período
def test_data_iso_valida():
    assert validacao.data("2026-11-17", "data_inicio") == date(2026, 11, 17)


def test_data_opcional_vazia():
    assert validacao.data(None, "data_fim") is None


@pytest.mark.parametrize("valor", ["17/11/2026", "2026-13-01", 20261117])
def test_data_invalida(valor):
    _rejeita(validacao.data, valor, "data_inicio")


def test_data_obrigatoria_ausente():
    _rejeita(validacao.data, None, "data_inicio", True)


def test_periodo_invertido_rejeitado():
    erro = _rejeita(validacao.periodo, date(2026, 11, 17), date(2026, 11, 1))
    assert erro.mensagem == validacao.MSG_DATAS


def test_periodo_valido():
    validacao.periodo(date(2026, 11, 1), date(2026, 11, 17))
