---
name: Change Request (CR)
about: Solicitação de mudança em Item de Configuração, conforme o PGC (seção 6) e o Modelo de CRF (GYM-GER-005)
title: "CR-NNN: "
labels: change-request
assignees: ''
---

<!--
Template de Change Request — GymManager
IC: GYM-CFG-004 · Versão 1.0.0 · Status: Aprovado (revisão do QA pelo WhatsApp em 17/11/2026; registro na issue #29) · Responsável: Gerente de Projeto/Configuração (Hugo Henry Lemos Carvalho)
Campos conforme o Modelo de CRF (documentos/gerencia/Modelo_CRF.md, GYM-GER-005).

Quando usar: mudança em IC sob baseline, mudança que atravessa vários ICs ou mudança de requisito após a BL-REQ-S1 (PGC, seção 6.3).
Correção simples em IC fora de baseline NÃO precisa de CR: basta uma issue comum e um Pull Request.

O solicitante preenche só a seção A. As demais seções são preenchidas nas etapas seguintes, por quem está indicado.
O número CR-NNN do título é atribuído pelo Gerente na etapa de registro.
-->

## A. Solicitação (solicitante)

- **Data da solicitação:** DD-MM-AAAA
- **Solicitante:** <nome e papel>
- **Tipo:** [ ] Correção  [ ] Melhoria  [ ] Mudança de requisito
- **Prioridade sugerida:** [ ] Baixa  [ ] Média  [ ] Alta  [ ] Urgente
- **ICs afetados (ID e versão atual, conforme a Planilha de ICs):**
  - GYM-XXX-NNN vX.Y.Z
- **Descrição da mudança:**

- **Justificativa (por que mudar; consequência de não mudar):**


## B. Verificação e registro (Gerente)

- **Formulário completo e pertinente ao escopo?** [ ] Sim  [ ] Não — motivo:
- **Número atribuído:** CR-NNN
- **Registrada no Status Accounting em:** DD-MM-AAAA
- **Estado:** Em análise

## C. Análise de custo e impacto (Analista de Requisitos e Dev)

- **ICs afetados confirmados (Planilha de ICs, coluna Dependências, e RTM):**
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
- **Pull Request:** #
- **Resultado do CI:** [ ] Verde  [ ] Vermelho
- **Verificação do QA:** [ ] Aprovada  [ ] Reprovada — observações:
- **Verificado por / data:**

## F. Fechamento (Gerente)

- **Versões resultantes dos ICs:**
  - GYM-XXX-NNN vX.Y.Z → vX.Y.Z
- **Planilha de ICs atualizada:** [ ] Sim
- **RTM atualizada (se houver mudança de requisito):** [ ] Sim  [ ] Não se aplica
- **Status Accounting atualizado:** [ ] Sim
- **Baseline reemitida (se o IC estava em baseline):**
- **Data de fechamento:** DD-MM-AAAA

---

**Estados da CR (PGC 6.4):** Aberta → Em análise → Aprovada / Rejeitada / Adiada → Em implementação → Verificada → Fechada
