# Casos de Uso — GymManager

**Sistema web de gerenciamento de treinos de academia**
Disciplina: Gerência de Configuração (6º período) · CENTRO UNIVERSITÁRIO FAMETRO
Professor: Paulo Rodrigo Barbosa Alves

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-REQ-002 |
| Caminho | `documentos/requisitos/Casos_de_Uso.md` |
| Versão | 0.2.0 |
| Status | Finalizado |
| Baseline prevista | BL-REQ-S1 (Funcional) |
| Responsável | Renata Martins da Silva (Analista de Requisitos) |
| Apoio | João Vitor Simonetti (Dev Backend e Frontend) |
| Dependência | GYM-REQ-001 (ERS) |
| ICs relacionados | GYM-REQ-003 (RTM), GYM-REQ-004 (Protótipos de tela), GYM-ARQ-003 (OpenAPI) |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.1.0 | 09-11-2026 | Renata Martins da Silva | Versão inicial do documento | — |
| 0.2.0 | 14-11-2026 | Renata Martins da Silva | Atualização conforme o sistema implementado (versão 0.1.0 do produto): fluxos, mensagens e códigos de erro reais; reativação de usuários, alunos e exercícios; encerramento de ficha; novas regras RN08 a RN12; painel inicial por perfil; filtros e comportamentos das telas; rastreabilidade com GYM-TST-005 e seção 8 (notas de implementação)
Atualização de versão do documento.
| — |
---

## 1. Introdução

### 1.1 Propósito

Este documento apresenta a modelagem de casos de uso do **GymManager**, detalhando como cada ator interage com o sistema para cumprir os requisitos do ERS (GYM-REQ-001). Ele serve de base para a especificação da API (GYM-ARQ-003), a interface web (GYM-SRC-006), o Plano de Testes (GYM-TST-001) e o Manual do Usuário (GYM-DOC-002). Na versão 0.2.0, os fluxos foram conferidos com o sistema implementado.

### 1.2 Convenções

- **Identificadores:** casos de uso `UC01` a `UC08`; requisitos `RF`, `RNF` e regras de negócio `RN`, todos conforme o ERS; telas `TL01` a `TL09`, conforme os protótipos (GYM-REQ-004).
- **Fluxo principal:** sequência normal de passos, sem falhas.
- **Fluxos alternativos (FA):** variações válidas do fluxo principal.
- **Fluxos de exceção (FE):** situações de erro, com a resposta do sistema.
- Mensagens de erro de validação seguem a seção 4.3 do ERS.
- Mensagens de erro de validação e de regras de negócio seguem a seção 4.3 do ERS.
- Ficha vigente: ficha ativa cuja data de fim está vazia ou não é anterior à data atual (RN10).
---

## 2. Atores

| Ator | Descrição | Observação |
| --- | --- | --- |
| Administrador | Responsável pela gestão do sistema: usuários, instrutores e perfis | Herda todas as permissões do Instrutor |
| Instrutor | Profissional da academia que gerencia alunos, exercícios e fichas e acompanha a evolução | — |
| Aluno | Praticante atendido pela academia; consulta fichas, registra execuções e vê seu histórico | Acessa apenas os próprios dados (RN02) não herda permissões da equipe  |

---
## 3. Diagrama de casos de uso

