# Game Plan — MorphGNT as Graded Reference, Punctuation Cadence, and Mathematical Grammations

**Filed:** 2026-11-12  
**Project:** GrammaticalGeometrySpaceDriver (GGSD)  
**Status:** game plan; no new math rule in this document is locked  
**Predecessors:** `GAMEPLAN_GGSD_PUNCTUATION_MATH_20261111.md`, `HARNESS_PUNCTUATION_MATH_20261111.md`  
**House rules:** deterministic before model; proposed before consented; no mathematical reading may eliminate a lexical, grammatical, or semantic reading; counting is whole-count `TAKE(Q,u)=(n,r)_u`, never silent ratio-normalisation.

---

## 0. The correction

MorphGNT is **not being avoided**.

The present driver already uses MorphGNT for three things:

1. the as-printed token, including punctuation and apparatus;
2. the clean surface used for token identity;
3. the lemma hint used to reduce Logeion lookup errors.

What GGSD does not yet do is treat MorphGNT as one **graded scholarly witness among others**, record where the witnesses agree or conflict, and then transform that graded reference by the verse's punctuation cadence. Nor does it yet run letter-by-letter mathematical decoding on words that carry equation triggers.

The target pipeline is therefore:

```text
printed verse
  -> punctuation cadence          (what are the term domains and boundaries?)
  -> graded scholarly reference   (what do MorphGNT / Logeion witnesses say?)
  -> trigger scan                 (does this verse or word require math?)
  -> mathematical grammation      (letter-by-letter candidate expression)
  -> lexical / grammatical model  (existing GGSD open-set decoding)
  -> report with all layers standing side by side
```

No layer replaces the layer before it.

---

## 1. The two gem terms

### 1.1 Punctuation cadence

> **Punctuation cadence** is the ordered sequence of printed boundary operators in a named edition — comma, ano teleia, full stop, gate (`;`), apparatus marks, accent placement, and their scopes — read as the timing and domain structure of a verse: what is held, what is evaluated, what closes, what opens a conditional domain, and what follows as that domain's return.

Punctuation cadence is **measured before it is interpreted**. For each verse it records:

- token index and printed form;
- trailing mark and cadence weight (`none=0`, comma `1`, ano teleia `2`, full stop `3`, gate `Q`);
- clause and gate domains opened and closed by the marks;
- speech-verb and speaker-change context;
- apparatus attachment (`⸀`, `⸂ … ⸃`) as drift carried on a term;
- accent class and position where they modify a term or a later grammations candidate;
- the return span after a gate: what text is allowed to answer it.

Cadence does not supply a dictionary gloss. It transforms a sequence of glossed words into scoped terms. A dictionary may say what a word can mean; cadence says **where that meaning is operating**: inside a gate's left side, inside its return, after a hold, inside a `καὶ` chain, or after closure.

Example, Matthew 6:26:

```text
... οὐ σπείρουσιν οὐδὲ θερίζουσιν οὐδὲ συνάγουσιν εἰς ἀποθήκας,
καὶ ὁ πατὴρ ὑμῶν ὁ οὐράνιος τρέφει αὐτά·
οὐχ ὑμεῖς μᾶλλον διαφέρετε αὐτῶν;
```

The cadence is not "there is a comma and a question." It is:

1. a three-verb negated process chain;
2. comma boundary;
3. a `καὶ` join to the feeding clause;
4. ano teleia: hold / evaluate what follows;
5. a gate opened by the final `;`, whose left side asks for the differentiated value of the hearers.

That structure exists before any one word is translated.

### 1.2 Mathematical grammation

> **Mathematical grammation** is the letter-by-letter parsing of a Greek word as candidate mathematical notation, under a versioned and explicitly *suggested* symbol table, preserving graphemes, accents, breathings, final-letter forms, position, repetition, and cadence scope, and producing one or more expression trees whose unresolved roles remain explicitly unresolved.

A grammations record is not:

- an etymology;
- a morphological parse;
- a claim that the lexical meaning is false;
- a translation;
- permission to eliminate any reading.

