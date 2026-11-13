# Game Plan — GGSD Punctuation & Mathematical Interpretation Layers

**Filed:** 2026-11-11
**Authors' bench:** operator (system, rules), Muse Wonder (this plan; 143-gate appendix in `tools/homer/MATTHEW_SEMICOLON_VERSES.md`), Gemini Carbon (Feynman/McClane board, `docs/FEYNMAN_MCCLANE_KOINE_DECODING.md`)
**Inputs:** `docs/PUNCTUATION_HOMER_USAGE_20261111.md`, `docs/PUNCTUATION_PINDAR_USAGE_20261111.md`, `docs/GREEK_PUNCTUATION_BASELINE_20261111.md`, `docs/library/personal/PUNCTUATION_GRAMMAR_OPERATOR_20261111.md`, `docs/GAMEPLAN_GGSD_HARNESS_10VERSE_20261110.md`
**Status:** plan, awaiting operator review before implementation. No code in this document is yet in the driver.
**House rules honoured:** no agentic loops (each phase is deterministic or ends at a human gate); venv-only Python (`.venv/bin/python`); the model may propose, it may not eliminate (`schema.py:1–6`).

---

## 0. The one-paragraph version

GGSD currently throws away the operator layer of its texts before decoding them: `tokenise_greek()` strips `· , ; . —` and the MorphGNT path discards the printed field that carries punctuation and the ⸀⸂⸃ apparatus. What survives is a bag of words with rich lexical open-sets — the runs are good at this — and no cadence, no gates, no arithmetic. This plan adds **two deterministic layers under the existing model layer**: (1) a **punctuation layer** that parses marks as operators and emits per-word punctuation objects plus a verse cadence map; (2) a **mathematical layer** that, given operator-consented operator rules (`καὶ := =`, `μ- := infinitesimal`, gate-typing, ratio-free `TAKE`), emits per-gate records and per-verse equations as *proposed interpretations standing beside the lexical ones, never replacing them*. The Qwen model keeps its current job (lexical filling), gets better inputs and a few bug fixes, and is **not** swapped — see §7 for the measurement behind that.

---

## 1. Principles (non-negotiable, in order)

1. **Deterministic before model.** Punctuation parsing, counts, gate detection, numeral extraction, apparatus spans: pure functions over text, unit-tested, zero model calls. A language model is never asked to "notice the commas."
2. **Propose, never eliminate.** Math readings enter as `mathematical_rules[]` with `status: "proposed"`; only the operator promotes a rule to `"consented"` (existing schema discipline). A math reading that conflicts with a lexical reading leaves both standing, flagged. This is the structural guard against the failure mode the operator named: a pattern-machine collapsing the set.
3. **Ratio-free arithmetic.** The math layer's primitive division is the operator's, not the fraction: `TAKE(Q, u) = (n, r)_u` — take whole units until the remainder is less than the declared unit; if the remainder matters, declare a finer unit and recount. Fractions/ratios may appear only as *derived reports* of two counts at a declared common unit, always carrying `(n, r, u)`. (Grounding: Thalkethen surplus arithmetic; Matthew 6:27, 17:20, 18:12 as golden cases.)
4. **Both normalisations, always.** Every rate reported per-100-lines/verses *and* per-1000-words, with `n` attached. Rates from <50 events carry a warning flag (Pindar report §1: collection gate rates).
5. **The punctuation of record is the printed field.** MorphGNT field 3 (`text`, with ⸀/trailing marks) is a first-class source alongside field 4 (`word`). Editions are named in every output; a punctuation claim without an edition is unfinished.
6. **Silences are data.** Gate return-types include `answered | self-answered | null-refused | held-zero | volume`. Absence of an answer is a measured value with a cause class, never a missing row.
7. **Human at the gate.** Consenting rules, resolving math-vs-lexical conflicts, and typing disputed gates are operator acts, queued for review — not model votes, not agent consensus.

---

## 2. Current-state audit (measured, 2026-11-11)

