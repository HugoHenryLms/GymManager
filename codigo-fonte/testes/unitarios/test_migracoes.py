"""Testes unitários do executor de migrações (migracoes.py) — RNF11.

IC: GYM-TST-002 · Plano de Testes (GYM-TST-001), seção 3.1.
Usam pastas temporárias (tmp_path); não acessam o banco.
"""

from pathlib import Path

import pytest

from gymmanager.migracoes import ErroMigracao, checksum, instrucoes, listar_migracoes

PASTA_REAL = Path(__file__).resolve().parents[3] / "banco-de-dados" / "migracoes"


# TU-11 — listagem, checksum e separação de instruções
def test_lista_migracao_real_v001():
    versoes = [versao for versao, _, _ in listar_migracoes(PASTA_REAL)]
    assert "V001" in versoes


def test_lista_em_ordem_numerica(tmp_path):
    (tmp_path / "V010__dez.sql").write_text("SELECT 10;", encoding="utf-8")
    (tmp_path / "V002__dois.sql").write_text("SELECT 2;", encoding="utf-8")
    assert [v for v, _, _ in listar_migracoes(tmp_path)] == ["V002", "V010"]


def test_nome_fora_do_padrao_rejeitado(tmp_path):
    (tmp_path / "cria_tabelas.sql").write_text("SELECT 1;", encoding="utf-8")
    with pytest.raises(ErroMigracao):
        listar_migracoes(tmp_path)


def test_pasta_inexistente_rejeitada(tmp_path):
    with pytest.raises(ErroMigracao):
        listar_migracoes(tmp_path / "nao-existe")


def test_checksum_estavel_e_ignora_fim_de_linha_windows(tmp_path):
    unix = tmp_path / "V001__a.sql"
    windows = tmp_path / "V002__b.sql"
    unix.write_bytes(b"SELECT 1;\n")
    windows.write_bytes(b"SELECT 1;\r\n")
    assert checksum(unix) == checksum(unix)
    assert checksum(unix) == checksum(windows)


def test_checksum_muda_quando_o_conteudo_muda(tmp_path):
    arquivo = tmp_path / "V001__a.sql"
    arquivo.write_text("SELECT 1;", encoding="utf-8")
    antes = checksum(arquivo)
    arquivo.write_text("SELECT 2;", encoding="utf-8")
    assert checksum(arquivo) != antes


def test_instrucoes_separadas_e_comentarios_ignorados():
    sql = "-- comentário\nCREATE TABLE a (\n  id INT\n);\n\nINSERT INTO a VALUES (1);\n"
    assert instrucoes(sql) == ["CREATE TABLE a (\n  id INT\n)", "INSERT INTO a VALUES (1)"]