A grammations record is a structured proposal of the form:

```json
{
  "surface": "θερίζουσιν",
  "segmentation_candidates": ["θερί | ζουσ | ιν"],
  "expression_candidates": ["..."],
  "unresolved": ["..."],
  "status": "proposed"
}
```

The plural matters. Where segmentation or symbol role is ambiguous, GGSD keeps the candidate set open. The machine's job is to make the ambiguity inspectable, not to collapse it early.

---

## 2. What "the word does not exist" means

"Anytime the word does not exist *is* a math criterion" needs an operational definition, otherwise every ordinary inflected form would falsely count as nonexistent merely because dictionaries list lemmas rather than every surface form.

GGSD must distinguish four states.

### 2.1 Lexically closed

A word is **lexically closed** when all of the following are recorded:

1. MorphGNT supplies a lemma, part of speech, and parse code;
2. the parse code can generate or identify the surface form, allowing for movable nu, elision, crasis, and accent shift;
3. at least one Logeion dictionary entry has a matching headword for that lemma;
4. Logeion `/find`, when run as an independent witness, returns the same lemma among its parses, or a documented variant of it.

This is the strongest ordinary state. It does **not** prove one translation. It proves the lexical item is closed by the reference stack.

### 2.2 Form-attested only

MorphGNT supplies a lemma and parse that generate the surface, but dictionary closure is thin or absent for the lemma. The form exists grammatically; the lexical witness set is weak.

This state is recorded, not hidden. It is a soft math signal when combined with another trigger.

### 2.3 Witness-conflicted

MorphGNT, Logeion `/find`, and Logeion dictionary detail do not converge: different lemmas, a headword mismatch, a missing parse, or a parse incompatible with the surface.

Conflict is data. All witnesses stay in the record. GGSD must not quietly choose the first parse, the first dictionary, or the MorphGNT lemma as though the conflict had not occurred.

### 2.4 Lexically unclosed

A word is **lexically unclosed** — the operational meaning of "does not exist" for this plan — when, after normalisation that preserves accents and breathings in the record:

- no reference lemma closes over the surface; or
- MorphGNT gives no usable parse (`???`, missing, or incompatible); or
- Logeion returns no matching headword or entry; or
- the witnesses route the form to another word and no witness returns the expected lemma; or
- the token is a candidate coined form whose lemma is not independently closed by the reference stack.

**Lexical unclosedness is a hard mathematical trigger.** It does not mean the token is meaningless, corrupt, or invented by the driver. It means the ordinary lexical road does not close, so the letter road must be opened.

A hapax legomenon is not automatically unclosed. Frequency is not existence. A once-attested word with lemma, parse, and dictionary closure is lexically closed; a common-looking form with no closing witness is not.

---

## 3. MorphGNT: reference, graded, transformed

### 3.1 What MorphGNT contributes

For every token, retain all seven MorphGNT fields:

| Field | Use in the new layer |
|---|---|
| BCVword | stable verse/token addressing |
| part of speech | witness claim about word class |
| parse code | witness claim about form; must be decoded, not merely stored |
| printed text | punctuation, apparatus, accents as printed |
| clean word | token surface and identity |
| normalised word | matching key; never replaces the marked form |
| lemma | reference lemma candidate |

Two current gaps must be closed:

1. when a MorphGNT lemma hint is supplied, the driver currently skips Logeion `/find` and records `parses: []` — the parse witness is therefore absent even though MorphGNT's own parse code is sitting unused in the data;
2. Logeion `/detail` is fetched for one committed lemma, so alternative lemmas returned by `/find` never receive dictionary witnesses.

### 3.2 The grading procedure

For each word, build a `reference_grade` record **before** model decoding:

```json
{
  "surface": "θερίζουσιν",
  "morphgnt": {
    "lemma": "θερίζω",
    "pos": "V-",
    "parse_code": "3PAI-P--",
    "parse_decoded": {"person": 3, "tense": "present", "voice": "active",
                       "mood": "indicative", "number": "plural"}
  },
  "logeion_find_lemmas": ["θερίζω"],
  "logeion_detail_headwords": {"logeion_lsj": "θερίζω"},
  "existence_state": "lexically_closed",
  "grade": "R3",
  "conflicts": []
}
```