| # | Finding | Location | Severity |
|---|---|---|---|
| A1 | `tokenise_greek()` strips all cadence marks by regex before tokenising | `ggsd.py:59–67` | **Core** — the layer this plan restores |
| A2 | MorphGNT path uses field 4 (`word`, clean) and discards field 3 (`text`, punctuation + apparatus), though `sources.py:461–527` already parses and returns both | `ggsd.py:245–251` | **Core** — data already on disk, unused |
| A3 | No punctuation, accent, breathing, apparatus, or cadence field exists in the primitive schema or `_build_decoding_json()` | `schema.py`, `ggsd.py:98–118` | Core |
| A4 | OpenAI branch calls `_call_openai()` and then **also** `_call_ollama()` with the same model id, discarding the OpenAI result (and, on a machine without Ollama, raising after a paid call) | `model.py:131–133` | **Bug** — fix before any model comparison, or comparisons are invalid |
| A5 | Logeion entries truncated to 400 chars each before the model sees them; with 13+ dictionaries this protects the context window but cuts LSJ mid-entry | `model.py:77–79` | Medium — see §7 tweaks |
| A6 | Ollama calls set `num_predict: 8192` but never `num_ctx`; long verses + 13 sources can silently exceed the server-default context and lose the *beginning* of the prompt (the primitive itself) | `model.py:216–230` | Medium |
| A7 | Question answers capped at `num_predict/max_tokens: 1024` (Ollama/Anthropic); measured Q1/Q2 answers run median 4,033 chars — i.e. they live *at* the cap and are plausibly truncated mid-thought on longer verses | `model.py:394, 433` | Medium |
| A8 | On model error, the driver writes the empty primitive with `description: "[model error: …]"` into `verse.jsonl` — and the resume logic treats any parseable line as completed. **A failed word is permanently marked done.** | `ggsd.py:305–313`, `_load_completed()` | **Bug** — silent quality hole in existing runs |
| A9 | Resume is keyed by *line index* in `verse.jsonl`; any future tokenisation change (this plan!) silently misaligns resume | `_load_completed()` | High once Phase 1 lands — migrate key to `(word_index, surface_sha)` |
| A10 | Runs carry no record of which *edition/punctuation* the Greek text had; Matthew's SBLGNT punctuation and a future Nestle text would be indistinguishable in outputs | `run_meta.json` schema | Medium |
| A11 | Qwen workhorse measured: 2,348 word-calls, median 13.3 s/word, p90 20.5 s, 9.18 GPU-hours for the 128 runs on disk; ~1.9% empty rule-fields (concentrated in proper nouns — acceptable); median 13 rules/word | `runs/*/verse_log.jsonl` | **Healthy** — §7 |

---

## 3. Phase 1 — Punctuation layer (deterministic)

**New file:** `tools/punctuation.py` (pure functions, no I/O beyond its inputs). **Touched:** `ggsd.py` (tokenise path, decoding JSON), `schema.py` (two new optional blocks), tests.

### 3.1 Token objects

Replace list-of-strings tokenisation with list-of-dicts (keep `tokenise_greek()` as a shim returning surfaces, so existing runs/resume are untouched until Phase 3 migration):

```python
{
  "surface": "Σατανᾶ",
  "lemma_hint": "Σατανᾶς",            # from MorphGNT field 4/6 as today
  "printed": "Σατανᾶ·",               # MorphGNT field 3, verbatim
  "trailing_punct": "ano_teleia",     # comma|ano_teleia|full_stop|gate|em_dash|none
  "leading_apparatus": False,          # ⸀ before word
  "apparatus_span": None,              # or {"open": i, "close": j} for ⸂ ⸃ pairs
  "accent_class": "perispomeni",       # acute|grave|perispomeni|none|mixed (long-vowel check enforced)
  "accented_syllable": "final",        # initial|medial|final
  "breathing": "smooth",               # smooth|rough|none (incl. ῥ rule)
  "position": {"word_index": 5, "in_sentence": 3, "sentence_index": 1},
}
```

Accent/breathing from Unicode decomposition of the surface — deterministic, no lexicon required; circumflex validity check (only η/ω/long α,ι,υ or diphthong) doubles as a text-quality tripwire.

