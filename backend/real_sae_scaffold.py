"""
Cultural Bridge Tech – Real SAE Integration Scaffold

This file shows the exact structure for replacing the mock analysis
with real GemmaScope / SAELens / nnsight code.

It is intentionally NOT imported by default so the MVP remains
lightweight and runnable without large model downloads.

When you have GPU + model access:

1. Install:
   pip install sae-lens nnsight transformer-lens torch

2. Set environment variable:
   export CB_SAE_MODE=real

3. Implement the functions below using the real libraries.
4. Update core.py to call these functions when CB_SAE_MODE=real.

Key references:
- GemmaScope 2 (DeepMind)
- SAELens documentation
- nnsight for activation extraction
- Wendler et al., Zhao et al., Tang et al. for layer targeting
"""

from typing import Dict, Any, List, Optional
import os

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SAE_MODE = os.getenv("CB_SAE_MODE", "mock").lower()  # "mock" | "real"

# Example model / SAE identifiers (update when real weights are available)
DEFAULT_MODEL = "google/gemma-2-2b"          # smaller for testing
DEFAULT_SAE_RELEASE = "gemma-scope-2b-pt-res-canonical"  # placeholder


def extract_activations(model, prompt: str, layers: List[str]) -> Dict[str, Any]:
    """
    Real implementation sketch using nnsight:

    from nnsight import LanguageModel
    model = LanguageModel(DEFAULT_MODEL, device_map="auto")

    with model.trace(prompt) as tracer:
        # Capture residual stream or specific layer outputs
        acts = {}
        for layer_name in layers:
            # Example: model.model.layers[i].output
            acts[layer_name] = ... .save()
    return acts
    """
    raise NotImplementedError("Real activation extraction not yet wired. See docstring.")


def load_sae(release: str = DEFAULT_SAE_RELEASE, layer: int = 12):
    """
    Real implementation sketch using SAELens:

    from sae_lens import SAE
    sae = SAE.from_pretrained(
        release=release,
        sae_id=f"blocks.{layer}.hook_resid_post",
        device="cuda"
    )
    return sae
    """
    raise NotImplementedError("Real SAE loading not yet wired. See docstring.")


def real_sae_analysis(prompt: str, language: str = "yoruba") -> Dict[str, Any]:
    """
    Full real analysis pipeline (to be implemented).

    Steps:
    1. Load model + SAEs for bottom / middle / generation target layers.
    2. Extract activations on the prompt (and optionally on translated versions).
    3. Encode with SAEs → sparse features.
    4. Identify features corresponding to:
       - language-identity / low-resource capability (bottom)
       - English-token / English-reasoning dominance (middle)
       - output confidence / capability claims (generation)
    5. Compute D6 / D3 style discrepancy scores.
    6. Return same schema as mock_sae_analysis so the API & frontend stay unchanged.
    """
    raise NotImplementedError(
        "Real SAE analysis is scaffolded but not implemented in this environment. "
        "Replace this function body with SAELens + nnsight code when compute is available."
    )


def get_analysis_fn():
    """Factory that returns the correct analysis function based on mode."""
    if SAE_MODE == "real":
        return real_sae_analysis
    from core import mock_sae_analysis
    return mock_sae_analysis