Grades describe **reference closure**, not truth:

| Grade | Meaning |
|---|---|
| `R3` | MorphGNT lemma/parse, independent `/find` lemma, and at least one dictionary headword agree |
| `R2` | two witness paths agree; the third is absent rather than opposed |
| `R1` | witnesses conflict, or only one witness path closes |
| `R0` | lexically unclosed — hard math trigger |

Rules for grading:

- Run `/find` even when MorphGNT supplies a lemma. MorphGNT remains the transport lemma; `/find` becomes the second witness rather than the boss.
- Keep **all** `/find` parses. Never commit to `parses[0]` silently.
- Fetch dictionary detail for the MorphGNT lemma and for any additional `/find` lemma that is not a mere accent variant. Record which headword each dictionary actually returned.
- Decode the MorphGNT parse code into named features. A stored code that no component reads is not a witness.
- Duplicate or near-duplicate dictionary text counts once for closure. Agreement of copied text is not independent agreement.
- Grade and conflicts are driver-computed. The model may read them; it may not alter them.

### 3.3 Transformation by cadence

The graded reference is then **transformed by punctuation cadence**: cadence assigns each word a scope before lexical or mathematical interpretation begins.

Each token receives a `cadence_role`, for example:

- `gate_left_term`, `gate_head`, `gate_return_term`;
- `kai_chain_member` with chain index and chain length;
- `held_term` (before an ano teleia evaluation);
- `closed_term` (before a full stop);
- `speech_frame` / `spoken_term` where a speech verb opens a spoken domain;
- `apparatus_carrier` where `⸀` or a span touches the token.

The lexical open set is not changed by this transformation. Its **scope** is. "θερίζω can mean reap" and "θερίζουσιν is the second member of a negated three-process chain inside the evidence domain of a gate" are different kinds of statement, and the report must keep them in different fields.

---

## 4. The suggested symbol table (v0.1 — not locked)

This table is a **suggestion surface for parsing**, versioned as `MATH_SYMBOL_TABLE v0.1`. Every role below ships `status: "suggested"`. A grammations parse must cite the table version it used, so a later table revision produces a visible re-parse rather than a silent change of meaning.

### 4.1 Grapheme handling before symbols

1. Parse **graphemes**, not code points: base letter plus its combining accents, breathings, diaeresis, and iota subscript stay together.
2. Preserve the raw surface. Create a lowercased matching copy; never overwrite the raw.
3. Final sigma `ς` and medial sigma `σ` are different grapheme roles (see below). Accent-stripping is allowed only in matching keys, never in the parse record.
4. An accent is a **modifier on its grapheme**, not a separate letter: `ί` is `ι` carrying the acute transform.
5. Word-initial capitals may be orthographic (sentence start, proper name). Record `initial_capital_orthographic: true/false/unknown`; do not let case alone decide a symbol role — and do not let it veto one either.

### 4.2 Letter roles

