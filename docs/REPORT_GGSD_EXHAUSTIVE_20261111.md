# GGSD — Exhaustive Report: the instrument, punctuation, grammar, Maththew, Koine, and the Aramaic question

**Date:** 2026-11-11 · **Scope:** everything the GrammaticalGeometrySpaceDriver
project has established, proposed, broken, and left open, through the
0.0.3 punctuation/math pass and the live hilarious_marcupial run.
**Epistemic key, used throughout:** *Measured* = counted/read directly, source
named. *Modelled* = consensus picture through lenses, labelled as such.
*His* = the operator's explicit deposit, recorded, not endorsed or dismissed.
Rates always carry their normalisation and n. Failures are datum.

Primary sources: `docs/` of this project (25 documents), `tools/homer/`,
`runs/` (local, 131 run dirs), `quarantine/hilarious_marcupial_20261111/`,
`runs_from_245_20261111/` (pulled today: 54 verse dirs + checkpoint).

---

## 0. Executive summary

1. **GGSD works and is running.** As of this writing, hilarious_marcupial
   (RTX 4090, Qwen3-30B-A3B-Instruct) has completed **181 / 1,071 verses** of
   Maththew under driver 0.0.3 (52 verses in the new punctuation-aware
   format), at ~11 verses/hour, ETA ~81 h, GPU 60 °C / 97 %.
2. **Punctuation is recoverable and now recovered.** The punctuated text of
   record (SBLGNT via MorphGNT field 3) was in the repo all along; 0.0.2
   discarded it. 0.0.3 tokenises it deterministically, verified by a 10/10
   harness and whole-book count invariance (`;` 168 · `·` 761 · `,` 910 · `.` 753).
3. **The headline punctuation discovery:** Maththew does not punctuate
   *more* than Homer, Pindar, or the orators (all corpora spend ≈141–156
   marks per 1,000 words). It **reallocates** — spending an outsized share of
   its cadence budget on the gate (`;`): 9.17/1,000 words vs Homer's 2.31.
4. **The gate tracks interlocutor presence, not translation, not genre.**
   Across Greek dialogue (Clouds 30.82, Gorgias 24.02, Memorabilia 18.34),
   oratory (Apology 9.47, On the Crown 7.99), instruction without an
   interlocutor (Didache 1.30), Aramaic-rendered history (Josephus 1.53),
   and inside Maththew itself (controversy dialogue 14–15 vs parable
   explanations 0.00), the gradient is one variable deep: *somebody else is
   in the room*. One-liner kept from the challenge report: the gate does not
   mark where Maththew is translated, or Greek, or inspired. It marks where
   somebody else is in the room.
5. **The Aramaic-oration belief survives only in refined form.** His two-mode
   belief (Chaucian oration for parables / Feynmanic narration for math
   lectures) fails naive discourse-vs-narrative segmentation (6.60 vs
   6.78 gates/1,000w) but survives as the interlocutor law. Translation-from-
   Aramaic as the *gate* explanation is not supported (Josephus control gates
   low; native Greek dialogue gates 3–5× higher). Lexis/syntax translation
   questions remain untested by punctuation.
6. **Grammar work is real but thinner than punctuation work.** The set-
   retention discipline (propose, never eliminate) caught a measured
   KJV-collapse on the project's two most important words (§5). Book-wide
   grammar census exists as harness criteria G1–G4, not yet run at scale.
7. **The mathematical reading of Maththew is a proposed layer, fully
   specified, never authorised to eliminate.** Rules M1–M10, ratio-free
   `TAKE(Q,u)=(n,r)_u`; 143 gated verses hand-read in
   `tools/homer/MATTHEW_SEMICOLON_VERSES.md`.
8. **Known defects are logged, not buried** (§11): a paid-model result was
   being overwritten (A4), model errors counted as completions (A8), the
   local verse file is duplicated from 22:7 (F4), and 25 model-error words
   sit inside otherwise completed verses in the current run.

---

## 1. The instrument

GGSD decodes a verse word-by-word: for each Greek word it assembles a
*primitive* — the set of grammatically possible readings — from Logeion
lexica (LSJ, Bailly, Abbott-Smith, Middle Liddell, Pape, Dutch, short def,
parse), MorphGNT morphology, and translation witnesses.