```mermaid
flowchart LR
    ADM([Administrador])
    INS([Instrutor])
    ALU([Aluno])

    subgraph GymManager
        UC01((UC01<br/>Autenticar-se))
        UC02((UC02<br/>Gerenciar usuários<br/>e instrutores))
        UC03((UC03<br/>Gerenciar alunos))
        UC04((UC04<br/>Gerenciar exercícios))
        UC05((UC05<br/>Montar e atribuir<br/>ficha de treino))
        UC06((UC06<br/>Consultar minhas<br/>fichas))
        UC07((UC07<br/>Registrar execução<br/>do treino))
        UC08((UC08<br/>Consultar histórico<br/>e evolução))
    end

    ADM -. "herda permissões" .-> INS

    ADM --- UC02
    INS --- UC03
    INS --- UC04
    INS --- UC05
    INS --- UC08
    ALU --- UC06
    ALU --- UC07
    ALU --- UC08

    UC02 -. "«include»" .-> UC01
    UC03 -. "«include»" .-> UC01
    UC04 -. "«include»" .-> UC01
    UC05 -. "«include»" .-> UC01
    UC06 -. "«include»" .-> UC01
    UC07 -. "«include»" .-> UC01
    UC08 -. "«include»" .-> UC01
    UC05 -. "«include»" .-> UC03
    UC05 -. "«include»" .-> UC04
```



**Leitura do diagrama:**

- Todos os casos de uso, exceto UC01, exigem autenticação (RNF02); por isso incluem UC01.
- O Administrador herda do Instrutor e, por isso, também realiza UC03, UC04, UC05 e UC08, além de UC02. **Não** realiza UC06 e UC07, que são exclusivos do Aluno.
- UC05 depende de alunos e exercícios já cadastrados (UC03 e UC04), representados como inclusões.
- UC01 é realizado por todos os atores.

---

## 4. Lista de casos de uso

| ID | Caso de uso | Ator(es) | Requisito(s) | Regras de negócio | Telas |
| --- | --- | --- | --- | --- | --- |
| UC01 | Autenticar-se | Todos | RF02, RF07 | RN05 | TL01, TL02 |
| UC02 | Gerenciar usuários e instrutores | Administrador | RF06 | RN03, RN05 | TL03 |
| UC03 | Gerenciar alunos | Administrador, Instrutor | RF01 | RN05 | TL04 |
| UC04 | Gerenciar exercícios | Administrador, Instrutor | RF03 | RN04 | TL05 |
| UC05 | Montar e atribuir ficha de treino | Instrutor, Administrador | RF04 | RN01, RN04, RN05, RN06 | TL06 |
| UC06 | Consultar minhas fichas | Aluno | RF04, RF07 | RN02 | TL07 |
| UC07 | Registrar execução do treino | Aluno | RF05 | RN02, RN07 | TL08 |
| UC08 | Consultar histórico e evolução de carga | Aluno, Instrutor, Administrador | RF05 | RN02 | TL09 |

---

## 5. Descrição dos casos de uso

### UC01 — Autenticar-se

| Item | Descrição |
| --- | --- |
| Ator | Administrador, Instrutor, Aluno |
| Requisitos | RF02, RF07 |
| Regras de negócio | RN05 |
| Tela | TL01 (Login), TL02 (Painel inicial) |
| Endpoints | `POST /auth/login`, `POST /auth/logout` |
| Pré-condição | Usuário cadastrado e ativo |
| Pós-condição | Sessão iniciada e menu exibido conforme o perfil; ou sessão encerrada (logout) |

**Fluxo principal**

1. O usuário acessa a tela de login (TL01).
2. Informa e-mail e senha.
3. O sistema valida o formato dos dados e confere as credenciais (o e-mail não diferencia maiúsculas de minúsculas).
4. O sistema inicia a sessão e identifica o perfil do usuário.
5. O sistema exibe o painel inicial (TL02) com as funções permitidas ao perfil: para administrador e instrutor, o resumo da academia (alunos ativos, fichas vigentes, fichas a renovar em 7 dias e alunos sem ficha); para o aluno, o treino atual, a semana e a evolução de carga.

**Fluxos alternativos**

- **FA1 — Encerrar sessão:** no passo 5 em diante, o usuário aciona "Sair"; o sistema encerra a sessão e retorna à TL01.
- **FA2 — Sessão já aberta:** se o navegador já tem sessão válida e o usuário acessa a TL01, o sistema o leva ao painel.
- 
**Fluxos de exceção**

