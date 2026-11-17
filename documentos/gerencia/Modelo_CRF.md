# Modelo de Change Request Form (CRF) — GymManager

**Sistema web de gerenciamento de treinos de academia**
Disciplina: Gerência de Configuração (6º período) · CENTRO UNIVERSITÁRIO FAMETRO
Professor: Paulo Rodrigo Barbosa Alves

| Campo | Valor |
| --- | --- |
| ID do IC | GYM-GER-005 |
| Caminho | `documentos/gerencia/Modelo_CRF.md` |
| Versão | 0.1.0 |
| Status | Em elaboração |
| Baseline prevista | BL-REQ-S1 (Funcional) |
| Responsável | Hugo Henry Lemos Carvalho (Gerente de Projeto/Configuração) |
| Apoio | QA/Testes |
| Dependência | GYM-GER-003 (Plano de Gerência de Configuração) |
| ICs relacionados | GYM-CFG-004 (template de issue `change-request.md`), GYM-GER-004 (CONTRIBUTING.md), GYM-GER-006 (Status Accounting), GYM-GER-002 (Planilha de ICs) |

## Histórico de revisões

| Versão | Data | Autor | Descrição | CR/Issue |
| --- | --- | --- | --- | --- |
| 0.1.0 | 16-11-2026 | Hugo Henry Lemos Carvalho | Versão inicial do modelo de CRF, conforme as seções 6.1 a 6.5 do PGC | #23 |

---

## 1. Objetivo

Este documento define o formulário usado para solicitar, analisar, decidir e acompanhar uma **Change Request (CR)** no GymManager, conforme a seção 6 do Plano de Gerência de Configuração (GYM-GER-003).

A CR é aberta como **issue no GitHub**, com o template `.github/ISSUE_TEMPLATE/change-request.md` (GYM-CFG-004), que reproduz os campos deste formulário. Este documento é a referência dos campos e de como preenchê-los.

## 2. Quando abrir uma CR

Conforme a seção 6.3 do PGC:

| Situação | Tratamento |
| --- | --- |
| Correção trivial em IC **fora** de baseline | Issue comum + Pull Request, com revisão de outro integrante (**não precisa de CR**) |
| Mudança em IC **sob** baseline | CR completa, decisão do CCB |
| Mudança que atravessa vários módulos ou ICs | CR completa, decisão do CCB |
| Mudança de requisitos após a BL-REQ-S1 | CR completa; atualização de ERS, Casos de Uso, RTM e testes afetados |
| Mudança urgente (falha crítica) | Correção imediata em branch próprio, com aprovação do Gerente; CR registrada em até 1 dia útil |

## 3. Fluxo e estados da CR

### 3.1 Fluxo (PGC, seção 6.1)

| Etapa | O que acontece | Responsável | Seção do formulário |
| --- | --- | --- | --- |
| 1. Submissão | Abertura da issue com o template de CR | Qualquer integrante | A |
| 2. Verificação de validade | Confere se o formulário está completo e se a mudança é pertinente ao escopo | Gerente | B |
| 3. Registro | A CR recebe o número `CR-NNN` e é registrada no Status Accounting (GYM-GER-006) | Gerente | B |
| 4. Análise de custo e impacto | Identifica ICs afetados (coluna Dependências da Planilha de ICs e RTM), esforço e riscos | Analista de Requisitos, Dev Backend e Frontend | C |
| 5. Decisão do CCB | Aprova, rejeita ou adia | CCB | D |
| 6. Implementação e teste | Branch dedicado, PR, CI e testes de verificação | Responsável designado + QA/Testes | E |
| 7. Fechamento | Atualiza versões, Planilha de ICs, RTM e Status Accounting; fecha a issue | Gerente | F |

### 3.2 Estados (PGC, seção 6.4)

`Aberta` → `Em análise` → `Aprovada` / `Rejeitada` / `Adiada` → `Em implementação` → `Verificada` → `Fechada`

| Estado | Significado |
| --- | --- |
| Aberta | Issue criada; aguarda verificação do Gerente |
| Em análise | Registrada como `CR-NNN`; análise de impacto em andamento |
| Aprovada | O CCB aprovou; pode ser implementada |
| Rejeitada | O CCB rejeitou; a issue é fechada com a justificativa |
| Adiada | O CCB adiou; registrar até quando ou sob qual condição |
| Em implementação | Branch e PR abertos |
| Verificada | PR mesclado, CI verde e teste de verificação do QA aprovado |
| Fechada | Versões e registros atualizados; issue fechada |

### 3.3 Numeração

