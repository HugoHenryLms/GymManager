"""Executor das migrações SQL versionadas (GYM-DB-001, RNF11).

- Arquivos: ``banco-de-dados/migracoes/V<NNN>__<descricao>.sql``, aplicados em ordem.
- Cada migração aplicada é registrada em ``schema_migracoes`` com o checksum
  SHA-256 do conteúdo (quebras de linha normalizadas para LF, para que o
  checksum seja o mesmo no Windows e no Linux).
- Se uma migração já aplicada for alterada, a execução é interrompida:
  correções devem entrar como uma nova migração.
"""

import hashlib
import re
from pathlib import Path

from sqlalchemy.engine import Engine

PADRAO_ARQUIVO = re.compile(r"^V(\d{3,})__([A-Za-z0-9_]+)\.sql$")

_DDL_CONTROLE = """
CREATE TABLE IF NOT EXISTS schema_migracoes (
    versao       VARCHAR(20)   NOT NULL PRIMARY KEY,
    descricao    VARCHAR(200)  NOT NULL,
    checksum     CHAR(64)      NOT NULL,
    aplicada_em  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""


class ErroMigracao(RuntimeError):
    pass


def listar_migracoes(pasta: str | Path) -> list[tuple[str, str, Path]]:
    pasta = Path(pasta)
    if not pasta.is_dir():
        raise ErroMigracao(f"Pasta de migrações não encontrada: {pasta}")
    migracoes = []
    for arquivo in pasta.iterdir():
        if arquivo.suffix != ".sql":
            continue
        encontrado = PADRAO_ARQUIVO.match(arquivo.name)
        if not encontrado:
            raise ErroMigracao(f"Nome de migração fora do padrão V<NNN>__<descricao>.sql: {arquivo.name}")
        migracoes.append((int(encontrado.group(1)), f"V{encontrado.group(1)}", encontrado.group(2), arquivo))
    migracoes.sort()
    numeros = [numero for numero, *_ in migracoes]
    if len(numeros) != len(set(numeros)):
        raise ErroMigracao("Há migrações com o mesmo número de versão.")
    return [(versao, descricao, arquivo) for _, versao, descricao, arquivo in migracoes]


def _conteudo(arquivo: Path) -> str:
    return arquivo.read_text(encoding="utf-8").replace("\r\n", "\n")


def checksum(arquivo: Path) -> str:
    return hashlib.sha256(_conteudo(arquivo).encode("utf-8")).hexdigest()


def instrucoes(sql: str) -> list[str]:
    """Separa o script em instruções terminadas por ';' no fim da linha."""
    resultado, atual = [], []
    for linha in sql.splitlines():
        if linha.strip().startswith("--") or not linha.strip():
            continue
        atual.append(linha)
        if linha.rstrip().endswith(";"):
            resultado.append("\n".join(atual).rstrip().rstrip(";"))
            atual = []
    if atual:
        resultado.append("\n".join(atual))
    return resultado


def aplicar(engine: Engine, pasta: str | Path, log=print) -> int:
    """Aplica as migrações pendentes. Retorna quantas foram aplicadas."""
    with engine.begin() as conexao:
        conexao.exec_driver_sql(_DDL_CONTROLE)
        aplicadas = dict(conexao.exec_driver_sql("SELECT versao, checksum FROM schema_migracoes").all())

    quantidade = 0
    for versao, descricao, arquivo in listar_migracoes(pasta):
        soma = checksum(arquivo)
        if versao in aplicadas:
            if aplicadas[versao] != soma:
                raise ErroMigracao(
                    f"A migração {arquivo.name} foi alterada depois de aplicada. "
                    "Migrações aplicadas não podem ser editadas: crie uma nova migração."
                )
            continue
        log(f"Aplicando {arquivo.name} ...")
        with engine.begin() as conexao:
            for instrucao in instrucoes(_conteudo(arquivo)):
                conexao.exec_driver_sql(instrucao)
            conexao.exec_driver_sql(
                "INSERT INTO schema_migracoes (versao, descricao, checksum) VALUES (%s, %s, %s)",
                (versao, descricao, soma),
            )
        quantidade += 1
    log(f"Migrações aplicadas nesta execução: {quantidade}.")
    return quantidade