**Founding discipline** (`schema.py`): *the model may propose properties;
it may not eliminate. Elimination requires a consented rule.* Every primitive
keeps its full set; reports must not state what a verse "means" while more
than one member stands; labels `[measured]` require a named measure and
`[his]` requires an explicit deposit.

**Pipeline (0.0.3):** MorphGNT tokens → `punctuation.py` (deterministic
token objects: printed form, trailing mark, ⸀/⸂…⸃ apparatus, accent class
and position, breathing) → per-word model fill (Qwen locally, others
configurable) with driver-managed fields restored after the call →
`math_layer.py` (proposed gates/equations) → `verse_grammatical_decoding.json`,
`report.md`, Q1/Q2 audit questions.

**Driver measurements (0.0.2 era, from run logs):** 2,348 word-calls,
median 13.3 s/word (p90 20.5 s), 9.18 GPU-hours over 128 runs, ≈1.9 % empty
fields, median 13 grammatical rules per word. These numbers are why the
full book is an 80+ hour job and why determinism was pushed as far down
the stack as it would go.

**Model decision (game plan, upheld):** keep `dengcao/Qwen3-30B-A3B-Instruct-2507:Q4_K_M`
(Ollama) as workhorse; frontier models are better spent as 5 % auditors.
Highest-value single improvement identified: deterministic quotation
verification — every rule's quotation must be a substring of its cited
Logeion entry (proposed, not yet built).

## 2. Corpora and editions (all punctuation claims are edition-relative)

| Corpus | Edition / source | n (words) | Use |
|---|---|---|---|
| Maththew | SBLGNT via MorphGNT (field 3 printed / field 4 clean) | 18,345 | text of record |
| Rest of NT | same | per book | internal comparison |
| Homer, Iliad + Odyssey | Perseus | ~195,000 | epic baseline |
| Pindar, 4 collections | Perseus | per collection | lyric baseline |
| Oration/dialogue pack | Perseus (+ Hermas via jtauber) | per work | genre gradient |
| LXX (8 books) | Swete, via `chadmonahan/septuagint-swete` TSV | per book | translated-Hebrew control |
| LXX via Perseus | — | — | **failed**: Perseus holds English only (F1) |

MorphGNT's seven fields matter: field 3 is the as-printed form (punctuation
+ apparatus `⸀ ⸂ ⸃`), field 4 the clean word. 0.0.2 decoded field 4 and threw
field 3 away. Every punctuation result below comes from field 3.

## 3. Punctuation — what was discovered

### 3.1 The inventory and the zeroth mark

The baseline reference (`GREEK_PUNCTUATION_BASELINE_20261111.md`) establishes:
space itself is the zeroth mark (scriptio continua is the unmarked state);
accents (acute/grave/perispomeni) and breathings are prosodic marks, not
cadence; the cadence marks in the editions are `,` (comma), `·` (ano teleia,
high point), `.` (full stop), `;` (gate). Scribal/critical marks (`⸀ ⸂ ⸃`)
carry the apparatus. Elision marks (U+02BC, U+1FBD) are orthography, **never
cadence** — miscounting them was a named trap and the layer excludes them by
construction. `—` and `:` are effectively absent from every Greek baseline
sampled: if they appear in the operator's hand, they are his grammar
(`PUNCTUATION_GRAMMAR_OPERATOR_20261111.md`), filed as his, not as "Greek".

A typographic fact the study keeps straight: in Greek type, the `;`-shaped
mark *is* the question mark (erotimatiko). The operator's name for it —
**gate** — is a functional reading of that mark: it opens a conditional
domain whose resolution (or measured absence) follows. The functional name
and the typographic name describe the same glyph at different levels; the
reports keep both.

### 3.2 The counts (Measured, whole texts)

Per 1,000 words, Maththew vs Homer: comma 49.65 vs 77.3 · ano teleia 41.52
vs 38.9 · full stop 41.08 vs 34.9 · **gate 9.17 vs 2.31 (≈4×)**. Whole-book
totals for Maththew, verified two independent ways (report count and 0.0.3
tokeniser): `;` **168 in 143 of 1,071 verses**, `·` 761, `,` 910, `.` 753.

