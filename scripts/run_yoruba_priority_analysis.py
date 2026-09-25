#!/usr/bin/env python3
"""
Yoruba-first systematic analysis runner.

Uses the priority subset (12 items) and the current mock (or real) SAE path.
Emits per-item analysis + L2 decision hints.
Depth-first rule: run this before opening Hausa/Igbo research-grade runs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from core import run_full_analysis


def main():
    prompts_path = Path(__file__).resolve().parents[1] / "data" / "parallel_prompts_yoruba_priority.jsonl"
    out_dir = Path(__file__).resolve().parents[1] / "namespaces" / "yoruba" / "runs"
    out_dir.mkdir(parents=True, exist_ok=True)

    items = [json.loads(l) for l in prompts_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"Loaded {len(items)} Yoruba-priority items")

    results = []
    for it in items:
        # Prefer Yoruba text; fall back to English if missing
        text = it.get("yoruba") or it.get("english")
        lang = "yoruba"
        analysis = run_full_analysis(text, language=lang)
        record = {
            "prompt_id": it["id"],
            "category": it["category"],
            "text_used": text,
            "language": lang,
            "analysis": analysis,
        }
        results.append(record)
        hint = analysis.get("l2_decision_hint", {})
        print(f"  {it['id']}: D6={analysis['deception_scores']['D6_capability']:.3f}  "
              f"D3={analysis['deception_scores']['D3_context']:.3f}  "
              f"hint={hint.get('recommended_decision_hint')}")

    out_file = out_dir / "yoruba_priority_mock_run.json"
    out_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out_file}")

    # Summary counts
    from collections import Counter
    hints = Counter(
        r["analysis"].get("l2_decision_hint", {}).get("recommended_decision_hint", "UNKNOWN")
        for r in results
    )
    print("Decision hint distribution:", dict(hints))


if __name__ == "__main__":
    main()
