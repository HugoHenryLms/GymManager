# Documento de Arquitetura — GymManager

**Sistema web de gerenciamento de treinos de academia**
Disciplina: Gerência de Configuração (6º período) · CENTRO UNIVERSITÁRIO FAMETRO
Professor: Paulo Rodrigo Barbosa Alves

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-ARQ-001 |
| Caminho | `documentos/arquitetura/Arquitetura.md` |
| Versão | 0.1.1 |
| Status | Em elaboração |
| Baseline prevista | BL-IMPL-S2 |
| Responsável | João Vitor Simonetti (Dev Backend e Frontend) |
| Apoio | DBA/DevOps |
| Dependência | GYM-REQ-001 (ERS) |
| ICs relacionados | GYM-ARQ-002 (Modelo de Dados), GYM-ARQ-003 (OpenAPI), GYM-ARQ-004 (ADR da stack), GYM-SRC-001 a 006, GYM-IAC-001, GYM-CI-001 |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.1.0 | 10/11/2026 | João Vitor Simonetti | Versão inicial do documento | — |
| 0.1.1 | 10/11/2026 | João Vitor Simonetti | Porta padrão do MySQL no host passa a 3316 (evita conflito com MySQL local em 3306/3307) | — |

---

## 1. Introdução

### 1.1 Propósito

Descreve a arquitetura do GymManager: componentes, camadas, organização do código, segurança, implantação e como cada parte se liga aos requisitos do ERS (GYM-REQ-001) e aos Itens de Configuração (ICs). As decisões de tecnologia estão justificadas no ADR-001 (GYM-ARQ-004).

### 1.2 Escopo

Cobre o backend (API REST), o frontend (interface web), o banco de dados, a infraestrutura em contêineres e o pipeline de CI da versão 1.0.0.

---

## 2. Visão geral

Aplicação web cliente-servidor em três camadas (ERS 2.1):

```mermaid
flowchart LR
    U([Navegador<br/>HTML/CSS/JS]) -- "HTTP :8080" --> N[frontend<br/>Nginx]
    N -- "arquivos estáticos" --> U
    N -- "proxy /api/*" --> B[backend<br/>Flask + Gunicorn :5000]
    B -- "SQL (PyMySQL)" --> D[(db<br/>MySQL 8.4)]
    M[[banco-de-dados/migracoes/*.sql]] -. "flask migrar" .-> D
```

- O navegador fala apenas com o contêiner **frontend** (mesma origem). Chamadas para `/api/...` são repassadas ao **backend**; por isso não há necessidade de CORS em produção.
- O **backend** é stateless: o estado da sessão fica no banco (tabela `sessao`), o que permite escalar o contêiner sem afinidade de sessão.
- O **banco** só é alterado por migrações versionadas (RNF11).

---

## 3. Backend (API REST)

### 3.1 Organização em camadas

| Camada | Onde fica | Responsabilidade |
| --- | --- | --- |
| Rotas (controle) | `gymmanager/<modulo>/rotas.py` | Recebe a requisição HTTP, aplica autenticação/autorização, chama validação e persistência, devolve JSON |
| Validação | `gymmanager/validacao.py` | Regras de validação da seção 4.3 do ERS, com as mensagens exatas exigidas |
| Modelo / persistência | `gymmanager/modelos.py` | Entidades SQLAlchemy mapeadas para as tabelas criadas pelas migrações |
| Segurança | `gymmanager/auth/seguranca.py` | Hash de senha, emissão e verificação de tokens, decoradores de perfil |
| Erros | `gymmanager/erros.py` | Formato único de erro e tratadores HTTP |
| Infraestrutura | `gymmanager/config.py`, `extensoes.py`, `migracoes.py`, `cli.py` | Configuração por variável de ambiente, conexão, executor de migrações e comandos de linha |

### 3.2 Módulos e rastreabilidade

