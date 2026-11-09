# Plano de Projeto — GymManager

**Sistema web de gerenciamento de treinos de academia** Disciplina: Gerência de Configuração (6º período) Professor: Paulo Rodrigo Barbosa Alves.

## 1. Identificação do projeto

| Item | Descrição |
| --- | --- |
| Nome | GymManager |
| Segmento | Saúde e fitness: gestão de treinos em academias |
| Tipo | Aplicação web |
| Repositório | GitHub (link compartilhado com o professor; todos os integrantes como colaboradores) |
| Gerente de Projeto/Configuração | Hugo Henry Lemos Carvalho |
| Equipe | Renata Martins Da Silva, João vitor Simonetti, Iago Medice Ferrreira Da Silva, Tiago Costa Dos Santos, Ruan Victor Assunção Costa |

## 2. Visão geral e objetivos

Academias costumam controlar fichas de treino em papel ou planilhas soltas, o que gera perda de histórico, fichas desatualizadas e pouca visibilidade da evolução do aluno. O GymManager centraliza o cadastro de alunos, o catálogo de exercícios, a montagem de fichas e o registro dos treinos realizados.

**Objetivo geral:** desenvolver um sistema web que permita a instrutores montar fichas de treino e a alunos consultá-las e registrar sua execução.

**Objetivos específicos:**

- Cadastrar e consultar alunos, instrutores e exercícios.
- Montar fichas de treino (exercício, séries, repetições, carga, descanso).
- Registrar treinos executados e acompanhar a evolução de carga.
- Aplicar de forma prática a Gerência de Configuração: identificação de ICs, controle de versões, controle de mudanças, baselines e auditoria.

## 3. Escopo

**Dentro do escopo (versão 1.0.0):**

- Autenticação e perfis de acesso (administrador, instrutor, aluno).
- Gestão de alunos, exercícios e fichas de treino.
- Registro e histórico de execução de treinos.
- API REST documentada (OpenAPI) e interface web.
- Testes automatizados e pipeline de integração contínua.

**Fora do escopo:** aplicativo móvel nativo, pagamentos e mensalidades, integração com catracas ou wearables.

## 4. Tecnologias

| Camada | Tecnologia |
| --- | --- |
| Frontend | HTML, CSS, JavaScript |
| Backend | Python com Flask (API REST) |
| Banco de dados | MySQL, com migrações versionadas em banco-de-dados/migracoes/. |
| Testes | pytest, Postman/Newman |
| CI/CD | GitHub Actions |
| Contêineres | Docker e docker-compose |
| Versionamento | Git + GitHub |

## 5. Equipe e papéis

| Papel | Integrante | Responsabilidades principais |
| --- | --- | --- |
| Gerente de Projeto/Configuração | Hugo Henry Lemos Carvalho | Coordenar entregas; manter repositório, baselines e tags; presidir o CCB; manter Plano de Projeto, PGC e planilha de controle de ICs |
| Analista de Requisitos | Renata Martins Da Silva | ERS, casos de uso e matriz de rastreabilidade (RTM) |
| Dev Backend e Frontend | João Vitor Simonetti | API REST, regras de negócio, autenticação, arquitetura, Interface web, consumo da API, manual do usuário |
| DBA/DevOps | João Vitor Simonetti | Modelo de dados, migrações, Docker, CI, configurações de ambiente |
| QA/Testes | Iago Medice Ferreira da Silva, Tiago Costa Dos Santos, Ruan Victor Assunção | Plano de testes, testes unitários e de integração, coleção Postman, revisão técnica |

## 6. Atividades e responsáveis

| # | Atividade | Responsável (papel) | Apoio | Artefato / IC |
| --- | --- | --- | --- | --- |
| 1 | Criar repositório no GitHub, adicionar colaboradores e compartilhar o link com o professor | Gerente de Projeto/Config | Todos | Repositório |
| 2 | Definir estrutura de diretórios e `.gitignore` | DBA/DevOps | Gerente | GYM-CFG-001 |
| 3 | Elaborar o Plano de Projeto | Gerente de Projeto/Config | Todos | GYM-GER-001 |
| 4 | Elaborar a planilha de controle de ICs | Gerente de Projeto/Config | Analista de Requisitos | GYM-GER-002 |
| 5 | Redigir README e guia de contribuição | Gerente de Projeto/Config | Dev Backend e Frontend | GYM-DOC-001, GYM-GER-004 |
| 6 | Redigir o Plano de Gerência de Configuração e o modelo de CRF | Gerente de Projeto/Config | QA/Testes | GYM-GER-003, GYM-GER-005 |
| 7 | Levantar e documentar requisitos (ERS) e casos de uso | Analista de Requisitos | Todos | GYM-REQ-001, GYM-REQ-002 |
| 8 | Construir a matriz de rastreabilidade (RTM) | Analista de Requisitos | QA/Testes | GYM-REQ-003 |
| 9 | Projetar a arquitetura e registrar a ADR da stack | Dev Backend e Frontend | DBA/DevOps | GYM-ARQ-001, GYM-ARQ-004 |
| 10 | Modelar o banco de dados e escrever as migrações | DBA/DevOps | Dev Backend e Frontend | GYM-ARQ-002, GYM-DB-001 |
| 11 | Especificar a API (OpenAPI) | Dev Backend e Frontend | Analista de Requisitos | GYM-ARQ-003 |
| 12 | Implementar módulos de alunos, exercícios, fichas e execuções | Dev Backend e Frontend | QA/Testes | GYM-SRC-002 a 005 |
| 13 | Implementar autenticação e perfis | Dev Backend e Frontend | DBA/DevOps | GYM-SRC-001 |
| 14 | Implementar a interface web | Dev Backend e Frontend | DBA/DevOps | GYM-SRC-006 |
| 15 | Elaborar plano de testes, testes automatizados e coleção Postman | QA/Testes | Dev Backend e Frontend | GYM-TST-001 a 004 |
| 16 | Configurar pipeline de CI e Docker | DBA/DevOps | QA/Testes | GYM-CI-001, GYM-IAC-001 |
| 17 | Estabelecer baselines, tags e registrar status accounting | Gerente de Projeto/Config | Todos | GYM-GER-006 |
| 18 | Manual do usuário e notas de versão | Dev Backend e Frontend | Gerente de Projeto/Config | GYM-DOC-002, GYM-DOC-003 |
| 19 | Auditoria de configuração e revisão técnica formal antes de cada baseline | QA/Testes | Gerente de Projeto/Config | Todas as baselines |

