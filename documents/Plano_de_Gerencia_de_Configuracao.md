# Plano de Gerência de Configuração — GymManager

**Sistema web de gerenciamento de treinos de academia**
Disciplina: Gerência de Configuração (6º período) · CENTRO UNIVERSITÁRIO FAMETRO
Professor: Paulo Rodrigo Barbosa Alves

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-GER-003 |
| Caminho | `documentos/gerencia/Plano_de_Gerencia_de_Configuracao.md` |
| Versão | 0.1.1 |
| Status | Em elaboração |
| Baseline prevista | BL-REQ-S1 |
| Responsável | Hugo Henry Lemos Carvalho (Gerente de Projeto/Configuração) |
| Apoio | QA/Testes |
| Dependência | GYM-GER-001 (Plano de Projeto) |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.1.1 | 09/11/2026 | Hugo Henry Lemos Carvalho | Versão inicial do plano | — |

---

## 1. Introdução

### 1.1 Propósito

Este plano define **como a configuração do GymManager será gerenciada** ao longo do projeto: como os artefatos são identificados, versionados, alterados, congelados em baselines, auditados e relatados. Ele detalha a seção 8 (Gerência de configuração), a seção 9 (Controle de mudanças) e a seção 10 (Auditoria e relato de status) do Plano de Projeto (GYM-GER-001).

### 1.2 Escopo

Aplica-se a **todos os Itens de Configuração (ICs)** do projeto, catalogados na planilha `documentos/gerencia/Planilha_Controle_de_ICs.xlsx` (GYM-GER-002): documentos de gerência, requisitos, arquitetura, banco de dados, código-fonte, testes, CI/CD, infraestrutura e documentação de usuário. Aplica-se a todos os integrantes da equipe.

### 1.3 Documentos de referência

- Plano de Projeto (GYM-GER-001).
- Planilha de Controle de ICs (GYM-GER-002).
- IEEE Std 828-2012: *Configuration Management in Systems and Software Engineering*.
- Apostilas das Aulas 1 a 7 e 10 da disciplina de Gerência de Configuração (Prof. Paulo Rodrigo).
- PRESTON-WERNER, T. *Semantic Versioning 2.0.0*. https://semver.org/
- CHACON, S.; STRAUB, B. *Pro Git*. 2. ed. Apress, 2014.

### 1.4 Definições e siglas

| Termo | Definição |
| --- | --- |
| GC | Gerência de Configuração |
| IC | Item de Configuração: artefato sob controle de versão e de mudanças |
| Baseline | Conjunto de ICs revisados e aprovados, congelado em um marco; só muda via CR |
| CR | *Change Request*: solicitação formal de mudança |
| CRF | *Change Request Form*: formulário da CR (`documentos/gerencia/Modelo_CRF.md`) |
| CCB | *Change Control Board*: comitê que decide sobre as CRs |
| RTM | Matriz de Rastreabilidade de Requisitos |
| PR | *Pull Request* |
| ERS | Documento de Especificação de Requisitos |
| ADR | *Architecture Decision Record* |
| SemVer | Versionamento Semântico (MAJOR.MINOR.PATCH) |

---

## 2. Organização e responsabilidades

| Papel | Integrante | Responsabilidades na GC |
| --- | --- | --- |
| Gerente de Projeto/Configuração | Hugo Henry Lemos Carvalho | Manter o repositório, as baselines e as tags; presidir o CCB; manter o Plano de Projeto, este plano e a planilha de ICs; atualizar o status accounting a cada entrega |
| Analista de Requisitos | Renata Martins da Silva | Manter ERS, casos de uso e RTM; membro do CCB; avaliar impacto de CRs sobre requisitos |
| Dev Backend e Frontend | João Vitor Simonetti | Implementar mudanças aprovadas no código e na documentação técnica; membro do CCB; avaliar impacto técnico |
| DBA/DevOps | João Vitor Simonetti | Estrutura de diretórios, migrações, Docker, CI e configurações de ambiente |
| QA/Testes | Iago Medice Ferreira da Silva, Tiago Costa dos Santos, Ruan Victor Assunção Costa | Revisão técnica formal antes de cada baseline; auditoria de configuração; testes de verificação das mudanças |

**Observações:**

- Um mesmo integrante acumula os papéis de Dev Backend e Frontend e de DBA/DevOps. Para preservar a independência da revisão, **o autor de uma alteração nunca aprova o próprio PR**: a revisão cabe a outro integrante (de preferência do QA/Testes).
- A decisão do CCB é por maioria simples; em caso de empate, vale o voto do presidente (Gerente de Projeto/Configuração).