- **FE1 — Credenciais inválidas:** o sistema informa o erro sem indicar qual campo está incorreto e permanece na TL01.
- **FE2 — Usuário inativo:** o sistema nega o acesso e informa que o usuário está inativo (RN05).
- **FE3 — Dados inválidos:** e-mail ou senha em branco; a interface exibe "Informe e-mail e senha." e a API responde `400`.
- **FE4 — Sessão expirada ou encerrada:** ao receber `401` em qualquer chamada, a interface descarta a sessão e volta à TL01. Isso ocorre também quando o usuário é inativado durante a sessão (RN05).
- **FE5 — Rota não permitida ao perfil:** a interface redireciona ao painel; se a chamada chegar à API, ela responde `403`.

---

### UC02 — Gerenciar usuários e instrutores

| Item | Descrição |
| --- | --- |
| Ator | Administrador |
| Requisitos | RF06 |
| Regras de negócio | RN03, RN05, RN08 |
| Tela | TL03 (Usuários e instrutores) |
| Endpoints | `GET /usuarios`, `POST /usuarios`, `PUT /usuarios/{id}`, `DELETE /usuarios/{id}` |
| Pré-condição | Administrador autenticado (UC01) |
| Pós-condição | Cadastro de usuário criado, atualizado, inativado ou rativado. |

**Fluxo principal (cadastrar usuário ou instrutor)**

1. O administrador acessa a TL03 e seleciona "Novo usuário".
2. Informa nome, e-mail, senha inicial e perfil (administrador, instrutor ou aluno).
3. O sistema valida os dados (e-mail único, senha com 8 caracteres ou mais, perfil válido).
4. O sistema grava a senha com hash e registra o usuário como ativo.
5. O sistema exibe o usuário na listagem e confirma o cadastro.

**Fluxos alternativos**

- **FA1 — Consultar:** o administrador visualiza a listagem e filtra por nome, e-mail ou perfil.
- **FA2 — Editar:** o administrador seleciona um usuário, altera nome, e-mail ou perfil, e salva.
- **FA3 — Inativar:** o administrador seleciona "Inativar" e confirma; o usuário passa a inativo e perde o acesso, e o histórico é preservado (RN05).
- **FA4 — Reativar:** ao editar um usuário inativo, o administrador marca "Ativo" e salva; o usuário volta a poder autenticar-se.
- 
**Fluxos de exceção**

- **FE1 — E-mail já cadastrado:** o sistema exibe "E-mail inválido ou já cadastrado."
- **FE2 — Senha fraca:** o sistema exibe "Senha fraca."
- **FE3 — Sem permissão:** usuário que não seja administrador tenta acessar; o sistema retorna erro 403 (RN03).
- **FE4 — Administrador altera a si mesmo:** ao tentar inativar a própria conta ou mudar o próprio perfil, o sistema responde `409` com "Não é possível inativar ou alterar o perfil do próprio usuário." (RN08). Na interface, a ação "Inativar" não aparece na própria linha e o campo perfil fica desabilitado.
- **FE5 — Usuário não encontrado:** o sistema retorna `404`.

---

### UC03 — Gerenciar alunos

| Item | Descrição |
| --- | --- |
| Ator | Administrador, Instrutor |
| Requisitos | RF01 |
| Regras de negócio | RN05 |
| Tela | TL04 (Alunos) |
| Endpoints | `GET /alunos`, `POST /alunos`, `GET /alunos/{id}`, `PUT /alunos/{id}`, `DELETE /alunos/{id}` |
| Pré-condição | Usuário autenticado (UC01) com perfil de instrutor ou administrador |
| Pós-condição | Aluno cadastrado, atualizado, inativado ou reativado |

**Fluxo principal (cadastrar aluno)**

1. O ator acessa a TL04 e seleciona "Novo aluno".
2. Informa nome, e-mail, senha inicial e demais dados do aluno (data de nascimento e telefone).
3. O sistema valida os dados.
4. O sistema registra o aluno com perfil ALUNO e situação ativa.
5. O sistema exibe o aluno na listagem e confirma o cadastro.

