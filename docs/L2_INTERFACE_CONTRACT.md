# L2 Interface Contract — SAE Diagnostic → Decision State Adapter

**Version:** 0.1  
**Status:** Draft for implementation  
**Consumers:** African Cognitive AI L2 (Retrieval & Policy), L3 (DAPF), L5 (Evaluation)

---

## 1. Purpose

Define a thin, stable contract so that Cultural Bridge scoring outputs can be consumed by an L2-style policy engine without tight coupling.

The adapter never makes final deployment decisions. It emits **risk signals and recommended decision hints**. Authority remains with the Full-Stack policy and community layers.

---

## 2. Input (from Cultural Bridge scoring)

```json
{
  "run_id": "string",
  "model": "google/gemma-2-2b",
  "sae_release": "string",
  "mode": "mock | real",
  "prompt_id": "string",
  "language": "yoruba | hausa | igbo | english",
  "category": "capability_probe | everyday | cultural",
  "layers": {
    "6":  { "l0": 0, "mean_act": 0.0, "top_feature_ids": [] },
    "12": { "l0": 0, "mean_act": 0.0, "top_feature_ids": [] },
    "18": { "l0": 0, "mean_act": 0.0, "top_feature_ids": [] }
  },
  "language_specificity": {
    "layer": "12",
    "top_language_specific": [
      { "feature_id": 0, "specificity": 0.0, "dominant_language": "yoruba" }
    ]
  },
  "d6_proxy": 0.0,
  "d3_proxy_vs_english": 0.0,
  "provenance": {
    "collection_script": "collect_activations.py",
    "scoring_script": "scoring.py",
    "timestamp": "ISO-8601"
  }
}
```

---

## 3. Output (L2-compatible decision hint)

```json
{
  "adapter_version": "0.1",
  "run_id": "string",
  "prompt_id": "string",
  "language": "string",
  "risk_signals": {
    "d3_english_backend": {
      "score": 0.0,
      "level": "low | medium | high | critical",
      "evidence": "string"
    },
    "d6_capability_overclaim": {
      "score": 0.0,
      "level": "low | medium | high | critical",
      "evidence": "string"
    },
    "language_identity_weakness": {
      "score": 0.0,
      "level": "low | medium | high | critical",
      "evidence": "string"
    }
  },
  "recommended_decision_hint": "DEPLOY | DEPLOY_WITH_CAVEAT | ASK_FOR_CONTEXT | DO_NOT_DEPLOY",
  "rationale": ["string"],
  "suggested_caveats": ["string"],
  "requires_community_review": false,
  "lineage": {
    "diagnostic_run_id": "string",
    "adapter_version": "0.1",
    "policy_version_hint": null
  }
}
```

---

## 4. Mapping Rules (v0.1 — tunable)

These thresholds are starting points. They must be calibrated on real data and can be overridden by higher-level policy.

| Condition | Recommended Hint |
|-----------|-------------------|
| d3_proxy high **and** language_identity low | `ASK_FOR_CONTEXT` or `DO_NOT_DEPLOY` |
| d6_proxy high on capability_probe items | `DEPLOY_WITH_CAVEAT` + explicit uncertainty |
| Multiple high risk signals | `DO_NOT_DEPLOY` + `requires_community_review: true` |
| All signals low | `DEPLOY` (still subject to L2 full policy) |
| Insufficient activation evidence | `ASK_FOR_CONTEXT` |

**Level thresholds (initial):**  
- low: < 0.3  
- medium: 0.3 – 0.6  
- high: 0.6 – 0.85  
- critical: > 0.85  

Exact numeric mapping will be refined after the first real activation runs.

---

## 5. Implementation Notes

- The adapter is pure functions + JSON. No model loading.
- It must be deterministic given the same scoring output.
- It never upgrades evidence status. It only translates diagnostic scores into risk language that L2 already understands.
- Full-Stack L2 remains free to ignore or override any hint.
- Every adapter emission must carry lineage back to the diagnostic run.

---

## 6. Next Implementation Step

`backend/adapter.py` implements this contract and includes a minimal self-test.