---

## 3. Identificação da configuração

### 3.1 Padrão de identificação dos ICs

Todo IC possui um ID único no padrão **`GYM-<TIPO>-<NNN>`** (ex.: `GYM-REQ-001`), em que `<NNN>` é um número sequencial de três dígitos dentro do tipo. IDs nunca são reutilizados, mesmo que o IC seja removido.

| Prefixo | Tipo | Exemplos |
| --- | --- | --- |
| CFG | Configuração do repositório | `.gitignore`, `.env.example`, `LICENSE` |
| GER | Gerência | Plano de Projeto, planilha de ICs, este plano, CRF, status accounting |
| REQ | Requisitos | ERS, casos de uso, RTM, protótipos |
| ARQ | Arquitetura | Arquitetura, modelo de dados, OpenAPI, ADRs |
| DB | Banco de dados | Migrações |
| SRC | Código-fonte | Módulos do backend e frontend |
| TST | Testes | Plano de testes, testes unitários/integração, coleção Postman |
| CI | Integração contínua | `ci.yml` |
| IAC | Infraestrutura como código | `docker-compose.yml`, Dockerfile(s) |
| DOC | Documentação | README, manual do usuário, notas de versão |

### 3.2 Catálogo de ICs

O catálogo oficial é a planilha `documentos/gerencia/Planilha_Controle_de_ICs.xlsx` (GYM-GER-002). Para cada IC ela registra: **ID, nome, tipo, descrição, caminho, versão, responsável, apoio, baseline, status, dependências e situação da revisão técnica**. A planilha é a fonte única de verdade para a identificação; qualquer divergência entre ela e o repositório é tratada como não conformidade na auditoria.

Todo novo artefato relevante deve ser registrado na planilha **antes** de ser incorporado ao repositório principal.

### 3.3 Convenções de nomenclatura

- Pastas de documentação em português, sem acentos e minúsculas (`documentos/gerencia/`).
- Arquivos de documentação em `Snake_Case` com inicial maiúscula (`Plano_de_Projeto.md`), exceto arquivos convencionais (`README.md`, `CONTRIBUTING.md`, `LICENSE`, `openapi.yaml`).
- Extensões corretas e conferidas (`.xlsx`, não `.xlxs`).
- Planilhas e documentos de gerência em `documentos/gerencia/`; requisitos em `documentos/requisitos/`; arquitetura (incluindo `openapi.yaml` e `adr/`) em `documentos/arquitetura/`.
- ADRs: `documentos/arquitetura/adr/ADR-NNN-titulo-curto.md`.

### 3.4 Estrutura do repositório

O repositório segue a estrutura da seção 8.2 do Plano de Projeto:

```
GymManager/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── .github/
│   ├── workflows/ci.yml
│   └── ISSUE_TEMPLATE/change-request.md
├── prototipos/
├── documentos/
│   ├── gerencia/        (Plano_de_Projeto, Planilha_Controle_de_ICs, este plano, Modelo_CRF, Status_Accounting)
│   ├── requisitos/      (ERS, Casos_de_Uso, RTM)
│   ├── arquitetura/     (Arquitetura, Modelo_de_Dados, openapi.yaml, adr/)
│   ├── testes/          (Plano_de_Testes)
│   └── usuario/         (Manual_do_Usuario, Notas_de_Versao)
├── codigo-fonte/
│   ├── frontend/
│   ├── backend/
│   └── testes/          (unitarios/, integracao/, postman/)
└── banco-de-dados/
    └── migracoes/
```

Nenhuma alteração estrutural (criar, mover ou remover pastas de primeiro nível) é feita sem registro na planilha de ICs e aprovação do Gerente de Projeto/Configuração.

### 3.5 Versionamento dos ICs

Adota-se o **Versionamento Semântico (MAJOR.MINOR.PATCH)** para ICs individuais e para o produto:

| Faixa | Significado |
| --- | --- |
| `0.0.0` | IC planejado, ainda sem arquivo no repositório |
| `0.x.y` | IC em elaboração |
| `1.0.0` | Primeira versão aprovada e baselinada |
| MAJOR | Mudança incompatível ou reestruturação profunda do IC |
| MINOR | Acréscimo de conteúdo ou funcionalidade compatível |
| PATCH | Correção que não altera o escopo (erros de grafia, ajustes pontuais) |

A versão do **produto** é marcada por *tag* no Git (`vMAJOR.MINOR.PATCH`); a primeira release é a `v1.0.0`. A versão de cada IC é registrada na planilha de ICs e, nos documentos, na tabela de controle e no histórico de revisões.