**Fluxos alternativos**

- **FA1 — Consultar:** o ator pesquisa e visualiza os dados de um aluno.
- **FA2 — Editar:** o ator altera os dados do aluno e salva.
- **FA3 — Inativar:** o ator inativa o aluno após confirmação; o aluno não se autentica nem recebe novas fichas, e o histórico é mantido (RN05).
- **FA4 — Reativar:** o ator aciona "Reativar" em um aluno inativo; o aluno volta a poder autenticar-se e receber fichas.

**Fluxos de exceção**

- **FE1 — E-mail já cadastrado ou dados inválidos:** o sistema exibe a mensagem de validação correspondente.
- **FE2 — Aluno não encontrado:** o sistema retorna erro 404.

---

### UC04 — Gerenciar exercícios

| Item | Descrição |
| --- | --- |
| Ator | Administrador, Instrutor |
| Requisitos | RF03 |
| Regras de negócio | RN04 |
| Tela | TL05 (Catálogo de exercícios) |
| Endpoints | `GET /exercicios`, `POST /exercicios`, `PUT /exercicios/{id}`, `DELETE /exercicios/{id}` |
| Pré-condição | Usuário autenticado (UC01) com perfil de instrutor ou administrador |
| Pós-condição | Exercício cadastrado, atualizado, reativado ou inativado no catálogo |

**Fluxo principal (cadastrar exercício)**

1. O ator acessa a TL05 e seleciona "Novo exercício".
2. Informa nome, grupo muscular e descrição.
3. O sistema valida os dados (nome obrigatório e único).
4. O sistema registra o exercício como ativo.
5. O sistema exibe o exercício no catálogo.

**Fluxos alternativos**

- **FA1 — Consultar:** o ator lista e filtra os exercícios por nome ou grupo muscular.
- **FA2 — Editar:** o ator altera os dados e salva.
- **FA3 — Inativar:** o ator inativa o exercício; ele deixa de ser oferecido para novas fichas, mas permanece nas fichas existentes (RN04).
- **FA4 — Reativar:** o ator aciona "Reativar"; o exercício volta a ser oferecido para novas fichas.

**Fluxos de exceção**

- **FE1 — Nome duplicado:** o sistema exibe "Exercício já cadastrado."
- **FE2 — Tentativa de exclusão de exercício em uso:** o sistema não exclui e propõe a inativação (RN04).
- **FE3 — Exercício não encontrado:** o sistema retorna `404`.

---

### UC05 — Montar e atribuir ficha de treino

| Item | Descrição |
| --- | --- |
| Ator | Instrutor (e Administrador) |
| Requisitos | RF04 |
| Regras de negócio | RN01, RN04, RN05, RN06 |
| Tela | TL06 (Montagem de ficha de treino) |
| Endpoints | `GET /fichas`, `POST /fichas`, `GET /fichas/{id}`, `PUT /fichas/{id}` |
| Pré-condição | Instrutor autenticado (UC01); aluno ativo (UC03) e exercícios ativos (UC04) cadastrados |
| Pós-condição | Ficha ativa, atribuída ao aluno e visível a ele |

**Fluxo principal**

1. O instrutor acessa a TL06 e aciona "+ Novo treino" (a partir do painel, o atalho "Montar ficha" já traz o aluno selecionado).
2. Informa o nome da ficha, seleciona o aluno (somente alunos ativos) e informa a data de início (preenchida com a data atual) e, opcionalmente, a data de fim.
3. Adiciona exercícios da biblioteca do catálogo (somente exercícios ativos; busca por nome e filtro por grupo), informando para cada um séries, repetições, carga (kg) e descanso (s); novos itens iniciam com 3 séries, 12 repetições, 0 kg e 60 s. A ordem é ajustada pelos botões de subir e descer.
4. Salva a ficha.
5. O sistema valida os dados e confere que há ao menos um exercício (RN06).
6. O sistema grava a ficha, registra o usuário logado como instrutor (RN01), atribui ao aluno e confirma a operação.


