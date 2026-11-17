# Relatório de Testes — GymManager

**Sistema web de gerenciamento de treinos de academia**
Disciplina: Gerência de Configuração (6º período) · CENTRO UNIVERSITÁRIO FAMETRO
Professor: Paulo Rodrigo Barbosa Alves

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-TST-007 |
| Caminho | `documentos/testes/Relatorio_de_Testes.md` |
| Versão | 0.3.0 |
| Status | Em elaboração |
| Baseline prevista | BL-REL-S3 (Product/Release) |
| Responsável | QA/Testes (Iago Medice Ferreira da Silva, Tiago Costa dos Santos, Ruan Victor Assunção Costa) |
| Elaboração desta versão | Renata Martins da Silva (Analista de Requisitos) |
| Dependências | GYM-TST-005 (Casos de Teste), GYM-TST-006 (Registro de Defeitos) |
| ICs relacionados | GYM-TST-001 (Plano de Testes), GYM-TST-002, GYM-TST-003, GYM-TST-004, GYM-CI-001, GYM-REQ-003 (RTM) |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.1.0 | 11-11-2026 | QA/Testes | Versão inicial (modelo, sem execuções) | — |
| 0.2.0 | 16-11-2026 | Renata Martins da Silva | Total corrigido de 10 para 12 casos, conforme GYM-TST-005 (Pendência 15 da Planilha de ICs); registro do ciclo 1 (testes automatizados do PR #17 no CI); cobertura por requisito; lista de funcionalidades alinhada aos casos CT01 a CT12 | #18 |
| 0.3.0 | 17-11-2026 | Renata Martins da Silva | Registro do ciclo 2 (136 testes pytest e coleção Newman entregues no PR #37); resumo e cobertura atualizados para os casos CT01 a CT30 de GYM-TST-005 v0.3.0 (Pendência 26 da Planilha de ICs); cobertura dos casos de teste pelos testes automatizados | #39 |

---

## 1. Objetivo

Apresentar os resultados dos testes do GymManager, ciclo a ciclo, conforme o Plano de Testes (GYM-TST-001), e servir de evidência para as baselines BL-IMPL-S2 e BL-REL-S3.

## 2. Ciclo 1 — Testes automatizados iniciais

| Item | Valor |
| --- | --- |
| Data | 16-11-2026 (execução do CI no PR #17; conferir a data exata na aba Actions) |
| Versão do sistema | 0.1.0 |
| Origem | PR #17 (`test: adiciona testes de integracao de autenticacao`), último commit do PR `f55a19c` |
| Ambiente | CI no GitHub Actions (GYM-CI-001): Ubuntu, Python 3.12, MySQL 8.4 |
| Jobs executados | *Backend — build, migrações e pytest* e *Docker — ambiente completo, fumaça e Newman* |
| Resultado do CI | Aprovado (os dois jobs concluídos com sucesso) |

### 2.1 Testes automatizados

| Arquivo | Nível | Teste | Caso | Resultado |
| --- | --- | --- | --- | --- |
| `unitarios/test_configuracao.py` | Unitário (GYM-TST-002) | `test_criacao_aplicacao_flask` | — | Aprovado |
| `integracao/test_autenticacao.py` | Integração (GYM-TST-003) | `test_login_admin_sucesso` | CT01 | Aprovado |
| `integracao/test_autenticacao.py` | Integração (GYM-TST-003) | `test_login_senha_incorreta` | CT02 | Aprovado |
| Workflow de CI | Fumaça (GYM-CI-001) | Login do administrador pelo proxy do frontend | CT01 | Aprovado |
| `postman/` | API (GYM-TST-004) | — | — | Não executado: coleção ainda não entregue (o CI emite aviso) |

### 2.2 Casos de teste manuais (GYM-TST-005)

Os casos manuais ainda não foram executados neste ciclo.

## 3. Ciclo 2 — Testes automatizados por módulo e coleção Newman

| Item | Valor |
| --- | --- |
| Data | 17-11-2026 |
| Versão do sistema | 0.1.0 |
| Origem | PR #37 (testes de integração dos seis módulos, testes unitários, `conftest.py` e coleção Postman) |
| Ambiente oficial | CI no GitHub Actions (GYM-CI-001): Ubuntu, Python 3.12, MySQL 8.4; Newman 6.2.3 no ambiente Docker, pelo proxy do frontend |
| Resultado do CI | **A confirmar**: abrir a aba *Actions* do PR #37, conferir os jobs *Backend — build, migrações e pytest* e *Docker — ambiente completo, fumaça e Newman* e registrar aqui o resultado, a data e o commit |
| Execução de verificação | 17-11-2026, ambiente local montado como o CI (MySQL 8.0, banco migrado duas vezes e administrador criado por `flask criar-admin`; Newman 6.2.3 direto na API): pytest executado duas vezes seguidas sem limpar o banco, com o mesmo resultado |

### 3.1 Testes pytest (GYM-TST-002 e GYM-TST-003)

| Arquivo | Nível | Testes | Aprovados | Reprovados |
| --- | --- | ---: | ---: | ---: |
| `integracao/test_autenticacao.py` | Integração | 10 | 10 | 0 |
| `integracao/test_usuarios.py` | Integração | 11 | 11 | 0 |
| `integracao/test_alunos.py` | Integração | 9 | 9 | 0 |
| `integracao/test_exercicios.py` | Integração | 8 | 8 | 0 |
| `integracao/test_fichas.py` | Integração | 12 | 12 | 0 |
| `integracao/test_execucoes.py` | Integração | 19 | 19 | 0 |
| `unitarios/test_validacao.py` | Unitário | 54 | 54 | 0 |
| `unitarios/test_seguranca.py` | Unitário | 5 | 5 | 0 |
| `unitarios/test_migracoes.py` | Unitário | 7 | 7 | 0 |
| `unitarios/test_configuracao.py` | Unitário | 1 | 1 | 0 |
| **Total** | | **136** | **136** | **0** |

Resultado da execução de verificação: `136 passed`.

### 3.2 Coleção Newman (GYM-TST-004)

| Indicador | Resultado |
| --- | --- |
| Requisições | 17 executadas, 0 com falha |
| Verificações (asserções) | 41 executadas, 0 com falha |
| Tempo de resposta (RNF04: < 2000 ms) | Atendido em todas as requisições; média de 37 a 42 ms e máximo de 180 ms nas duas execuções de verificação |
| Repetição | Duas execuções seguidas no mesmo banco, sem falhas (dados únicos por execução) |

O tempo medido na execução de verificação foi direto na API. No CI, a coleção passa pelo proxy do frontend; o resultado oficial do RNF04 é o do CI.

### 3.3 Casos de teste manuais (GYM-TST-005)

Os casos manuais ainda não foram executados neste ciclo.

## 4. Resumo dos testes

### 4.1 Casos de teste (CT01 a CT30)

| Situação | Quantidade |
| --- | ---: |
| Verificados por teste automatizado (total ou em parte) | 30 |
| Executados manualmente | 0 |
| Reprovados | 0 |
| Pendentes (execução manual) | 30 |
| Total de casos | 30 |

Todos os casos têm cobertura automatizada no nível da API (seção 5), mas **todos continuam pendentes de execução manual pela interface**, que é o que verifica RF07, RNF05 e RNF06. Por isso entram nas duas linhas.

### 4.2 Testes automatizados

| Situação | Ciclo 1 | Ciclo 2 |
| --- | ---: | ---: |
| Testes pytest aprovados | 3 | 136 |
| Testes pytest reprovados | 0 | 0 |
| Requisições Newman aprovadas | — (coleção não entregue) | 17 |
| Requisições Newman com falha | — | 0 |

## 5. Cobertura por requisito

| Requisito | Casos | Verificado por teste automatizado (ciclo 2) | Verificado manualmente |
| --- | --- | --- | --- |
| RF01 — Alunos | CT04 a CT07 | **Sim** (TI-ALU-01 a 06; Newman 04) | Não |
| RF02 — Autenticação e perfis | CT01, CT02, CT03, CT27, CT30 | **Sim** (TI-AUTH-01 a 08; Newman 01, 03, 07, 15 a 17) | Não |
| RF03 — Exercícios | CT10 a CT12 | **Sim** (TI-EXE-01 a 06; Newman 05) | Não |
| RF04 — Fichas de treino | CT13 a CT18, CT29 | **Sim** (TI-FIC-01 a 10; Newman 06, 08 e 09) | Não |
| RF05 — Execuções e histórico | CT19 a CT26 | **Sim** (TI-EXC-01 a 14; Newman 10 a 14) | Não |
| RF06 — Usuários e instrutores | CT08, CT09, CT27, CT28 | **Sim** (TI-USU-01 a 08; Newman 02) | Não |
| RF07 — Interface por perfil | CT01 a CT30 | Não (fora do escopo dos testes automatizados) | Não |
| RNF01 — Hash de senha | — | **Sim** (TU-09) | — |
| RNF02 — Rotas protegidas | — | **Sim** (TI-AUTH-05, TI-ALU-04; Newman 15) | — |
| RNF04 — Tempo de resposta | — | **Sim**, na verificação local (Newman, todas as requisições); confirmar no CI | — |
| RNF08 — Testes no CI | — | **Sim** (pytest e Newman executados a cada PR) | — |
| RNF11 — Migrações com checksum | — | **Sim** (TU-11; migrações aplicadas duas vezes no CI) | — |
| RNF13 — Sessão por token | — | **Sim** (TU-10, TI-AUTH-06 a 08; Newman 16 e 17) | — |

### 5.1 Casos de teste × testes automatizados

| Caso | Testes automatizados que o verificam | Cobertura |
| --- | --- | --- |
| CT01 | TI-AUTH-01; Newman 01 | Total |
| CT02 | TI-AUTH-02 | Total |
| CT03 | TI-AUTH-04 | Total |
| CT04 | TI-ALU-01; Newman 04 | Total |
| CT05 | TI-ALU-02 | Total |
| CT06 | TI-ALU-01 | Total |
| CT07 | TI-ALU-05 | Total |
| CT08 | TI-USU-01; Newman 02 | Total |
| CT09 | TI-USU-04 | Total |
| CT10 | TI-EXE-01; Newman 05 | Total |
| CT11 | TI-EXE-02 | Total |
| CT12 | TI-EXE-05 | Total |
| CT13 | TI-FIC-01; Newman 06 | Total |
| CT14 | TI-FIC-02 | Total |
| CT15 | TI-FIC-06; Newman 08 | Total |
| CT16 | TI-FIC-05, TI-EXC-05, TI-EXC-13 | Total |
| CT17 | TI-FIC-07 a 09 (edição pelo `PUT /fichas/{id}`) | Parcial: não há teste só de alteração de nome e datas |
| CT18 | TI-FIC-07 | Total |
| CT19 | TI-EXC-01; Newman 10 | Total |
| CT20 | TI-EXC-06 | Total |
| CT21 | TI-EXC-01; Newman 11 | Total |
| CT22 | TI-EXC-02 | Total |
| CT23 | TI-EXC-01; Newman 12 | Total |
| CT24 | TI-EXC-12, TI-EXC-14; Newman 14 | Total |
| CT25 | TI-EXC-10 | Parcial: o teste confirma a regra da API (RN13); a retomada pela interface só é verificada no teste manual |
| CT26 | TI-EXC-11 | Total |
| CT27 | TI-USU-04, TI-USU-05 | Parcial: o teste confirma o bloqueio no backend; a ocultação das funções na interface só é verificada no teste manual |
| CT28 | TI-USU-06, TI-USU-07 | Total |
| CT29 | TI-FIC-02 (séries), TI-EXC-08 (repetições e carga), TU-05 a TU-07 | Total |
| CT30 | TI-AUTH-07; Newman 16 e 17 | Total |

## 6. Defeitos

Nenhum defeito foi encontrado nos ciclos 1 e 2. Ver o Registro de Defeitos (GYM-TST-006).

## 7. Observações

- A asserção de `test_login_senha_incorreta` foi restrita a `401` no ciclo 2, como recomendado no ciclo 1.
- Os comportamentos registrados no ERS como RN13 (mais de uma execução aberta na mesma ficha) e RN14 (registro de item inativado após o início) foram confirmados pelos testes TI-EXC-10 e TI-EXC-11.
- Os testes pytest dependem do MySQL do CI (variáveis `DATABASE_URL`/`MYSQL_*`, `SECRET_KEY`, `ADMIN_EMAIL` e `ADMIN_SENHA`). Sem essas variáveis, não executam.
- RNF05, RNF06 e RNF14 continuam sem verificação: dependem do teste manual e da inspeção dos cabeçalhos da interface (Plano de Testes, seção 3.4).

## 8. Conclusão

O ciclo 2 atinge a meta de testes automatizados do Plano de Testes (seção 4.3): RF01 a RF06 têm testes de integração e de API, e os casos de segurança CT16 e CT27 estão automatizados. Para a baseline BL-IMPL-S2 ainda faltam, conforme os critérios de saída do Plano de Testes (seção 6.2): confirmar o CI verde do PR #37 na `main`, executar manualmente os casos CT01 a CT30, atualizar a situação de verificação na RTM (por CR, pois a RTM está na BL-REQ-S1) e registrar a revisão técnica do QA.
