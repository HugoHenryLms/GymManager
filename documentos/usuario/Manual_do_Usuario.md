# Manual do Usuário — GymManager

**Sistema web de gerenciamento de treinos de academia**
Disciplina: Gerência de Configuração (6º período) · CENTRO UNIVERSITÁRIO FAMETRO
Professor: Paulo Rodrigo Barbosa Alves

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-DOC-002 |
| Caminho | `documentos/usuario/Manual_do_Usuario.md` |
| Versão | 0.1.0 |
| Status | Em elaboração |
| Baseline prevista | BL-REL-S3 |
| Responsável | João Vitor Simonetti (Dev Backend e Frontend) |
| Apoio | Gerente de Projeto/Configuração |
| Dependência | GYM-REQ-002 (Casos de Uso), GYM-SRC-006 (Interface web) |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.1.0 | 10/11/2026 | João Vitor Simonetti | Versão inicial, cobrindo os três perfis | — |

---

## 1. Introdução

O GymManager organiza o dia a dia de treinos da academia: o **instrutor** cadastra alunos e exercícios e monta as fichas de treino; o **aluno** consulta sua ficha, registra o que executou e acompanha a evolução da carga; o **administrador** gerencia usuários e instrutores e também pode fazer tudo o que o instrutor faz.

### 1.1 Acesso

- Endereço: o informado pela academia (no ambiente local, `http://localhost:8080`).
- Navegadores: versões atuais de Chrome, Edge, Firefox ou Safari, no computador ou no celular.
- O primeiro administrador é criado na instalação do sistema (ver seção 6).

### 1.2 Mapa de telas

| Tela | Menu | Quem usa | Para quê |
| --- | --- | --- | --- |
| TL01 Login | — | Todos | Entrar no sistema |
| TL02 Painel | Painel | Todos | Resumo do dia (conteúdo muda conforme o perfil) |
| TL03 Usuários | Usuários | Administrador | Cadastrar usuários e instrutores, definir perfis |
| TL04 Alunos | Alunos | Administrador, Instrutor | Cadastrar, editar e inativar alunos |
| TL05 Exercícios | Exercícios | Administrador, Instrutor | Manter o catálogo de exercícios |
| TL06 Treinos | Treinos | Administrador, Instrutor | Montar fichas e atribuí-las a alunos |
| TL07 Minhas fichas | Meu treino | Aluno | Ver as fichas ativas |
| TL08 Registro de execução | (a partir da ficha) | Aluno | Registrar o treino do dia |
| TL09 Histórico | Histórico | Todos | Treinos realizados e gráfico de evolução de carga |

O menu lateral mostra apenas as opções do seu perfil. No celular, toque em **☰** para abrir o menu.

---

## 2. Entrar e sair (todos os perfis)

1. Na tela de login, informe **e-mail** e **senha** e clique em **Entrar**.
2. Você será levado ao **Painel**.
3. Para sair, clique em **Sair**, no canto inferior do menu.

| Mensagem | O que significa |
| --- | --- |
| "E-mail ou senha inválidos." | Algum dos dados está incorreto (por segurança, o sistema não diz qual) |
| "Usuário inativo." | Seu acesso foi desativado; procure a administração da academia |

A sessão expira após algumas horas (padrão: 8 h). Depois disso, basta entrar novamente.

---

## 3. Administrador

O administrador tem todas as funções do instrutor (seção 4) e, além disso, a tela **Usuários**.

### 3.1 Cadastrar usuário ou instrutor

1. Menu **Usuários** → **+ Novo usuário**.
2. Preencha nome, e-mail, perfil (Administrador, Instrutor ou Aluno) e senha inicial.
3. Clique em **Salvar**.

Regras: e-mail único; senha com **no mínimo 8 caracteres, com letras e números**.

### 3.2 Editar e inativar

- **Editar**: altere nome, e-mail, perfil ou defina uma nova senha (deixe em branco para manter a atual).
- **Inativar**: o usuário perde o acesso imediatamente; o histórico é mantido. Para reativar, abra **Editar** e marque **Ativo**.
- O administrador não pode inativar o próprio usuário nem tirar de si o perfil de administrador.

Use os filtros por nome e por perfil para localizar usuários.

---

## 4. Instrutor

### 4.1 Painel

Mostra alunos ativos, fichas vigentes, fichas que vencem nos próximos 7 dias e alunos ativos sem ficha, com atalhos para **+ Novo aluno** e **+ Novo treino**.

### 4.2 Alunos

1. Menu **Alunos** → **+ Novo aluno**.
2. Preencha nome, e-mail, telefone, data de nascimento e uma **senha provisória** (repasse-a ao aluno).
3. Clique em **Salvar aluno**.

