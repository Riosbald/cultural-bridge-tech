# Native-Speaker Review Guide — Parallel Prompt Set v1

**Purpose:** Ensure every Yoruba, Hausa, and Igbo string is natural, correctly toned (where applicable), and culturally appropriate before any research-grade activation or evaluation run.

**Status of current data:** Draft. All African-language fields require native-speaker review.

---

## 1. What to review

For each item in `data/parallel_prompts_v1.jsonl`:

| Field | Check |
|-------|-------|
| **Naturalness** | Does a fluent speaker actually say it this way? |
| **Tone marks / diacritics** | Yoruba: ẹ, ọ, ṣ, vowels with tones. Igbo: ị, ọ, ụ, etc. Hausa: correct orthography. |
| **Register** | Matches the intended context (everyday / formal / cultural). |
| **Cultural accuracy** | Especially for `category: cultural` items (proverbs, festivals, social concepts). |
| **Parallel fidelity** | Does the African-language version ask the same thing as the English version? |

---

## 2. Review workflow

1. Open `data/review/parallel_prompts_review.csv` (or the JSONL).
2. For each row, fill:
   - `yoruba_status`: `ok` | `needs_edit` | `rewrite`
   - `yoruba_corrected`: corrected text (if needed)
   - `hausa_status` / `hausa_corrected`
   - `igbo_status` / `igbo_corrected`
   - `notes`: free text
3. Priority order: **Yoruba first** (depth-first rule), then Hausa, then Igbo.
4. Return the completed file. Corrections will be merged into `parallel_prompts_v1.1.jsonl`.

---

## 3. Priority subset for first review (Yoruba focus)

Review these 12 items first (they form the initial Yoruba activation subset):

- cap_001, cap_002, cap_010, cap_014
- every_001, every_005, every_012
- cult_001, cult_002, cult_011, cult_013, cult_018

---

## 4. Reviewer requirements

- Native or near-native speaker of the language being reviewed.
- Comfortable with standard orthography (including tone marks for Yoruba/Igbo).
- Ideally one reviewer per language; second reviewer optional for cultural items.

---

## 5. What happens after review

- Corrected strings become the canonical research set.
- Only reviewed items are used for the first real activation runs.
- Unreviewed items remain marked `draft` and are excluded from baseline metrics.
