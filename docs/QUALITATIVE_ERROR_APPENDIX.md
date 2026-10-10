# Appendix A — Qualitative Error Analysis (Grounded in Public Benchmarks)

## A.1 Generative Collapse — Yoruba Proverbs
**Source:** `saaga/yoruba-cultural-reasoning-blindspots` (Hugging Face)

| Field | Content |
|-------|---------|
| **Input** | *A kì í fi ẹyẹlé sọ ilé.* |
| **Gold pragmatic intent** | Do not entrust security or heavy responsibilities to someone with a weak or flighty character. |
| **Observed model behaviour** | Collapses into Western-analogue or literal rendering. |
| **Failure type** | Generative Collapse + Cultural Hallucination |

## A.2 Sarcasm — Yoruba
**Source:** Yor-Sarc (`toheebadura/yor-sarc`, arXiv:2602.18964) — 436 instances, Fleiss' κ = 0.766.

## A.3 Action-Leakage — Nigerian Pidgin
**Source:** Wazobia Eval (arXiv:2608.21369)

| | Context A | Context B |
|---|-----------|-----------|
| **Utterance** | *You don try well well.* | *You don try well well.* |
| **Situation** | Student first in family to graduate | Mechanic damaged vehicle |
| **Gold intent** | Celebration / pride | Sarcasm / contempt |
| **Correct action** | reward | hold payment / dispute |

## A.4 Hausa & Igbo
Public research proverbs used as ALR cases (see `data/external_benchmark_instances.json`).

## A.5 Research Direction Summary
| Failure mode | Primary public resource | Cultural Bridge instrument |
|--------------|-------------------------|----------------------------|
| Generative Collapse | saaga blindspots | PAL CAA + pragmatic accuracy |
| Yoruba sarcasm | Yor-Sarc | MÍMO Route B + ALR harness |
| Pidgin pragmatic | Wazobia Eval | ALR harness |
| Token / orthography tax | AfriSwitch CMI, fertility studies | Fertility table + diacritic ablation |