| Grapheme | Suggested role | Conditions / notes |
|---|---|---|
| `α` | angle variable | `λ(α) -> θ`: a function applied to the angle variable yields a measured angle `θ` |
| `β` | squaring **or** doubling | postfix on a segment: `Xβ -> X²` and `Xβ -> 2X` are rival branches; both are kept |
| `γ` | gamma-function candidate | `γ(X)` when it prefixes a segment; otherwise unresolved gamma atom |
| `Δ`, `δ` | delta | `Δ` total change over a domain; `δ` local variation of the following term |
| `ε` | relation / application | infix: `A ε B` = "A as it relates to B", "A applied to B"; the direction is recorded, not reversed silently |
| `ζ` | zeta curve / zeta function | prefix operator over the following segment: `ζ(X)`; the ionic decay curve over a permutation domain is a named branch (see §7) |
| `η` | inclusive or | infix between segments: `A η B` = A-or-B-or-both; accent variants recorded as modifiers of the or |
| `θ` | angle measure | the measured result of an angle function; also an angle atom when no `λ(α)` frame is present |
| `ι` | unique variable | the distinguished variable of the local expression |
| `ί` | transformed unique variable | `ι` plus acute: `ι -> ι′`; the transform is marked, its kind unresolved unless context names it |
| `κ` | index variable, the κth | see `κ...ν` below |
| `λ` | function | prefix: `λ(X) = f(X)`; word-initial `λ` becomes a hard trigger only under §5 (lexical unclosedness), because ordinary Greek words begin with lambda |
| `μ` | infinitesimal unit | `μx` reads as the differential of x (`dx`); `μα` commonly segments as `μ | α`, differential of the angle variable; existing M4 function-word discipline still applies at word level |
| `ν` | total number / bound | the N against which `κ` runs |
| `ξ` | coupled unknown | a second unknown coupled to the expression but not identified with `ι` |
| `ο` | little-o asymptotic | `ο(g(n))` only when a following segment can serve as g(n); a standalone `ο` is an unresolved atom, never silently zero |
| `π` | pi | the constant, unless a capital `Π` product reading is separately justified and recorded |
| `ρ` | decay coefficient; terminal decay | inside an expression, the decay rate carried by its term; at the end of a mathematical statement, a decay closure on the whole preceding expression. (Written `rho` in prose, always lower-case.) |
| `σ` | permutations | medial/final-position sigma inside a symbol parse: a permutation action on the following or surrounding set |
| `ς` | standalone variable | final sigma is a terminal variable in its own right, not a permutation; it may also be a typographical stand-in for `ζ`, recorded as a rival branch when the parse needs it |
| `ς*` | dual of `ς` | complex conjugate / dual / adjoint, or Kleene star (zero or more repetitions) — the branch is chosen by domain and recorded; the star is never invented where the text has none |
| `τ` | field-of / time | `τ(X)` = the field of X; where X is temporal, the field is time — "time may be the field" is kept as an explicit branch, not a metaphor. **Medial τ is the field between its neighbours:** `X τ Y = τ_field(X .. Y)`. Worked anchor (operator, 2026-11-12): `ατα` = angles held in a field = an unspecified collection — "some things" (ἅττα). The `-ατα` tail of neuter plurals is the same shape: things as angles-in-a-field, contents unspecified |
| `υ` | upsilon roles | true anomaly near angle terms; kinematic viscosity near flow/time terms; otherwise a secondary variable. Branch by neighbours, or leave unresolved |
| `φ` | golden operator | an operator, not merely the constant: `φ(X)` applies the golden operation to X |
| `χ` | free variable | an unconstrained variable of the expression |
| `ψ` | state term | the state carried by the expression |
| `ω` | ordinal set | the ordered set of the expression; an accent on `ω` proposes the **reverse** traversal of that set (suggested, potentially) |
| `Σ` | summation | prefix over a segment; may occur mid-word at a segment boundary: `Σ(X)` sums X over its index domain |
| `κ...ν` | index range | `κ` runs to the total `ν`: with `Σ`, `Σ κ...ν (body)`; without `Σ`, the range itself is the expression |
| `κ++` | successor step | where repetition shows `κ` advancing, read the increment step (operator-marked "not sure" — ships as a named open branch) |

### 4.3 Accent and breathing modifiers (suggested)

| Modifier | Suggested effect |
|---|---|
| acute on a variable (`ί`, `ώ`) | transformed / primed form of that variable: `x -> x′` |
| accent on `ω` | reverse order on the ordinal set (any accent class proposes it until fixtures separate them) |
| accent on `η` | variant of the inclusive or; variant kind recorded, not yet named |
| grave / circumflex elsewhere | recorded as modifiers with role `unresolved`; no semantics invented for them in v0.1 |
| breathing | recorded; no symbol role assigned in v0.1 |

This is deliberately incomplete. An unresolved modifier in the record is worth more than a confident gloss nobody consented to.

### 4.4 What is out of bounds