| Módulo (pasta em `codigo-fonte/backend/gymmanager/`) | IC | Endpoints (base `/api/v1`) | Requisitos | Casos de uso |
| --- | --- | --- | --- | --- |
| `auth/` | GYM-SRC-001 | `POST /auth/login`, `POST /auth/logout` | RF02, RNF01, RNF02 | UC01 |
| `usuarios/` | GYM-SRC-001 | `GET/POST /usuarios`, `PUT/DELETE /usuarios/{id}` | RF06, RN03, RN05 | UC02 |
| `alunos/` | GYM-SRC-002 | `GET/POST /alunos`, `GET/PUT/DELETE /alunos/{id}` | RF01, RN05 | UC03 |
| `exercicios/` | GYM-SRC-003 | `GET/POST /exercicios`, `PUT/DELETE /exercicios/{id}` | RF03, RN04 | UC04 |
| `fichas/` | GYM-SRC-004 | `GET/POST /fichas`, `GET/PUT /fichas/{id}` | RF04, RN01, RN02, RN04, RN05, RN06 | UC05, UC06 |
| `execucoes/` | GYM-SRC-005 | `POST /execucoes`, `POST /execucoes/{id}/exercicios`, `PATCH /execucoes/{id}/finalizar`, `GET /alunos/{id}/historico` | RF05, RN02, RN07 | UC07, UC08 |

O cadastro de instrutores (objetivo específico do Plano de Projeto) está no módulo `usuarios/`, que pertence ao IC GYM-SRC-001, conforme a descrição desse IC na planilha.

### 3.3 Estrutura de pastas do backend

```
codigo-fonte/backend/
├── Dockerfile               (GYM-IAC-001)
├── requirements.txt         dependências de execução (versões fixadas)
├── requirements-dev.txt     dependências de teste (pytest)
├── wsgi.py                  ponto de entrada WSGI (gunicorn wsgi:app)
├── iniciar.py               inicialização do contêiner: aguarda o banco, migra, cria admin, sobe o gunicorn
└── gymmanager/
    ├── __init__.py          create_app() e versão do backend
    ├── config.py            configuração via variáveis de ambiente (.env)
    ├── extensoes.py         instância do SQLAlchemy
    ├── modelos.py           entidades
    ├── validacao.py         regras da seção 4.3 do ERS
    ├── erros.py             formato de erro e tratadores
    ├── migracoes.py         executor de migrações SQL
    ├── cli.py               comandos: flask migrar | flask criar-admin
    ├── auth/                GYM-SRC-001
    ├── usuarios/            GYM-SRC-001
    ├── alunos/              GYM-SRC-002
    ├── exercicios/          GYM-SRC-003
    ├── fichas/              GYM-SRC-004
    └── execucoes/           GYM-SRC-005
```

### 3.4 Formato das respostas

- Sucesso: JSON do recurso (objeto) ou lista de recursos (array). Datas no formato ISO 8601 (`AAAA-MM-DD`); data/hora em UTC com sufixo `Z`.
- Erro: sempre `{"erro": "<mensagem>", "campo": "<campo opcional>"}`, com os códigos da seção 4.5 do ERS: `400` dados inválidos, `401` não autenticado, `403` sem permissão, `404` não encontrado, `409` conflito, `500` erro interno.
- As mensagens de validação são exatamente as da seção 4.3 do ERS (ex.: `"Senha fraca."`, `"Exercício já cadastrado."`).

---

## 4. Segurança

