"""Rotas de fichas de treino — UC05 (Montar e atribuir) e UC06 (Consultar minhas fichas), RF04.

GET  /fichas        ALUNO: só as próprias (RN02); ADMIN/INSTRUTOR: todas (filtro aluno_id). Filtro ativa.
POST /fichas        cria e atribui a um aluno ativo (RN01, RN05, RN06)
GET  /fichas/{id}   detalha (ALUNO só a própria — RN02)
PUT  /fichas/{id}   atualiza; `exercicios` substitui a lista de itens (removidos viram inativos)
"""

from flask import Blueprint, g, jsonify
from sqlalchemy import or_

from .. import validacao
from ..auth.seguranca import autenticado, exige_perfil
from ..erros import ErroAPI, acesso_negado, nao_encontrado
from ..extensoes import db
from ..modelos import Execucao, Exercicio, Ficha, FichaExercicio, Usuario, agora_utc

bp = Blueprint("fichas", __name__)

MSG_SEM_EXERCICIO = "A ficha deve ter pelo menos um exercício."
MSG_ALUNO_INATIVO = "Aluno inativo não pode receber fichas."


def buscar_ficha(id_ficha: int) -> Ficha:
    ficha = db.session.get(Ficha, id_ficha)
    if ficha is None:
        raise nao_encontrado("Ficha")
    return ficha


def _aluno_para_ficha(valor) -> Usuario:
    aluno = db.session.get(Usuario, validacao.identificador(valor, "aluno_id"))
    if aluno is None or aluno.perfil != "ALUNO":
        raise ErroAPI("Aluno não encontrado.", 400, "aluno_id")
    if not aluno.ativo:
        raise ErroAPI(MSG_ALUNO_INATIVO, 409, "aluno_id")  # RN05 / UC05 FE3
    return aluno


def _validar_item(dados, posicao: int, item_existente: FichaExercicio | None) -> dict:
    prefixo = f"exercicios[{posicao}]"
    if not isinstance(dados, dict):
        raise ErroAPI("Item da ficha inválido.", 400, prefixo)

    exercicio = db.session.get(Exercicio, validacao.identificador(dados.get("exercicio_id"), f"{prefixo}.exercicio_id"))
    if exercicio is None:
        raise ErroAPI("Exercício não encontrado.", 400, f"{prefixo}.exercicio_id")
    mesmo_exercicio = item_existente is not None and item_existente.exercicio_id == exercicio.id
    if not exercicio.ativo and not mesmo_exercicio:
        # RN04: exercício inativo não entra em fichas novas, mas permanece nas existentes
        raise ErroAPI("Exercício inativo não pode ser adicionado à ficha.", 400, f"{prefixo}.exercicio_id")

    return {
        "exercicio_id": exercicio.id,
        "series": validacao.inteiro_positivo(dados.get("series"), f"{prefixo}.series"),
        "repeticoes": validacao.inteiro_positivo(dados.get("repeticoes"), f"{prefixo}.repeticoes"),
        "carga_kg": validacao.carga(dados.get("carga_kg", 0), f"{prefixo}.carga_kg"),
        "descanso_s": validacao.descanso(dados.get("descanso_s", 0), f"{prefixo}.descanso_s"),
        "ordem": validacao.inteiro_positivo(dados.get("ordem", posicao + 1), f"{prefixo}.ordem"),
    }


def _lista_de_itens(valor) -> list:
    if not isinstance(valor, list) or not valor:
        raise ErroAPI(MSG_SEM_EXERCICIO, 400, "exercicios")  # RN06 / UC05 FE1
    return valor


def _aplicar_itens(ficha: Ficha, lista: list) -> None:
    """Sincroniza os itens: atualiza (com id), cria (sem id), inativa os ausentes."""
    existentes = {item.id: item for item in ficha.itens if item.ativo}
    mantidos: set[int] = set()

    for posicao, dados in enumerate(lista):
        id_item = dados.get("id") if isinstance(dados, dict) else None
        if id_item is not None:
            item = existentes.get(id_item) if isinstance(id_item, int) else None
            if item is None or id_item in mantidos:
                raise ErroAPI("Item da ficha inválido.", 400, f"exercicios[{posicao}].id")
            for campo, valor in _validar_item(dados, posicao, item).items():
                setattr(item, campo, valor)
            mantidos.add(id_item)
        else:
            ficha.itens.append(FichaExercicio(**_validar_item(dados, posicao, None), ativo=True))

    for id_item, item in existentes.items():
        if id_item not in mantidos:
            item.ativo = False  # preserva o histórico de execuções


