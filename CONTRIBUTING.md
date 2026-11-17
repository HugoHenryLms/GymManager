# Guia de contribuição — GymManager

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-GER-004 |
| Caminho | `CONTRIBUTING.md` |
| Versão | 0.1.0 |
| Status | Em elaboração |
| Baseline prevista | BL-REQ-S1 (Funcional) |
| Responsável | Hugo Henry Lemos Carvalho (Gerente de Projeto/Configuração) |
| Dependência | GYM-GER-003 (Plano de Gerência de Configuração) |
| ICs relacionados | GYM-GER-005 (Modelo de CRF), GYM-CFG-004 (template `change-request.md`), GYM-GER-002 (Planilha de ICs), GYM-CI-001 (CI) |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.1.0 | 17-11-2026 | Hugo Henry Lemos Carvalho | Versão inicial, conforme as seções 3, 4 e 6 do PGC | #23 |

---

Este guia resume **como contribuir com o repositório** seguindo o Plano de Gerência de Configuração (`documentos/gerencia/Plano_de_Gerencia_de_Configuracao.md`, GYM-GER-003). Em caso de dúvida, o PGC prevalece.

## 1. Fluxo de trabalho

Toda alteração no repositório segue esta ordem:

```
Issue  →  Branch  →  Commit(s)  →  Pull Request  →  Revisão  →  Merge  →  Apagar branch
```

1. **Issue:** abra uma issue descrevendo o que será feito e quais ICs são afetados. Toda alteração precisa estar vinculada a uma issue ou CR (PGC 4.3).
2. **Branch:** crie um branch curto **a partir da `main`** (seção 2).
3. **Commits:** faça commits pequenos, no padrão da seção 3, citando a issue.
4. **Pull Request:** abra o PR para a `main`, com `Closes #N` na descrição (seção 4).
5. **Revisão:** peça a revisão de **outro integrante**. O autor não aprova o próprio PR.
6. **Merge:** só depois da aprovação e com o CI verde. O merge é feito pelo autor do PR ou pelo Gerente.
7. **Apagar o branch** logo após o merge (botão **Delete branch**).

## 2. Branches

- **`main`**: versão estável, protegida. Nada é enviado direto para ela; toda alteração entra por Pull Request aprovado e com CI verde. As baselines são marcadas com *tags* nela.
- **Branches de trabalho**: curtos, criados a partir da `main` e integrados com frequência.

**Nomenclatura:** `<tipo>/<id-do-IC>-<descricao-curta>`, em minúsculas e sem acentos.

| Tipo | Uso | Exemplo |
| --- | --- | --- |
| `feat` | Nova funcionalidade | `feat/gym-src-004-fichas-de-treino` |
| `fix` | Correção | `fix/gym-tst-001-local-do-plano` |
| `docs` | Documentação | `docs/gym-tst-001-plano-de-testes` |
| `test` | Testes | `test/gym-tst-003-testes-alunos` |
| `ci` | Pipeline de CI | `ci/gym-ci-001-atualiza-actions` |
| `chore` | Configuração e manutenção | `chore/gym-cfg-001-002-estrutura-e-ambiente` |

Quando a mudança vier de uma Change Request, use o número da CR: `fix/cr-001-<descricao>`.

> **Atenção:** a edição de arquivos pelo site do GitHub cria branches com nomes automáticos (por exemplo, `usuario-patch-1`). Crie o branch com o nome correto **antes** de editar.

## 3. Commits

Padrão **Conventional Commits**, com a referência da issue ou CR no final:

```
<tipo>: <descrição no imperativo> (#N)
```

Tipos: `feat:`, `fix:`, `docs:`, `test:`, `chore:`, `ci:`.

Exemplos:

```
docs: elabora Plano de Testes v0.1.0 (GYM-TST-001) (#18)
fix: corrige cálculo de carga (#12)
test: adiciona testes de integração do módulo de alunos (#30)
```

- Commits pequenos e atômicos: um assunto por commit.
- **Nunca enviar código que quebre o build.**
- Para documentos, cite o ID do IC e a nova versão na descrição.