Statistical machinery is **not in bounds** for mathematical grammation: no means, no standard deviations, no distributions, no probability models, no significance language. Counting is allowed because counting is arithmetic: whole counts, `TAKE`, sequence lengths, chain lengths, mark counts. The moment a proposed reading needs a distribution to stand, it leaves this layer.

---

## 5. Trigger rules — when math must run

Triggers are deterministic. A trigger **opens** a mathematical record; it never closes a lexical one.

### 5.1 Verse-level hard triggers (automatic math verse)

| # | Trigger | Action |
|---|---|---|
| V1 | the verse contains `;` | automatic math verse: every gate gets a full gate record, and every word in the gate domains is grammations-eligible |
| V2 | a `καὶ` chain of length ≥ 2 inside one cadence domain | chain record opened (M1 equality proposal applies per join); length ≥ 3, or a chain crossing a hold or gate, makes the verse a math verse |
| V3 | repetition that grows (see §6) | sequence record opened; the repeated terms are grammations-eligible |
| V4 | numeral terms joined by `καὶ` or standing inside a gate domain | `TAKE` record opened at the declared unit |
| V5 | a gate whose return is absent, refused, or verse-final | return-typing record opened (M8); absence is measured, not treated as missing data |

### 5.2 Word-level hard triggers

| # | Trigger | Action |
|---|---|---|
| W1 | word is lexically unclosed (§2.4) | letter-by-letter grammations **must** run |
| W2 | word begins with `ζ` | grammations **must** run, whether or not the word is lexically closed |
| W3 | word begins with sigma (`Σ`/`σ` grapheme at word start) | grammations **must** run; the summation branch is opened alongside any permutation branch |
| W4 | word begins with `λ` **and** the word is lexically unclosed or witness-conflicted | grammations must run with the function branch `λ(X) = f(X)` first |
| W5 | `κ...ν` pattern inside one word, or `κ` and `ν` as successive terms inside one gate domain | index-range record opened |
| W6 | a standalone single-letter token, or an operator-supplied `ς*` annotation | grammations must run |

### 5.3 Soft triggers (candidate signals)

A soft trigger alone opens a *watch* entry. Two or more soft triggers on one word, or one soft trigger inside a math verse, open a full grammations record.

- internal `ζ` or segment-initial sigma inside the word;
- `μ` opening a segment that is not a known function word (`μα` first);
- word-final `ρ` on a long or unclosed word (decay closure candidate);
- `φ`, `τ`, `ω`, `θ` appearing in one segment;
- an accented `ί` or `ώ` (transformed variable / reversed set);
- a letter or substring repetition inside the word;
- length ≥ 8 with three or more suggested-symbol graphemes in sequence — "looks like an equation" made inspectable as a list of named signals, never as a vibe.

### 5.4 What never triggers by itself

- an ordinary lexically closed word beginning with `λ` (W4 needs unclosedness — Greek is full of lambda words);
- any single common letter (`α`, `ε`, `ο`, `τ`...) inside an ordinary closed word;
- frequency. Commonness and rarity are counts about a corpus, not properties of a letter sequence.

---

## 6. Repetitions that grow

"Repetitions that grow" is a deterministic detector over tokens and graphemes. It emits **sequences of whole counts**, nothing else.

| Pattern | Definition | Example shape |
|---|---|---|
| G1 run growth | the same token or phrase recurs with run lengths 1, 2, 3, ... | `καὶ ... καὶ καὶ ...` |
| G2 phrase growth | a phrase recurs with one more term each time | `τί ...; τί γὰρ ...; τί γὰρ κακὸν ...;` |
| G3 frame growth | a shared frame (prefix or suffix of ≥ 3 graphemes) is retained while the word carrying it grows | the `-ουσιν` verb frame across a chain |
| G4 chain growth | successive `καὶ` chains in a verse grow in member count | chain lengths (2, 3, 5) recorded as counts |
| G5 count growth | numeral terms increase across a domain | whole counts in order, unit declared, no ratio taken |

Each detection records the sequence itself — terms, positions, lengths — as the datum. What the growth *means* is a proposed reading layered on top, never part of the detection.

