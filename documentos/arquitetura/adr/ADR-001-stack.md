# ADR-001 — Stack tecnológica do GymManager

**Sistema web de gerenciamento de treinos de academia**
Disciplina: Gerência de Configuração (6º período) · CENTRO UNIVERSITÁRIO FAMETRO
Professor: Paulo Rodrigo Barbosa Alves

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-ARQ-004 |
| Caminho | `documentos/arquitetura/adr/ADR-001-stack.md` |
| Versão | 0.1.1 |
| Status | Em elaboração |
| Baseline prevista | BL-IMPL-S2 |
| Responsável | João Vitor Simonetti (Dev Backend e Frontend) |
| Apoio | DBA/DevOps |
| Dependência | GYM-ARQ-001 (Arquitetura) |
| ICs relacionados | GYM-GER-001 (Plano de Projeto, seção 4), GYM-REQ-001 (ERS, seção 2.2), GYM-IAC-001, GYM-CI-001 |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.1.0 | 10/11/2026 | João Vitor Simonetti | Versão inicial do ADR | — |
| 0.1.1 | 10/11/2026 | João Vitor Simonetti | Ajusta versões fixadas (Flask 3.1.3, Gunicorn 27.0) ao requirements.txt | — |

---

## Situação da decisão

**Proposta** — aguardando revisão técnica do QA/Testes e aprovação para a baseline BL-IMPL-S2.

## Contexto

O Plano de Projeto (GYM-GER-001, seção 4) e o ERS (GYM-REQ-001, seção 2.2) já definem as tecnologias de cada camada. Este ADR registra **por que** elas foram escolhidas, **como** são usadas e quais versões são fixadas, para que qualquer mudança futura de stack seja tratada como mudança de IC (via issue/PR ou CR, conforme o Plano de GC).

Restrições consideradas:

- Projeto acadêmico, equipe pequena, entregas semanais.
- Aplicação exclusivamente web (ERS 2.5).
- Ambiente reproduzível (RNF10), CI a cada Pull Request (RNF08) e esquema do banco evoluído por migrações (RNF11).
- Nenhum segredo versionado (RNF03).

## Decisão

| Camada | Tecnologia | Versão fixada | Justificativa |
| --- | --- | --- | --- |
| Frontend | HTML, CSS e JavaScript puro (ES2020, sem framework) | — | Sem etapa de build; qualquer integrante consegue ler e alterar; atende a RF07/RNF05 com layout responsivo |
| Servidor web do frontend | Nginx | `nginx:1.27-alpine` | Serve os arquivos estáticos e faz proxy de `/api/` para o backend, evitando CORS |
| Backend | Python + Flask (API REST) | Python 3.12, Flask 3.1.3 | Framework leve, curva de aprendizado baixa, ótimo suporte a testes com pytest |
| Acesso a dados | Flask-SQLAlchemy / SQLAlchemy 2.0 + PyMySQL | ver `requirements.txt` | ORM com SQL parametrizado (evita injeção de SQL) e independência de banco nos testes unitários (SQLite em memória) |
| Servidor de aplicação | Gunicorn | 27.0 | Servidor WSGI de produção dentro do contêiner |
| Banco de dados | MySQL | `mysql:8.4` (LTS) | Definido no Plano; versão LTS com suporte longo |
| Migrações | Scripts SQL versionados em `banco-de-dados/migracoes/` + executor próprio (`flask migrar`) | — | Scripts legíveis pelo DBA, versionados como IC (GYM-DB-001), com controle de checksum para impedir alteração de migração já aplicada (RNF11) |
| Senhas | `werkzeug.security` (scrypt) | — | Hash seguro com sal (RNF01) |
| Autenticação | Token opaco aleatório (Bearer) com hash SHA-256 armazenado na tabela `sessao` | — | Permite logout real (`POST /auth/logout` invalida o token) e revogação imediata ao inativar um usuário (RN05) |
| Testes | pytest; Postman/Newman | ver `requirements-dev.txt` | Definido no Plano (RNF08) |
| CI | GitHub Actions | — | Integrado ao GitHub; executa build, migrações e testes a cada PR (GYM-CI-001) |
| Contêineres | Docker + docker-compose | Compose v2 | Ambiente idêntico para todos os integrantes e para o CI (RNF10) |

## Alternativas consideradas

| Alternativa | Motivo da rejeição |
| --- | --- |
| Django + Django REST Framework | Mais completo, porém mais pesado e com convenções próprias que não agregam ao escopo; o Plano já fixa Flask |
| JWT sem estado | Não permite logout/revogação sem lista de bloqueio adicional; o token em banco resolve RN05 de forma mais simples |
| Alembic para migrações | Gera scripts em Python acoplados ao ORM; scripts SQL puros são mais fáceis de revisar pelo DBA e pelo QA e de auditar na GC |
| React/Vue no frontend | Exigiria etapa de build e dependências Node; desproporcional ao escopo da versão 1.0.0 |
| PostgreSQL | Tecnicamente equivalente, mas o Plano de Projeto fixa MySQL |

## Consequências

**Positivas**

- Ambiente sobe com um único comando (`docker compose up --build`).
- Backend testável sem MySQL (SQLite em memória) nos testes unitários e com MySQL real nos testes de integração e no CI.
- Esquema do banco rastreável: cada migração é um arquivo versionado e registrado na tabela `schema_migracoes`.

**Negativas / riscos**

- Frontend sem framework exige disciplina na organização do JavaScript (mitigado por módulos separados por responsabilidade).
- O executor de migrações é próprio; não há *rollback* automático (mitigado: migrações só avançam; correções são feitas por nova migração).

## Controle de configuração

Este ADR é o IC **GYM-ARQ-004**. Qualquer troca de tecnologia ou de versão principal listada na seção *Decisão* exige atualização deste documento (nova versão) e, após a baseline BL-IMPL-S2, CR aprovada pelo CCB.
