# Native-Speaker Review Package — Nigerian Pidgin (pcm) Priority Set

**Status:** Expert review required before any research-grade claim  
**Principle:** Community validation outranks model confidence (Full-Stack INV-6)

## Review protocol
- ≥2 independent native speakers of Nigerian Pidgin
- Prefer different generational/regional backgrounds
- Disagreement is **preserved**, never majority-collapsed

## Fields per item
`pcm_correct`, `naturalness` (1-5), `intent_preserved`, `register`, `ambiguity_flag`, `notes`

## Acceptance
`pcm_status = community_validated` only when:
1. ≥2 native-speaker reviews exist
2. naturalness ≥4 from both (or documented disagreement retained)
3. intent_preserved = Yes (or Partial with note)

**Worksheet:** `data/review/pcm_priority_review_worksheet.csv`  
**Source:** `data/parallel_prompts_yoruba_priority_with_pcm.jsonl`

Do **not** use unvalidated drafts for camera-ready tables or steering-vector training.
