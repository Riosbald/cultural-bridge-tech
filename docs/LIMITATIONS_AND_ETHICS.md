# Limitations & Ethics

**Paper 1 companion – Cultural Bridge / African Cognitive AI**  
**Version:** 0.2 · Camera-ready draft  
**Provenance rule:** Every quantitative claim is tagged `MOCK_SAE`, `PUBLIC_BENCHMARK`, or `PENDING_REAL_SAE`.

## 1. Limitations

### 1.1 Mock vs Real SAE Provenance (Critical)

All D6 / D3 proxy distributions and L2 decision-hint rates reported in Section 3 were produced by the Cultural Bridge **rule-based mock SAE layer** (`CB_SAE_MODE=mock`).

- The mock deliberately assigns high English-backend dominance (D3) and elevated capability-overclaim (D6) to any low-resource language input.
- Consequently the adapter emits `DO_NOT_DEPLOY` for 100% of Yoruba, Hausa and Igbo items in the current 60-item parallel set.
- **These numbers are diagnostic of the pipeline, not of real Gemma-Scope or SAELens features.**
- Real activation collection has been instrumented but not yet executed at scale on GPU. Results from that path will replace every `MOCK_SAE` cell.

We pre-commit to reporting whether real SAE features yield cleaner monosemantic deception / cultural-intent signals than the mock baselines (negative results will be published).

### 1.2 Coverage Gaps

| Gap | Status | Mitigation |
|-----|--------|------------|
| Nigerian Pidgin in parallel prompt set | Schema added; 12 priority items drafted; full set still empty | Native-speaker expansion + Wazobia Eval alignment |
| Real SAE activations | Scaffold only | Oracle / Colab / grant compute path defined |
| Agent-harness ALR on full gold sets | Script exists; cases from public benchmarks | Load full Yor-Sarc + Wazobia sarcasm pairs |
| Native-speaker review of all 60×3 strings | Review CSV + guide published | Community panel required before research-grade claims |

### 1.3 Evaluation Validity

- Diacritic-preserving scoring is required for Yoruba and Igbo.
- Choice-order sensitivity means single-order MC scores are unstable.
- Human pragmatic labels must preserve disagreement (Full-Stack INV-3).

### 1.4 Intervention Claims

PAL (CAA steering) and MÍMO (deterministic gate) are specified and partially instrumented.
End-to-end causal evidence remains **PENDING_REAL_SAE + agent-harness**.

## 2. Ethics

### 2.1 Data & Community Authority
- Parallel prompts and Pidgin expansions are marked `draft_needs_native_review` until corrected by native speakers.
- Community validation outranks model confidence (Full-Stack INV-6).

### 2.2 Dual-Use & Action-Leakage
- All harness runs are offline and use simulated tools only.
- MÍMO gate: `POSSIBLE_MEANING_LOSS` and `INSUFFICIENT` always block; final authorization contains zero LLM sampling.

### 2.3 Representation Harm
- Variance across regional and generational readings is preserved.
- Cultural hallucination is treated as a failure mode to measure and mitigate.

### 2.4 Attribution of Public Resources
- `saaga/yoruba-cultural-reasoning-blindspots`
- `toheebadura/yor-sarc` (arXiv:2602.18964)
- Wazobia Eval (arXiv:2608.21369) / WAZOBIALABS
- `mxronga/yoruba-proverbs-parallel-corpora`
- NaijaSenti, AfriSwitch CMI, AfroBench literature

## 3. Reproducibility Commitments
- Every research run writes a run bundle (config, mode flag, metrics).
- Mock vs real mode is visible in every API response.
- Negative results will be reported.
