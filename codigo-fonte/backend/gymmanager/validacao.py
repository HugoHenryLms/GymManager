"""Regras de validação da seção 4.3 do ERS (GYM-REQ-001).

As mensagens são exatamente as definidas no ERS; mensagens adicionais
(ex.: "Data inválida.") cobrem casos que o ERS não detalha.
"""

import re
from datetime import date
from decimal import Decimal, InvalidOperation

from flask import request

from .erros import ErroAPI
from .modelos import PERFIS

MSG_EMAIL = "E-mail inválido ou já cadastrado."
MSG_SENHA = "Senha fraca."
MSG_NOME = "Nome obrigatório."
MSG_PERFIL = "Perfil inválido."
MSG_EXERCICIO_DUPLICADO = "Exercício já cadastrado."
MSG_MAIOR_QUE_ZERO = "Valor deve ser maior que zero."
MSG_CARGA = "Carga inválida."
MSG_DESCANSO = "Descanso inválido."
MSG_DATAS = "Data final anterior à inicial."
MSG_DATA = "Data inválida."

_REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_CARGA_MAXIMA = Decimal("9999.99")


def corpo_json() -> dict:
    """Corpo da requisição como objeto JSON."""
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise ErroAPI("Envie os dados em JSON.", 400)
    return dados


def nome(valor, campo: str = "nome") -> str:
    if not isinstance(valor, str) or not 2 <= len(valor.strip()) <= 100:
        raise ErroAPI(MSG_NOME, 400, campo)
    return valor.strip()


def email(valor) -> str:
    if not isinstance(valor, str) or len(valor.strip()) > 254 or not _REGEX_EMAIL.match(valor.strip()):
        raise ErroAPI(MSG_EMAIL, 400, "email")
    return valor.strip().lower()


def senha(valor) -> str:
    """Mínimo de 8 caracteres, com letras e números."""
    if (
        not isinstance(valor, str)
        or len(valor) < 8
        or len(valor) > 128
        or not re.search(r"[A-Za-zÀ-ÿ]", valor)
        or not re.search(r"\d", valor)
    ):
        raise ErroAPI(MSG_SENHA, 400, "senha")
    return valor


def perfil(valor) -> str:
    if valor not in PERFIS:
        raise ErroAPI(MSG_PERFIL, 400, "perfil")
    return valor


def texto_opcional(valor, campo: str, tamanho_maximo: int | None = None) -> str | None:
    if valor is None:
        return None
    if not isinstance(valor, str) or (tamanho_maximo and len(valor.strip()) > tamanho_maximo):
        raise ErroAPI(f"Campo {campo} inválido.", 400, campo)
    return valor.strip() or None


def booleano(valor, campo: str) -> bool:
    if not isinstance(valor, bool):
        raise ErroAPI(f"Campo {campo} inválido.", 400, campo)
    return valor


def identificador(valor, campo: str) -> int:
    if isinstance(valor, bool) or not isinstance(valor, int) or valor < 1:
        raise ErroAPI(f"Campo {campo} inválido.", 400, campo)
    return valor


def inteiro_positivo(valor, campo: str) -> int:
    """Séries e repetições: inteiros maiores que zero."""
    if isinstance(valor, bool) or not isinstance(valor, int) or not 0 < valor <= 65535:
        raise ErroAPI(MSG_MAIOR_QUE_ZERO, 400, campo)
    return valor


def descanso(valor, campo: str = "descanso_s") -> int:
    if isinstance(valor, bool) or not isinstance(valor, int) or not 0 <= valor <= 65535:
        raise ErroAPI(MSG_DESCANSO, 400, campo)
    return valor


def carga(valor, campo: str = "carga_kg") -> Decimal:
    """Número maior ou igual a zero, com até 2 casas decimais."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float, str)):
        raise ErroAPI(MSG_CARGA, 400, campo)
    try:
        numero = Decimal(str(valor))
    except InvalidOperation:
        raise ErroAPI(MSG_CARGA, 400, campo) from None
    if not numero.is_finite() or numero < 0 or numero > _CARGA_MAXIMA or numero != numero.quantize(Decimal("0.01")):
        raise ErroAPI(MSG_CARGA, 400, campo)
    return numero.quantize(Decimal("0.01"))


def data(valor, campo: str, obrigatoria: bool = False) -> date | None:
    if valor is None or valor == "":
        if obrigatoria:
            raise ErroAPI(MSG_DATA, 400, campo)
        return None
    if not isinstance(valor, str):
        raise ErroAPI(MSG_DATA, 400, campo)
    try:
        return date.fromisoformat(valor)
    except ValueError:
        raise ErroAPI(MSG_DATA, 400, campo) from None


def periodo(inicio: date | None, fim: date | None, campo: str = "data_fim") -> None:
    if inicio and fim and fim < inicio:
        raise ErroAPI(MSG_DATAS, 400, campo)


def parametro_booleano(nome_parametro: str) -> bool | None:
    """Lê ?param=true|false da query string; ausente = None."""
    valor = request.args.get(nome_parametro)
    if valor is None or valor == "":
        return None
    if valor.lower() in ("true", "1", "sim"):
        return True
    if valor.lower() in ("false", "0", "nao", "não"):
        return False
    raise ErroAPI(f"Parâmetro {nome_parametro} inválido.", 400, nome_parametro)


def parametro_inteiro(nome_parametro: str) -> int | None:
    valor = request.args.get(nome_parametro)
    if valor is None or valor == "":
        return None
    if not valor.isdigit() or int(valor) < 1:
        raise ErroAPI(f"Parâmetro {nome_parametro} inválido.", 400, nome_parametro)
    return int(valor)


def parametro_data(nome_parametro: str) -> date | None:
    return data(request.args.get(nome_parametro), nome_parametro)