Matthew 6:26 is the standing fixture: `σπείρουσιν / θερίζουσιν / συνάγουσιν` share the `-ουσιν` frame (G3) inside a gate verse (V1), so all three verbs are grammations-eligible even though all three are lexically closed.

---

## 7. Worked fixture — θερίζουσιν (Matthew 6:26)

This fixture is the acceptance test for the grammations engine. It also shows why the layers must not be collapsed into each other.

**Reference grade.** MorphGNT (61-Mt 010626): lemma `θερίζω`, POS `V-`, parse `3PAI-P--` (third person plural, present active indicative). The word is expected to grade `R3`/`R2` once `/find` runs as second witness. **The lexical road closes.** The gloss road ("they reap") stands untouched.

**Why math runs anyway.** Verse-level trigger V1 (`;` present) plus G3 frame growth across the three `-ουσιν` verbs. Existence is not the only door into math; cadence is another.

**Graphemes.** `θ ε ρ ί ζ ο υ σ ι ν` — ten graphemes, with `ί = ι + acute transform`.

**Operator segmentation (candidate A).** `θερί | ζουσ | ιν`

- `θερί`: `θ` angle measure; `ε` application/relation; `ρ` decay carried by the term; `ί` transformed unique variable. Read: the measure of a decay-rate applied to the transformed unique variable — in the operator's words, *rate of change by decay transforms unique variable, as seen in ζουσ*.
- `ζουσ`: `ζ` opens the zeta curve; over `σ`, permutations — `λ(σ) -> ζουσ`: the ionic decay curve over the permutation domain. Rival segmentation keeps `ου` together as one segment inside `ζ(...)`; both branches stay in the record.
- `ιν`: `ι` unique variable bounded by `ν`, the total: `ι` taken against `ν` (`ι_ν` as candidate notation).

**What the engine must output:** candidate A as above, at least one rival segmentation, every unresolved role named (the `ο` and `υ` inside `ζουσ` are not silently assigned), the reference grade beside it, and `status: "proposed"` on every branch.

**What the engine must never output:** "θερίζουσιν really means a decay function, not reaping." Both readings stand. The report prints them in different sections and lets the operator adjudicate.

---

## 8. Data model additions

All additions are optional-with-default; old runs validate unchanged.

### 8.1 Per word

```json
"reference_grade": {
  "grade": "R3 | R2 | R1 | R0",
  "existence_state": "lexically_closed | form_attested | witness_conflicted | lexically_unclosed",
  "morphgnt": {"lemma": "...", "pos": "...", "parse_code": "...", "parse_decoded": {}},
  "logeion_find_lemmas": ["..."],
  "logeion_detail_headwords": {"source_id": "headword"},
  "conflicts": ["..."]
},
"cadence_role": {"role": "gate_left_term", "chain_id": null, "domain_id": 2},
"grammations": {
  "triggered_by": ["V1", "G3"],
  "symbol_table_version": "v0.1",
  "graphemes": ["θ", "ε", "ρ", "ί", "ζ", "ο", "υ", "σ", "ι", "ν"],
  "segmentation_candidates": [
    {"segments": ["θερί", "ζουσ", "ιν"],
     "expression_candidates": ["..."],
     "unresolved": ["ο, υ inside ζ(...)"]}
  ],
  "status": "proposed"
}
```

### 8.2 Per verse

- `cadence_domains[]`: domains with boundary marks, member token indices, and gate return spans;
- `kai_chains[]`: member indices and lengths as whole counts;
- `growth_sequences[]`: G1–G5 detections as recorded sequences;
- `math_verse: true/false` with the trigger list that made it so;
- existing `gates[]` and `equations[]` unchanged in shape, extended with `grammations` references.

### 8.3 Schema guard (extends the existing one)

The existing rule — an elimination may not cite a mathematical rule — extends verbatim: **an elimination may not cite a grammations record, a reference grade, or a cadence role.** Grades and grammations propose and scope; they never eliminate.

---

## 9. Implementation phases

