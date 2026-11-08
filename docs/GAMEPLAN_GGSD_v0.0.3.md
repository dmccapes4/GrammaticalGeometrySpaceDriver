# Game Plan — GGSD v0.0.3

**Filed:** 2026-11-06  
**Status:** DRAFT — awaiting operator review before implementation begins  
**Reference implementation:** `docs/MATTHEW_25_18_MANUAL_DECODING.md`  
**Prior quarantined:** `quarantine/v0_0_2/`

---

## Design principle

Grammar is a constraint. The lexical field is a set. The model filters the set
by the constraint in context. The output is the surviving field — not a translation.

The operator's decoding is the reference. If the decoder diverges from it on a
verse the operator has decoded by hand, that divergence is filed for review.

---

## What changes from v0.0.2

| | v0.0.2 | v0.0.3 |
|---|---|---|
| Lemma source | MorphGNT `hint_lemma` | Logeion `/find` only |
| Grammar source | Model inference | Logeion `/find` parses (programmatic) |
| Passes | 1 (forward only) | 3 (forward → backward → full-verse) |
| Model role | Generate grammar + lexical rules | Apply grammar constraint to filter set |
| Verse text source | greekbible.com or MorphGNT | Logeion (verse ref is enough) |

---

## Algorithm

### Phase 0: Source collection (per word, once)

For each word at index `i` in the verse:

**Step 1 — Logeion /find:**
```
GET /find?w={surface_form}
```
Returns: `{lemma, parses: [{case, number, gender, tense, voice, mood, person}, ...]}`.

**Step 1a — Redirect check:**
If `/find` returns fewer than `LOGEION_FIND_MIN_RESULTS = 3` parses OR
the API signals a redirect form (e.g. "Did you mean X?"):
```
GET /find?w={redirect_form}
```
Both results are passed to the model with provenance: "first form returned N parses;
redirect form returned M parses." The model records this as a provenance note in
`word.logeion_note`. It does not pick one silently.

**Step 2 — Logeion /detail:**
```
GET /detail?w={lemma_from_find}
```
Returns: all dictionary entries (`dicos` array) — LSJ, Middle Liddell, Dodson,
Thayer, Strong, etc. Each entry is one witness.

**Step 3 — Lemma set:**
Collect all definitions from all dictionary entries into `lemma_set[]`.
One entry per definition per source. Sources are not collapsed.
The set is complete — nothing is discarded yet.

The grammar parses from `/find` are stored separately as `grammar_parses[]`.
These are the programmatic grammar. The model does not generate grammar.
The model receives grammar as input.

---

### Phase 1: Forward pass (i = 0 → N-1)

For each word `i`:

**Window:** words at indices `[max(0, i-2), i-1, i, i+1, min(N-1, i+2)]`.

**Model call — forward filter:**

Input:
```
lemma_set[i]          — full lexical field for word i
grammar_parses[i]     — programmatic grammar from Logeion /find
window_context        — for each word j in window (j ≠ i):
                          lemma_set[j], grammar_parses[j]
```

Task for the model:
> "Given the grammatical parses for this word and the surrounding words' lexical
>  fields and grammar, filter `lemma_set[i]` to the subset that is grammatically
>  possible in this window. Do not collapse to one meaning. Return the surviving
>  set with the grammar rule that each entry satisfies or violates."

Output: `filtered_forward[i]` — the surviving set + per-entry grammar notes.

---

### Phase 2: Backward pass (i = N-1 → 0)

For each word `i` (in reverse):

**Window:** same ±2, but now `filtered_forward[j]` is available for words after `i`.

**Model call — backward filter:**

Input:
```
filtered_forward[i]    — surviving set from forward pass
grammar_parses[i]
window_context         — for each j in window:
                           filtered_forward[j], grammar_parses[j]
```

Task:
> "Given the backward direction — reasoning from the end of the verse toward
>  the beginning — apply grammar constraints to further filter the set.
>  Record what the backward pass eliminates that the forward pass kept, and why."

Output: `filtered_backward[i]` + `backward_eliminations[i]` (what changed and why).

**Disagreement recording:**
If `filtered_backward[i] ≠ filtered_forward[i]`:
- Flag the word as `pass_disagreement = True`
- Store both sets
- Do not resolve — the disagreement is data