- As CRs são numeradas em sequência: `CR-001`, `CR-002`, e assim por diante. O número é atribuído pelo Gerente na etapa de registro.
- O título da issue fica no formato `CR-NNN: <resumo da mudança>`.
- Branches de implementação seguem o padrão do PGC (seção 4.2), por exemplo `fix/cr-001-<descricao>`; o PR referencia a issue da CR (`Closes #N`).

## 4. Formulário

Copiar o bloco abaixo para a issue (o template `change-request.md` já faz isso automaticamente) e preencher cada seção na etapa correspondente.

```markdown
# CR-NNN: <resumo da mudança>

## A. Solicitação (preenchida pelo solicitante)
- **Data da solicitação:** DD-MM-AAAA
- **Solicitante:** <nome e papel>
- **Tipo:** [ ] Correção  [ ] Melhoria  [ ] Mudança de requisito
- **Prioridade sugerida:** [ ] Baixa  [ ] Média  [ ] Alta  [ ] Urgente
- **ICs afetados (ID e versão atual):**
  - GYM-XXX-NNN vX.Y.Z
- **Descrição da mudança:**
  <o que deve mudar>
- **Justificativa:**
  <por que mudar; consequência de não mudar>

## B. Verificação e registro (Gerente)
- **Formulário completo e pertinente ao escopo?** [ ] Sim  [ ] Não — motivo:
- **Número atribuído:** CR-NNN
- **Registrada no Status Accounting em:** DD-MM-AAAA
- **Estado:** Em análise

## C. Análise de custo e impacto (Analista de Requisitos e Dev)
- **ICs afetados confirmados (pela Planilha de ICs e RTM):**
- **Requisitos afetados (RF/RNF/RN):**
- **Módulos de código afetados:**
- **Testes afetados ou a criar:**
- **Documentos a atualizar:**
- **Esforço estimado:**
- **Impacto no prazo:**
- **Riscos:**

## D. Decisão do CCB
- **Data da reunião:** DD-MM-AAAA
- **Participantes:**
- **Decisão:** [ ] Aprovada  [ ] Rejeitada  [ ] Adiada
- **Justificativa da decisão:**
- **Prioridade final:** [ ] Baixa  [ ] Média  [ ] Alta  [ ] Urgente
- **Responsável pela implementação:**

## E. Implementação e verificação
- **Branch:**
- **Pull Request:** #N
- **Resultado do CI:** [ ] Verde  [ ] Vermelho
- **Verificação do QA:** [ ] Aprovada  [ ] Reprovada — observações:
- **Verificado por / data:**

## F. Fechamento (Gerente)
- **Versões resultantes dos ICs:**
  - GYM-XXX-NNN vX.Y.Z → vX.Y.Z
- **Planilha de ICs atualizada:** [ ] Sim
- **RTM atualizada (se houver mudança de requisito):** [ ] Sim  [ ] Não se aplica
- **Status Accounting atualizado:** [ ] Sim
- **Baseline reemitida (se o IC estava em baseline):** <tag / revisão>
- **Data de fechamento:** DD-MM-AAAA
```

## 5. Orientações de preenchimento

| Campo | Orientação |
| --- | --- |
| Tipo | **Correção:** o sistema ou documento não cumpre o que já foi definido. **Melhoria:** acrescenta ou aprimora algo sem mudar requisito. **Mudança de requisito:** altera o ERS, os Casos de Uso ou a RTM |
| Prioridade | **Baixa:** pode esperar o próximo ciclo. **Média:** entra na próxima entrega semanal. **Alta:** afeta uma função principal ou uma baseline próxima. **Urgente:** falha crítica (segue o tratamento de urgência da seção 2) |
| ICs afetados | Usar os IDs e as versões que constam na Planilha de ICs (GYM-GER-002) no momento da solicitação |
| Análise de impacto | Consultar a coluna **Dependências** da Planilha de ICs e a RTM (GYM-REQ-003) para encontrar todos os ICs atingidos |
| Decisão do CCB | O CCB é formado pelo Gerente (presidente), pela Analista de Requisitos e pelo Dev Backend e Frontend (PGC, seção 6.2). Critérios: consequências de não mudar, benefícios, usuários afetados, custo e ciclo de liberação |
| Versões resultantes | Seguir o versionamento semântico do projeto (MAJOR.MINOR.PATCH), conforme a legenda da Planilha de ICs |

## 6. Controle de configuração deste documento

- Toda alteração é feita por issue e Pull Request e registrada no histórico de revisões.
- Alterações nos campos deste formulário devem ser repetidas no template `change-request.md` (GYM-CFG-004), para que os dois continuem iguais.
- Após a baseline BL-REQ-S1, este modelo só muda mediante CR aprovada pelo CCB.
