# Casos de Teste — GymManager

**Sistema web de gerenciamento de treinos de academia**
Disciplina: Gerência de Configuração (6º período) · CENTRO UNIVERSITÁRIO FAMETRO
Professor: Paulo Rodrigo Barbosa Alves

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-TST-005 |
| Caminho | `documentos/testes/Casos_de_Teste.md` |
| Versão | 0.2.0 |
| Status | Em elaboração |
| Baseline prevista | BL-IMPL-S2 (Design/Implementação) |
| Responsável | QA/Testes (Iago Medice Ferreira da Silva, Tiago Costa dos Santos, Ruan Victor Assunção Costa) |
| Elaboração desta versão | Renata Martins da Silva (Analista de Requisitos) |
| Dependências | GYM-TST-001 (Plano de Testes), GYM-REQ-001 (ERS) |
| ICs relacionados | GYM-REQ-002 (Casos de Uso), GYM-REQ-003 (RTM), GYM-TST-002 a 004, GYM-TST-006, GYM-TST-007 |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.1.0 | 11-11-2026 | QA/Testes | Versão inicial com os casos CT01 a CT12 | — |
| 0.2.0 | 16-11-2026 | Renata Martins da Silva | Inclusão da tabela de controle do IC; rastreabilidade de cada caso com requisito, caso de uso e regra de negócio (Pendência 19 da Planilha de ICs); pré-condições, procedimentos e resultados esperados conforme o sistema 0.1.0; indicação dos testes automatizados correspondentes (PR #17) | #18 |

---

## 1. Objetivo

Verificar se as funcionalidades do GymManager atendem aos requisitos do ERS (GYM-REQ-001). Os casos seguem a estratégia do Plano de Testes (GYM-TST-001) e estão ligados aos casos de uso (GYM-REQ-002) e à RTM (GYM-REQ-003).

## 2. Dados de teste

Os casos usam o ambiente Docker local (`docker compose up`, a partir do `.env.example`), com o administrador inicial criado pelo comando `flask criar-admin`. Durante a execução, o QA cadastra os demais dados (instrutor, aluno, exercício e ficha) seguindo a ordem dos casos. Nenhuma senha real é usada.

## 3. Resumo e rastreabilidade

| ID | Funcionalidade | Requisito(s) | Caso de uso | Regra(s) | Execução | Teste automatizado | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT01 | Login | RF02 | UC01 | — | Manual + automatizado | `integracao/test_autenticacao.py::test_login_admin_sucesso` | Automatizado: Aprovado (CI do PR #17). Manual: Pendente |
| CT02 | Login inválido | RF02 | UC01 | — | Manual + automatizado | `integracao/test_autenticacao.py::test_login_senha_incorreta` | Automatizado: Aprovado (CI do PR #17). Manual: Pendente |
| CT03 | Cadastro de usuário | RF06 | UC02 | RN03 | Manual | Planejado | Pendente |
| CT04 | Cadastro de instrutor | RF06 | UC02 | RN03 | Manual | Planejado | Pendente |
| CT05 | Cadastro de aluno | RF01 | UC03 | RN05 | Manual | Planejado | Pendente |
| CT06 | Cadastro de exercício | RF03 | UC04 | RN04 | Manual | Planejado | Pendente |
| CT07 | Criar ficha de treino | RF04 | UC05 | RN01, RN06 | Manual | Planejado | Pendente |
| CT08 | Consultar ficha | RF04, RF07 | UC06 | RN02 | Manual | Planejado | Pendente |
| CT09 | Registrar treino | RF05 | UC07 | RN07, RN10, RN11 | Manual | Planejado | Pendente |
| CT10 | Histórico de treinos | RF05 | UC08 | RN02 | Manual | Planejado | Pendente |
| CT11 | Privacidade | RF04, RF05 | UC06, UC07, UC08 | RN02 | Manual | Planejado | Pendente |
| CT12 | Permissões | RF02, RNF02 | UC01 a UC08 | RN01, RN03 | Manual | Planejado | Pendente |

## 4. Detalhamento dos casos

### CT01 — Login

- **Pré-condição:** administrador inicial ativo.
- **Procedimento:** na tela de login (TL01), informar o e-mail e a senha do administrador e acionar "Entrar".
- **Resultado esperado:** o sistema abre o painel inicial do perfil administrador. Pela API, `POST /auth/login` retorna `200` com `token` e `usuario.perfil = "ADMIN"`.

### CT02 — Login inválido

- **Pré-condição:** administrador inicial ativo.
- **Procedimento:** informar o e-mail do administrador com uma senha incorreta e acionar "Entrar".
- **Resultado esperado:** acesso negado com a mensagem "E-mail ou senha inválidos.", sem indicar qual campo está incorreto, e o sistema permanece na TL01. Pela API, a resposta é `401`.

### CT03 — Cadastro de usuário

- **Pré-condição:** sessão iniciada como administrador.
- **Procedimento:** na tela de usuários (TL03), cadastrar um novo usuário com nome, e-mail, senha e perfil; repetir com um e-mail já cadastrado.
- **Resultado esperado:** o primeiro cadastro aparece na listagem com o perfil escolhido. O segundo é recusado com "E-mail inválido ou já cadastrado.".

### CT04 — Cadastro de instrutor

- **Pré-condição:** sessão iniciada como administrador.
- **Procedimento:** cadastrar um usuário com perfil instrutor, encerrar a sessão e entrar com as credenciais do instrutor.
- **Resultado esperado:** o instrutor é registrado e consegue entrar, vendo o painel e o menu do perfil instrutor (critério de aceite do RF06).

### CT05 — Cadastro de aluno

- **Pré-condição:** sessão iniciada como instrutor.
- **Procedimento:** na tela de alunos (TL04), cadastrar um aluno; depois, inativá-lo e tentar entrar com as credenciais dele.
- **Resultado esperado:** o aluno aparece na listagem. Depois de inativado, o login é negado com "Usuário inativo." (`403`), conforme RN05.

### CT06 — Cadastro de exercício

- **Pré-condição:** sessão iniciada como instrutor.
- **Procedimento:** na tela de exercícios (TL05), cadastrar um exercício com nome, grupo muscular e descrição; repetir com o mesmo nome.
- **Resultado esperado:** o exercício fica disponível para a montagem de fichas. O nome repetido é recusado com "Exercício já cadastrado.".

### CT07 — Criar ficha de treino

- **Pré-condição:** sessão iniciada como instrutor; aluno ativo e exercício ativo cadastrados (CT05 e CT06, com o aluno reativado).
- **Procedimento:** na tela de fichas (TL06), montar uma ficha com um exercício (séries, repetições, carga e descanso) e atribuí-la ao aluno; tentar salvar uma segunda ficha sem exercícios.
- **Resultado esperado:** a ficha é salva e atribuída ao aluno. A ficha sem exercícios é recusada com "A ficha deve ter pelo menos um exercício." (`400`), conforme RN06.

### CT08 — Consultar ficha

- **Pré-condição:** ficha do CT07 atribuída ao aluno.
- **Procedimento:** entrar como o aluno e abrir a ficha (TL07).
- **Resultado esperado:** a ficha é exibida com os exercícios e parâmetros definidos pelo instrutor.

### CT09 — Registrar treino

- **Pré-condição:** sessão iniciada como o aluno; ficha vigente atribuída a ele.
- **Procedimento:** acionar "Iniciar treino" (TL08), registrar repetições e carga de um exercício e finalizar a execução; depois, tentar registrar outro exercício na execução finalizada.
- **Resultado esperado:** o registro é salvo e a execução finalizada. A execução encerrada não aceita novos registros (RN11).

### CT10 — Histórico de treinos

- **Pré-condição:** execução do CT09 finalizada.
- **Procedimento:** como o aluno, abrir o histórico (TL09); repetir como instrutor, consultando o histórico desse aluno.
- **Resultado esperado:** a execução aparece no histórico, com a evolução de carga por exercício (critério de aceite do RF05).

### CT11 — Privacidade

- **Pré-condição:** dois alunos cadastrados, cada um com a própria ficha.
- **Procedimento:** com a sessão do aluno A, tentar abrir a ficha e o histórico do aluno B (alterando o identificador na URL ou chamando a API diretamente).
- **Resultado esperado:** acesso negado com `403` (ou `404` para a ficha), sem exibir nenhum dado do aluno B (RN02).

### CT12 — Permissões

- **Pré-condição:** sessões de aluno e de instrutor disponíveis.
- **Procedimento:** como aluno, tentar criar exercício ou ficha; como instrutor, tentar cadastrar usuário; sem sessão, chamar uma rota protegida da API.
- **Resultado esperado:** o menu de cada perfil mostra só as funções permitidas (RF07). Pela API, as chamadas com perfil não autorizado retornam `403` e a chamada sem token retorna `401` (RNF02).

## 5. Status dos testes

- **Aprovado:** resultado esperado alcançado.
- **Reprovado:** resultado diferente do esperado; o defeito é registrado no Registro de Defeitos (GYM-TST-006) e como issue.
- **Pendente:** teste ainda não executado.

Os resultados de cada ciclo são consolidados no Relatório de Testes (GYM-TST-007), com a data e a versão do sistema testada.

## 6. Observações

- A automação dos casos ainda não automatizados segue a meta por módulo definida no Plano de Testes (GYM-TST-001, seção 4.3).
- Qualquer mudança em requisito ou caso de uso exige a revisão dos casos afetados e da RTM.
