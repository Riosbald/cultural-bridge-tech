"""
MÍMO – Representation Gap Challenge + Deterministic Authorization Gate

Pre-execution sidecar:
  1. Run three independent discovery routes on the utterance.
  2. Assign one of five Epistemic States.
  3. Emit a deterministic gate decision with ZERO LLM sampling in the final authorize step.

Epistemic states:
  UNDERSTOOD | CONTEXT_DEPENDENT | CONTESTED | POSSIBLE_MEANING_LOSS | INSUFFICIENT
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Dict, Any, Optional
import re


class EpistemicState(str, Enum):
    UNDERSTOOD = "UNDERSTOOD"
    CONTEXT_DEPENDENT = "CONTEXT_DEPENDENT"
    CONTESTED = "CONTESTED"
    POSSIBLE_MEANING_LOSS = "POSSIBLE_MEANING_LOSS"
    INSUFFICIENT = "INSUFFICIENT"


class GateDecision(str, Enum):
    ALLOW = "ALLOW"
    CLARIFY = "CLARIFY"
    PRESERVE = "PRESERVE"
    BLOCK = "BLOCK"
    ABSTAIN = "ABSTAIN"


@dataclass
class RouteResult:
    route: str
    reading: str
    confidence: float
    flags: List[str]


@dataclass
class MimoVerdict:
    utterance: str
    language: str
    routes: List[RouteResult]
    epistemic_state: EpistemicState
    gate: GateDecision
    rationale: str
    allowed_tools: List[str]


PROVERB_CUES = [
    r"\bproverb\b", r"àwọn", r"kì í", r"a kì í",
    r"ora na-", r"egbe bere", r"nwaanyi",
    r"komai nisan", r"gidan nan", r"kowa ya yi",
]
SARCASM_CUES = [
    r"you don try well well", r"don try", r"well well",
    r"sarcasm", r"contempt",
]
TECHNICAL_CUES = [r"dosage", r"register", r"NAFDAC", r"company law", r"act amendment"]


def route_a_lexical(utterance: str) -> RouteResult:
    return RouteResult(
        route="A_lexical",
        reading="literal_surface",
        confidence=0.7,
        flags=["surface_ok"] if len(utterance.split()) >= 3 else ["too_short"],
    )


def route_b_pragmatic(utterance: str, language: str) -> RouteResult:
    flags = []
    conf = 0.5
    text = utterance.lower()
    if any(re.search(p, text, re.I) for p in PROVERB_CUES):
        flags.append("proverb_pattern")
        conf = 0.85
    if any(re.search(p, text, re.I) for p in SARCASM_CUES):
        flags.append("sarcasm_pattern")
        conf = 0.9
    if language in {"yoruba", "igbo", "hausa", "pcm"} and conf < 0.7:
        flags.append("low_resource_pragmatic_risk")
        conf = max(conf, 0.65)
    reading = "pragmatic_or_figurative" if flags else "no_strong_pragmatic_signal"
    return RouteResult(route="B_pragmatic", reading=reading, confidence=conf, flags=flags)


def route_c_residual(utterance: str) -> RouteResult:
    flags = []
    if len(utterance.strip()) < 5:
        flags.append("insufficient_length")
    if any(re.search(p, utterance, re.I) for p in TECHNICAL_CUES):
        flags.append("tool_param_sensitive")
    return RouteResult(
        route="C_residual",
        reading="edge_check",
        confidence=0.6 if not flags else 0.4,
        flags=flags or ["clean"],
    )


def assign_epistemic_state(routes: List[RouteResult], language: str) -> EpistemicState:
    a, b, c = routes[0], routes[1], routes[2]
    if "insufficient_length" in c.flags:
        return EpistemicState.INSUFFICIENT
    if "sarcasm_pattern" in b.flags or "proverb_pattern" in b.flags:
        if a.reading == "literal_surface" and b.reading.startswith("pragmatic"):
            return EpistemicState.POSSIBLE_MEANING_LOSS
        return EpistemicState.CONTESTED
    if "low_resource_pragmatic_risk" in b.flags:
        return EpistemicState.CONTEXT_DEPENDENT
    if "tool_param_sensitive" in c.flags and language != "english":
        return EpistemicState.CONTEXT_DEPENDENT
    if a.confidence > 0.65 and b.confidence < 0.6:
        return EpistemicState.UNDERSTOOD
    return EpistemicState.CONTEXT_DEPENDENT


def gate_from_state(state: EpistemicState) -> GateDecision:
    return {
        EpistemicState.UNDERSTOOD: GateDecision.ALLOW,
        EpistemicState.CONTEXT_DEPENDENT: GateDecision.CLARIFY,
        EpistemicState.CONTESTED: GateDecision.PRESERVE,
        EpistemicState.POSSIBLE_MEANING_LOSS: GateDecision.BLOCK,
        EpistemicState.INSUFFICIENT: GateDecision.ABSTAIN,
    }[state]


def analyze(utterance: str, language: str = "english", policy_allowlist: Optional[List[str]] = None) -> MimoVerdict:
    routes = [
        route_a_lexical(utterance),
        route_b_pragmatic(utterance, language),
        route_c_residual(utterance),
    ]
    state = assign_epistemic_state(routes, language)
    gate = gate_from_state(state)
    allowed = []
    if gate == GateDecision.ALLOW and policy_allowlist:
        allowed = list(policy_allowlist)
    elif gate == GateDecision.CLARIFY:
        allowed = ["clarify"]
    elif gate in {GateDecision.BLOCK, GateDecision.ABSTAIN, GateDecision.PRESERVE}:
        allowed = ["abstain"]
    rationale = (
        f"Routes A={routes[0].reading}/{routes[0].confidence:.2f}, "
        f"B={routes[1].reading}/{routes[1].confidence:.2f} flags={routes[1].flags}, "
        f"C={routes[2].flags} \u2192 state={state.value} \u2192 gate={gate.value}"
    )
    return MimoVerdict(
        utterance=utterance,
        language=language,
        routes=routes,
        epistemic_state=state,
        gate=gate,
        rationale=rationale,
        allowed_tools=allowed,
    )


def verdict_to_dict(v: MimoVerdict) -> Dict[str, Any]:
    d = asdict(v)
    d["epistemic_state"] = v.epistemic_state.value
    d["gate"] = v.gate.value
    return d


if __name__ == "__main__":
    tests = [
        ("You don try well well.", "pcm"),
        ("A kì í fi ẹyẹlé sọ ilé.", "yoruba"),
        ("Ora na-azu nwa.", "igbo"),
        ("Komai nisan jifa, allah ya kan kawo harshe.", "hausa"),
        ("How do I register a small business in Lagos?", "english"),
    ]
    for utt, lang in tests:
        v = analyze(utt, language=lang, policy_allowlist=["release_payment", "hold_payment", "clarify"])
        print(f"[{lang}] gate={v.gate.value:8} state={v.epistemic_state.value:24} | {utt[:50]}")
