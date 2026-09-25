"""
Cultural Bridge Tech – Activation Collection Script (Real Data Path)

Purpose
-------
Collect residual-stream activations from Gemma-2 2B on parallel
English / Yoruba / Hausa / Igbo prompts, encode them with Gemma Scope
SAEs, and save sparse feature activations for language-identity analysis.

Designed to run first on CPU / Oracle ARM (quantized or small batch).
Set USE_GPU=1 when a CUDA device is available.

Dependencies (install when ready for real run):
  pip install torch transformer-lens sae-lens einops
  # optional for speed: bitsandbytes (quantization)

Usage
-----
  python collect_activations.py --prompts data/parallel_prompts.jsonl --layers 6,12,18 --out data/activations/
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import torch

# ---------------------------------------------------------------------------
# Configuration – change these for your environment
# ---------------------------------------------------------------------------
MODEL_NAME = "google/gemma-2-2b"          # or "google/gemma-2-2b-it"
SAE_RELEASE = "gemma-scope-2b-pt-res"     # adjust to exact Gemma Scope release id
DEFAULT_LAYERS = [6, 12, 18]              # early / middle / later residual
DEVICE = "cuda" if os.getenv("USE_GPU") == "1" and torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32


def load_model_and_saes(layers: List[int]):
    """
    Load Gemma-2 2B + selected Gemma Scope SAEs.

    Returns
    -------
    model : HookedTransformer
    saes  : dict[layer -> SAE]
    """
    try:
        from transformer_lens import HookedTransformer
        from sae_lens import SAE
    except ImportError as e:
        raise ImportError(
            "transformer-lens and sae-lens are required for real activation collection.\n"
            "Install with: pip install transformer-lens sae-lens"
        ) from e

    print(f"Loading model {MODEL_NAME} on {DEVICE}...")
    model = HookedTransformer.from_pretrained(
        MODEL_NAME,
        device=DEVICE,
        dtype=DTYPE,
    )
    model.eval()

    saes = {}
    for layer in layers:
        # Exact SAE id depends on the Gemma Scope release naming.
        # Common pattern: blocks.{layer}.hook_resid_post or similar.
        # Adjust sae_id after checking https://huggingface.co/google/gemma-scope
        sae_id = f"blocks.{layer}.hook_resid_post"
        print(f"Loading SAE for layer {layer} ({sae_id})...")
        try:
            sae = SAE.from_pretrained(
                release=SAE_RELEASE,
                sae_id=sae_id,
                device=DEVICE,
            )
            saes[layer] = sae
        except Exception as e:
            print(f"  Warning: could not load SAE for layer {layer}: {e}")
            print("  Continuing without this layer. Check exact release/sae_id on Hugging Face.")

    return model, saes


def load_prompts(path: str) -> List[Dict[str, Any]]:
    """Load parallel prompts. Expected JSONL format per line:
    {
      "id": "ex001",
      "english": "...",
      "yoruba": "...",
      "hausa": "...",
      "igbo": "...",
      "category": "capability_probe" | "cultural" | "everyday" | ...
    }
    """
    prompts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                prompts.append(json.loads(line))
    return prompts


@torch.no_grad()
def collect_for_text(
    model,
    saes: Dict[int, Any],
    text: str,
    language: str,
) -> Dict[str, Any]:
    """Run one text through the model and return SAE feature activations."""
    tokens = model.to_tokens(text, prepend_bos=True)
    _, cache = model.run_with_cache(tokens)

    result = {
        "language": language,
        "text": text,
        "n_tokens": tokens.shape[-1],
        "layers": {},
    }

    for layer, sae in saes.items():
        # Residual stream post layer (adjust hook name if needed)
        hook_name = f"blocks.{layer}.hook_resid_post"
        if hook_name not in cache:
            # fallback common names
            for candidate in [
                f"blocks.{layer}.hook_resid_pre",
                f"blocks.{layer}.hook_resid_mid",
            ]:
                if candidate in cache:
                    hook_name = candidate
                    break

        acts = cache[hook_name]  # [batch, seq, d_model]
        # Encode with SAE – take mean over sequence for a single vector, or keep all
        # For language-identity we often use max or mean pooled features
        feature_acts = sae.encode(acts)  # [batch, seq, d_sae] or similar
        # Pool: max over sequence (common for presence detection)
        if feature_acts.dim() == 3:
            pooled = feature_acts.max(dim=1).values.squeeze(0)  # [d_sae]
        else:
            pooled = feature_acts.squeeze(0)

        # Keep only top-k active features to save space
        topk = torch.topk(pooled, k=min(50, pooled.numel()))
        result["layers"][str(layer)] = {
            "hook": hook_name,
            "top_feature_ids": topk.indices.cpu().tolist(),
            "top_feature_acts": topk.values.cpu().tolist(),
            "l0": (pooled > 0).sum().item(),
            "mean_act": pooled.mean().item(),
        }

    return result


def run_collection(
    prompts_path: str,
    layers: List[int],
    out_dir: str,
    languages: Optional[List[str]] = None,
):
    languages = languages or ["english", "yoruba", "hausa", "igbo"]
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    model, saes = load_model_and_saes(layers)
    if not saes:
        raise RuntimeError("No SAEs loaded. Check SAE_RELEASE and sae_id naming.")

    prompts = load_prompts(prompts_path)
    print(f"Loaded {len(prompts)} prompt groups.")

    all_results = []
    for i, item in enumerate(prompts):
        print(f"[{i+1}/{len(prompts)}] id={item.get('id', i)}")
        group = {"id": item.get("id", str(i)), "category": item.get("category"), "results": {}}

        for lang in languages:
            text = item.get(lang)
            if not text:
                continue
            try:
                res = collect_for_text(model, saes, text, lang)
                group["results"][lang] = res
            except Exception as e:
                print(f"  Error on {lang}: {e}")
                group["results"][lang] = {"error": str(e)}

        all_results.append(group)

        # Incremental save
        with open(out_path / "activations.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(group, ensure_ascii=False) + "\n")

    # Also write a summary
    summary = {
        "model": MODEL_NAME,
        "sae_release": SAE_RELEASE,
        "layers": layers,
        "n_prompts": len(prompts),
        "languages": languages,
        "device": DEVICE,
    }
    with open(out_path / "run_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Done. Results written to {out_path}")
    return all_results


def main():
    parser = argparse.ArgumentParser(description="Collect SAE activations for Cultural Bridge")
    parser.add_argument("--prompts", type=str, required=True, help="Path to parallel JSONL prompts")
    parser.add_argument("--layers", type=str, default="6,12,18", help="Comma-separated layer indices")
    parser.add_argument("--out", type=str, default="data/activations", help="Output directory")
    parser.add_argument("--langs", type=str, default="english,yoruba,hausa,igbo")
    args = parser.parse_args()

    layers = [int(x) for x in args.layers.split(",")]
    languages = [x.strip() for x in args.langs.split(",")]

    run_collection(
        prompts_path=args.prompts,
        layers=layers,
        out_dir=args.out,
        languages=languages,
    )


if __name__ == "__main__":
    main()