---

## 4. Gerenciamento do repositório e fluxo de trabalho

### 4.1 Ferramentas

| Finalidade | Ferramenta |
| --- | --- |
| Controle de versão | Git + GitHub (todos os integrantes como colaboradores; link compartilhado com o professor) |
| Solicitações de mudança e tarefas | GitHub Issues (template `change-request.md`) |
| Integração contínua | GitHub Actions (`ci.yml`) |
| Testes | pytest e Postman/Newman |
| Ambiente reprodutível | Docker e docker-compose, `.env.example` |
| Catálogos e relatórios | Planilhas `.xlsx` em `documentos/gerencia/` |

### 4.2 Estratégia de branches

- **`main`**: contém sempre a última versão estável; protegida (sem push direto; alteração apenas via Pull Request aprovado e CI verde). Cada baseline é marcada nela.
- **Branches de trabalho curtos**, criados a partir da `main` e integrados com frequência (integração diária), para reduzir conflitos de merge. Nomenclatura: `<tipo>/<id-issue>-<descricao-curta>` (ex.: `feat/12-ficha-de-treino`, `docs/7-ers`, `fix/21-calculo-carga`).
- Branches são removidos após o merge.

### 4.3 Commits

- Padrão **Conventional Commits**: `feat:`, `fix:`, `docs:`, `test:`, `chore:`.
- Referência à issue ou CR quando houver: `fix: corrige cálculo de carga (#12)`.
- Commits pequenos e atômicos; **nunca enviar código que quebre o build**.
- **Toda alteração no repositório deve estar vinculada a uma issue ou CR**, garantindo rastreabilidade bidirecional (issue ↔ commit/PR).
- Segredos (senhas, chaves, tokens) nunca são versionados; o `.gitignore` e a revisão de PR reduzem esse risco, e apenas `.env.example` (sem valores reais) é commitado.

### 4.4 Pull Requests

Todo PR deve:

1. Referenciar a issue/CR (`Closes #N`).
2. Atualizar a versão e o histórico do IC alterado, quando aplicável.
3. Passar no pipeline de CI (build e testes).
4. Ser aprovado por ao menos **um revisor diferente do autor**.
5. Para IC sob baseline: só ser mesclado com CR aprovada pelo CCB.

### 4.5 Backup e recuperação

O repositório no GitHub é a cópia mestre; cada integrante mantém clone local completo, o que constitui as demais cópias de segurança. Em caso de perda, o repositório é recuperado a partir de qualquer clone atualizado. Baselines são preservadas por *tags* anotadas.

---

## 5. Baselines

### 5.1 Baselines previstas

| Baseline | Tipo | Critério de congelamento | Marco |
| --- | --- | --- | --- |
| BL-PLAN | Developmental | Plano de Projeto e planilha de controle de ICs aprovados | Tag `BL-PLAN` |
| BL-REQ-S1 | Funcional | ERS, casos de uso e RTM revisados e aprovados pelo CCB | Tag `BL-REQ-S1` |
| BL-IMPL-S2 | Design/Implementação | Backend e testes estáveis, CI verde, revisão técnica concluída | Tag `BL-IMPL-S2` |
| BL-REL-S3 | Product/Release | Sistema completo, manual e notas de versão | Tag `v1.0.0` |

A relação de ICs de cada baseline está na coluna **Baseline** da planilha de ICs (GYM-GER-002).

### 5.2 Procedimento de criação de uma baseline

1. O Gerente de Projeto/Configuração confirma na planilha que todos os ICs da baseline estão com status **Aprovado**.
2. O QA/Testes realiza a **revisão técnica formal** de cada IC e a **auditoria de configuração** (seção 8), registrando o resultado.
3. O CCB aprova o congelamento (obrigatório em BL-REQ-S1; nas demais, aprovação do Gerente com registro).
4. O Gerente cria a *tag* anotada na `main`, com a mensagem listando os ICs e suas versões.
5. A planilha de ICs e o status accounting são atualizados (status **Em baseline**).

### 5.3 Regra de proteção

**IC sob baseline só muda mediante Change Request aprovada.** Após a mudança, o IC recebe nova versão e a baseline é reemitida (ex.: `BL-REQ-S1` revisão 2), preservando as tags anteriores para histórico.

---

## 6. Controle de mudanças

### 6.1 Processo