| Aspecto | Solução | Requisito |
| --- | --- | --- |
| Armazenamento de senha | Hash `scrypt` com sal (`werkzeug.security`); a senha nunca é devolvida pela API | RNF01 |
| Autenticação | `POST /auth/login` devolve um token aleatório de 256 bits; o banco guarda apenas o hash SHA-256 do token e sua validade (`SESSAO_HORAS`) | RF02 |
| Envio do token | Cabeçalho `Authorization: Bearer <token>` em toda requisição, exceto o login | RNF02 |
| Logout | `POST /auth/logout` apaga a sessão no banco; o token deixa de valer imediatamente | RF02 |
| Autorização | Decorador `@exige_perfil(...)` verificado no backend; o administrador herda as permissões do instrutor | RNF02, RN01, RN03 |
| Dados do próprio aluno | Fichas, execuções e histórico filtrados pelo aluno logado; acesso a dados de outro aluno retorna `403` | RN02, RN07 |
| Usuário inativo | Não autentica (`403 "Usuário inativo."`); ao ser inativado, todas as suas sessões são removidas | RN05 |
| Segredos | Somente via variáveis de ambiente (`.env`, não versionado); `.env.example` sem valores reais | RNF03 |
| Injeção de SQL | Consultas via ORM / parâmetros vinculados; migrações não recebem entrada do usuário | — |
| XSS no frontend | Todo texto vindo da API é escapado antes de ir para o HTML | — |
| Cabeçalhos HTTP | Nginx envia `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` e `Content-Security-Policy` | — |

---

## 5. Frontend (interface web)

### 5.1 Organização

```
codigo-fonte/frontend/
├── Dockerfile        (GYM-IAC-001) imagem Nginx
├── nginx.conf        arquivos estáticos + proxy /api/ -> backend:5000
├── index.html        página única (SPA) com as telas TL01 a TL09
├── css/estilo.css    layout responsivo (RNF05), padrão visual dos protótipos
└── js/
    ├── api.js        cliente HTTP da API (token, erros, JSON)
    ├── ui.js         utilitários de interface (escape de HTML, mensagens, formulários, gráfico)
    ├── telas.js      renderização de cada tela
    └── app.js        roteamento por hash (#/rota) e menu por perfil
```

### 5.2 Telas, perfis e rotas

| Tela | Rota | Perfis | Requisitos |
| --- | --- | --- | --- |
| TL01 Login | `#/login` | Todos | RF02, RF07 |
| TL02 Painel inicial | `#/painel` | Todos (conteúdo por perfil) | RF07 |
| TL03 Usuários e instrutores | `#/usuarios` | Administrador | RF06 |
| TL04 Alunos | `#/alunos` | Administrador, Instrutor | RF01 |
| TL05 Catálogo de exercícios | `#/exercicios` | Administrador, Instrutor | RF03 |
| TL06 Montagem de ficha | `#/fichas`, `#/fichas/nova`, `#/fichas/{id}` | Administrador, Instrutor | RF04 |
| TL07 Minhas fichas | `#/minhas-fichas` | Aluno | RF04, RF07 |
| TL08 Registro de execução | `#/treino/{fichaId}` | Aluno | RF05 |
| TL09 Histórico e evolução | `#/historico` | Aluno (próprio), Instrutor, Administrador | RF05 |

O menu lateral mostra apenas as rotas permitidas ao perfil logado; se o usuário digitar uma rota não permitida, é redirecionado ao painel. A verificação definitiva é sempre feita no backend (RNF02).

---

## 6. Dados

O modelo físico, o dicionário de dados e as restrições estão em `documentos/arquitetura/Modelo_de_Dados.md` (GYM-ARQ-002). O esquema é criado e evoluído **somente** pelos scripts de `banco-de-dados/migracoes/` (GYM-DB-001):

- Nome dos arquivos: `V<NNN>__<descricao>.sql` (ex.: `V001__cria_tabelas.sql`), aplicados em ordem crescente.
- O executor (`flask migrar`) registra cada script na tabela `schema_migracoes` com o *checksum* SHA-256. Se um script já aplicado for alterado, a execução é interrompida com erro: **migração aplicada nunca é editada**; correções entram como nova migração.
- O primeiro administrador é criado por `flask criar-admin`, a partir de `ADMIN_NOME`, `ADMIN_EMAIL` e `ADMIN_SENHA` do `.env` (ERS 2.6), e somente se ainda não existir administrador.

---

## 7. Implantação (Docker)