**Fluxos alternativos**

- **FA1 — Editar ficha:** o instrutor abre uma ficha existente, altera exercícios ou parâmetros e salva.
- **FA2 — Consultar fichas:** o instrutor lista as fichas, filtrando por aluno.
- **FA3 — Encerrar ficha:** o instrutor informa a data de fim ou marca a ficha como inativa; ela deixa de aparecer como ativa para o aluno, e o histórico é mantido.
- **FA4 — Reativar ficha:** ao editar uma ficha encerrada, o instrutor pode torná-la ativa novamente, desde que o aluno esteja ativo (RN09).
- **FA5 — Trocar o aluno da ficha:** permitido apenas enquanto a ficha não tiver execuções registradas (RN09).


**Fluxos de exceção**

- **FE1 — Ficha sem exercício:** o sistema impede o salvamento e responde `400` com "A ficha deve ter pelo menos um exercício." (RN06).
- **FE2 — Valores inválidos:** séries ou repetições menores ou iguais a zero ("Valor deve ser maior que zero."), carga negativa ou fora do limite ("Carga inválida."), descanso inválido ("Descanso inválido."), nome fora do tamanho ("Nome obrigatório.") ou data de fim anterior à de início ("Data final anterior à inicial."); o sistema mantém a ficha em edição e destaca o campo (e a linha do exercício) com erro.
- **FE3 — Aluno inativo:** o sistema não permite atribuir a ficha e responde `409` com "Aluno inativo não pode receber fichas." (RN05).
- **FE4 — Exercício inativo:** o sistema não aceita adicionar exercício inativo a uma ficha e responde `400` (RN04); um exercício que já consta na ficha e foi inativado depois continua nela.
- **FE5 — Ficha com execuções muda de aluno:** o sistema responde `409` com "Ficha com execuções registradas não pode mudar de aluno." (RN09).
- **FE6 — Usuário sem permissão:** perfil aluno tenta criar ou alterar ficha; o sistema retorna erro `403` (RN01).
- **FE7 — Ficha não encontrada:** o sistema retorna `404`.

---

### UC06 — Consultar minhas fichas

| Item | Descrição |
| --- | --- |
| Ator | Aluno |
| Requisitos | RF04, RF07 |
| Regras de negócio | RN02 |
| Tela | TL07 (Minhas fichas) |
| Endpoints | `GET /fichas`, `GET /fichas/{id}` |
| Pré-condição | Aluno autenticado (UC01) |
| Pós-condição | Fichas do aluno exibidas |

**Fluxo principal**

1. O aluno acessa a TL07 (item "Meu treino" do menu).
2. O sistema lista as fichas vigentes atribuídas ao aluno logado, com instrutor e período.
3. Para cada ficha, o sistema exibe os exercícios, com séries, repetições, carga e descanso, na ordem definida.

**Fluxos alternativos**

- **FA1 — Sem ficha ativa:** o sistema informa que não há fichas atribuídas e orienta procurar o instrutor.
- **FA2 — Iniciar treino:** a partir da ficha exibida, o aluno aciona "Iniciar treino" e segue para o UC07.

**Fluxos de exceção**

- **FE1 — Ficha de outro aluno:** o aluno tenta acessar ficha que não lhe pertence; o sistema retorna erro 403 ou 404 (RN02).

---

### UC07 — Registrar execução do treino

| Item | Descrição |
| --- | --- |
| Ator | Aluno |
| Requisitos | RF05 |
| Regras de negócio | RN02, RN07 |
| Tela | TL08 (Registro de execução) |
| Endpoints | `POST /execucoes`, `POST /execucoes/{id}/exercicios`, `PATCH /execucoes/{id}/finalizar` |
| Pré-condição | Aluno autenticado (UC01) com ficha ativa atribuída (UC05) |
| Pós-condição | Execução registrada e disponível no histórico (UC08) |