Na lista é possível **Editar**, **Inativar** (o aluno deixa de entrar e de receber fichas novas; o histórico é mantido), **Reativar** e abrir o **Histórico** do aluno. O filtro permite ver alunos ativos, inativos ou todos.

### 4.3 Exercícios

1. Menu **Exercícios** → **+ Novo exercício**.
2. Informe o nome (único), o grupo muscular (ex.: Peito, Costas, Pernas) e, se quiser, uma descrição.
3. Clique em **Salvar**.

Exercícios **não são excluídos**, apenas inativados: um exercício inativo continua nas fichas em que já estava, mas não aparece para fichas novas. Use os botões de grupo muscular para filtrar o catálogo.

### 4.4 Montar uma ficha de treino

1. Menu **Treinos** → **+ Novo treino** (ou **Montar ficha** no painel, para um aluno sem ficha).
2. Informe o **nome do treino**, o **aluno**, a **data de início** e, se houver, a **data de fim**.
3. Na **Biblioteca de exercícios** (à direita), busque ou filtre por grupo e clique em **Adicionar**.
4. Para cada exercício, ajuste **séries**, **repetições**, **carga (kg)** e **descanso (s)**. Use **↑ ↓** para mudar a ordem e **Remover** para tirar da ficha.
5. Clique em **Salvar treino**.

Regras: a ficha precisa de **pelo menos um exercício**; séries e repetições maiores que zero; carga maior ou igual a zero (até 2 casas decimais); data de fim não pode ser anterior à de início; o aluno precisa estar ativo.

### 4.5 Editar ou encerrar uma ficha

Em **Treinos**, clique em **Abrir** na ficha desejada. Altere o que precisar e clique em **Salvar treino**. Para encerrar, clique em **Encerrar ficha**: ela deixa de aparecer como ativa para o aluno, e os treinos já registrados continuam no histórico.

### 4.6 Acompanhar a evolução

Menu **Histórico**, escolha o aluno e, se quiser, um período. Veja a lista de treinos realizados (clique em um treino para ver o detalhe) e o gráfico de evolução de carga por exercício.

---

## 5. Aluno

### 5.1 Painel

Mostra sua ficha ativa com os exercícios do dia, os dias da semana em que você treinou e o gráfico de carga de um exercício. Use **Iniciar treino** (ou **Continuar treino**, se houver um treino em andamento).

### 5.2 Minhas fichas

Menu **Meu treino**: lista as fichas ativas, com séries, repetições, carga e descanso de cada exercício, na ordem definida pelo instrutor. Se não houver ficha, procure seu instrutor.

### 5.3 Registrar o treino

1. Na ficha, clique em **Iniciar treino** e, na tela seguinte, novamente em **Iniciar treino**.
2. Para cada exercício feito, confira as **repetições** e a **carga** usadas e clique em **Registrar**. O exercício fica marcado com ✓.
3. Errou algum valor? Altere e clique em **Corrigir** (vale enquanto o treino não for finalizado).
4. Ao terminar, clique em **Finalizar treino**. Se faltar algum exercício, o sistema pergunta se deseja finalizar mesmo assim; só os registrados são gravados.

Se você fechar o navegador no meio do treino, ele fica **em andamento**: volte pelo painel em **Continuar treino**.

### 5.4 Histórico e evolução

Menu **Histórico**: seus treinos, do mais recente para o mais antigo, e o gráfico de evolução de carga. Escolha o exercício na lista acima do gráfico e, se quiser, filtre por período. Você vê apenas os seus próprios dados.

---

## 6. Instalação (equipe técnica)

```bash
cp .env.example .env        # troque todos os valores "trocar-..."
docker compose up --build
```

- Interface: `http://localhost:8080` · API: `http://localhost:8080/api/v1`
- O administrador inicial é criado com `ADMIN_EMAIL` e `ADMIN_SENHA` do `.env`. **Troque essa senha no primeiro acesso** (Usuários → Editar).
- Detalhes técnicos: `documentos/arquitetura/Arquitetura.md` (GYM-ARQ-001).

## 7. Perguntas frequentes

| Pergunta | Resposta |
| --- | --- |
| Esqueci minha senha. | Peça ao administrador ou ao instrutor para definir uma nova senha no seu cadastro. |
| Não consigo adicionar um exercício à ficha. | Ele pode estar inativo; reative-o em **Exercícios**. |
| O aluno não aparece na lista ao montar a ficha. | Apenas alunos **ativos** podem receber fichas; reative-o em **Alunos**. |
| A ficha sumiu da tela do aluno. | Ela foi encerrada ou passou da data de fim; o histórico continua disponível. |

## 8. Controle de configuração deste documento

Este manual é o IC **GYM-DOC-002**, sujeito ao Plano de GC (GYM-GER-003). Toda mudança de tela ou de fluxo (GYM-SRC-006, GYM-REQ-002) deve atualizar este documento no mesmo Pull Request.
