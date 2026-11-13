"""Regras compartilhadas de cadastro de pessoas (usuários, instrutores e alunos).

Usado pelos módulos ``usuarios`` (GYM-SRC-001) e ``alunos`` (GYM-SRC-002).
"""

from sqlalchemy import func

from .. import validacao
from ..auth.seguranca import encerrar_sessoes, gerar_hash_senha
from ..erros import ErroAPI
from ..modelos import Usuario


def garantir_email_disponivel(email: str, ignorar_id: int | None = None) -> None:
    consulta = Usuario.query.filter(func.lower(Usuario.email) == email.lower())
    if ignorar_id is not None:
        consulta = consulta.filter(Usuario.id != ignorar_id)
    if consulta.first() is not None:
        raise ErroAPI(validacao.MSG_EMAIL, 409, "email")


def novo_usuario(dados: dict, perfil: str) -> Usuario:
    """Valida os dados e cria um usuário ativo com a senha em hash (RNF01)."""
    usuario = Usuario(
        nome=validacao.nome(dados.get("nome")),
        email=validacao.email(dados.get("email")),
        senha_hash=gerar_hash_senha(validacao.senha(dados.get("senha"))),
        perfil=validacao.perfil(perfil),
        ativo=True,
        data_nascimento=validacao.data(dados.get("data_nascimento"), "data_nascimento"),
        telefone=validacao.texto_opcional(dados.get("telefone"), "telefone", 20),
    )
    garantir_email_disponivel(usuario.email)
    return usuario


def atualizar_usuario(usuario: Usuario, dados: dict) -> None:
    """Atualiza somente os campos enviados (perfil e ativo são tratados por quem chama)."""
    if "nome" in dados:
        usuario.nome = validacao.nome(dados["nome"])
    if "email" in dados:
        email = validacao.email(dados["email"])
        garantir_email_disponivel(email, ignorar_id=usuario.id)
        usuario.email = email
    if "senha" in dados:
        usuario.senha_hash = gerar_hash_senha(validacao.senha(dados["senha"]))
    if "data_nascimento" in dados:
        usuario.data_nascimento = validacao.data(dados["data_nascimento"], "data_nascimento")
    if "telefone" in dados:
        usuario.telefone = validacao.texto_opcional(dados["telefone"], "telefone", 20)


def definir_situacao(usuario: Usuario, ativo: bool) -> None:
    """Ativa ou inativa. Ao inativar, encerra as sessões e preserva o histórico (RN05)."""
    usuario.ativo = ativo
    if not ativo:
        encerrar_sessoes(usuario)
