# Casos de Teste — GymManager

**Sistema web de gerenciamento de treinos de academia**
Disciplina: Gerência de Configuração (6º período) · CENTRO UNIVERSITÁRIO FAMETRO
Professor: Paulo Rodrigo Barbosa Alves

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-TST-005 |
| Caminho | `documentos/testes/Casos_de_Teste.md` |
| Versão | 0.3.0 |
| Status | Em elaboração |
| Baseline prevista | BL-IMPL-S2 (Design/Implementação) |
| Responsável | QA/Testes (Iago Medice Ferreira da Silva, Tiago Costa dos Santos, Ruan Victor Assunção Costa) |
| Dependências | GYM-TST-001 (Plano de Testes), GYM-REQ-001 (ERS v1.1.0) |
| ICs relacionados | GYM-TST-006 (Registro de Defeitos), GYM-TST-007 (Relatório de Testes), GYM-REQ-003 (RTM) |
| Situação da execução | Casos preparados, aguardando execução |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.1.0 | 16-11-2026 | QA/Testes | Casos CT01 a CT12 | — |
| 0.2.0 | 16-11-2026 | QA/Testes | Indicação do requisito verificado em cada caso (Pendência 19 da Planilha de ICs) | #18 |
| 0.3.0 | 17-11-2026 | Renata Martins da Silva | Casos ampliados para CT01 a CT30 com base no ERS v1.1.0 (inclui RN13 e RN14); cabeçalho e histórico no padrão dos demais ICs; versão alinhada à Planilha de ICs (o arquivo informava 1.1.0 sem aprovação registrada) | #35 |

## 1. Objetivo

Verificar se o GymManager atende aos requisitos funcionais, às regras de negócio e aos critérios de aceite definidos no documento ERS.

## 2. Legenda dos resultados

- **Aprovado:** resultado corresponde ao esperado.
- **Reprovado:** resultado diferente do esperado.
- **Pendente:** teste ainda não executado.
- **Bloqueado:** não pode ser executado por falta de ambiente ou funcionalidade.

## 3. Casos de teste

### CT01 — Login com dados válidos
- **Requisito:** RF02
- **Prioridade:** Alta
- **Pré-condição:** Usuário ativo cadastrado.
- **Passos:** Informar e-mail e senha corretos e clicar em entrar.
- **Resultado esperado:** Login realizado e token de acesso gerado.
- **Status:** Pendente.

### CT02 — Login com senha incorreta
- **Requisito:** RF02
- **Prioridade:** Alta
- **Passos:** Informar e-mail cadastrado e senha incorreta.
- **Resultado esperado:** Acesso negado e mensagem de erro.
- **Status:** Pendente.

### CT03 — Login com usuário inativo
- **Requisito:** RF02 / RN05
- **Prioridade:** Alta
- **Pré-condição:** Usuário inativado.
- **Passos:** Tentar entrar com as credenciais do usuário.
- **Resultado esperado:** Autenticação recusada.
- **Status:** Pendente.

### CT04 — Cadastro de aluno
- **Requisito:** RF01
- **Prioridade:** Alta
- **Pré-condição:** Administrador ou instrutor autenticado.
- **Passos:** Preencher os dados obrigatórios e cadastrar um aluno.
- **Resultado esperado:** Aluno cadastrado e disponível na listagem.
- **Status:** Pendente.

### CT05 — Cadastro de aluno com dados inválidos
- **Requisito:** RF01
- **Prioridade:** Alta
- **Passos:** Tentar cadastrar aluno sem nome ou com e-mail inválido.
- **Resultado esperado:** Cadastro recusado com mensagem de validação.
- **Status:** Pendente.

### CT06 — Edição de aluno
- **Requisito:** RF01
- **Prioridade:** Média
- **Pré-condição:** Aluno cadastrado.
- **Passos:** Alterar os dados do aluno e salvar.
- **Resultado esperado:** Dados atualizados corretamente.
- **Status:** Pendente.

### CT07 — Inativação de aluno
- **Requisito:** RF01 / RN05
- **Prioridade:** Alta
- **Pré-condição:** Aluno ativo.
- **Passos:** Inativar o aluno e tentar autenticar com sua conta.
- **Resultado esperado:** Aluno inativado, sem conseguir autenticar ou receber novas fichas; histórico preservado.
- **Status:** Pendente.