## 4. Pull Requests

Todo PR deve (PGC 4.4):

1. Referenciar a issue ou CR na descrição: `Closes #N`.
2. Atualizar a **versão** e o **histórico de revisões** do IC alterado, e a Planilha de ICs quando aplicável.
3. Passar no **CI** (build e testes).
4. Ser aprovado por **ao menos um revisor diferente do autor**.
5. Se o IC estiver **sob baseline**: só ser mesclado com CR aprovada pelo CCB.

**Modelo de descrição:**

```
Closes #N

- GYM-XXX-NNN: <nome do IC> vX.Y.Z → vX.Y.Z
- <o que mudou>
- Revisão: <papel ou nome do revisor>
```

**Antes de pedir a revisão, confira na aba *Files changed*:**

- [ ] Os arquivos estão nas **pastas corretas** (estrutura da seção 3.4 do PGC).
- [ ] Os nomes dos arquivos seguem as convenções da seção 6.
- [ ] A versão e o histórico de revisões do documento foram atualizados.
- [ ] Não há segredos, `.env` ou arquivos temporários no PR.
- [ ] O CI está verde na aba *Checks*.

**Para quem revisa:** aprove pela aba *Files changed* → **Review changes** → **Approve** → **Submit review**. Se algo precisar mudar, use **Request changes** e explique.

## 5. Change Requests

Abra uma **Change Request** (issue com o template **Change Request (CR)**) nos casos abaixo (PGC 6.3):

| Situação | O que fazer |
| --- | --- |
| Correção simples em IC **fora** de baseline | Issue comum + Pull Request (sem CR) |
| Mudança em IC **sob** baseline | CR completa, decisão do CCB |
| Mudança que atravessa vários módulos ou ICs | CR completa, decisão do CCB |
| Mudança de requisito após a BL-REQ-S1 | CR completa; atualizar ERS, Casos de Uso, RTM e testes |
| Falha crítica urgente | Correção imediata com aprovação do Gerente; CR registrada em até 1 dia útil |

O formulário e as instruções de preenchimento estão em `documentos/gerencia/Modelo_CRF.md` (GYM-GER-005). Para abrir: **Issues → New issue → Change Request (CR)**.

## 6. Itens de Configuração e nomes de arquivos

- Todo artefato relevante é um **IC**, com ID `GYM-<TIPO>-<NNN>`, registrado na Planilha de ICs (`documentos/gerencia/Planilha_Controle_de_ICs.xlsx`) **antes** de entrar na `main` (PGC 3.2).
- Documentos têm, no topo, a **tabela de controle do IC** e o **histórico de revisões**.
- Versionamento semântico `MAJOR.MINOR.PATCH`: `0.0.0` = planejado; `0.x.y` = em elaboração; `1.0.0` = primeira versão aprovada e baselinada.
- Pastas em português, minúsculas e sem acentos (`documentos/gerencia/`).
- Arquivos de documentação em `Snake_Case` com inicial maiúscula (`Plano_de_Testes.md`), exceto os convencionais (`README.md`, `CONTRIBUTING.md`, `LICENSE`, `openapi.yaml`).
- Extensões conferidas: `.xlsx`, `.md`, `.yml`.

## 7. Segurança

- **Nunca versionar segredos** (senhas, chaves, tokens). O `.env` está no `.gitignore`; apenas o `.env.example`, sem valores reais, é commitado (RNF03).
- Cada integrante usa a **própria conta** do GitHub, para que autoria, revisões e aprovações fiquem rastreáveis.

## 8. Ambiente e testes

```bash
cp .env.example .env
docker compose up -d --build
```

Para rodar os testes do backend localmente:

```bash
pip install -r codigo-fonte/backend/requirements-dev.txt
PYTHONPATH=codigo-fonte/backend python -m pytest codigo-fonte/testes -v
```

A estratégia de testes está no Plano de Testes (`documentos/testes/Plano_de_Testes.md`, GYM-TST-001). O CI (`.github/workflows/ci.yml`) roda os testes em todo Pull Request.