Total cadence spending is unremarkable everywhere: ≈141 marks/1,000w in
Maththew, ≈151 Homer, ≈146–156 Pindar. **Maththew's signature is allocation,
not volume.**

### 3.3 Pindar: the per-line artifact

"Pindar gates less than narrative" dissolves under normalisation. Per 100
lines the odes look gate-poor; per 1,000 words: Olympian 1.53, Pythian 2.29,
Nemean 0.40 (2 gates total — n too small to bear weight), Isthmian 3.45.
Averaging the four collections manufactures a fact none of them contains.
The defensible claim: metre is the primary cadence system in Pindar and the
printed punctuation is its shadow; Maththew has no metre, so punctuation is
the *only* cadence system — which is why its allocation is legible at all.

### 3.4 Apparatus is data

`⸀` (single), `⸂ … ⸃` (span) mark editorial uncertainty against witnesses.
The math layer files them as **drift measurements on their terms** (M9):
carried in every record, never deleted, never counted as cadence. In Mt
17:17 the apparatus span commutes with the gates around it; in 4:10 the `⸀`
sits on Ὕπαγε, the verb of dismissal — the most-edited word in the verse is
its hinge. Whether apparatus density predicts anything is untested; that it
must be *preserved to be testable* is now enforced by the tokeniser.

## 4. The gate — the study's central object

Of the gated clauses, only ≈40 % contain an interrogative word in Homer:
the gate is typed by the mark and what returns through it, not by vocabulary.
The typing adopted (M7, proposed): τί unknown · τίς element · διὰ τί cause ·
πῶς construction · πότε time · πόθεν source · ποῦ position · ἕως πότε limit ·
μήτι loaded · οὐχί negated. Returns (M8, proposed): answered · self-answered ·
null-refused (τίς ἐξ ὑμῶν, 6:27 — the answer is the empty set, measured) ·
held-zero (6:27's one cubit, asked and held at zero) · volume (27:23 — a
shout returned where a value was requested; whether "volume" is a type or a
failure of typing is left open for Carbon, §9) · left-open (27:46 — the final
gate of the book's cry, unclosed by design in the reading).

Speech gating: verses containing a speech verb gate at 15.71/1,000w against
5.12 for speechless verses; inside parable *stories*, speech-bearing verses
gate 12.43 vs 4.76 without. The gate lives where voices change.

## 5. Grammar — discoveries and discipline

**The KJV-collapse case (Measured, `ASSESSMENT_GGSD_AND_MATH_PARSING_20261108.md`).**
An early full run, audited by hand, had collapsed to the KJV reading on both
words the project exists to keep open: κυρίου (report.md:435–451) and αὐτοῦ
(453–467). The audit trail did not catch it because the set had been narrowed
before the witnesses were checked. The fix class: set algebra over witness
classes as a cheap post-check, and dimensional analysis as the first
*legitimate* eliminating oracle (it eliminates readings that don't
dimensionally compose, under consented rules only).

**Manual gold standard.** `MATTHEW_25_18_MANUAL_DECODING.md` +
`REVIEW_…_20261102.md`: one verse decoded entirely by hand, kept as the
measuring stick for model output; the 10-verse harness
(`GAMEPLAN_GGSD_HARNESS_10VERSE_20261110.md`) generalises it — 4 grammar
criteria (G), 3 lemma (L), 3 no-collapse (NC), verses 4:10, 25:18, 1:1,
3:17, 5:3, 6:26, 19:24, 22:37, 26:26, 27:46. The punctuation harness
(PM1–PM10) reuses the same verses so layers can be compared verse-for-verse.

**Morphology.** Hapax-lemma shares (Measured): Maththew 6.0 % ≈ Mark 5.9 %,
John 7.2 %, **Luke 14.2 %** — the "Maththew coins words" hypothesis fails on
this proxy (Luke is the NT's outlier), and the proxy itself was retired as
too weak: the pr
...[truncated 9113 chars]