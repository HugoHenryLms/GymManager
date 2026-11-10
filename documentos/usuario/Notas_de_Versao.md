# Notas de Versão — GymManager

**Sistema web de gerenciamento de treinos de academia**
Disciplina: Gerência de Configuração (6º período) · CENTRO UNIVERSITÁRIO FAMETRO
Professor: Paulo Rodrigo Barbosa Alves

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-DOC-003 |
| Caminho | `documentos/usuario/Notas_de_Versao.md` |
| Versão | 0.1.0 |
| Status | Em elaboração |
| Baseline prevista | BL-REL-S3 |
| Responsável | João Vitor Simonetti (Dev Backend e Frontend) |
| Apoio | Gerente de Projeto/Configuração |
| Dependência | GYM-GER-006 (Status Accounting), GYM-SRC-006 |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.1.0 | 10/11/2026 | João Vitor Simonetti | Criação do documento com a seção "Não lançado" | — |

---

Formato: cada release (tag `vMAJOR.MINOR.PATCH`, Plano de GC 3.5) lista as CRs incorporadas, as novidades, as correções e as versões dos ICs principais. Mudanças ainda não publicadas ficam em **Não lançado** até a criação da tag pelo Gerente de Projeto/Configuração.

---

## [Não lançado]

Candidata à primeira release **v1.0.0** (baseline BL-REL-S3). Ainda depende da revisão técnica do QA/Testes, dos testes automatizados (GYM-TST-001 a 004) e da aprovação das baselines BL-IMPL-S2 e BL-REL-S3.

### Novidades

- **Autenticação e perfis** (RF02, RF06): login por e-mail e senha, perfis Administrador, Instrutor e Aluno, logout com invalidação imediata da sessão.
- **Usuários e instrutores** (RF06): cadastro, edição e inativação pelo administrador.
- **Alunos** (RF01): cadastro, consulta, edição, inativação e reativação.
- **Catálogo de exercícios** (RF03): cadastro por grupo muscular; inativação sem perda das fichas existentes.
- **Fichas de treino** (RF04): montagem com biblioteca de exercícios, séries, repetições, carga, descanso e ordem; atribuição ao aluno; encerramento.
- **Execução e histórico** (RF05): registro do treino exercício a exercício, correção antes de finalizar, histórico com filtros e gráfico de evolução de carga.
- **Interface web responsiva** (RF07, RNF05): telas TL01 a TL09 com menu por perfil.
- **API REST** documentada em OpenAPI 3.0 (RNF09).
- **Infraestrutura**: ambiente completo com `docker compose up --build` (RNF10); migrações versionadas com checksum (RNF11); pipeline de CI no GitHub Actions (RNF08).

### Change Requests incorporadas

Nenhuma (desenvolvimento inicial, antes das baselines de implementação).

### Correções

- Porta padrão do MySQL no host alterada de 3307 para 3316, para evitar conflito com instalações locais.

### Versões dos ICs nesta entrega

| IC | Artefato | Versão |
| --- | --- | --- |
| GYM-CFG-001 | Estrutura de diretórios e `.gitignore` | 0.2.0 |
| GYM-CFG-002 | `.env.example` | 0.1.1 |
| GYM-ARQ-001 | Arquitetura | 0.1.1 |
| GYM-ARQ-002 | Modelo de Dados | 0.1.0 |
| GYM-ARQ-003 | OpenAPI | 0.1.0 |
| GYM-ARQ-004 | ADR-001 da stack | 0.1.1 |
| GYM-DB-001 | Migrações (V001) | 0.1.0 |
| GYM-SRC-001 | Autenticação, perfis e usuários | 0.1.0 |
| GYM-SRC-002 | Alunos | 0.1.0 |
| GYM-SRC-003 | Exercícios | 0.1.0 |
| GYM-SRC-004 | Fichas de treino | 0.1.0 |
| GYM-SRC-005 | Execuções e histórico | 0.1.0 |
| GYM-SRC-006 | Interface web | 0.1.0 |
| GYM-CI-001 | Pipeline de CI | 0.1.0 |
| GYM-IAC-001 | Docker e docker-compose | 0.1.0 |
| GYM-DOC-002 | Manual do Usuário | 0.1.0 |
| GYM-DOC-003 | Notas de Versão | 0.1.0 |

### Limitações conhecidas

- Testes automatizados (pytest e Postman/Newman) ainda não entregues pelo QA/Testes; o CI emite aviso enquanto não existirem.
- Não há recuperação de senha por e-mail; a redefinição é feita pelo administrador ou instrutor.

## Controle de configuração deste documento

Este documento é o IC **GYM-DOC-003**, sujeito ao Plano de GC (GYM-GER-003). Ao criar uma tag de release, o Gerente de Projeto/Configuração move o conteúdo de **Não lançado** para uma seção com o número da versão e a data.