### CT08 — Cadastro de instrutor
- **Requisito:** RF06 / RN03
- **Prioridade:** Alta
- **Pré-condição:** Administrador autenticado.
- **Passos:** Cadastrar usuário com perfil INSTRUTOR.
- **Resultado esperado:** Instrutor cadastrado e capaz de autenticar com o perfil correto.
- **Status:** Pendente.

### CT09 — Restrição de cadastro de instrutor
- **Requisito:** RF06 / RN03
- **Prioridade:** Alta
- **Passos:** Tentar cadastrar instrutor utilizando uma conta de aluno ou instrutor.
- **Resultado esperado:** Operação negada por falta de permissão.
- **Status:** Pendente.

### CT10 — Cadastro de exercício
- **Requisito:** RF03
- **Prioridade:** Alta
- **Pré-condição:** Administrador ou instrutor autenticado.
- **Passos:** Cadastrar exercício com nome, grupo muscular e descrição.
- **Resultado esperado:** Exercício salvo e disponível no catálogo.
- **Status:** Pendente.

### CT11 — Cadastro de exercício duplicado
- **Requisito:** RF03
- **Prioridade:** Média
- **Pré-condição:** Exercício já cadastrado.
- **Passos:** Tentar cadastrar novamente o mesmo nome, inclusive com letras maiúsculas ou minúsculas diferentes.
- **Resultado esperado:** Cadastro recusado com mensagem de duplicidade.
- **Status:** Pendente.

### CT12 — Inativação de exercício
- **Requisito:** RF03 / RN04
- **Prioridade:** Média
- **Pré-condição:** Exercício cadastrado.
- **Passos:** Inativar um exercício.
- **Resultado esperado:** Exercício deixa de ficar disponível para novas fichas, sem ser excluído definitivamente.
- **Status:** Pendente.

### CT13 — Criação de ficha de treino
- **Requisito:** RF04 / RN01 / RN06
- **Prioridade:** Alta
- **Pré-condição:** Administrador ou instrutor autenticado, aluno e exercício cadastrados.
- **Passos:** Criar ficha com nome, aluno, data de início e pelo menos um exercício, séries, repetições, carga e descanso.
- **Resultado esperado:** Ficha criada e atribuída ao aluno.
- **Status:** Pendente.

### CT14 — Criação de ficha sem exercícios
- **Requisito:** RF04 / RN06
- **Prioridade:** Alta
- **Passos:** Tentar salvar uma ficha sem adicionar exercícios.
- **Resultado esperado:** Operação recusada.
- **Status:** Pendente.

### CT15 — Consulta de ficha pelo aluno
- **Requisito:** RF04 / RN02
- **Prioridade:** Alta
- **Pré-condição:** Aluno autenticado com ficha atribuída.
- **Passos:** Acessar a tela de minhas fichas.
- **Resultado esperado:** Aluno visualiza somente suas próprias fichas.
- **Status:** Pendente.

### CT16 — Acesso indevido à ficha de outro aluno
- **Requisito:** RF04 / RN02
- **Prioridade:** Alta
- **Pré-condição:** Dois alunos cadastrados com fichas diferentes.
- **Passos:** Tentar consultar a ficha de outro aluno.
- **Resultado esperado:** Acesso negado.
- **Status:** Pendente.

### CT17 — Edição de ficha
- **Requisito:** RF04
- **Prioridade:** Média
- **Pré-condição:** Ficha cadastrada.
- **Passos:** Alterar dados da ficha ou seus exercícios e salvar.
- **Resultado esperado:** Alterações persistidas corretamente.
- **Status:** Pendente.

### CT18 — Transferência de ficha com execução registrada
- **Requisito:** RF04 / RN09
- **Prioridade:** Alta
- **Pré-condição:** Ficha com execução registrada.
- **Passos:** Tentar atribuir a ficha a outro aluno.
- **Resultado esperado:** Transferência recusada.
- **Status:** Pendente.

### CT19 — Início de execução de treino
- **Requisito:** RF05 / RN07 / RN10
- **Prioridade:** Alta
- **Pré-condição:** Aluno autenticado com ficha própria e vigente.
- **Passos:** Iniciar a execução da ficha.
- **Resultado esperado:** Execução criada e vinculada ao aluno e à ficha.
- **Status:** Pendente.

### CT20 — Início de execução de ficha vencida ou inativa
- **Requisito:** RF05 / RN10
- **Prioridade:** Alta
- **Pré-condição:** Aluno com ficha vencida ou inativa.
- **Passos:** Tentar iniciar a execução.
- **Resultado esperado:** Operação recusada.
- **Status:** Pendente.

