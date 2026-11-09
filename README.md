# 🏋️ GymManager

Sistema web de gerenciamento de treinos de academia: cadastro de alunos e exercícios, montagem de fichas de treino e registro da evolução de cada aluno.

Projeto Integrador da disciplina **Gerência de Configuração** (6º período), CENTRO UNIVERSITÁRIO FAMETRO. Professor: Paulo Rodrigo Barbosa Alves.

> **Status:** em desenvolvimento.


## Sobre o projeto

Academias costumam controlar fichas de treino em papel ou planilhas soltas, o que gera perda de histórico, fichas desatualizadas e pouca visibilidade da evolução do aluno. O GymManager centraliza essas informações: o instrutor monta as fichas e o aluno consulta o treino e registra o que executou.

## Funcionalidades

Escopo da versão 1.0.0:

- Autenticação e perfis de acesso (administrador, instrutor e aluno)
- Gestão de alunos, exercícios e fichas de treino (exercício, séries, repetições, carga e descanso)
- Registro e histórico de execução de treinos, com acompanhamento da evolução de carga
- API REST documentada com OpenAPI
- Interface web
- Testes automatizados e integração contínua

Fora do escopo: aplicativo móvel nativo, pagamentos e mensalidades, integração com catracas ou wearables.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Frontend | HTML, CSS e JavaScript |
| Backend | Python com Flask (API REST) |
| Banco de dados | MySQL, com migrações versionadas |
| Testes | pytest e Postman/Newman |
| CI/CD | GitHub Actions |
| Contêineres | Docker e docker-compose |
| Versionamento | Git e GitHub |

## Estrutura do repositório

```
GymManager/
│
├── README.md
│
├── LICENSE
│
├── prototipos/
│   ├── telas-login.png
│   ├── telas-cadastro.png
│   └── outras-telas.png
│
├── documentos/
│   │
│   ├── Plano_de_Projeto.md
│   ├── ERS.md
│   ├── Inventario_de_ICs.md
│   ├── Planilha_Controle_de_ICs.md
│   └── outras-planilhas.md
│
├── codigo-fonte/
│   │
│   ├── frontend/
│   │   ├── index.html
│   │   ├── css/
│   │   └── js/
│   │
│   └── backend/
│       └── ...
│
└── banco-de-dados/
    └── ...

```

## Gerência de configuração

- **Itens de Configuração (ICs):** todo artefato relevante tem ID no padrão `GYM-<TIPO>-<NNN>` e está catalogado em [`docs/gerencia/inventario-ics.xlsx`](docs/gerencia/inventario-ics.xlsx).

- **Controle de mudanças:** alterações em itens sob baseline exigem uma Change Request (issue com o formulário CRF), avaliada pelo Comitê de Controle de Mudanças (CCB). Todo commit deve estar vinculado a uma issue ou CR.

## Equipe

| Papel | Integrante |
|---|---|
| Gerente de Projeto/Configuração | Hugo Henry Lemos Carvalho |
| Analista de Requisitos | Renata Martins Da Silva |
| Dev Backend e Frontend | João Vitor Simonetti |
| DBA/DevOps | João vitor Simonetti |
| QA/Testes | Iago Medice Ferrreira Da Silva, Tiago Costa Dos Santos, Ruan Victor Assunção Costa |

## Documentação

- [Plano de Projeto](docs/gerencia/plano-projeto.md)
- [Inventário de ICs](docs/gerencia/inventario-ics.xlsx)
- [Documento de Requisitos (ERS)](docs/requisitos/ers.md) *(em elaboração)*
- [Contrato da API (OpenAPI)](docs/api/openapi.yaml) *(planejado)*
- [Decisões arquiteturais (ADR)](docs/adr/)

---

Projeto acadêmico em desenvolvimento, disciplina de Gerência de Configuração.
