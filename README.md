# Cultural Bridge Tech – Minimal Viable Prototype (MVP)

**Version:** 0.1.1-mvp  
**Date:** 2026-09-23  
**Status:** Runnable MVP (backend live) + real SAE scaffold added  
**Protocol applied:** HUMAN–AI MULTI-LANE v2.0 → Option B (Prototype First) → Implement 1+2

## What this is
A minimal, verifiable prototype of **Cultural Bridge Tech**.

It implements:
- Multilingual prompt intake (Yoruba / Hausa / Igbo / English focus)
- Simulated SAE feature analysis for D6 (capability misrepresentation) and D3 (context / English-backend reasoning)
- Simple adversarial variant generation (code-switch simulation)
- Streamlit dashboard matching the designed UI structure
- FastAPI backend ready for later real GemmaScope / SAELens / nnsight integration

## What this is NOT (important provenance)
- This MVP does **not** run real GemmaScope 2 SAEs or load large models.
- Scores and features are **mock / rule-based** so the system is immediately runnable and testable in constrained environments.
- The architecture, API shape, UI layout, and data contracts are designed so real SAELens + nnsight code can replace the mock layer later without breaking the frontend or Docker setup.

## Quick Start (local, no GPU required)

```bash
cd cultural-bridge-tech

# Option 1 – Docker (recommended)
docker compose up --build

# Option 2 – Local Python
# Backend
cd backend && pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd frontend && pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

- Frontend: http://localhost:8501  
- Backend API docs: http://localhost:8000/docs  

## Project Structure
```
cultural-bridge-tech/
├── README.md
├── docker-compose.yml
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── core.py                 # Analysis + adversarial logic (mock SAE)
│   ├── real_sae_scaffold.py    # Exact integration path for real SAELens/nnsight
│   └── requirements.txt
├── frontend/
│   ├── app.py                  # Streamlit dashboard
│   └── requirements.txt
├── data/                       # Future real activation logs / results
└── docs/
    └── PROTOCOL_APPLICATION.md
```

## Core API Endpoints
- `POST /analyze` – run deception analysis on a prompt + language
- `POST /adversarial` – generate code-switch / cultural variants
- `GET /health` – health check

## Current Runtime Status
- Backend is running on port 8000 (health + /analyze tested).
- SAE mode is currently **MOCK** (explicit in every response and /health).
- Real integration path is documented in `backend/real_sae_scaffold.py`.

## Next Real Steps
1. When GPU + model access is available: implement the functions in `real_sae_scaffold.py` and set `CB_SAE_MODE=real`.
2. Add multilingual fine-tuning / activation collection for African languages.
3. Connect to LOG_ON platform for deployment-style validation.
4. Add reconstruction error modelling and ensemble SAEs.
5. Run empirical tests and decide next vehicle (paper / new grant / product).

## Protocol Reflection (v2.0)
- **Memory recovered**: Prior architecture, Docker intent, UI screens, D6/D3 priority, Track 3 reframe.
- **Rejection treated as data**: Schmidt RFP window closed → pivoted to prototype-first.
- **Change surface**: Built only the minimal runnable path. Did not rebuild the full proposal text.
- **Provenance**: Mock analysis is explicitly labelled. No claim of real SAE execution.

## License
Apache 2.0 (intended)
