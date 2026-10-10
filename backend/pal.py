"""
PAL – Proverbial Activation Layer (CAA)
Contrastive Activation Addition for cultural-intent steering.
Real path: google/gemma-2-2b residual hooks when CB_PAL_REAL=1 and torch available.
Fallback: deterministic mock (dim 2304 = Gemma-2-2b residual width).
"""
from __future__ import annotations
import json, os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
import numpy as np

_HAS_TORCH = False
_MODEL = None
_TOKENIZER = None
_MODEL_NAME = os.getenv("CB_PAL_MODEL", "google/gemma-2-2b")
try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    _HAS_TORCH = True
except ImportError:
    torch = None

@dataclass
class ContrastivePair:
    literal: str
    pragmatic: str
    language: str
    source: str = ""

@dataclass
class SteeringVector:
    vector: np.ndarray
    layer: int
    language: str
    n_pairs: int
    provenance: str
    model_name: str = "mock"
    def to_serializable(self) -> Dict[str, Any]:
        return {"layer": self.layer, "language": self.language, "n_pairs": self.n_pairs,
                "provenance": self.provenance, "model_name": self.model_name,
                "dim": int(self.vector.shape[0]), "norm": float(np.linalg.norm(self.vector))}

def build_contrastive_pairs_from_proverbs(proverbs: List[Dict[str, str]], language: str) -> List[ContrastivePair]:
    pairs = []
    for p in proverbs:
        surface = p.get("input") or p.get("utterance") or ""
        gold = p.get("expected_output") or p.get("gold_intent") or ""
        if not surface or not gold:
            continue
        pairs.append(ContrastivePair(
            literal=f"Translate literally, word for word, with no cultural interpretation: {surface}",
            pragmatic=f"Explain the cultural and pragmatic meaning and the intended advice of this expression: {surface}",
            language=language, source=p.get("source", ""),
        ))
    return pairs

def _load_model():
    global _MODEL, _TOKENIZER
    if not _HAS_TORCH:
        return None, None
    if _MODEL is not None:
        return _MODEL, _TOKENIZER
    try:
        _TOKENIZER = AutoTokenizer.from_pretrained(_MODEL_NAME)
        _MODEL = AutoModelForCausalLM.from_pretrained(
            _MODEL_NAME,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
        )
        _MODEL.eval()
        return _MODEL, _TOKENIZER
    except Exception as e:
        print(f"[PAL] Real model load failed ({e}); mock fallback.")
        return None, None

def get_activations_mock(text: str, layer: int = 16, d_model: int = 2304) -> np.ndarray:
    rng = np.random.RandomState(abs(hash(text + str(layer))) % (2**32))
    return rng.randn(d_model).astype(np.float32)

def get_activations_real(text: str, layer: int = 16, d_model: int = 2304) -> np.ndarray:
    model, tokenizer = _load_model()
    if model is None or tokenizer is None:
        return get_activations_mock(text, layer=layer, d_model=d_model)
    device = next(model.parameters()).device
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256).to(device)
    captured = {}
    def hook_fn(module, inp, out):
        captured["act"] = out.detach()
    handle = model.model.layers[layer].register_forward_hook(hook_fn)
    with torch.no_grad():
        _ = model(**inputs)
    handle.remove()
    return captured["act"][0].mean(dim=0).float().cpu().numpy().astype(np.float32)

def get_activations(text: str, layer: int = 16, d_model: int = 2304) -> np.ndarray:
    if _HAS_TORCH and os.getenv("CB_PAL_REAL", "0") == "1":
        return get_activations_real(text, layer=layer, d_model=d_model)
    return get_activations_mock(text, layer=layer, d_model=d_model)

def compute_caa_vector(pairs: List[ContrastivePair], layer: int = 16, get_acts: Optional[Callable] = None) -> SteeringVector:
    if not pairs:
        raise ValueError("Need at least one contrastive pair")
    get_acts = get_acts or get_activations
    diffs = [get_acts(p.pragmatic, layer=layer) - get_acts(p.literal, layer=layer) for p in pairs]
    v = np.mean(diffs, axis=0)
    v = v / (np.linalg.norm(v) + 1e-8)
    real = _HAS_TORCH and os.getenv("CB_PAL_REAL", "0") == "1"
    return SteeringVector(vector=v, layer=layer, language=pairs[0].language, n_pairs=len(pairs),
                          provenance="CAA real Gemma-2 residual" if real else "CAA mock residual (set CB_PAL_REAL=1 for real hooks)",
                          model_name=_MODEL_NAME if real else "mock")

def apply_steering(residual: np.ndarray, steering: SteeringVector, coefficient: float = 1.0) -> np.ndarray:
    return residual + coefficient * steering.vector

def recompute_all_language_vectors(layer: int = 16, out_dir: str = "namespaces/pal_vectors") -> Dict[str, Any]:
    path = Path("data/external_benchmark_instances.json")
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    lang_sources = {"yoruba": data.get("blindspots", []), "hausa": data.get("hausa_proverbs", []), "igbo": data.get("igbo_proverbs", [])}
    summary = {}
    for lang, rows in lang_sources.items():
        if not rows:
            summary[lang] = {"status": "no_data"}; continue
        proverbs = [{"input": r.get("input") or r.get("utterance", ""), "expected_output": r.get("expected_output") or r.get("gold_intent", ""), "source": r.get("source", "")} for r in rows]
        pairs = build_contrastive_pairs_from_proverbs(proverbs, language=lang)
        if not pairs:
            summary[lang] = {"status": "no_pairs"}; continue
        vec = compute_caa_vector(pairs, layer=layer)
        np.save(out / f"pal_{lang}_layer{layer}.npy", vec.vector)
        meta = vec.to_serializable()
        (out / f"pal_{lang}_layer{layer}.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        summary[lang] = {"status": "ok", **meta}
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary

if __name__ == "__main__":
    print(f"torch available: {_HAS_TORCH}; CB_PAL_REAL={os.getenv('CB_PAL_REAL', '0')}")
    print(json.dumps(recompute_all_language_vectors(layer=16), indent=2))
