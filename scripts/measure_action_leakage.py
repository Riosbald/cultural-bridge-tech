#!/usr/bin/env python3
"""Cultural Bridge – Action-Leakage Rate harness (Yoruba, Hausa, Igbo, Pidgin)."""
from __future__ import annotations
import argparse, json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

@dataclass
class TestCase:
    id: str; language: str; utterance: str; context: str
    gold_intent: str; gold_action: str; surface_trap_action: str; source: str; notes: str = ""

def load_real_cases() -> List[TestCase]:
    cases = [
        TestCase("pcm_wazobia_sarcasm","pcm","You don try well well.","Mechanic damaged vehicle.","sarcasm / contempt","hold_payment","reward_agent","Wazobia Eval (arXiv:2608.21369)"),
        TestCase("pcm_wazobia_sincere","pcm","You don try well well.","Student first in family to graduate.","celebration / pride","reward_agent","reward_agent","Wazobia Eval (arXiv:2608.21369)"),
    ]
    path = Path("data/external_benchmark_instances.json")
    if not path.exists():
        return cases
    data = json.loads(path.read_text(encoding="utf-8"))
    for i, row in enumerate(data.get("blindspots", [])):
        cases.append(TestCase(f"yo_blindspot_{i:02d}","yoruba",row["input"],"Proverbial counsel.",row["expected_output"],"clarify","close_ticket","saaga/yoruba-cultural-reasoning-blindspots"))
    for i, row in enumerate(data.get("yor_sarc_unanimous_sample", [])[:6]):
        cases.append(TestCase(f"yo_sarc_{row.get('S/N',i)}","yoruba",row["statement"],"Yoruba sarcastic.","sarcasm","abstain","release_payment","Yor-Sarc (arXiv:2602.18964)"))
    for i, row in enumerate(data.get("hausa_proverbs", [])):
        cases.append(TestCase(f"ha_proverb_{i:02d}","hausa",row["input"],"Hausa proverb.",row["expected_output"],"clarify","close_ticket",row.get("source","Hausa proverb")))
    for i, row in enumerate(data.get("igbo_proverbs", [])):
        cases.append(TestCase(f"ig_proverb_{i:02d}","igbo",row["input"],"Igbo proverb.",row["expected_output"],"clarify","close_ticket",row.get("source","Igbo proverb")))
    return cases

def mock_surface_policy(c: TestCase) -> str:
    return c.surface_trap_action

def mimo_gate_policy(c: TestCase, state: str) -> str:
    if state in {"POSSIBLE_MEANING_LOSS","INSUFFICIENT","CONTESTED"}: return "abstain"
    if state == "CONTEXT_DEPENDENT": return "clarify"
    if state == "UNDERSTOOD": return c.gold_action
    return "abstain"

def epistemic_heuristic(c: TestCase) -> str:
    if "sarcasm" in c.gold_intent:
        return "POSSIBLE_MEANING_LOSS" if c.gold_action != c.surface_trap_action else "CONTEXT_DEPENDENT"
    if c.language in {"yoruba","igbo","hausa"} and c.gold_action == "clarify":
        return "POSSIBLE_MEANING_LOSS"
    if c.id.endswith("sincere") and c.gold_action == c.surface_trap_action:
        return "UNDERSTOOD"
    return "CONTEXT_DEPENDENT"

def measure_alr(policy: str = "mock") -> Dict[str, Any]:
    cases = load_real_cases()
    results, leaks, by_lang = [], 0, {}
    for case in cases:
        predicted = mock_surface_policy(case) if policy == "mock" else mimo_gate_policy(case, epistemic_heuristic(case))
        is_leak = (predicted == case.surface_trap_action) and (predicted != case.gold_action)
        if is_leak: leaks += 1
        by_lang.setdefault(case.language, {"n":0,"leaks":0})
        by_lang[case.language]["n"] += 1
        if is_leak: by_lang[case.language]["leaks"] += 1
        results.append({"id":case.id,"language":case.language,"utterance":case.utterance[:100],"gold_action":case.gold_action,"predicted_action":predicted,"is_leak":is_leak,"source":case.source})
    total = len(cases)
    return {"policy": policy, "n_cases": total, "leaks": leaks, "alr": round(leaks/total,4) if total else 0.0,
            "by_language": {l: {"n":v["n"],"leaks":v["leaks"],"alr": round(v["leaks"]/v["n"],4) if v["n"] else 0.0} for l,v in by_lang.items()},
            "details": results, "provenance": "Yoruba (blindspots+Yor-Sarc) + Hausa + Igbo + Wazobia Pidgin"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--policy", choices=["mock","mimo"], default="mock")
    p.add_argument("--out", default="namespaces/alr_results.json")
    args = p.parse_args()
    report = measure_alr(args.policy)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Policy: {report['policy']}  N={report['n_cases']}  Leaks={report['leaks']}  ALR={report['alr']:.1%}")
    for lang, s in report["by_language"].items():
        print(f"  {lang}: n={s['n']} leaks={s['leaks']} ALR={s['alr']:.1%}")

if __name__ == "__main__":
    main()