---

### Phase 3: Full-verse pass (i = 0 → N-1 again)

**Input for each word:**
```
filtered_backward[i]   — set after both directional passes
grammar_parses[i]
full_verse_context     — all words' filtered_backward sets + grammar_parses
```

**Task:**
> "Reasoning against the full verse as a unit, apply any remaining grammar constraints
>  that require whole-verse context (e.g. subject-verb agreement across the full
>  clause, case chains that span more than ±2 words). Filter further if warranted.
>  Return `possible_interpretations[i]` — the final field."

Output: `possible_interpretations[i]` — what is grammatically possible for this word
in this verse. This is the product of the decoder. It is a field, not a reading.

---

## Output per word (primitive v0.0.3)

```json
{
  "word": {
    "surface":          "κύριος",
    "letters":          ["κ", "ύ", "ρ", "ι", "ο", "ς"],
    "logeion_note":     "(optional) redirect or sparse note"
  },
  "grammar_parses":     [{"case": "genitive", "number": "singular", "gender": "masculine", ...}],
  "lemma_set":          [{"source_id": "logeion_lsj", "definition": "...", "quotation": "..."}, ...],
  "filtered_forward":   [...],
  "filtered_backward":  [...],
  "pass_disagreement":  false,
  "possible_interpretations": [
    "valid / lawful",
    "bounded and constrained",
    "appropriate / available"
  ],
  "backward_eliminations": [],
  "source_retrievals":  {},
  "verse":              "Matthew 1:1",
  "meta_data":          {}
}
```

---

## Model calls per word

| Call | Purpose | When |
|---|---|---|
| Step 1a redirect (optional) | Provenance of sparse /find result | Only if < 3 parses or redirect |
| Forward filter | Filter lemma_set by grammar in window | Always |
| Backward filter | Filter further from verse end | Always |
| Full-verse filter | Final pass against whole-verse context | Always |

**Minimum:** 3 model calls per word (no redirect).  
**Maximum:** 4 model calls per word (with redirect).

For a verse with N words: 3N to 4N model calls.  
Matthew 1:1 has 9 words → 27–36 model calls.  
Matthew 25:18 has 15 words → 45–60 model calls.

This is expensive compared to v0.0.2's 1 model call per word.
It is correct. A fast wrong answer fills the file and looks finished.

---

## Questions phase (unchanged from v0.0.2)

After the three-pass decode, two questions are asked against the full decoded verse:

1. "What was taken?"
2. "Is it moral?"

The questions are generic enough to apply to any verse. The answers are filed in
`questions.jsonl` with full verse context.

---

## What is NOT in scope for v0.0.3

- Multi-source cross-referencing (v0.0.4): comparing readings across dictionaries
  to identify where sources diverge on the same word
- Operator annotation interface: a way to record the operator's reading against
  the decoder's field
- Divergence detection from reference decoding: automated comparison against
  `docs/MATTHEW_25_18_MANUAL_DECODING.md`

These are the next version. v0.0.3 is: get the three-pass algorithm right with
Logeion-only grammar. No MorphGNT.

---

## Files to write

1. `ggsd.py` — rewrite from scratch (v0.0.3). Three-pass architecture.
2. `sources.py` — keep, minor revision: remove MorphGNT hint_lemma references,
   add redirect detection to `fetch_logeion()`.
3. `schema.py` — revision: add `grammar_parses`, `filtered_forward`,
   `filtered_backward`, `pass_disagreement`, `backward_eliminations` fields.
4. `model.py` — revision: three separate call functions
   (`call_forward_filter`, `call_backward_filter`, `call_fullverse_filter`)
   replacing the single `call_model`.
5. `run_matthew.py` — remove `--morphgnt` argument.
6. `harness_matthew_10.py` — update criteria for v0.0.3 output fields.

---

## Start condition

Write `sources.py` revision first. The source collection (Phase 0) must work
before the pass architecture is built. The redirect detection is the new piece.
Verify against a live Logeion call for a word known to redirect
(e.g. ἓν, which is the numeral form that caused the ἓν/ἐν confusion in v0.0.1).

Then `schema.py`. Then `model.py`. Then `ggsd.py`. Then harness.