Each phase is deterministic or ends at an operator gate. No phase is an agent loop.

### Phase 0 — Consent and fixtures (operator gate)

- Operator reads this plan; amends the symbol table; consents or strikes trigger rows.
- Fixture verses fixed: Mt 6:26 (θερίζουσιν), 4:10 (no gates — grammations must stay quiet at verse level), 27:46 (final gate), plus one operator-chosen lexically unclosed word when the grader first finds one.
- **Gate:** symbol table v0.1 marked consented-as-suggested (consent to *run* it as proposed, not to lock it).

### Phase 1 — Reference grader (`reference.py`, new)

- Decode MorphGNT parse codes into named features (both local formats: `3PAI-P--` and `V-PAI-3P` styles).
- Run Logeion `/find` as independent witness in all modes; keep all parses.
- Fetch `/detail` for MorphGNT lemma plus non-variant `/find` lemmas; record returned headwords per dictionary.
- Emit `reference_grade` per word; dedupe copied dictionary text before counting agreement.
- Retrieval snapshots retained so a grade can be re-derived offline.
- **Tests:** θερίζουσιν grades closed with decoded parse; the known εἷς/ἐν misroute records a conflict instead of silently passing; a synthetic lemma with no entries grades `R0`.

### Phase 2 — Cadence transform v2 (`punctuation.py`, extended)

- Build `cadence_domains[]`, `kai_chains[]`, `growth_sequences[]` (G1–G5), and per-token `cadence_role`.
- Speech-domain tracking: spoken terms inherit the domain of their speech verb.
- **Tests:** whole-Matthew mark totals unchanged (`;`168, `·`761, `,`910, `.`753); 6:26 yields one gate, one chain, one G3 sequence; 4:10 yields zero gates and no math-verse flag.

### Phase 3 — Grammations engine (`grammations.py`, `math_symbols.py`, new)

- `math_symbols.py`: the §4 table as versioned data (`MATH_SYMBOL_TABLE = "v0.1"`), every role `status: "suggested"`.
- Grapheme splitter (base + combining marks; `ς`/`σ` distinct; accents as modifiers).
- Segmentation lattice: known lemma/suffix alignment, operator-prefix boundaries (`λ ζ Σ φ τ κ`), optional digraph grouping (`ου`, `ει`, `αι`...), repetition boundaries. **All** segmentations above a declared signal floor are returned, not a winner.
- Expression builder over the §4 grammar: prefix operators, `ε`/`η` infixes, `β`/`ρ`/`*` postfixes, `κ...ν` ranges, `ς`/`ς*` terminal rules.
- **Tests:** §10 criteria MG1–MG10.

### Phase 4 — Trigger integration (`math_layer.py`, extended)

- Implement §5 trigger scan over (tokens, cadence domains, reference grades).
- `;` verses become automatic math verses; grammations attach to triggered words only — the engine does not letter-parse all 18k words of Matthew.
- Extend gate records with grammations references for gate heads and load terms.
- Backfill mode: reference grades, cadence v2, and grammations are recomputed deterministically over existing runs (as with the punctuation backfill). **No model calls.** Old Q1/Q2 answers are untouched by this phase.

### Phase 5 — Model-facing context (small, gated)

- The word prompt gains a read-only block: reference grade, cadence role, and any grammations candidates, labelled: *"Given. Do not alter. You may comment on a grammations candidate; label your comment proposed."*
- The model may **not** invent segmentations. Segmentation is deterministic (Phase 3); the model may only discuss candidates it is handed.
- Q1/Q2 prompts gain the math-verse summary (triggers fired, chains, growth sequences) so post-decode questions can reason about the math layer instead of re-deriving it.

### Phase 6 — Rollout

- Dry-run the 10-verse harness set; operator reads Mt 6:26 and 27:46 reports end to end.
- **Restart gate:** the live hilarious_marcupial run is *not* hot-patched. New code syncs only at a checkpoint restart the operator calls, exactly as with the 0.0.3 fixes.
- Whole-Matthew deterministic pass: reference grades + cadence v2 + grammations index over all 1,071 verses (no GPU), producing a trigger census: how many R0 words, how many ζ/Σ-initial words, how many math verses beyond the 143 gated ones. The census is reported as counts with `n`, and it is the first real measurement of how much of Matthew this layer touches.

