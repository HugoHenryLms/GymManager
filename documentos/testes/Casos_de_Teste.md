# Casos de Teste – GymManager

## 1. Objetivo
Verificar se as funcionalidades do GymManager atendem aos requisitos definidos no projeto.

## 2. Casos de teste

| ID | Funcionalidade | Procedimento | Resultado esperado |
|---|---|---|---|
| CT01 | Login | Acessar com dados válidos | Usuário consegue entrar |
| CT02 | Login inválido | Informar senha incorreta | Acesso negado |
| CT03 | Cadastro de usuário | Cadastrar um novo usuário | Usuário registrado corretamente |
| CT04 | Cadastro de instrutor | Administrador cadastrar um instrutor | Instrutor registrado |
| CT05 | Cadastro de aluno | Instrutor cadastrar um aluno | Aluno registrado |
| CT06 | Cadastro de exercício | Instrutor adicionar um exercício | Exercício salvo |
| CT07 | Criar ficha de treino | Instrutor montar uma ficha | Ficha criada corretamente |
| CT08 | Consultar ficha | Aluno acessar sua ficha | Ficha exibida corretamente |
| CT09 | Registrar treino | Aluno registrar a execução de um treino | Registro salvo |
| CT10 | Histórico de treinos | Consultar treinos anteriores | Histórico exibido |
| CT11 | Privacidade | Aluno tentar acessar dados de outro aluno | Acesso negado |
| CT12 | Permissões | Usuário tentar acessar função não autorizada | Acesso bloqueado |

## 3. Status dos testes

Todos os testes estão inicialmente pendentes de execução.

- **Aprovado:** resultado esperado alcançado.
- **Reprovado:** resultado diferente do esperado.
- **Pendente:** teste ainda não executado.

## 4. Observações

Os testes serão realizados após a disponibilização das funcionalidades do aplicativo. Os resultados e possíveis defeitos serão registrados nos documentos correspondentes.
