# Mechanistic Diagnostic & Monitoring Layer

**Document status:** Integration source of truth for Cultural Bridge ↔ African Cognitive AI  
**Version:** 0.2.0  
**Date:** 2026-09-25

---

## 1. Summary Judgement

Cultural Bridge Tech and the African Cognitive AI Full-Stack are **complementary**.

- Cultural Bridge supplies the missing **white-box, activation-level sensor**.
- The Full-Stack supplies the **knowledge representation, policy, product, and community authority** structures that pure interpretability work needs to become more than a research tool.

**Official positioning:**  
Cultural Bridge Tech is the **Mechanistic Diagnostic & Monitoring Layer** (informally L2.5 / L5.5) inside the African Cognitive AI architecture.

---

## 2. What Each Side Owns

| Concern | Owner |
|---------|-------|
| Structured cultural knowledge (13-dim PAL records, evidence statuses, variance) | African Cognitive AI – L1 |
| Retrieval policy & decision states (`DEPLOY`, `DEPLOY_WITH_CAVEAT`, `ASK_FOR_CONTEXT`, `DO_NOT_DEPLOY`) | African Cognitive AI – L2 |
| Discourse-adaptive generation (DAPF) | African Cognitive AI – L3 |
| Human capability preservation (Cognitive Gym) | African Cognitive AI – L4 |
| Community authority & governance | African Cognitive AI – L6 |
| SAE feature extraction, language-identity scoring, D6/D3 discrepancy metrics, activation evidence | **Cultural Bridge** |
| Parallel prompt instruments for African languages | **Cultural Bridge** (shared evaluation instrument) |

---

## 3. Integration Points

### 3.1 Into L2 (Retrieval & Policy)
High D3 score (English-backend dominance on non-English input) or low language-identity activation → elevate risk → prefer `ASK_FOR_CONTEXT` or `DO_NOT_DEPLOY`.

### 3.2 Into L3 (DAPF)
Before selecting a cultural strategy (`PROVERB`, `STORY_FIRST`, etc.), consult the diagnostic layer. If internal state shows high capability overclaim (D6) or translation-layer collapse (D3), force restraint or surface uncertainty.

### 3.3 Into L4 (Cognitive Gym)
Expose “translation-layer risk” and “capability overclaim risk” as user-facing transparency / friction signals.

### 3.4 Into L5 (Evaluation)
- Language-specificity ranks and D6/D3 proxies become standard instruments.
- Parallel prompt sets (capability / everyday / cultural) are shared evaluation materials.
- Activation evidence supports error taxonomy (especially cultural-compression and epistemic-translation-loss probes).

### 3.5 Into L6 (Governance)
Persistent elevated risk scores on a language or domain can trigger community review or temporary generation restrictions.

---

## 4. Multi-Language Expansion Principle (Hard Rule)

Follow the Full-Stack rule:

> No cross-cultural namespace before the local corpus is stable.  
> Comparative namespaces — one tradition at a time.

Operationalisation:

1. **Depth first**  
   Achieve high-quality Yoruba baselines (language-identity features + early cultural-feature discovery + stable D6/D3 measurements).

2. **Then parallel namespaces**  
   Open Hausa and Igbo as separate, equally rigorous namespaces. Each receives its own provenance, community validation path, and research-ready gate.

3. **Shared tools, separate stores**  
   Activation collection, language-specificity scoring, and D6/D3 proxies are language-agnostic instruments. Knowledge records and community panels remain per-tradition.

4. **Never route by demographic identity**  
   Absolute. Aligns with Full-Stack INV-7.

---

## 5. Immediate Expansion Actions (started 2026-09-25)

- [x] Positioning section added to README
- [x] This merge document created
- [x] L2 interface contract drafted (`docs/L2_INTERFACE_CONTRACT.md`)
- [x] Adapter implementation (`backend/adapter.py`)
- [ ] Native-speaker review of parallel_prompts_v1.jsonl
- [ ] First real (or high-fidelity) activation run on Yoruba subset
- [ ] Hausa / Igbo namespace scaffolding (after Yoruba baseline stability)

---

## 6. Invariants Inherited / Shared

From African Cognitive AI (non-negotiable):

- INV-1 Evidence before interpretation
- INV-4 Refusal is first-class
- INV-5 Provenance is first-class
- INV-6 Human/community validation outranks model confidence
- INV-7 Culture is contextual evidence, not a demographic shortcut

Cultural Bridge specific:

- Mock vs real mode is always explicit in every output
- Negative results (features that do not separate cleanly) are reported, not suppressed
- Activation evidence is retained for audit

---

## 7. Change Log

| Date | Change |
|------|--------|
| 2026-09-25 | Initial positioning and merge document created. Expansion started. |
