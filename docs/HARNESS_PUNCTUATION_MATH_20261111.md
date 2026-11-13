# Harness — punctuation + mathematical layers, 10 verses (2026-11-11)

**Run:** `.venv/bin/python tools/harness_punctuation_math.py` — deterministic,
no model calls, no GPU. Results JSON: `tools/harness_punctuation_math_results.json`.
**Outcome: 10/10 criteria pass** (after one real bug found and fixed mid-run; see Failures).

Verses (the established 10-verse set, reused so punctuation results sit beside
the grammar results): Mt 4:10, 25:18, 1:1, 3:17, 5:3, 6:26, 19:24, 22:37, 26:26, 27:46.

## Do we have the data to confidently punctuate? — Yes, for Matthew

- The punctuated text of record is already in the repo: SBLGNT via MorphGNT,
  field 3 (as-printed, carries `;` `·` `,` `.` and the ⸀ ⸂ ⸃ apparatus).
  GGSD was discarding it and decoding the clean field 4. That discard, not
  missing data, was the gap.
- Counts verified against the independent punctuation report: whole-Matthew
  `;` = 168 in 143 verses, `·` = 761, `,` = 910, `.` = 753 (PM3 below).
- Golden cases exist: the 143 hand-typed gates in
  `tools/homer/MATTHEW_SEMICOLON_VERSES.md`, Homer/Pindar/oration baselines
  for what is normal.
- Confidence is edition-relative and the output says so: every run now records
  its `text_source` (SBLGNT via MorphGNT, fields named) in `run_meta.json`.

## What was built

| Piece | File | What it does |
|---|---|---|
| Punctuation layer | `punctuation.py` | Token objects: printed form, trailing mark, ⸀/⸂…⸃ apparatus, accent class/position, breathing. Elision is never cadence. Cadence map + mark counts. |
| Math layer | `math_layer.py` | Rules M1–M10 as data, all `status: proposed`. Gate records (head type, καὶ positions, μ-terms, numerals, apparatus, proposed return). `TAKE(Q,u)=(n,r)_u`, r<u — ratio-free. |
| Schema | `schema.py` | Primitives gain `punctuation` (driver-filled) and `mathematical_rules` (proposed only). **An elimination citing a mathematical rule now fails validation.** |
| Driver | `ggsd.py` | Tokenises through the punctuation layer; surfaces still from the clean field (counts unchanged); punctuation block stored per word and restored after the model call; decoding JSON gains `cadence_map`, `mark_counts`, `gates`, `equations`; `--dry-run` prints the cadence map; driver 0.0.3. |
| Report | `report.py` | New "## Cadence & gates" section (deterministic; proposed rules labelled proposed). |

### Audit fixes landed in the same pass

- **A4 (model.py):** the OpenAI branch called OpenAI, then called Ollama and
  kept the Ollama result — paid output discarded. Stray call deleted.
- **A6 (model.py):** Ollama payloads now set `num_ctx: 32768` (word and question calls).
- **A7 (model.py):** question caps 1024 → 2048 tokens (measured answers ran longer).
- **A8 (ggsd.py):** model-error primitives (`[model error …]`) were written as
  completions and skipped on resume. They now carry `_model_error` and
  `_load_completed` refuses them, so a resume retries the word.

## Criteria and results

| # | Criterion | Result |
|---|---|---|
| PM1 | Token invariance: punctuated tokenisation returns exactly the MorphGNT clean-field surfaces, same order and count, all 10 verses | PASS |
| PM2 | Mark counts per verse equal a naive count over the raw printed field, 10/10 | PASS |
| PM3 | Whole-Matthew totals from the new layer: `;`=168, `·`=761, `,`=910, `.`=753 | PASS |
| PM4 | Mt 4:10 fixtures: 0 gates, 3 ano teleiai, ⸀ on Ὕπαγε, Σατανᾶ = perispomeni/final | PASS |
| PM5 | Mt 27:46: ≥2 gates, verse-final gate, last gate return proposed `left-open` | PASS |
| PM6 | Mt 6:26: exactly 1 gate, μ-term μᾶλλον captured | PASS |
| PM7 | `TAKE(100,99)=(1,1)`, `TAKE(1,100)` takes 0 remainder 1, unit 0 rejected | PASS |
| PM8 | All καὶ-equality claims (8 over the 10 verses) carry `status: proposed` — none auto-consented | PASS |
| PM9 | Schema: primitive with punctuation validates; elimination via a mathematical rule is rejected | PASS |
| PM10 | Breathing: Ἰησοῦς tokens read `smooth` | PASS (after fix, below) |

End-to-end check: `ggsd.py --verse "Matthew 27:46" --dry-run` (MorphGNT path)
prints 24 tokens, mark counts, and the cadence map — λέγων· typed `speech_verb`,
both gates at weight Q, final gate on ἐγκατέλιπες — with no model call.
The dry-run directory was removed afterwards; `runs/` untouched otherwise.

## Failures, recorded as datum

1. **PM10 failed on first run.** `accent_profile` matched breathing by the name
   "PSILI", but NFD gives U+0313 COMBINING COMMA ABOVE, so every initial-vowel
   breathing read `none`. Fixed by matching both combining names (comma above =
   smooth, reversed comma above = rough). Re-run: 10/10.
2. **Mt 27:46 gate heads type `untyped`.** ἱνατί is not in the M7 head table
   (the appendix read it as the why/x gate). The layer reports `untyped`
   rather than guessing — correct behaviour, open item: add ἱνατί → `cause`
   to `_head_type` with the operator's consent.
3. **Not done in this pass:** no model runs (GPU stayed cool; the quarantined
   remote run stays quarantined); `tools/matthew_verses.jsonl` still contains
   the 336 duplicated verses found earlier (F4) — the harness reads MorphGNT
   directly and is unaffected, but the rebuild is still owed; gate *return*
   typing beyond `left-open`/`answered-in-scene`/`continues` remains proposed
   and coarse, as designed — refinement is operator-gated, not automated.

## The one-liner

The gate does not mark where Matthew is translated, or Greek, or inspired.
It marks where somebody else is in the room — and now the driver can see it,
count it, and propose on it, without ever being allowed to eliminate by it.