| Serviço (`docker-compose.yml`) | Imagem | Porta no host | Observações |
| --- | --- | --- | --- |
| `db` | `mysql:8.4` | `MYSQL_PORTA_HOST` (3316) | Volume nomeado `mysql-data`; *healthcheck* com consulta `SELECT 1` usando o usuário da aplicação |
| `backend` | `codigo-fonte/backend/Dockerfile` | `BACKEND_PORTA` (5000) | Ao iniciar: aguarda o banco → `flask migrar` → `flask criar-admin` → gunicorn |
| `frontend` | `codigo-fonte/frontend/Dockerfile` | `FRONTEND_PORTA` (8080) | Nginx com proxy para o backend |

Subir o ambiente:

```bash
cp .env.example .env      # e troque os valores "trocar-..."
docker compose up --build
# Interface:  http://localhost:8080
# API:        http://localhost:8080/api/v1  (ou http://localhost:5000/api/v1)
```

Executar o backend sem Docker (desenvolvimento):

```bash
cd codigo-fonte/backend
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
# exporte as variáveis do .env (MYSQL_HOST=localhost, MYSQL_PORT=3316 etc.)
flask --app wsgi migrar
flask --app wsgi criar-admin
flask --app wsgi run --debug
```

---

## 8. Testes e integração contínua

### 8.1 Pontos de apoio para o QA/Testes (GYM-TST-002 a 004)

- `create_app(config)` aceita configuração de teste. Exemplo para testes unitários sem MySQL:
  `create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://", "CRIAR_TABELAS": True})` — com `CRIAR_TABELAS`, o esquema é gerado a partir dos modelos.
- Testes de integração usam MySQL real com o esquema criado pelas migrações (`flask migrar`), definindo `DATABASE_URL` (ex.: `mysql+pymysql://usuario:senha@127.0.0.1:3306/gymmanager`).
- A coleção Postman deve ficar em `codigo-fonte/testes/postman/` com nome `*.postman_collection.json` e usar a variável `baseUrl` (o CI passa `http://localhost:8080/api/v1`) e as variáveis `adminEmail` e `adminSenha`.

### 8.2 Pipeline (GYM-CI-001, `.github/workflows/ci.yml`)

Executado em todo Pull Request e em todo push na `main`:

1. **backend** — instala dependências, verifica a sintaxe de todo o código Python, sobe um MySQL de serviço, aplica as migrações (duas vezes, para garantir idempotência), cria o administrador e executa o `pytest` em `codigo-fonte/testes/`.
2. **docker** — copia o `.env.example`, sobe os três contêineres com `docker compose up --build --wait`, faz um teste de fumaça (login do administrador através do proxy do frontend) e executa a coleção Postman com Newman, quando existir.

PR com CI vermelho não é mesclado (Plano de GC, seção 9).

---

## 9. Atendimento aos requisitos não funcionais

| RNF | Como a arquitetura atende |
| --- | --- |
| RNF01 | Hash scrypt com sal (seção 4) |
| RNF02 | Token obrigatório em todas as rotas, exceto o login; perfis verificados no backend |
| RNF03 | `.env` fora do Git; `.env.example` sem segredos |
| RNF04 | Consultas indexadas (Modelo de Dados), API stateless, gunicorn com múltiplos workers |
| RNF05, RNF06 | CSS responsivo sem dependências; JavaScript padrão suportado pelos navegadores atuais |
| RNF07 | Camadas separadas por módulo; commits no padrão Conventional Commits |
| RNF08 | pytest e Newman no CI a cada PR |
| RNF09 | Contrato em `openapi.yaml` (GYM-ARQ-003), revisado junto com as rotas |
| RNF10 | `docker compose up --build` a partir do `.env.example` |
| RNF11 | Migrações versionadas com checksum |
| RNF12 | Tabela de módulos × ICs × requisitos (seção 3.2) |

## 10. Controle de configuração deste documento

Este documento é o IC **GYM-ARQ-001** e segue o Plano de GC (GYM-GER-003): alterações por issue e Pull Request revisado por outro integrante até a baseline BL-IMPL-S2; depois, somente via CR aprovada pelo CCB. Mudanças de arquitetura devem atualizar no mesmo PR o Modelo de Dados (GYM-ARQ-002), o OpenAPI (GYM-ARQ-003) e o ADR correspondente, quando afetados.
