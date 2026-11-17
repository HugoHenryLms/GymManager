# 🏋️ GymManager

Sistema web de gerenciamento de treinos de academia: cadastro de alunos e exercícios, montagem de fichas de treino e registro da evolução de cada aluno.

Projeto Integrador da disciplina **Gerência de Configuração** (6º período), CENTRO UNIVERSITÁRIO FAMETRO. Professor: Paulo Rodrigo Barbosa Alves.

> **Status:** versão do sistema 0.1.0. Backend, banco de dados, interface web e ambiente Docker implementados; testes automatizados em andamento (testes iniciais de autenticação e configuração no CI desde o PR #17). A release v1.0.0 está prevista para a baseline BL-REL-S3.


## Sobre o projeto

Academias costumam controlar fichas de treino em papel ou planilhas soltas, o que gera perda de histórico, fichas desatualizadas e pouca visibilidade da evolução do aluno. O GymManager centraliza essas informações: o instrutor monta as fichas e o aluno consulta o treino e registra o que executou.

## Funcionalidades

Escopo da versão 1.0.0:

Implementado na versão 0.1.0:

Autenticação por e-mail e senha, com sessão por token (validade de 8 horas) e perfis de acesso: administrador, instrutor e aluno
Gestão de usuários instrutores (administrador) e de alunos
Catálogo de exercícios
Fichas de treino (exercício, séries, repetições, carga e descanso), com uma ficha vigente por aluno
Registro e histórico de execução de treinos, com acompanhamento da evolução de carga
Exclusão lógica (inativação) com possibilidade de reativação
API REST (/api/v1) documentada com OpenAPI
Interface web

Previsto para a versão 1.0.0: testes automatizados (pytest e Postman/Newman) e manual do usuário completo.

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
├── .github/
│   └── workflows/
│       └── ci.yml
├── banco-de-dados/
│   └── migracoes/
├── codigo-fonte/
│   ├── backend/
│   │   ├── gymmanager/
│   │   ├── Dockerfile
│   │   ├── iniciar.py
│   │   ├── requirements-dev.txt
│   │   ├── requirements.txt
│   │   └── wsgi.py
│   ├── frontend/
│   │   ├── css/
│   │   ├── js/
│   │   ├── Dockerfile
│   │   ├── index.html
│   │   └── nginx.conf
│   └── testes/
│       ├── integracao/
│       ├── postman/
│       └── unitarios/
├── documentos/
│   ├── arquitetura/
│   │   ├── adr/
│   │   ├── Arquitetura.md
│   │   ├── Modelo_de_Dados.md
│   │   └── openapi.yaml
│   ├── gerencia/
│   │   ├── Planilha_Controle_de_ICs.xlsx
│   │   ├── Plano_de_Gerencia_de_Configuracao.md
│   │   └── Plano_de_Projeto.md
│   ├── requisitos/
│   │   ├── Casos_de_Uso.md
│   │   ├── ERS.md
│   │   └── RTM.xlsx
│   ├── testes/
│   │   ├── Casos_de_Teste.md
│   │   ├── Plano_de_Testes.md
│   │   ├── Registro_de_Defeitos.md
│   │   └── Relatorio_de_Testes.md
│   └── usuario/
│       ├── Manual_do_Usuario.md
│       └── Notas_de_Versao.md
├── prototipos/
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── LICENSE
└── README.md
```

## Gerência de configuração

- **Itens de Configuração (ICs):** todo artefato relevante tem ID no padrão `GYM-<TIPO>-<NNN>` (ex.: `GYM-REQ-001`), com nome, tipo, caminho, versão, responsável, baseline, status e dependências, e está catalogado em [`documentos/gerencia/Planilha_Controle_de_ICs.xlsx`](documentos/gerencia/Planilha_Controle_de_ICs.xlsx).

- **Controle de mudanças:** alterações em itens sob baseline exigem uma Change Request (issue com o formulário CRF), avaliada pelo Comitê de Controle de Mudanças (CCB). Todo commit deve estar vinculado a uma issue ou CR.
  
- **Baselines:** BL-PLAN, BL-REQ-S1, BL-IMPL-S2 e BL-REL-S3 (release v1.0.0), um IC sob baseline só muda mediante Change Request aprovada

- **Commits:** padrão Conventional Commits (feat:, fix:, docs:, test:, chore:), conforme o [CONTRIBUTING.md](CONTRIBUTING.md).
- **Branches:** <tipo>/<id-do-ic>-<descricao-curta> (ex.: feat/gym-src-004-fichas-de-treino), integrados à main por Pull Request. A lista dos branches utilizados está no Plano de Gerência de Configuração, seção 4.2.

## Equipe

| Papel | Integrante |
|---|---|
| Gerente de Projeto/Configuração | Hugo Henry Lemos Carvalho |
| Analista de Requisitos | Renata Martins Da Silva |
| Dev Backend e Frontend | João Vitor Simonetti |
| DBA/DevOps | João Vitor Simonetti |
| QA/Testes | Iago Medice Ferreira Da Silva, Tiago Costa Dos Santos, Ruan Victor Assunção Costa |

## Documentação

- [Plano de Projeto](documentos/gerencia/Plano_de_Projeto.md)
- [Plano de Gerência de Configuração](documentos/gerencia/Plano_de_Gerencia_de_Configuracao.md)
- [Inventário de ICs (Planilha de Controle)](documentos/gerencia/Planilha_Controle_de_ICs.xlsx)
- [Documento de Requisitos (ERS)](documentos/requisitos/ERS.md)
- [Casos de Uso](documentos/requisitos/Casos_de_Uso.md)
- [Matriz de Rastreabilidade (RTM)](documentos/requisitos/RTM.xlsx)
- [Arquitetura](documentos/arquitetura/Arquitetura.md) e [Modelo de Dados](documentos/arquitetura/Modelo_de_Dados.md)
- [Contrato da API (OpenAPI)](documentos/arquitetura/openapi.yaml)
- [Decisões arquiteturais (ADR)](documentos/arquitetura/adr/ADR-001-stack.md)
- [Plano de Testes](documentos/testes/Plano_de_Testes.md) e [Casos de Teste](documentos/testes/Casos_de_Teste.md)
- [Manual do Usuário](documentos/usuario/Manual_do_Usuario.md) e [Notas de Versão](documentos/usuario/Notas_de_Versao.md)

Projeto acadêmico em desenvolvimento, disciplina de Gerência de Configuração.
