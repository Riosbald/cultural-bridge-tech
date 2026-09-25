# Cultural Bridge Tech

**Version:** 0.2.0  
**Status:** Mechanistic Diagnostic Layer (MVP + real SAE path)  
**Programme affiliation:** African Cognitive AI / Cultural Bridge Research

---

## Positioning (Integration Source of Truth)

**Cultural Bridge Tech is the Mechanistic Diagnostic & Monitoring Layer** inside the broader African Cognitive AI architecture.

| Full-Stack Layer | Role of Cultural Bridge |
|------------------|-------------------------|
| L2 Retrieval & Policy | Supplies activation-derived risk signals (D3 English-backend dominance, language-identity weakness) that can raise risk → `ASK_FOR_CONTEXT` or `DO_NOT_DEPLOY` |
| L3 DAPF Generation | Pre-generation check: high D6/D3 scores force restraint or explicit uncertainty disclosure |
| L4 Cognitive Gym | Surfaces “translation-layer risk” / “capability overclaim risk” as transparency features |
| L5 Evaluation | Parallel prompts, language-specificity scoring, and D6/D3 proxies become standard instruments alongside T1–T6 and human studies |
| L6 Governance | Persistent high risk scores on a language or domain can trigger community review or temporary restriction |

**What this repository is:**  
A white-box, SAE-based sensor for detecting when models collapse African-language inputs into English-backend reasoning or overclaim competence (D6/D3). It produces language-specificity scores, discrepancy metrics, and activation evidence.

**What this repository is not:**  
A full cultural knowledge base, generation policy engine, or product layer. Those belong to the African Cognitive AI stack (PAL, DAPF, Cognitive Gym, Governance). Cultural Bridge feeds them; it does not replace them.

**Multi-language expansion principle (hard rule):**  
Depth first, then parallel namespaces. Finish high-quality Yoruba baselines (language-identity + early cultural features) before opening Hausa and Igbo as equally rigorous, separate namespaces. Shared diagnostic tools; separate knowledge stores and community validation panels. Never route by demographic identity.

See `docs/MECHANISTIC_DIAGNOSTIC_LAYER.md` for the full merge rationale and `docs/L2_INTERFACE_CONTRACT.md` for the decision-state adapter.

---

## Current Capabilities (v0.2.0)

- Multilingual prompt intake (Yoruba / Hausa / Igbo / English)
- Parallel prompt set v1 (60 items: capability / everyday / cultural)
- Activation collection script for Gemma-2 2B + Gemma Scope SAEs
- Language-specificity scoring (SAE-LAPE style)
- D6 / D3 discrepancy proxies
- Mock SAE analysis path (immediately runnable)
- Real SAE scaffold (`real_sae_scaffold.py`)
- FastAPI + Streamlit + Docker Compose
- L2 decision-hint adapter (`backend/adapter.py`)

## Quick Start

```bash
# Docker
docker compose up --build

# Local
cd backend && pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Separate terminal
cd frontend && pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

- Frontend: http://localhost:8501  
- API docs: http://localhost:8000/docs  

## Real Activation Path (when compute available)

```bash
# Install real dependencies
pip install torch transformer-lens sae-lens einops

# Collect (tiny batch first)
python backend/collect_activations.py \
  --prompts data/parallel_prompts_v1.jsonl \
  --layers 6,12,18 \
  --out data/activations \
  --langs english,yoruba,hausa,igbo

# Score
python backend/scoring.py \
  --activations data/activations/activations.jsonl \
  --out data/scoring
```

## Project Structure

```
cultural-bridge-tech/
├── README.md                          # This file (positioning + quick start)
├── docker-compose.yml
├── backend/
│   ├── main.py                        # FastAPI
│   ├── core.py                        # Mock analysis
│   ├── real_sae_scaffold.py           # Real SAE integration path
│   ├── collect_activations.py         # Activation collection
│   ├── scoring.py                     # Language-specificity + D6/D3
│   ├── adapter.py                     # L2 decision-hint adapter
│   └── requirements.txt
├── frontend/
│   └── app.py                         # Streamlit dashboard
├── data/
│   ├── parallel_prompts_v1.jsonl      # 60-item parallel set
│   └── parallel_prompts.example.jsonl
└── docs/
    ├── MECHANISTIC_DIAGNOSTIC_LAYER.md  # Merge rationale
    ├── L2_INTERFACE_CONTRACT.md         # Decision-state adapter
    └── PROTOCOL_APPLICATION.md
```

## Invariants (aligned with African Cognitive AI)

- Evidence before interpretation. Mock vs real is always explicit.
- Provenance is first-class. Every analysis run carries mode and lineage.
- Refusal / high-risk signals are first-class outputs.
- Human / community validation outranks model-internal scores when they conflict.
- Culture is contextual evidence, not a demographic shortcut.

## License

Apache 2.0 (intended)
