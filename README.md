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
| Banco de dados | MySQL, com migrações versionadas em banco-de-dados/migracoes/ |
| Testes | pytest e Postman/Newman |
| CI/CD | GitHub Actions |
| Contêineres | Docker e docker-compose |
| Versionamento | Git e GitHub |

## Estrutura do repositório

```
GymManager/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   └── ISSUE_TEMPLATE/
│       └── change-request.md
│
├── prototipos/
│   ├── telas-login.png
│   ├── telas-cadastro.png
│   └── outras-telas.png
│
├── documentos/
│   ├── gerencia/
│   │   ├── Plano_de_Projeto.md
│   │   ├── Planilha_Controle_de_ICs.xlsx
│   │   ├── Plano_de_Gerencia_de_Configuracao.md
│   │   ├── Modelo_CRF.md
│   │   └── Status_Accounting.xlsx
│   ├── requisitos/
│   │   ├── ERS.md
│   │   ├── Casos_de_Uso.md
│   │   └── RTM.xlsx
│   ├── arquitetura/
│   │   ├── Arquitetura.md
│   │   ├── Modelo_de_Dados.md
│   │   ├── openapi.yaml
│   │   └── adr/
│   ├── testes/
│   │   └── Plano_de_Testes.md
│   └── usuario/
│       ├── Manual_do_Usuario.md
│       └── Notas_de_Versao.md
│
├── codigo-fonte/
│   ├── frontend/
│   │   ├── index.html
│   │   ├── css/
│   │   └── js/
│   ├── backend/
│   │   └── ...
│   └── testes/
│       ├── unitarios/
│       ├── integracao/
│       └── postman/
│
└── banco-de-dados/
    └── migracoes/

```

## Gerência de configuração

- **Itens de Configuração (ICs):** todo artefato relevante tem ID no padrão `GYM-REQ-001(nome, tipo, caminho, versão, responsável, baseline, status e dependências` e está catalogado em [`documento/gerencia/Planilha_Controle_de_ICs.xlxs`](documento/gerencia/Planilha_Controle_de_ICs.xlxs).

- **Controle de mudanças:** alterações em itens sob baseline exigem uma Change Request (issue com o formulário CRF), avaliada pelo Comitê de Controle de Mudanças (CCB). Todo commit deve estar vinculado a uma issue ou CR.
  
-**Baselines:** BL-PLAN, BL-REQ-S1, BL-IMPL-S2 e BL-REL-S3 (release v1.0.0), um IC sob baseline só muda mediante Change Request aprovada

-**Commits:** padrão Conventional Commits (feat:, fix:, docs:, test:, chore:), CONTRIBUTING.md

## Equipe

| Papel | Integrante |
|---|---|
| Gerente de Projeto/Configuração | Hugo Henry Lemos Carvalho |
| Analista de Requisitos | Renata Martins Da Silva |
| Dev Backend e Frontend | João Vitor Simonetti |
| DBA/DevOps | João Vitor Simonetti |
| QA/Testes | Iago Medice Ferreira Da Silva, Tiago Costa Dos Santos, Ruan Victor Assunção Costa |

## Documentação

- [Plano de Projeto](documentos/gerencia/Plano-De-Projeto.md)
- [Inventário de ICs](documentos/gerencia/Planilha-de-Controle-ICs.xlsx)
- [Documento de Requisitos (ERS)](documentos/requisitos/ERS.md) *(em elaboração)*
- [Contrato da API (OpenAPI)](documentos/api/openapi.yaml) *(planejado)*
- [Decisões arquiteturais (ADR)](documentos/adr/)

---

Projeto acadêmico em desenvolvimento, disciplina de Gerência de Configuração.
