# Relatório de Testes — GymManager

**Sistema web de gerenciamento de treinos de academia**
Disciplina: Gerência de Configuração (6º período) · CENTRO UNIVERSITÁRIO FAMETRO
Professor: Paulo Rodrigo Barbosa Alves

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-TST-007 |
| Caminho | `documentos/testes/Relatorio_de_Testes.md` |
| Versão | 0.2.0 |
| Status | Em elaboração |
| Baseline prevista | BL-REL-S3 (Product/Release) |
| Responsável | QA/Testes (Iago Medice Ferreira da Silva, Tiago Costa dos Santos, Ruan Victor Assunção Costa) |
| Elaboração desta versão | Renata Martins da Silva (Analista de Requisitos) |
| Dependências | GYM-TST-005 (Casos de Teste), GYM-TST-006 (Registro de Defeitos) |
| ICs relacionados | GYM-TST-001 (Plano de Testes), GYM-TST-002, GYM-TST-003, GYM-CI-001, GYM-REQ-003 (RTM) |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.1.0 | 11-11-2026 | QA/Testes | Versão inicial (modelo, sem execuções) | — |
| 0.2.0 | 16-11-2026 | Renata Martins da Silva | Total corrigido de 10 para 12 casos, conforme GYM-TST-005 (Pendência 15 da Planilha de ICs); registro do ciclo 1 (testes automatizados do PR #17 no CI); cobertura por requisito; lista de funcionalidades alinhada aos casos CT01 a CT12 | #18 |

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

## 3. Resumo dos testes

### 3.1 Casos de teste (CT01 a CT12)

| Situação | Quantidade |
| --- | ---: |
| Aprovados (por teste automatizado) | 2 |
| Reprovados | 0 |
| Pendentes (execução manual) | 12 |
| Total de casos | 12 |

CT01 e CT02 foram verificados por teste automatizado, mas também continuam pendentes de execução manual pela interface. Por isso entram nas duas linhas.

### 3.2 Testes automatizados

| Situação | Quantidade |
| --- | ---: |
| Aprovados | 3 |
| Reprovados | 0 |
| Total | 3 |

## 4. Cobertura por requisito

| Requisito | Casos | Verificado neste ciclo |
| --- | --- | --- |
| RF01 — Alunos | CT05 | Não |
| RF02 — Autenticação e perfis | CT01, CT02, CT12 | **Parcial** (login válido e senha incorreta) |
| RF03 — Exercícios | CT06 | Não |
| RF04 — Fichas de treino | CT07, CT08, CT11 | Não |
| RF05 — Execuções e histórico | CT09, CT10, CT11 | Não |
| RF06 — Usuários e instrutores | CT03, CT04 | Não |
| RF07 — Interface por perfil | CT01 a CT12 | Não |
| RNF08 — Testes no CI | — | **Sim** (pytest executado a cada PR) |

## 5. Defeitos

Nenhum defeito foi encontrado neste ciclo. Ver o Registro de Defeitos (GYM-TST-006).

## 6. Observações

- `test_login_senha_incorreta` aceita `400` ou `401`, mas o sistema 0.1.0 responde `401` para senha incorreta (UC01, FE1). Recomenda-se restringir a asserção a `401`, para que o teste detecte uma mudança indevida de comportamento.
- A coleção Postman (GYM-TST-004) e os testes dos módulos de usuários, alunos, exercícios, fichas e execuções ainda não existem. A meta mínima por módulo está no Plano de Testes, seção 4.3.

## 7. Conclusão

O ciclo 1 confirma que o pipeline de CI executa os testes automatizados e que a autenticação básica funciona. A cobertura ainda é insuficiente para a baseline BL-IMPL-S2: faltam testes automatizados para RF01 e RF03 a RF06, a coleção Postman e a execução manual de CT01 a CT12, conforme os critérios de saída do Plano de Testes (seção 6.2).