| Etapa | Descrição | Responsável |
| --- | --- | --- |
| 1. Submissão | Abertura de issue com o template `change-request.md` e o CRF preenchido | Qualquer integrante |
| 2. Verificação de validade | Confere se o formulário está completo e se a mudança é pertinente ao escopo | Gerente |
| 3. Registro | A CR recebe número (`CR-NNN`) e é registrada no status accounting | Gerente |
| 4. Análise de custo e impacto | Identifica ICs afetados (pela coluna Dependências e pela RTM), esforço e riscos | Analista de Requisitos, Dev Backend e Frontend |
| 5. Decisão do CCB | Aprova, rejeita ou adia | CCB |
| 6. Implementação e teste | Execução em branch dedicado, PR, CI e testes de verificação | Responsável designado + QA/Testes |
| 7. Fechamento | Atualiza versões, planilha de ICs, RTM e status accounting; fecha a issue/CR | Gerente |

### 6.2 Comitê de Controle de Mudanças (CCB)

- **Composição:** Gerente de Projeto/Configuração (presidente), Analista de Requisitos e Dev Backend e Frontend.
- **Critérios de decisão:** consequências de não mudar, benefícios, usuários afetados, custo de implementação e ciclo de liberação.
- **Reuniões:** sob demanda, preferencialmente na semana da entrega; decisões registradas na própria issue/CR.

### 6.3 Formalidade calibrada

| Situação | Tratamento |
| --- | --- |
| Correção trivial em IC **fora** de baseline | Issue + Pull Request, com revisão de outro integrante |
| Mudança em IC **sob** baseline | CR completa, decisão do CCB |
| Mudança que atravessa vários módulos ou ICs | CR completa, decisão do CCB |
| Mudança de requisitos após BL-REQ-S1 | CR completa; atualização de ERS, casos de uso, RTM e testes afetados |
| Mudança urgente (falha crítica) | Correção imediata em branch próprio com aprovação do Gerente; CR registrada em até 1 dia útil |

### 6.4 Estados de uma CR

`Aberta` → `Em análise` → `Aprovada` / `Rejeitada` / `Adiada` → `Em implementação` → `Verificada` → `Fechada`

### 6.5 Conteúdo mínimo do CRF

Número da CR; data e solicitante; ICs afetados (IDs e versões); descrição e justificativa; tipo (correção, melhoria, mudança de requisito); prioridade; análise de impacto (custo, prazo, módulos, testes, documentos); decisão do CCB e data; responsável pela implementação; resultado da verificação; versões resultantes.

---

## 7. Relato de status (status accounting)

O registro de status é mantido em `documentos/gerencia/Status_Accounting.xlsx` (GYM-GER-006), atualizado **a cada entrega semanal** pelo Gerente de Projeto/Configuração.

| Aba | Conteúdo |
| --- | --- |
| ICs | Situação de cada IC: versão atual, status, baseline, data da última alteração e autor |
| Baselines | Baselines emitidas: data, tag, ICs e versões incluídas |
| Change Requests | Número, data, solicitante, ICs afetados, decisão do CCB, situação e versões resultantes |
| Relatório da entrega | Resumo da semana: ICs criados/alterados, CRs abertas/fechadas, pendências de auditoria |

**Consultas que o registro deve responder:** qual a versão atual de cada IC; quais ICs pertencem a cada baseline; quais mudanças foram feitas desde a última baseline e por quê; quais CRs estão abertas.

Os dados de rastreabilidade (data, autor, nº da CR) devem constar tanto no registro quanto no histórico do Git.

---

## 8. Auditoria e revisões

### 8.1 Revisão técnica formal

Realizada pelo **QA/Testes sobre cada IC antes de entrar em baseline**. Verifica correção, completude, consistência com os demais ICs (RTM) e aderência a padrões. O resultado é registrado na coluna *Revisão técnica (QA)* da planilha de ICs (Pendente / Em andamento / Concluída).

### 8.2 Auditoria de configuração

Executada pelo QA/Testes, com apoio do Gerente, **antes de cada baseline** e ao final do projeto. Verifica:

1. A modificação realizada é a solicitada (conformidade com a CR).
2. A revisão técnica ocorreu.
3. O processo definido neste plano foi seguido.
4. Os dados de rastreabilidade (data, autor, nº da CR) constam registrados.

### 8.3 Lista de verificação da auditoria