### CT21 — Registro de exercício realizado
- **Requisito:** RF05 / RN11
- **Prioridade:** Alta
- **Pré-condição:** Execução em andamento.
- **Passos:** Registrar repetições realizadas e carga utilizada.
- **Resultado esperado:** Registro salvo corretamente.
- **Status:** Pendente.

### CT22 — Correção de registro de exercício
- **Requisito:** RF05 / RN11
- **Prioridade:** Média
- **Pré-condição:** Exercício já registrado na execução.
- **Passos:** Registrar novamente o mesmo exercício com valores diferentes.
- **Resultado esperado:** Registro anterior atualizado, sem duplicação.
- **Status:** Pendente.

### CT23 — Finalização da execução
- **Requisito:** RF05 / RN11
- **Prioridade:** Alta
- **Pré-condição:** Execução em andamento.
- **Passos:** Finalizar o treino e tentar registrar outro exercício nessa execução.
- **Resultado esperado:** Execução finalizada e novos registros recusados.
- **Status:** Pendente.

### CT24 — Consulta do histórico e evolução de carga
- **Requisito:** RF05
- **Prioridade:** Alta
- **Pré-condição:** Aluno com execuções registradas.
- **Passos:** Acessar o histórico e consultar a evolução de um exercício.
- **Resultado esperado:** Histórico exibido com registros e evolução de carga.
- **Status:** Pendente.

### CT25 — Retomada de execução em andamento
- **Requisito:** RF05 / RN13
- **Prioridade:** Média
- **Pré-condição:** Ficha com execução ainda em andamento.
- **Passos:** Acessar novamente a ficha para continuar o treino.
- **Resultado esperado:** Interface retoma a execução aberta em vez de iniciar outra pela interface.
- **Status:** Pendente.

### CT26 — Registro de exercício inativado após início da execução
- **Requisito:** RF05 / RN14
- **Prioridade:** Média
- **Pré-condição:** Execução iniciada antes da inativação do item da ficha.
- **Passos:** Inativar o item na ficha e tentar registrar o exercício na execução já iniciada.
- **Resultado esperado:** Registro aceito e preservado no histórico.
- **Status:** Pendente.

### CT27 — Controle de acesso às funções administrativas
- **Requisito:** RF02 / RF06 / RF07
- **Prioridade:** Alta
- **Pré-condição:** Aluno autenticado.
- **Passos:** Tentar acessar funções de gerenciamento de usuários e instrutores.
- **Resultado esperado:** Acesso negado pelo backend e funções não disponibilizadas ao aluno.
- **Status:** Pendente.

### CT28 — Proteção da própria conta do administrador
- **Requisito:** RF06 / RN08
- **Prioridade:** Alta
- **Pré-condição:** Administrador autenticado.
- **Passos:** Tentar inativar a própria conta ou alterar o próprio perfil.
- **Resultado esperado:** Operação recusada.
- **Status:** Pendente.

### CT29 — Validação de campos numéricos
- **Requisito:** RF04
- **Prioridade:** Média
- **Passos:** Tentar cadastrar séries e repetições com zero, carga negativa ou descanso negativo.
- **Resultado esperado:** Valores inválidos recusados com mensagens de validação.
- **Status:** Pendente.

### CT30 — Encerramento de sessão
- **Requisito:** RF02 / RNF13
- **Prioridade:** Alta
- **Pré-condição:** Usuário autenticado.
- **Passos:** Realizar logout e tentar acessar uma rota protegida utilizando o token encerrado.
- **Resultado esperado:** Sessão encerrada e acesso negado.
- **Status:** Pendente.

## 4. Observações

- Os casos foram elaborados com base no ERS versão 1.1.0.
- Os testes ainda precisam ser executados para confirmação dos resultados.
- Os casos dependem de um ambiente de execução funcional e de dados de teste adequados.
- Qualquer falha encontrada deverá ser registrada em `Registro_de_Defeitos.md`.
- Evidências, como capturas de tela e resultados de execução, deverão ser associadas aos respectivos casos.

## 5. Resumo

| Indicador | Quantidade |
|---|---:|
| Casos preparados | 30 |
| Aprovados | 0 |
| Reprovados | 0 |
| Pendentes | 30 |
| Bloqueados | 0 |

**Conclusão:** Os casos de teste estão especificados e aguardam execução no ambiente do GymManager.
