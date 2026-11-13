"""Entidades mapeadas para as tabelas criadas pelas migrações (GYM-DB-001).

O modelo físico está documentado em documentos/arquitetura/Modelo_de_Dados.md
(GYM-ARQ-002). Qualquer mudança aqui exige uma nova migração e a atualização
desse documento no mesmo Pull Request.
"""

from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .extensoes import db

PERFIS = ("ADMIN", "INSTRUTOR", "ALUNO")


def agora_utc() -> datetime:
    """Data/hora atual em UTC, sem fuso (o banco grava em UTC)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def iso_datahora(valor: datetime | None) -> str | None:
    return valor.replace(microsecond=0).isoformat() + "Z" if valor else None


def iso_data(valor: date | None) -> str | None:
    return valor.isoformat() if valor else None


def numero(valor: Decimal | None) -> float | None:
    return float(valor) if valor is not None else None


class Usuario(db.Model):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(254), unique=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    perfil: Mapped[str] = mapped_column(Enum(*PERFIS, name="perfil"))
    ativo: Mapped[bool] = mapped_column(default=True)
    data_nascimento: Mapped[date | None]
    telefone: Mapped[str | None] = mapped_column(String(20))
    criado_em: Mapped[datetime] = mapped_column(default=agora_utc)
    atualizado_em: Mapped[datetime] = mapped_column(default=agora_utc, onupdate=agora_utc)

    sessoes: Mapped[list["Sessao"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")

    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "perfil": self.perfil,
            "ativo": self.ativo,
            "data_nascimento": iso_data(self.data_nascimento),
            "telefone": self.telefone,
            "criado_em": iso_datahora(self.criado_em),
        }

    def referencia(self) -> dict:
        return {"id": self.id, "nome": self.nome}


class Sessao(db.Model):
    __tablename__ = "sessao"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id", ondelete="CASCADE"))
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    criado_em: Mapped[datetime] = mapped_column(default=agora_utc)
    expira_em: Mapped[datetime]

    usuario: Mapped[Usuario] = relationship(back_populates="sessoes")


class Exercicio(db.Model):
    __tablename__ = "exercicio"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)
    grupo_muscular: Mapped[str | None] = mapped_column(String(50))
    descricao: Mapped[str | None] = mapped_column(Text)
    ativo: Mapped[bool] = mapped_column(default=True)
    criado_em: Mapped[datetime] = mapped_column(default=agora_utc)
    atualizado_em: Mapped[datetime] = mapped_column(default=agora_utc, onupdate=agora_utc)

    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "grupo_muscular": self.grupo_muscular,
            "descricao": self.descricao,
            "ativo": self.ativo,
        }


class Ficha(db.Model):
    __tablename__ = "ficha"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    aluno_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    instrutor_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    data_inicio: Mapped[date]
    data_fim: Mapped[date | None]
    ativa: Mapped[bool] = mapped_column(default=True)
    criado_em: Mapped[datetime] = mapped_column(default=agora_utc)
    atualizado_em: Mapped[datetime] = mapped_column(default=agora_utc, onupdate=agora_utc)

    aluno: Mapped[Usuario] = relationship(foreign_keys=[aluno_id])
    instrutor: Mapped[Usuario] = relationship(foreign_keys=[instrutor_id])
    itens: Mapped[list["FichaExercicio"]] = relationship(
        back_populates="ficha", order_by="FichaExercicio.ordem, FichaExercicio.id"
    )

    @property
    def itens_ativos(self) -> list["FichaExercicio"]:
        return [item for item in self.itens if item.ativo]

    @property
    def vigente(self) -> bool:
        hoje = agora_utc().date()
        return self.ativa and (self.data_fim is None or self.data_fim >= hoje)

    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "aluno": self.aluno.referencia(),
            "instrutor": self.instrutor.referencia(),
            "data_inicio": iso_data(self.data_inicio),
            "data_fim": iso_data(self.data_fim),
            "ativa": self.ativa,
            "vigente": self.vigente,
            "exercicios": [item.para_dict() for item in self.itens_ativos],
        }

    def referencia(self) -> dict:
        return {"id": self.id, "nome": self.nome}


class FichaExercicio(db.Model):
    __tablename__ = "ficha_exercicio"

    id: Mapped[int] = mapped_column(primary_key=True)
    ficha_id: Mapped[int] = mapped_column(ForeignKey("ficha.id"))
    exercicio_id: Mapped[int] = mapped_column(ForeignKey("exercicio.id"))
    series: Mapped[int]
    repeticoes: Mapped[int]
    carga_kg: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=Decimal("0"))
    descanso_s: Mapped[int] = mapped_column(default=0)
    ordem: Mapped[int] = mapped_column(default=1)
    ativo: Mapped[bool] = mapped_column(default=True)

    ficha: Mapped[Ficha] = relationship(back_populates="itens")
    exercicio: Mapped[Exercicio] = relationship()

    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "exercicio": self.exercicio.para_dict(),
            "series": self.series,
            "repeticoes": self.repeticoes,
            "carga_kg": numero(self.carga_kg),
            "descanso_s": self.descanso_s,
            "ordem": self.ordem,
        }


class Execucao(db.Model):
    __tablename__ = "execucao"

    id: Mapped[int] = mapped_column(primary_key=True)
    ficha_id: Mapped[int] = mapped_column(ForeignKey("ficha.id"))
    aluno_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    inicio: Mapped[datetime] = mapped_column(default=agora_utc)
    fim: Mapped[datetime | None]

    ficha: Mapped[Ficha] = relationship()
    registros: Mapped[list["ExecucaoExercicio"]] = relationship(
        back_populates="execucao", order_by="ExecucaoExercicio.id"
    )

    @property
    def duracao_min(self) -> int | None:
        if self.fim is None:
            return None
        return int((self.fim - self.inicio).total_seconds() // 60)

    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "ficha": self.ficha.referencia(),
            "aluno_id": self.aluno_id,
            "inicio": iso_datahora(self.inicio),
            "fim": iso_datahora(self.fim),
            "duracao_min": self.duracao_min,
            "registros": [registro.para_dict() for registro in self.registros],
        }


class ExecucaoExercicio(db.Model):
    __tablename__ = "execucao_exercicio"
    __table_args__ = (UniqueConstraint("execucao_id", "ficha_exercicio_id", name="uq_ee_execucao_item"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    execucao_id: Mapped[int] = mapped_column(ForeignKey("execucao.id"))
    ficha_exercicio_id: Mapped[int] = mapped_column(ForeignKey("ficha_exercicio.id"))
    repeticoes: Mapped[int]
    carga_kg: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=Decimal("0"))
    registrado_em: Mapped[datetime] = mapped_column(default=agora_utc)

    execucao: Mapped[Execucao] = relationship(back_populates="registros")
    item: Mapped[FichaExercicio] = relationship()

    def para_dict(self) -> dict:
        return {
            "ficha_exercicio_id": self.ficha_exercicio_id,
            "exercicio": {"id": self.item.exercicio.id, "nome": self.item.exercicio.nome},
            "repeticoes": self.repeticoes,
            "carga_kg": numero(self.carga_kg),
            "registrado_em": iso_datahora(self.registrado_em),
        }
