# Protocol Application Record – Option B

**Protocol:** HUMAN–AI MULTI-LANE EXPLORATION & REASONING PROTOCOL v2.0  
**Date:** 2026-09-23  
**Decision:** Option B – Prototype First

## What changed
- Schmidt RFP window treated as closed (timeline rejection signal).
- Pivot from grant-centric path to runnable prototype.
- Built only the minimal viable surface: API + mock SAE analysis + Streamlit dashboard + Docker scaffolding.
- Explicit provenance that the SAE layer is currently mocked.

## What was preserved
- D6 / D3 priority and mechanistic framing.
- Layer targeting (bottom language-identity, middle English-reasoning, generation confidence).
- Adversarial robustness testing concept.
- UI structure from earlier design (dashboard / adversarial / steering).
- Docker-first deployment intent.

## What was deferred
- Real GemmaScope 2 / SAELens / nnsight integration.
- Multilingual SAE fine-tuning on African data.
- LOG_ON platform live connection.
- Full empirical evaluation and paper writing.

## Artifact integrity
- All files are real, inspectable text/code.
- No claim of real SAE execution or model loading.
- Health endpoint and provenance field make the mock status visible at all times.

## Next useful actions (for human decision)
1. Run the MVP locally or via Docker and inspect the UI + API.
2. Replace `backend/core.py` mock with real SAELens code when compute and model access are available.
3. Collect small set of real Yoruba/Hausa prompts and measure actual behaviour.
4. Decide whether the next vehicle is paper, new grant, product, or pure research.