**Fluxo principal**

1. O aluno seleciona a ficha do dia e aciona "Iniciar treino" (a partir do UC06).
2. O sistema cria a execução, registra a data e a hora de início e exibe os exercícios da ficha.
3. Para cada exercício, o aluno informa as repetições realizadas e a carga utilizada (kg).
4. O sistema grava cada registro, vinculado ao item correspondente da ficha.
5. Ao concluir, o aluno aciona "Finalizar treino".
6. O sistema registra a data e a hora de término e confirma a execução.

**Fluxos alternativos**

- **FA1 — Corrigir registro:** antes de finalizar, o aluno altera a repetição ou a carga de um exercício já registrado.
- **FA2 — Finalizar parcialmente:** o aluno finaliza sem ter registrado todos os exercícios; o sistema grava apenas os informados.
- **FA3 — Retomar treino em andamento:** ao abrir a ficha que já tem execução em andamento, a interface a retoma, exibindo os exercícios já registrados e o botão "Continuar treino" no painel.


**Fluxos de exceção**

- **FE1 — Valores inválidos:** repetições ou carga negativas; o sistema exibe "Carga inválida." ou "Valor deve ser maior que zero." e não grava o registro.
- **FE2 — Ficha não atribuída ao aluno:** o sistema retorna erro 403 (RN02, RN07).
- **FE3 — Execução já finalizada:** o sistema impede novos registros na execução encerrada.
- **FE4 — Ficha não vigente:** ficha encerrada ou com data de fim vencida; o sistema não inicia a execução e responde `409` com "Ficha inativa." (RN10). Na interface, o botão "Iniciar treino" não é exibido para fichas não vigentes.
- **FE5 — Exercício de outra ficha:** o registro de um item que não pertence à ficha da execução é recusado (`400`, "Exercício não pertence à ficha desta execução.").
- **FE6 — Execução de outro aluno ou inexistente:** o sistema retorna `403` ou `404`, respectivamente (RN02).
---

### UC08 — Consultar histórico e evolução de carga

| Item | Descrição |
| --- | --- |
| Ator | Aluno (próprio histórico); Instrutor e Administrador (histórico dos alunos) |
| Requisitos | RF05 |
| Regras de negócio | RN02 |
| Tela | TL09 (Histórico e evolução de carga) |
| Endpoints | `GET /alunos/{id}/historico` |
| Pré-condição | Usuário autenticado (UC01); existem execuções registradas (UC07) |
| Pós-condição | Histórico e evolução exibidos |

**Fluxo principal**

1. O ator acessa a TL09 (o aluno vê o próprio histórico; o instrutor seleciona um aluno).
2. O sistema lista as execuções realizadas, da mais recente para a mais antiga, com data, ficha e duração.
3. O ator seleciona um exercício.
4. O sistema exibe o gráfico de evolução da carga desse exercício ao longo do tempo e a variação desde o primeiro registro. A API entrega também as repetições de cada ponto da evolução.

**Fluxos alternativos**

- **FA1 — Filtrar por período ou ficha:** o ator restringe o histórico a um intervalo de datas ou a uma ficha.
- **FA2 — Detalhar execução:** o ator abre uma execução e vê o registro de cada exercício.

**Fluxos de exceção**

- **FE1 — Sem execuções:** o sistema informa que ainda não há treinos registrados.
- **FE2 — Histórico de outro aluno:** o aluno tenta consultar o histórico de terceiros; o sistema retorna erro 403 (RN02).
- **FE3 — Aluno não encontrado:** o identificador informado não pertence a um aluno; o sistema retorna `404`.
- **FE4 — Período inválido:** data final anterior à inicial; o sistema responde `400` com "Data final anterior à inicial."

---

