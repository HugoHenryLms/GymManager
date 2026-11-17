# Plano de Testes — GymManager

**Sistema web de gerenciamento de treinos de academia**
Disciplina: Gerência de Configuração (6º período) · CENTRO UNIVERSITÁRIO FAMETRO
Professor: Paulo Rodrigo Barbosa Alves

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-TST-001 |
| Caminho | `documentos/testes/Plano_de_Testes.md` |
| Versão | 0.1.0 |
| Status | Em elaboração |
| Baseline prevista | BL-IMPL-S2 (Design/Implementação) |
| Responsável | QA/Testes (Iago Medice Ferreira da Silva, Tiago Costa dos Santos, Ruan Victor Assunção Costa) |
| Elaboração desta versão | Renata Martins da Silva (Analista de Requisitos) |
| Apoio | João Vitor Simonetti (Dev Backend e Frontend) |
| Dependências | GYM-REQ-001 (ERS), GYM-REQ-003 (RTM) |
| ICs relacionados | GYM-TST-002 a GYM-TST-007, GYM-CI-001, GYM-REQ-002 (Casos de Uso) |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.0.0 | 11-11-2026 | QA/Testes | Arquivo criado vazio (placeholder) | — |
| 0.1.0 | 16-11-2026 | Renata Martins da Silva | Primeira versão do plano. Formaliza a estratégia já aplicada nos testes automatizados iniciais (PR #17) e define o escopo, os níveis, os critérios de aceite e a cobertura planejada até a baseline BL-IMPL-S2 | #18 |

> **Observação de configuração:** este plano foi formalizado depois dos primeiros testes automatizados, incorporados à `main` pelo PR #17. O desvio está registrado aqui para fins de rastreabilidade. A partir desta versão, o plano é atualizado **antes** da implementação de novos testes.

---

## 1. Introdução

### 1.1 Propósito

Este documento define a estratégia, o escopo, os recursos, os critérios de aceite e a cobertura dos testes do **GymManager**. Ele orienta a elaboração dos testes automatizados (GYM-TST-002 a 004) e manuais (GYM-TST-005) e o registro dos resultados (GYM-TST-006 e 007). Também garante que cada requisito do ERS (GYM-REQ-001) seja verificado e rastreado na RTM (GYM-REQ-003).

### 1.2 Escopo

**Dentro do escopo:**

- API REST do backend (Flask): as 23 operações especificadas no ERS (seção 4.5) e no contrato OpenAPI (GYM-ARQ-003).
- Regras de negócio RN01 a RN12.
- Autenticação, sessão e controle de acesso por perfil (RF02, RNF01, RNF02, RNF13).
- Integração com o banco MySQL e as migrações (GYM-DB-001).
- Interface web (GYM-SRC-006), por meio dos casos de teste manuais CT01 a CT12.
- Ambiente completo em Docker (teste de fumaça do CI).

**Fora do escopo nesta versão:**

- Teste de carga e estresse (apenas a verificação simples de tempo de resposta do RNF04, ver 4.4).
- Testes automatizados de interface (Selenium, Playwright ou semelhantes).
- Funções que aparecem nos protótipos mas não foram implementadas (relatórios, metas semanais, avaliação física, perfil do usuário), conforme ERS 1.2.

### 1.3 Referências

- ERS — GYM-REQ-001 (`documentos/requisitos/ERS.md`)
- Casos de Uso — GYM-REQ-002 (`documentos/requisitos/Casos_de_Uso.md`)
- RTM — GYM-REQ-003 (`documentos/requisitos/RTM.xlsx`)
- Plano de Gerência de Configuração — GYM-GER-003
- Especificação OpenAPI — GYM-ARQ-003 (`documentos/arquitetura/openapi.yaml`)
- Pipeline de CI — GYM-CI-001 (`.github/workflows/ci.yml`)
- ISO/IEC/IEEE 29119-3 — Documentação de testes de software

### 1.4 Definições

| Termo | Significado |
| --- | --- |
| Teste unitário | Verifica uma função ou módulo isolado, sem banco de dados nem rede |
| Teste de integração | Verifica a API junto com o banco de dados real (MySQL), pelo cliente de testes do Flask |
| Teste de API | Requisições HTTP ao sistema em execução no Docker, pela coleção Postman/Newman |
| Teste funcional manual | Execução de um caso de teste (CT) pela interface web, seguindo o procedimento descrito |
| Teste de fumaça | Verificação mínima de que o sistema sobe e responde (login do administrador) |
| Regressão | Defeito que volta a aparecer em uma função que já funcionava |

---

## 2. Itens a testar

| IC | Item | Versão testada |
| --- | --- | --- |
| GYM-SRC-001 | Módulo de autenticação e perfis (`auth/`, `usuarios/`) | 0.1.0 |
| GYM-SRC-002 | Módulo de alunos (`alunos/`) | 0.1.0 |
| GYM-SRC-003 | Módulo de exercícios (`exercicios/`) | 0.1.0 |
| GYM-SRC-004 | Módulo de fichas de treino (`fichas/`) | 0.1.0 |
| GYM-SRC-005 | Módulo de execuções de treino (`execucoes/`) | 0.1.0 |
| GYM-SRC-006 | Interface web (`frontend/`) | 0.1.0 |
| GYM-DB-001 | Migrações do banco de dados | 0.1.0 |
| GYM-IAC-001 | Docker e docker-compose | 0.1.0 |

A versão testada de cada IC é registrada no Relatório de Testes (GYM-TST-007) a cada ciclo.

---

## 3. Níveis e estratégia de teste

| Nível | IC | Ferramenta | Onde fica | Quando executa |
| --- | --- | --- | --- | --- |
| Unitário | GYM-TST-002 | pytest | `codigo-fonte/testes/unitarios/` | A cada PR e push na `main` (CI, job *Backend*) |
| Integração | GYM-TST-003 | pytest + MySQL 8.4 | `codigo-fonte/testes/integracao/` | A cada PR e push na `main` (CI, job *Backend*) |
| API | GYM-TST-004 | Postman / Newman | `codigo-fonte/testes/postman/` | A cada PR e push na `main` (CI, job *Docker*) |
| Fumaça | GYM-CI-001 | curl + jq | `.github/workflows/ci.yml` | A cada PR e push na `main` (CI, job *Docker*) |
| Funcional manual | GYM-TST-005 | Navegador | `documentos/testes/Casos_de_Teste.md` | Antes de cada baseline (BL-IMPL-S2 e BL-REL-S3) |

### 3.1 Testes unitários (GYM-TST-002)

Verificam funções que não dependem de banco nem de requisição HTTP. Alvos principais:

- `validacao.py`: `nome`, `email`, `senha`, `perfil`, `carga`, `descanso`, `inteiro_positivo`, `data` e `periodo`, com valores válidos e inválidos (devem lançar `ErroAPI`).
- `auth/seguranca.py`: `gerar_hash_senha` (o hash nunca é igual à senha em texto, conforme RNF01) e `_hash_token`.
- `migracoes.py`: `listar_migracoes`, `checksum` e `instrucoes` (separação do SQL em instruções).
- `create_app()`: criação da aplicação e configuração obrigatória (`SECRET_KEY`).

### 3.2 Testes de integração (GYM-TST-003)

Usam o cliente de testes do Flask (`app.test_client()`) contra o MySQL do CI, já migrado e com o administrador inicial criado (`flask criar-admin`). Para cada módulo, cobrem no mínimo:

1. **Caminho de sucesso** (ex.: cadastrar e consultar).
2. **Erro de validação** (ex.: campo obrigatório ausente, retorno `400`).
3. **Controle de acesso**: sem token (`401`) e com perfil não autorizado (`403`).

**Regras para os dados de teste:**

- O banco do CI **não é limpo entre os testes**. Cada teste cria os próprios dados, com nomes e e-mails únicos (por exemplo, com `uuid4()`), e não depende da ordem de execução.
- As credenciais do administrador vêm das variáveis `ADMIN_EMAIL` e `ADMIN_SENHA` definidas no CI. Nenhuma senha real é versionada (RNF03).
- Fixtures comuns (cliente, login como admin, criação de instrutor e de aluno) devem ser centralizadas em `codigo-fonte/testes/conftest.py`, para evitar repetição.

### 3.3 Testes de API (GYM-TST-004)

Coleção Postman executada pelo Newman no ambiente Docker completo, passando pelo proxy do frontend. O CI fornece as variáveis `baseUrl`, `adminEmail` e `adminSenha`. A coleção deve seguir um fluxo completo: login do administrador → cadastro de instrutor → cadastro de aluno → cadastro de exercício → criação de ficha → login do aluno → início, registro e finalização da execução → consulta do histórico → logout.

### 3.4 Requisitos não funcionais

| RNF | Como será verificado |
| --- | --- |
| RNF01 | Teste unitário: hash da senha diferente do texto puro |
| RNF02 | Testes de integração: rotas protegidas retornam `401` sem token |
| RNF03 | Revisão de PR e auditoria de configuração (item 10 da checklist do PGC) |
| RNF04 | Asserção na coleção Newman: tempo de resposta < 2000 ms em cada requisição |
| RNF05, RNF06 | Teste manual em desktop e celular e nos navegadores Chrome, Firefox e Edge, registrado no Relatório de Testes |
| RNF08 | Execução do CI a cada PR (verificada na aba *Checks*) |
| RNF09 | Validação do `openapi.yaml` no CI |
| RNF11 | Migrações aplicadas duas vezes no CI (idempotência) |
| RNF13 | Teste de integração: token inválido ou de sessão encerrada (logout) retorna `401` |
| RNF14 | Inspeção dos cabeçalhos de resposta do frontend (manual ou Newman) |

---

## 4. Cobertura planejada

### 4.1 Requisitos funcionais × níveis × casos de teste

| Requisito | Caso de uso | Caso(s) de teste manual | Integração (pytest) | API (Newman) |
| --- | --- | --- | --- | --- |
| RF01 — Alunos | UC03 | CT05 | Planejado | Planejado |
| RF02 — Autenticação e perfis | UC01 | CT01, CT02, CT12 | **Parcial** (login válido e senha incorreta) | Planejado |
| RF03 — Exercícios | UC04 | CT06 | Planejado | Planejado |
| RF04 — Fichas de treino | UC05, UC06 | CT07, CT08, CT11 | Planejado | Planejado |
| RF05 — Execuções e histórico | UC07, UC08 | CT09, CT10, CT11 | Planejado | Planejado |
| RF06 — Usuários e instrutores | UC02 | CT03, CT04 | Planejado | Planejado |
| RF07 — Interface por perfil | UC01 a UC08 | CT01 a CT12 | — | — |

### 4.2 Testes automatizados existentes (versão 0.1.0 do sistema)

| Arquivo | Nível | Teste | Verifica | CT |
| --- | --- | --- | --- | --- |
| `unitarios/test_configuracao.py` | Unitário | `test_criacao_aplicacao_flask` | Aplicação criada com `SECRET_KEY` | — |
| `integracao/test_autenticacao.py` | Integração | `test_login_admin_sucesso` | Login válido retorna token e perfil `ADMIN` (RF02) | CT01 |
| `integracao/test_autenticacao.py` | Integração | `test_login_senha_incorreta` | Senha incorreta retorna `400` ou `401` (RF02) | CT02 |

### 4.3 Meta mínima por módulo até a BL-IMPL-S2

| Módulo | Testes de integração mínimos | Regras cobertas |
| --- | --- | --- |
| Autenticação | Login válido ✅; senha incorreta ✅; usuário inativo não autentica; logout invalida o token; rota protegida sem token → `401` | RF02, RN05, RNF02, RNF13 |
| Usuários | Admin cadastra instrutor; e-mail duplicado rejeitado; instrutor tenta cadastrar usuário → `403`; admin não inativa a própria conta | RF06, RN03, RN08 |
| Alunos | Cadastrar, consultar e editar aluno; campo obrigatório ausente → `400`; aluno inativado não recebe ficha | RF01, RN05 |
| Exercícios | Cadastrar exercício; nome duplicado rejeitado; aluno tenta cadastrar → `403`; exercício usado em ficha é apenas inativado | RF03, RN04 |
| Fichas | Criar ficha com exercício para um aluno; ficha sem exercício → `400`; aluno tenta criar ficha → `403`; aluno vê só as próprias fichas | RF04, RN01, RN02, RN06 |
| Execuções | Aluno inicia, registra e finaliza execução; execução finalizada não aceita registro; ficha não vigente rejeitada; aluno consulta histórico de outro → `403` | RF05, RN02, RN07, RN10, RN11 |

O objetivo é que **todo requisito funcional tenha pelo menos um teste automatizado**, e que os casos de segurança CT11 (privacidade) e CT12 (permissões) estejam automatizados.

---

## 5. Ambiente de teste

| Ambiente | Descrição |
| --- | --- |
| CI (GitHub Actions) | Ubuntu, Python 3.12, MySQL 8.4 como serviço; credenciais descartáveis definidas no próprio workflow |
| Docker local | `docker compose up` a partir do `.env.example`; usado nos testes manuais e na coleção Postman |
| Navegadores | Chrome, Firefox e Edge (versões atuais), em desktop e celular |

Para executar os testes pytest localmente, com o banco migrado e o administrador criado:

```bash
pip install -r codigo-fonte/backend/requirements-dev.txt
PYTHONPATH=codigo-fonte/backend python -m pytest codigo-fonte/testes -v
```

---

## 6. Critérios

### 6.1 Critérios de entrada

- O IC a ser testado está na `main` ou em um PR aberto, com a versão registrada na Planilha de ICs.
- O CI está configurado e o ambiente sobe sem erros (migrações e administrador inicial).
- Os casos de teste do ciclo estão descritos (GYM-TST-005) e ligados aos requisitos.

### 6.2 Critérios de saída e aceite (para a BL-IMPL-S2)

- CI verde na `main`, com os testes pytest e Newman **executados** (sem o aviso de "nenhum teste encontrado").
- Todo requisito funcional (RF01 a RF06) com pelo menos um teste automatizado de integração ou de API.
- CT01 a CT12 executados manualmente, com resultado registrado no Relatório de Testes.
- Nenhum defeito de gravidade **Crítica** ou **Alta** em aberto no Registro de Defeitos.
- RTM atualizada com a situação de verificação de cada requisito.
- Revisão técnica do QA registrada para os ICs de teste.

### 6.3 Critérios de suspensão e retomada

- **Suspensão:** o ambiente não sobe (falha nas migrações ou no Docker) ou um defeito crítico impede a execução da maior parte dos casos.
- **Retomada:** após a correção ser incorporada à `main` por PR, com o CI verde.

---

## 7. Gestão de defeitos

1. O defeito encontrado é registrado no **Registro de Defeitos** (GYM-TST-006) e como **issue** no GitHub, com passos para reproduzir, resultado esperado, resultado obtido e gravidade.
2. A gravidade segue a classificação do GYM-TST-006: Baixa, Média, Alta ou Crítica.
3. A correção é feita em um branch `fix/<id>-<descricao>`, por PR que referencia a issue (`Closes #N`).
4. O QA executa o teste de verificação e, quando possível, inclui um **teste automatizado de regressão** que reproduz o defeito.
5. Defeito em IC sob baseline segue o processo de Change Request (PGC, seção 6).

---

## 8. Entregáveis de teste

| IC | Entregável | Atualização |
| --- | --- | --- |
| GYM-TST-001 | Este plano | Antes de cada novo ciclo de testes |
| GYM-TST-002 | Testes unitários | A cada PR que altere o backend |
| GYM-TST-003 | Testes de integração | A cada PR que altere o backend |
| GYM-TST-004 | Coleção Postman | A cada mudança na API |
| GYM-TST-005 | Casos de Teste (CT01 a CT12) | Quando um requisito ou caso de uso mudar |
| GYM-TST-006 | Registro de Defeitos | A cada defeito encontrado ou corrigido |
| GYM-TST-007 | Relatório de Testes | Ao fim de cada ciclo e antes de cada baseline |

---

## 9. Papéis e responsabilidades

| Papel | Integrante(s) | Responsabilidade nos testes |
| --- | --- | --- |
| QA/Testes | Iago Medice Ferreira da Silva, Tiago Costa dos Santos, Ruan Victor Assunção Costa | Manter este plano, escrever e executar os testes, registrar defeitos e resultados, revisão técnica |
| Analista de Requisitos | Renata Martins da Silva | Garantir a ligação entre requisitos, casos de teste e RTM |
| Dev Backend e Frontend / DevOps | João Vitor Simonetti | Corrigir defeitos, manter o CI e o ambiente Docker, apoiar os testes automatizados |
| Gerente de Projeto/Configuração | Hugo Henry Lemos Carvalho | Aprovar o encerramento do ciclo e criar a tag da baseline |

---

## 10. Cronograma

As entregas seguem o ritmo semanal da equipe (quartas-feiras), na ordem abaixo:

| Ordem | Atividade | IC(s) | Marco |
| --- | --- | --- | --- |
| 1 | Plano de Testes (esta versão) e atualização de Casos de Teste e Relatório | TST-001, 005, 007 | — |
| 2 | Testes de integração dos módulos de usuários, alunos e exercícios | TST-003 | — |
| 3 | Testes de integração de fichas e execuções (inclui CT11 e CT12) e testes unitários de validação | TST-002, 003 | — |
| 4 | Coleção Postman com fluxo completo e asserção de tempo (RNF04) | TST-004 | — |
| 5 | Execução manual de CT01 a CT12, Relatório de Testes e revisão técnica | TST-005, 006, 007 | BL-IMPL-S2 |
| 6 | Regressão completa e testes de navegadores e dispositivos (RNF05, RNF06) | Todos | BL-REL-S3 (`v1.0.0`) |

---

## 11. Riscos

| Risco | Impacto | Ação |
| --- | --- | --- |
| Divergências entre o sistema 0.1.0 e o ERS (ver Pendências da Planilha de ICs, item 20) | Testes podem falhar por requisito desatualizado, e não por defeito | O CCB decide, para cada divergência, entre corrigir o código ou ajustar o ERS por CR, antes de escrever o teste correspondente |
| Banco compartilhado entre os testes no CI | Testes dependentes entre si ou falhas intermitentes | Dados únicos por teste e fixtures centralizadas (seção 3.2) |
| Equipe de QA com pouca experiência em pytest e Postman | Atraso na cobertura | Começar pelos módulos mais simples; usar os testes existentes como modelo |
| Plano formalizado após os primeiros testes | Testes iniciais sem critério documentado | Registrado no histórico; testes existentes revisados frente a este plano (seção 4.2) |

---

## 12. Controle de configuração deste documento

- Toda alteração é feita por PR, com issue vinculada, e registrada no histórico de revisões.
- A versão e o status deste IC são mantidos iguais aos da Planilha de ICs (GYM-GER-002).
- Após a baseline BL-IMPL-S2, alterações só mediante Change Request aprovada pelo CCB.