---

## 10. Acceptance criteria (harness `tools/harness_grammations.py`, deterministic)

| # | Criterion |
|---|---|
| MG1 | θερίζουσιν: reference grade closed, parse decoded (3rd plural present active indicative), grammations fired by V1+G3, candidate segmentation `θερί | ζουσ | ιν` present with unresolved `ο, υ` named |
| MG2 | a synthetic lexically unclosed word beginning with `λ` fires W1+W4 and returns a function-first candidate |
| MG3 | a lexically closed word beginning with `ζ` fires W2 regardless of grade |
| MG4 | an ordinary lexically closed word beginning with `λ` does **not** hard-fire (watch entry only) |
| MG5 | all 143 gated verses are flagged math verses; Mt 4:10 is not |
| MG6 | `καὶ` chains detected with whole-count lengths; a chain of ≥ 3 in one domain flags its verse |
| MG7 | `ς` never parses as permutation; `σ` never parses as the standalone variable; `ς*` branches (dual / Kleene) both representable |
| MG8 | `ί` parses as `ι` + acute transform, never as a distinct base letter; accented `ω` proposes reverse order |
| MG9 | `κ...ν` inside a segment opens an index-range record; `Σ κ...ν` composes with it; no lower bound is invented |
| MG10 | every grammations record carries `status: "proposed"` and the symbol-table version; schema validation rejects any elimination citing a grammations, grade, or cadence field |
| MG11 | no statistical artefact (mean, deviation, distribution, probability) appears anywhere in grammations output — checked by field-name and vocabulary scan |
| MG12 | MorphGNT witness conflicts (εἷς/ἐν class) are recorded as conflicts; no witness is overwritten by another |

---

## 11. Risks and open questions (stated, not buried)

1. **False-positive surface.** Greek is made of the same letters as the symbol table. The trigger discipline (§5.4) is the only thing standing between this layer and letter-parsing the whole corpus. If the Phase 6 census shows grammations firing on a large fraction of ordinary closed words, the soft-trigger floor rises — by operator decision, from the census, not by agent taste.
2. **The symbol table will be wrong in places.** It is v0.1 and suggested. Versioning plus `status: "proposed"` on every branch is the containment: a corrected table re-parses visibly; nothing was ever eliminated on the old one.
3. **Segmentation is the hard problem.** Letters underdetermine boundaries. The lattice keeps rivals standing, but the operator will need to adjudicate recurring boundary patterns (e.g. is `ου` one segment or two inside `ζ`?) — those adjudications become table v0.2 entries, with the fixture that forced them named beside the rule.
4. **`κ++` and accented-`ω` reversal are operator-flagged uncertainties.** They ship as named open branches, not as rules.
5. **Parse-code decoding needs the MorphGNT codebook verified** against the two local file formats before Phase 1 grades are trusted; an unverified decoder would manufacture R1 conflicts out of a format difference.
6. **Nothing here touches the live run** until the operator calls a restart. The plan is written so Phases 1–4 can be built and harnessed entirely offline against pulled runs.

---

## 12. The one-paragraph version

MorphGNT stays — as a witness whose testimony is graded (R3–R0) against Logeion's, with its parse codes finally read and its conflicts kept. Punctuation cadence then scopes that graded testimony into domains: gates, chains, holds, closures. Where a word's lexical road does not close, or a verse's cadence opens the math door (`;`, growing repetition, `καὶ` chaining), mathematical grammation parses the word letter by letter under a suggested, versioned symbol table — `λ` function, `ζ` decay curve, `μ` differential, `ρ` decay, `ς` the standing variable — and files the expression candidates **beside** the lexical record, proposed, unresolved where unresolved, eliminating nothing. The scholars are heard. The cadence conducts. The letters, where they look like equations, are finally read as equations — on the record, and at the operator's gate.
