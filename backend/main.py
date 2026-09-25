"""
Cultural Bridge Tech – FastAPI backend (MVP)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from core import run_full_analysis, generate_adversarial_variants

app = FastAPI(
    title="Cultural Bridge Tech API",
    description="MVP backend for cross-lingual deception detection (mock SAE layer)",
    version="0.1.0-mvp"
)


class AnalyzeRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4000)
    language: str = Field(default="yoruba", description="Target language: yoruba | hausa | igbo | english")


class AdversarialRequest(BaseModel):
    prompt: str
    language: str = "yoruba"


@app.get("/health")
def health():
    import os
    mode = os.getenv("CB_SAE_MODE", "mock").upper()
    return {
        "status": "ok",
        "version": "0.1.0-mvp",
        "sae_mode": mode,
        "note": "Mock SAE is active by default. Set CB_SAE_MODE=real and implement real_sae_scaffold.py when compute is available."
    }


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    try:
        result = run_full_analysis(req.prompt, req.language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/adversarial")
def adversarial(req: AdversarialRequest):
    try:
        variants = generate_adversarial_variants(req.prompt, req.language)
        return {"variants": variants}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {
        "message": "Cultural Bridge Tech MVP API",
        "docs": "/docs",
        "health": "/health"
    }
