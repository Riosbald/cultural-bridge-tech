"""
Cultural Bridge Tech – FastAPI backend (MVP)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from core import run_full_analysis, generate_adversarial_variants

app = FastAPI(
    title="Cultural Bridge Tech API",
    description="Mechanistic Diagnostic Layer – SAE-based D6/D3 detection + L2 decision hints",
    version="0.3.0"
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
        "version": "0.3.0",
        "sae_mode": mode,
        "layer": "Mechanistic Diagnostic & Monitoring",
        "l2_adapter": "enabled",
        "mimo_gate": "enabled",
        "pal_steering": "scaffolded",
        "note": "Every /analyze response includes mimo.gate + l2_decision_hint. PAL uses real Gemma-2 hooks when transformers+torch available, else mock."
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