def _garantir_acesso(ficha: Ficha) -> None:
    if g.usuario.perfil == "ALUNO" and ficha.aluno_id != g.usuario.id:
        raise acesso_negado()  # RN02 / UC06 FE1


@bp.get("/fichas")
@autenticado
def listar():
    consulta = Ficha.query
    if g.usuario.perfil == "ALUNO":
        consulta = consulta.filter(Ficha.aluno_id == g.usuario.id)
    elif (aluno_id := validacao.parametro_inteiro("aluno_id")) is not None:
        consulta = consulta.filter(Ficha.aluno_id == aluno_id)

    ativa = validacao.parametro_booleano("ativa")
    hoje = agora_utc().date()
    if ativa is True:
        consulta = consulta.filter(Ficha.ativa.is_(True), or_(Ficha.data_fim.is_(None), Ficha.data_fim >= hoje))
    elif ativa is False:
        consulta = consulta.filter(or_(Ficha.ativa.is_(False), Ficha.data_fim < hoje))

    fichas = consulta.order_by(Ficha.ativa.desc(), Ficha.data_inicio.desc(), Ficha.id.desc()).all()
    return jsonify([f.para_dict() for f in fichas])


@bp.post("/fichas")
@exige_perfil("INSTRUTOR")
def criar():
    dados = validacao.corpo_json()
    nome = validacao.nome(dados.get("nome"))
    aluno = _aluno_para_ficha(dados.get("aluno_id"))
    data_inicio = validacao.data(dados.get("data_inicio"), "data_inicio", obrigatoria=True)
    data_fim = validacao.data(dados.get("data_fim"), "data_fim")
    validacao.periodo(data_inicio, data_fim)
    itens = _lista_de_itens(dados.get("exercicios"))

    ficha = Ficha(
        nome=nome,
        aluno_id=aluno.id,
        instrutor_id=g.usuario.id,  # RN01
        data_inicio=data_inicio,
        data_fim=data_fim,
        ativa=True,
    )
    _aplicar_itens(ficha, itens)
    db.session.add(ficha)
    db.session.commit()
    return jsonify(ficha.para_dict()), 201


@bp.get("/fichas/<int:id_ficha>")
@autenticado
def detalhar(id_ficha: int):
    ficha = buscar_ficha(id_ficha)
    _garantir_acesso(ficha)
    return jsonify(ficha.para_dict())


@bp.put("/fichas/<int:id_ficha>")
@exige_perfil("INSTRUTOR")
def atualizar(id_ficha: int):
    ficha = buscar_ficha(id_ficha)
    dados = validacao.corpo_json()

    if "nome" in dados:
        ficha.nome = validacao.nome(dados["nome"])
    if "aluno_id" in dados and dados["aluno_id"] != ficha.aluno_id:
        aluno = _aluno_para_ficha(dados["aluno_id"])
        if Execucao.query.filter_by(ficha_id=ficha.id).first() is not None:
            raise ErroAPI("Ficha com execuções registradas não pode mudar de aluno.", 409, "aluno_id")
        ficha.aluno_id = aluno.id
    if "data_inicio" in dados:
        ficha.data_inicio = validacao.data(dados["data_inicio"], "data_inicio", obrigatoria=True)
    if "data_fim" in dados:
        ficha.data_fim = validacao.data(dados["data_fim"], "data_fim")
    validacao.periodo(ficha.data_inicio, ficha.data_fim)
    if "ativa" in dados:
        ativa = validacao.booleano(dados["ativa"], "ativa")
        if ativa and not ficha.ativa and not ficha.aluno.ativo:
            raise ErroAPI(MSG_ALUNO_INATIVO, 409, "ativa")
        ficha.ativa = ativa
    if "exercicios" in dados:
        _aplicar_itens(ficha, _lista_de_itens(dados["exercicios"]))

    db.session.commit()
    db.session.refresh(ficha)
    return jsonify(ficha.para_dict())