## 6. Rastreabilidade dos casos de uso

| Caso de uso | Requisito(s) | IC de código | IC de teste | Tela(s) |
| --- | --- | --- | --- | --- |
| UC01 | RF02, RF07 | GYM-SRC-001, GYM-SRC-006 | GYM-TST-001 a GYM-TST-004 | TL01, TL02 |
| UC02 | RF06 | GYM-SRC-001, GYM-SRC-006 | GYM-TST-001 a GYM-TST-004 | TL03 |
| UC03 | RF01 | GYM-SRC-002, GYM-SRC-006 | GYM-TST-001 a GYM-TST-004 | TL04 |
| UC04 | RF03 | GYM-SRC-003, GYM-SRC-006 | GYM-TST-001 a GYM-TST-004 | TL05 |
| UC05 | RF04 | GYM-SRC-004, GYM-SRC-006 | GYM-TST-001 a GYM-TST-004 | TL06 |
| UC06 | RF04, RF07 | GYM-SRC-004, GYM-SRC-006 | GYM-TST-001 a GYM-TST-004 | TL07 |
| UC07 | RF05 | GYM-SRC-005, GYM-SRC-006 | GYM-TST-001 a GYM-TST-004 | TL08 |
| UC08 | RF05 | GYM-SRC-005, GYM-SRC-006 | GYM-TST-001 a GYM-TST-004 | TL09 |

Correspondência com os casos de teste funcionais (GYM-TST-005): CT01 e CT02 → UC01; CT03 e CT04 → UC02; CT05 → UC03; CT06 → UC04; CT07 → UC05; CT08 → UC06; CT09 → UC07; CT10 → UC08; CT11 → UC06, UC07 e UC08 (RN02); CT12 → UC01 a UC08 (RNF02).

A matriz completa, com todos os requisitos funcionais e não funcionais, está em `documentos/requisitos/RTM.xlsx` (GYM-REQ-003).

---

## 7. Controle de configuração deste documento

- Este documento é o IC **GYM-REQ-002** e está sujeito às regras do Plano de GC (GYM-GER-003).
- Até a baseline BL-REQ-S1, alterações seguem por issue e Pull Request, revisadas por outro integrante; após a baseline, somente mediante CR aprovada pelo CCB.
- Qualquer mudança de caso de uso deve manter coerência com o ERS (GYM-REQ-001), a RTM (GYM-REQ-003), os protótipos (GYM-REQ-004), a especificação OpenAPI (GYM-ARQ-003) e o Plano de Testes (GYM-TST-001).
- Cada revisão incrementa a versão (SemVer) no início do documento, no histórico de revisões e na planilha de ICs (GYM-GER-002).
- Antes da baseline, o documento passa por revisão técnica formal do QA/Testes (Iago Medice Ferreira da Silva, Tiago Costa dos Santos e Ruan Victor Assunção Costa).

## 8. Notas de implementação

Comportamentos do sistema implementado que o leitor dos fluxos acima deve conhecer (detalhes e situação de cada requisito na seção 7 do ERS):

- **Exclusões são sempre lógicas:** não há exclusão física de usuários, alunos, exercícios, fichas ou execuções; "Inativar" mantém o histórico.
- **Instrutor da ficha:** é sempre o usuário que a criou, mesmo quando é o administrador; qualquer instrutor ou administrador pode editar qualquer ficha.
- **Execuções simultâneas:** a API não impede iniciar uma nova execução da mesma ficha enquanto outra está em andamento; a interface retoma a execução aberta (UC07, FA3).
- **Vigência da ficha:** é verificada ao iniciar a execução; uma execução já iniciada pode continuar a ser registrada e finalizada mesmo que a ficha seja encerrada depois.
- **Evolução na interface:** o gráfico exibe a carga; as repetições de cada ponto são entregues pela API, mas ainda não aparecem na tela.
- **Telas e menu por perfil:** ver a seção 4.4 do ERS.

  