| # | Verificação | Resultado |
| --- | --- | --- |
| 1 | Todo IC do repositório consta na planilha, com ID, versão, responsável e baseline | ☐ |
| 2 | Caminhos e nomes dos arquivos coincidem com a planilha e com a estrutura da seção 3.4 | ☐ |
| 3 | A versão informada na planilha coincide com a do próprio IC | ☐ |
| 4 | Todos os commits do período referenciam issue ou CR | ☐ |
| 5 | Nenhuma alteração em IC sob baseline sem CR aprovada | ☐ |
| 6 | Revisão técnica registrada para todos os ICs da baseline | ☐ |
| 7 | CI verde na `main` e testes executados | ☐ |
| 8 | RTM atualizada (requisito ↔ IC de projeto ↔ código ↔ teste) | ☐ |
| 9 | Status accounting atualizado | ☐ |
| 10 | Nenhum segredo ou arquivo indevido no repositório | ☐ |
| 11 | Tag da baseline criada e coerente com o conteúdo | ☐ |

Não conformidades são registradas como issues, atribuídas a um responsável e corrigidas antes do congelamento da baseline.

---

## 9. Gerenciamento de build e release

- O pipeline **GitHub Actions** (GYM-CI-001) executa build e testes (pytest e Newman) a cada Pull Request e a cada push na `main`; PR com CI vermelho não é mesclado.
- O ambiente de execução é reproduzível com Docker e docker-compose (GYM-IAC-001), com variáveis definidas a partir do `.env.example` (GYM-CFG-002).
- A **release `v1.0.0`** (BL-REL-S3) só é emitida com: todos os ICs aprovados e revisados, CI verde, manual do usuário e notas de versão publicados, auditoria final concluída e tag anotada na `main`.
- As **notas de versão** (GYM-DOC-003) listam, para cada release, as CRs incorporadas, as correções e as versões dos ICs principais.

---

## 10. Cronograma de atividades de GC

As entregas são semanais, às **quartas-feiras**, acompanhando o conteúdo da disciplina (as datas após a Entrega 1 seguem o calendário da disciplina).

| Marco | Atividade de GC | Responsável |
| --- | --- | --- |
| Entrega 1| Repositório criado, planilha de ICs, Plano de Projeto atualizado, BL-PLAN | Gerente |
| Entrega 2| ERS e RTM no repositório |Analista de Requisitos; 
| A cada entrega | Atualização do status accounting e da planilha de ICs | Gerente |
| Antes de BL-REQ-S1 | Revisão técnica e CCB sobre ERS, casos de uso e RTM | QA/Testes, CCB |
| Antes de BL-IMPL-S2 | Revisão técnica e auditoria; CI verde | QA/Testes |
| Antes de BL-REL-S3 | Auditoria final; tag `v1.0.0` | QA/Testes, Gerente |

---

## 11. Riscos da gerência de configuração

| Risco | Mitigação neste plano |
| --- | --- |
| Conflitos de merge frequentes | Branches curtos, integração diária e commits pequenos (seções 4.2 e 4.3) |
| Alterações fora do processo | Branch `main` protegida, PR obrigatório, auditoria (seções 4.4 e 8) |
| Planilha de ICs desatualizada | Registro prévio do IC e atualização a cada entrega; verificação na auditoria (itens 1 a 3) |
| Mudança de requisitos tardia | Fluxo de CR e baseline de requisitos (seções 5 e 6) |
| Integrante indisponível | Papéis com apoio definido e documentação no repositório; qualquer integrante pode abrir CR e PR |
| Vazamento de segredos | `.gitignore` rígido, `.env.example` sem valores reais e revisão de PR |
| Acúmulo de papéis (Dev e DBA/DevOps) | Revisão obrigatória por outro integrante (seção 2) |

---

## 12. Manutenção deste plano

Este plano é um IC (GYM-GER-003) e está sujeito às próprias regras: mudanças após a baseline BL-REQ-S1 exigem CR aprovada pelo CCB, e cada revisão incrementa a versão e o histórico no início do documento.

## Anexo A — ICs previstos por baseline

| Baseline | ICs |
| --- | --- |
| BL-PLAN | GYM-GER-001, GYM-GER-002 |
| BL-REQ-S1 | GYM-GER-003, GYM-GER-004, GYM-GER-005, GYM-CFG-004, GYM-REQ-001, GYM-REQ-002, GYM-REQ-003, GYM-REQ-004 |
| BL-IMPL-S2 | GYM-CFG-002, GYM-ARQ-001 a 004, GYM-DB-001, GYM-SRC-001 a 005, GYM-TST-001 a 004, GYM-CI-001, GYM-IAC-001 |
| BL-REL-S3 | GYM-CFG-003, GYM-SRC-006, GYM-DOC-001, GYM-DOC-002, GYM-DOC-003 |
| Sem baseline | GYM-CFG-001, GYM-GER-006 |

*Fonte: planilha de ICs (GYM-GER-002). Em caso de divergência, a planilha prevalece.*