## 7. Cronograma de entregas

As entregas são semanais, sempre às **quartas-feiras**, acompanhando o conteúdo das aulas. As datas após a Entrega 1 devem ser ajustadas ao calendário da disciplina.

## 8. Gerência de configuração

### 8.1 Identificação

Todo artefato relevante é um Item de Configuração, com ID no padrão `GYM-<TIPO>-<NNN>` (ex.: GYM-REQ-001), catalogado na planilha `documentos/gerencia/Planilha_Controle_de_ICs.xlsx` com nome, tipo, caminho, versão, responsável, baseline, status e dependências (Aulas 3 e 4).

### 8.2 Estrutura do repositório

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

### 8.3 Commits e versionamento

- Mensagens no padrão Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`), com referência à CR ou issue quando houver (ex.: `fix: corrige cálculo de carga (#12)`).
- Nunca enviar código que quebre o build.

### 8.4 Baselines

| Baseline | Tipo | Critério de congelamento |
| --- | --- | --- |
| BL-PLAN | Developmental | Plano de Projeto e planilha de controle de ICs aprovados |
| BL-REQ-S1 | Funcional | ERS, casos de uso e RTM revisados e aprovados pelo CCB |
| BL-IMPL-S2 | Design/Implementação | Backend e testes estáveis, CI verde, revisão técnica concluída |
| BL-REL-S3 | Product/Release | Sistema completo, manual e notas de versão; tag `v1.0.0` |

IC sob baseline só muda mediante Change Request aprovada.

## 9. Controle de mudanças

(1) submissão da CR via issue com o CRF; (2) verificação de validade; (3) registro; (4) análise de custo e impacto; (5) decisão do CCB; (6) implementação e teste; (7) fechamento.

- **CCB:** Gerente de Projeto/Configuração (presidente), Analista de Requisitos e Dev Backend e Frontend.
- **Critérios de decisão:** consequências de não mudar, benefícios, usuários afetados, custo de implementação e ciclo de liberação.
- **Formalidade calibrada:** correções triviais em ICs fora de baseline seguem por issue e Pull Request; mudanças em ICs de baseline ou que atravessam vários módulos passam pelo CCB.
- Toda alteração no repositório deve estar vinculada a uma issue ou CR (rastreabilidade bidirecional).

## 10. Auditoria e relato de status

- **Status accounting:** registro da situação de ICs e baselines atualizado a cada entrega (`documentos/gerencia /Status_Accounting.xlxs`).
- **Revisão técnica formal:** realizada pelo QA/Testes sobre cada IC antes de entrar em baseline.
- **Auditoria de configuração:** verifica se a modificação realizada é a solicitada, se a revisão ocorreu, se o processo foi seguido e se os dados de rastreabilidade (data, autor, nº da CR) constam registrados.

## 11. Riscos

| Risco | Probabilidade | Impacto | Mitigação |
| --- | --- | --- | --- |
| Conflitos de merge frequentes | Média | Médio | Branches curtos, integração diária, commits pequenos |
| Integrante indisponível | Média | Alto | Papéis com apoio definido, documentação no repositório |
| Atraso nas entregas semanais | Média | Alto | Acompanhamento semanal pelo Gerente, escopo mínimo priorizado |
| Mudança de requisitos tardia | Média | Médio | Fluxo de CR e baseline de requisitos |
| Divergência entre ambientes ("funciona na minha máquina") | Baixa | Médio | Docker, `.env.example` e CI |
| Vazamento de segredos no repositório | Baixa | Alto | `.gitignore` rígido, revisão de PR |

## 12. Critérios de qualidade e aceite

- Todos os ICs listados na planilha de controle, com responsável e baseline.
- Pipeline de CI executando build e testes a cada Pull Request.
- Requisitos rastreados até código e testes (RTM).
- Nenhuma alteração em baseline sem CR aprovada.
- Repositório organizado conforme a estrutura da seção 8.2.

## 13. Referências

- Aulas 1 a 7 e 10 da disciplina de Gerência de Configuração (apostilas do Prof. Paulo Rodrigo, CEUNI FAMETRO).
- CHACON, S.; STRAUB, B. *Pro Git*. 2. ed. Apress, 2014.
- SOMMERVILLE, I. *Engenharia de Software*. 10. ed. Pearson, 2019.
- PRESSMAN, R. S.; MAXIM, B. R. *Engenharia de Software: Uma Abordagem Profissional*. 9. ed. AMGH, 2021.
- IEEE Std 828-2012: Configuration Management in Systems and Software Engineering.
- SPÍNOLA, R. O. et al. Gerência de Configuração. *Engenharia de Software Magazine*, ed. 24, 2009.
- PRESTON-WERNER, T. *Semantic Versioning 2.0.0*. https://semver.org/