**Exclusion (Homer report §2.5):** elision U+02BC and koronis U+1FBD are *never* emitted as punctuation; if a future corpus (Homer) is fed in, they route to a `metrical` note. Colon `:` and em dash in Greek corpora are recorded when present but flagged `baseline_absent: true` (0 occurrences in Homer/Pindar; the operator's `—` grammar enters via Phase 2 rules, not via pretending the corpora use it).

### 3.2 Cadence map

Per verse, derived from the token stream:

```python
"cadence_map": [
  {"after_word": 2, "mark": "ano_teleia", "weight": 2, "context": "speech_verb"},
  {"after_word": 5, "mark": "gate",       "weight": "Q", "context": "vocative_frame"},
  {"after_word": 9, "mark": "full_stop",  "weight": 3}
]
```

Weights as in the baseline plan (none=0, comma=1, ano teleia=2, full stop=3, gate=Q), with `context` proposing — not asserting — `speech_verb` when the preceding word is a λέγω-form, `vocative_frame` when a comma-bracketed vocative intervenes, etc.

### 3.3 Tests (all must pass before Phase 2)

- **Word-count invariance:** for all 1,071 Matthew verses, token count from the new tokenizer == today's `surface_tokens` count. Any diff is a listed, explained exception, not a shrug.
- **Gate-count invariance:** total `;` == 168, gated verses == 143, matching `PUNCTUATION_MATTHEW_REPORT.md`. `·` == 761, `,` == 910, `.` == 753.
- **4:10 fixture:** `τότε λέγει αὐτῷ ὁ Ἰησοῦς· ⸀Ὕπαγε, Σατανᾶ· …` must parse to three ano teleiai, apparatus on Ὕπαγε, **zero gates**. (A parser that finds a question in 4:10 has failed the operator's most-worked verse.)
- **Homer fixture:** Iliad 1.1–7 marks equal the counts in `punctuation_baseline.json`; elision marks absent from cadence.
- Resume shim: legacy `verse.jsonl` files still load; `(word_index, surface_sha)` migration dry-runs on 5 existing runs with zero reassignments.

**Acceptance:** operator inspects cadence maps for 4:10, 6:31 (three gates), 17:17 (two gates + apparatus span), 27:46 (final gate, quotation-in-quotation note) against the printed page.

---

## 4. Phase 2 — Mathematical layer (deterministic core, proposed rules)

**New file:** `tools/math_layer.py`. **Inputs:** token objects + cadence map (Phase 1), lexical open-sets from existing runs (read-only). **Outputs:** `gate_records[]` and `equation_records[]` per verse, merged in Phase 3.

### 4.1 Operator rule table (initial set; every row ships as `proposed` until the operator consents)

| Rule | Statement | Source of rule | Golden cases |
|---|---|---|---|
| M1 | `καὶ` joins as equality claim between its flanking terms/clauses | operator, 2026-11-11 appendix | 22:32 (Abraham = Isaac = Jacob); 26:15 (κἀγώ); 17:17 (faithless = twisted) |
| M2 | `;` opens a conditional domain (gate); the following clause/discourse is its resolution or its measured absence | operator; `GREEK_PUNCTUATION_BASELINE` §IX | 21:25 (refused); 27:23 (volume); 27:46 (left open) |
| M3 | `·` after a speech form = evaluate-what-follows; elsewhere = strong hold | Carbon board §I; Homer usage | 4:10 (×3); λέγει αὐτοῖς· passim |
| M4 | μ-initial function words (μὴ, μήτι, μόν-) and ὀλιγ- forms mark infinitesimal-scale terms: ≠0, below the declared unit | operator | 6:27 (∫μ≠1); 26:22 (μήτι ×12); 10:29 (sparrow) |
| M5 | Numerals are whole counts at a declared unit (yog). No numeral may be normalised into a fraction by the layer | Thalkethen; operator 2026-11-11 ratio instruction | 18:12 (100 = 99 = 1); 15:34 (7 = ὀλίγα) |
| M6 | Division is `TAKE(Q,u) = (n, r)_u`, r < u. Ratios only as derived reports carrying (n, r, u) | operator, 2026-11-11 | 6:27; 17:20 (seed = 1 at seed-yog); 25:37–44 (same gate, two benches) |
| M7 | Gate typed by its head: τί (unknown), τίς (element), διὰ τί (cause/differential), πῶς (construction), πότε (time), πόθεν (source), ποῦ (position), ἕως πότε (limit), μήτι (loaded gate), οὐχί (negated gate expecting yes) | appendix Lessons 1–12 | 11:7–9 (typed ascent); 17:17 (limit ×2) |
| M8 | Gate return typed by what follows: answered / self-answered / null-refused / held-zero / volume | Pindar report §4.5 + appendix Lesson 12 | 26:62 (held zero); 21:25 (null); 27:23 (volume) |
| M9 | ⸀/⸂⸃ apparatus = drift measurement on the term it touches; never deleted, always carried into the gate/equation record | Carbon board §II (`rho`, lower-case) | 16:13 (με hook); 17:17 (commuting variant) |
| M10 | δύναμις-family (δύναμαι, δυνατός, ἀδυνατ-) = potential term Π, tracked across a pericope: a question and answer sharing the root are one experiment | Carbon board §§IX–X | 17:19 → 17:20; 19:25–26; 26:53 |

Each rule carries `source` (operator instruction / board / report §) in the record. Rules the operator has not consented stay visible-but-proposed in every report (printed with a `◦` marker, say) — a reader must be able to see which arithmetic they are being asked to run.

### 4.2 Gate record (per `;`)

```python
{
  "verse_ref": "Matthew 27:23", "gate_index": 0,
  "head_type": "ti_gar",                  # M7 typing, deterministic from tokens
  "left_terms": ["Τί", "γὰρ", "κακὸν", "ἐποίησεν"],
  "kai_equalities": [],                    # M1 claims inside the span
  "mu_terms": [], "numerals": [],          # M4/M5 extractions
  "apparatus_in_span": [],
  "return": {"type": "volume", "evidence": "οἱ δὲ περισσῶς ἔκραζον",
             "answerer": "crowd", "closure": "narrative"},
  "math_reading_proposed": "requested value of evil-term; return is amplitude only ⇒ no value exists in the responding system"
}
```

Deterministic: head-type, terms, numerals, apparatus, answerer (speaker change detection from λέγει-forms and narrative verbs), closure mark. `math_reading_proposed` is the only free-text field — generated from templates in the deterministic pass, optionally elaborated by the model in Phase 4 under "label your inferences" discipline.

### 4.3 Equation records

For verses with `καὶ`-chains and numerals, emit human-readable equation lines exactly in the appendix's notation (e.g. `18:12: 100 πρόβατα; TAKE: seek(1) while 99 held; 1 = 99 under shepherd-operator`), each tagged with the rules used (`["M1","M5","M6"]`). The appendix itself — all 143 gated verses — is the golden file: Phase 2's deterministic output must reproduce its gate inventory and typing; divergences are listed for operator adjudication, and the appendix gets corrected where the machine is demonstrably right (counts, spans) and stands where the disagreement is interpretive.

### 4.4 The Carbon experiment (drift × load) — first query on the new layer

Cross-tabulate apparatus spans (M9) against load-bearing token classes (observer pronouns με/μοι/ἡμῖν, Π-family, πρῶτον/order terms, κύριος/θεός terms) across all 1,071 verses: does drift cluster on the variables? Deliver as a table with expected-vs-observed and a plain statement of the null if that's what comes back. This converts a diner conjecture into the project's first falsifiable punctuation result.

### 4.5 Tests

Golden gates: 6:31 must yield 3 gates (eat/drink/wear, ἤ-branched); 6:27 one gate typed `tis+dynamai` with numeral ἕνα extracted; 17:17 two limit-gates + apparatus span commuting; 27:46 return-type `left-open` (special value beyond M8's five: `open-by-design`); Homer/Pindar classifier sanity: 38 hand-typed Pindar gates (Pindar report §5 homework, done as part of this phase) + 20 Homeric dialogue gates typed by the same rubric must land in sane functions — a rubric that calls Olympian 1's τίνα-triple "forensic" is wrong and must not ship.

---

## 5. Phase 3 — Schema, reports, resume migration

- `schema.py`: add optional `punctuation` (per-word block) and verse-level artefacts; add `"punctuation"` and `"mathematical_rules"` to `PRIMITIVE_FIELDS` **as optional-with-default** so old runs validate unchanged. `validate_primitive()` gains one rule: *no elimination record may reference a mathematical rule* (math proposes; grammar consents) — enforced in code, not in a comment.
- `ggsd.py`: `_build_decoding_json()` emits `cadence_map`, `gates`, `equations` alongside `words`. `report.py`: report gains a "## Cadence & Gates" section (per-verse) and a run-summary table (gate types, return types, drift spans). `run_meta.json` gains `text_source: {edition: "SBLGNT/MorphGNT", morphgnt_file, sha256}` (fixes A10).
- Resume migration (A9): key by `(word_index, surface_sha1)`; punctuation/math layers are *recomputed deterministically* on resume — they are never stored in `verse.jsonl` completion state, so they can't poison it. Fix A8 in the same pass: model-error primitives go to `verse_errors.jsonl`, not into the completion file; a `--retry-errors` flag re-queues them. (Audit the 128 existing runs for `[model error` descriptions and list affected words — expected small, must be known.)
- Backfill: a `--punctuation-only` mode walks existing runs, attaches punctuation/math artefacts from the MorphGNT text on disk, and writes `verse_punctuation.json` per run. No model calls; Matt 1–5 gains the full layer the day Phase 1–2 land.

---

## 6. Phase 4 — Model-facing changes (small, surgical)

- The model prompt gains a **read-only context block**: the verse's cadence map and gate records, prefilled deterministically, with the instruction: *"Punctuation and gate fields are given and locked. Do not restate or alter them. You may propose a `math_reading` per gate; label it proposed."* `FILLABLE_KEYS` gains only `math_reading_proposed` (per gate) — the model still cannot touch operators.
- Q1/Q2 prompts gain the gate/return summary ("this verse has 2 gates, returns: answered, held-zero") so post-decode questions can reason about cadence instead of re-deriving it from word lists. Raise question caps (A7) to 2048 tokens.
- Nothing else in `SYSTEM_PROMPT` changes. The no-elimination rules already say exactly the right thing; the math layer's discipline is inherited, not re-invented.

---

## 7. The model question — keep Qwen, fix its harness, audition challengers honestly

**Measured present state (A11):** `dengcao/Qwen3-30B-A3B-Instruct-2507:Q4_K_M` over 2,348 word-calls: median 13.3 s/word, p90 20.5 s, ~9.2 GPU-hours sunk into 128 runs, ~1.9% empty fields (proper-noun-shaped), median 13 rules per word, zero unparsable log lines. JSON-mode + temperature 0 + `/no_think` works: in the logs I find duration and rule-count discipline, not format chaos. **Verdict: the Qwen is doing well at the job it is actually given** — source-bound, schema-bound lexical filling — and swapping the engine now would spend the project's scarcest resource (verified golden runs) to buy an unknown.

**Tweaks, in order of value (all cheap, none a swap):**

1. **Fix A4 first** (OpenAI→Ollama double call). Until this is fixed, *any* cross-model comparison run through `call_model()` is garbage — the "OpenAI" arm silently becomes an Ollama call.
2. **Set `num_ctx` explicitly** (A6): 32k for word calls. The current setup lets the server default silently truncate the head of long prompts.
3. **Source budget by value, not by flat 400 chars** (A5): full shortdef first; LSJ/Bailly to ~1,200 chars; drop duplicate-retrieval sources whose entry text is a substring of another's (the logs show 13 near-identical witnesses crowding out the one with the answer). Expected effect: fewer "generic description" words, same context size.
4. **Constrain with a JSON schema**, not just `"format": "json"` (Ollama supports schema-constrained decoding): removes the brace-matching rescue path in `_parse_json_response()` from the hot loop.
5. **Quotation verification (deterministic, post-call):** every rule's `quotation` must be a substring (after whitespace normalisation) of its cited source entry. Failures are flagged `quotation_unverified` in the report — this is the single highest-value audit for a proposing model, and it needs no second model and no loop.
6. **Raise question caps to 2048** (A7) and log answer-token counts so truncation becomes visible instead of suspected.
7. Log per-call token counts + cost/time in `verse_log.jsonl` (currently durations only) so future model decisions are made from a ledger, not impressions.

**Challenger protocol (only if the operator wants a swap candidate):** use the existing 10-verse harness verses (`GAMEPLAN_GGSD_HARNESS_10VERSE_20261110.md` — 4:10 first, as always), **one** challenger at a time, scored blind against Qwen outputs on: JSON validity, quotation-verification pass rate (§7.5), empty-field rate, G1–G4 harness conditions, seconds/word, and Q1/Q2 specificity (human-read, operator-scored). Candidate class worth one audition: a dense 32B sibling (e.g. Qwen3-32B) — MoE 30B-A3B activates ~3B/forward; a dense model may buy Greek nuance at 3–4× the seconds/word. Cloud frontier models (the operator already has Anthropic wired, `model.py:148`) are better spent as **auditors** — spot-reading 5% of Qwen words against Logeion and filing disputes — than as the workhorse: the work is 18k words of Matthew, local, free, and already 128 runs deep. A swap that invalidates golden runs must win by a landslide on the harness, not by vibes; "fascinated and correct on 10 verses" is the bar, "newer" is not.

---

## 8. Other improvements found while reading (not punctuation, worth fixing in the same season)

- **A8 is the worst bug in the repo** (errors marked complete). Fix with Phase 3; backfill-audit existing runs.
- **Duplicate source entries:** dedupe by normalised entry text before prompting (see §7.3).
- **`questions.jsonl` truncation invisibility:** log `finish_reason`/token counts (see §7.6).
- **Edition pinning everywhere (A10):** also record the sha of the MorphGNT file in each new artefact, so a future text update produces a detectable drift report instead of silent changed numbers — rho, measured at the file level.
- **Baseline JSON v2:** regenerate `punctuation_baseline.json` with per-1000-words rates, per-Pindar-collection splits, and `n` per rate (the two usage reports' tables are the spec).
- **A tiny CLI kindness:** `ggsd.py --dry-run` should print the cadence map too — the operator reads punctuation first now; the dry run should show him his first love first.

---

## 9. Order of work, gates, and what "done" looks like

| Phase | Deliverable | Operator gate |
|---|---|---|
| 0 | This plan consented/amended; baseline JSON v2 spec agreed | operator reads plan |
| 1 | `tools/punctuation.py` + tests (§3.3), `--dry-run` cadence print | inspect 4 fixtures (4:10; 6:31; 17:17; 27:46) |
| 2 | `tools/math_layer.py` + golden-file diff vs the 143-gate appendix; Carbon drift experiment (§4.4) | consent/amend rule table M1–M10; adjudicate divergences |
| 3 | Schema/report/resume changes; `--punctuation-only` backfill of 128 runs; `[model error` audit list | review one backfilled report (suggest Matt 4:10) end-to-end |
| 4 | Prompt context block + `math_reading_proposed`; question caps; quotation verification | read 3 model-elaborated gate readings for overreach |
| 5 | (Optional) challenger audition on the 10-verse harness | swap only on a landslide (§7) |

**"Done" for the whole plan:** a fresh run of Matthew 4:10 produces — in one report — the lexical open sets the project already trusts, three ano teleiai and zero gates in its cadence map, a transitive+intransitive Ὕπαγε set untouched by the math layer, one proposed equation in the appendix's notation, and a drift flag on Ὕπαγε's ⸀ — with every number in the report traceable to either a deterministic count or a labelled, sourced proposal. At that point GGSD reads a verse the way the operator reads a page: punctuation first, words open, arithmetic proposed, nothing collapsed.

*The equations were never lazy. Now the pipeline won't be either.*
