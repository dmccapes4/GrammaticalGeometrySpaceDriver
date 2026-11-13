# Game Plan — GGSD 10-Verse Grammar Harness

**Filed:** 2026-11-10  
**Prior harness:** `harness_matthew_10.py` (C1–C10) — structural/health checks only; does not test grammar, lemma fidelity, or collapse  
**This plan:** replace those criteria with conditions that derive from grammar and lemmas  
**Reference decoding:** `docs/library/personal/MATHTHEW_4_10_DECODING_WALKTHROUGH_20261109.md`  
**Operator constraint:** grammar asserts. No consented elimination = no collapse.

---

## 1. The 10 verses

Selected for grammar coverage, not sequence. Each verse is a test of at least one named condition.

| # | Ref | Why |
|---|---|---|
| 1 | Matthew 4:10 | ὁ + nominative; historical present λέγει; intransitive/transitive Ὕπαγε; Σατανᾶ as address; no ὀπίσω μου |
| 2 | Matthew 25:18 | Existing benchmark; ἓν/ἐν headword mismatch; αὐτοῦ adverb vs pronoun |
| 3 | Matthew 1:1 | Baseline first verse; Βίβλος as noun not title; genealogy chain construction |
| 4 | Matthew 3:17 | ὁ υἱός ὁ ἀγαπητός — article + nominative again; voice from heaven dative; same ὁ issue as 4:10 |
| 5 | Matthew 5:3 | μακάριοι — "blessed" collapse test; πτωχοὶ τῷ πνεύματι dative chain |
| 6 | Matthew 6:26 | κατανοήσατε — attend/consider vs "look at"; οὐρανοῦ genitive; Nature=God vocabulary |
| 7 | Matthew 19:24 | εὐκοπώτερόν ἐστιν — comparative; διὰ τρήματος ῥαφίδος — needle eye; κάμηλον — camel spelling debate |
| 8 | Matthew 22:37 | Shares κύριον τὸν θεόν σου with 4:10 citation half; ἀγαπήσεις imperative-future ambiguity |
| 9 | Matthew 26:26 | τοῦτό ἐστιν τὸ σῶμά μου — demonstrative; σῶμά collapse test ("body" vs "physical substance") |
| 10 | Matthew 27:46 | ηλι ηλι λεμα σαβαχθανι — transliterated Aramaic embedded in Greek; Logeion will fail these words; special handling required |

---

## 2. Criteria — three groups

### Group G: Grammar conditions (4 criteria)

**G1 — Article gate**  
*Derives from:* the grammar of ὁ/ἡ/τό. The Greek article does not attach to proper nouns as a required bearer. If an article precedes a nominative form, the following word cannot be its sole reading as "proper noun (name)."  

Pass: for any word `w` in the verse where `w[-1]` is a nominative form preceded by the article, `possible_interpretations[w]` is not a singleton `["proper noun: [name]"]`.  
Fail: if the only interpretation returned is a named-person gloss with no open field.  
*Verses that exercise this:* 4:10 (ὁ Ἰησοῦς, ὁ implied on Σατανᾶ), 3:17 (ὁ υἱός), 22:37.

**G2 — Historical present not past-collapsed**  
*Derives from:* λέγω in present tense third-person singular in narrative. The Greek is λέγει (present). "Said" (past) is an editorial shift. Both must survive in the set.  

Pass: for any λέγει in a narrative verse, `possible_interpretations` includes both a present-force reading ("it/he speaks", "it/he says") and acknowledges the English past as a translation choice — not as the grammatical form.  
Fail: if only a past-tense reading ("said") appears and the present-force is absent.  
*Verses:* 4:10 (λέγει αὐτῷ).

**G3 — Dative set not single-gloss**  
*Derives from:* dative case in Greek licenses "to," "for," "with," "by," "in" depending on context. No single gloss is grammatically required.  

Pass: for any dative word, `possible_interpretations` contains ≥ 2 distinct dative sense glosses, or a note that context narrows it with a stated grammar rule.  
Fail: if only "to him" appears for αὐτῷ with no stated elimination.  
*Verses:* 4:10 (αὐτῷ twice), 25:18 (αὐτοῦ adverb reading must be present), 3:17.

**G4 — Imperative/transitive set**  
*Derives from:* ὑπάγω lexicon. LSJ entries include classical transitive "lead/bring under" alongside Koine intransitive "go away." Both must be in the set unless a consented rule eliminates one.  

Pass: for Ὕπαγε, `possible_interpretations` includes at minimum one transitive gloss ("lead under," "bring under yoke") and the classical source citation is present in `lemma_set`.  
Fail: if only "go away" / "depart" appears with no transitive entry.  
*Verses:* 4:10.

---

### Group L: Lemma conditions (3 criteria)

**L1 — Headword fidelity**  
*Derives from:* the ἓν/ἐν mismatch documented in READINESS. If Logeion's `/detail` returns a headword that does not match the parsed lemma (after Unicode normalization), the mismatch must be flagged in `logeion_note` and a retry attempted.  

Pass: for all words, either headword matches parsed lemma, OR `logeion_note` contains a mismatch flag and a retry result is present.  
Fail: if a mismatch is silently ignored and the wrong word's definitions are used as the field.  
*Verses:* 25:18 (ἓν → ἐν known case). Others may surface new mismatches.

**L2 — Multi-source coverage**  
*Derives from:* GGSD's source architecture. The driver fetches LSJ, Middle Liddell, Dodson, Thayer, Strong, Abbott-Smith. Each is a distinct witness. Collapse to one source is information loss.  

Pass: for each word, `source_retrievals` contains entries from ≥ 2 distinct named sources.  
Fail: if only one source's definitions populate the lemma_set (e.g. Strong's only — which is the concordance-study default and skews KJV).  
*Applies to all 10 verses.*

**L3 — No void lemma**  
*Derives from:* the obligation to leave the field open. A word with an empty lemma_set has no field. The model has nothing to constrain. It fills from training priors — which is where KJV enters.  

Pass: every word in every verse has `lemma_set.length ≥ 1`.  
Fail: any word with an empty lemma_set, regardless of how sparse Logeion was.  
Note: Matthew 27:46 (Aramaic transliterations) will likely fail L3 for those words specifically. Log this as expected, not as a harness failure — it is a coverage gap in Logeion, not a driver error. File a special result: `logeion_coverage_gap`.  
*Applies to all 10 verses. Verse 10 expected L3 exception.*

---

### Group NC: No-collapse conditions (3 criteria)

**NC1 — Set cardinality**  
*Derives from:* the core GGSD contract. If Logeion returns ≥ 2 grammatically valid parses for a word, the `possible_interpretations` must contain ≥ 2 entries — unless a `consented_elimination_rule` is present with a source quotation.  

Pass: for every word with multiple parse forms, `possible_interpretations.length ≥ 2` OR `consented_elimination_rule` is non-empty and cites a source.  
Fail: `possible_interpretations.length == 1` with empty `consented_elimination_rule` for a word with documented multiple parses.  
*Applies to all 10 verses.*

**NC2 — No KJV singleton**  
*Derives from:* the proper-noun bias documented in the readiness report. The model trained on KJV will produce KJV readings as defaults when the field is underconstrained.  

Pass: for each word, if `possible_interpretations` is a singleton, it must not exactly match a known KJV rendering for that word without a consented rule. A list of known KJV singletons is maintained in `harness_data/kjv_singletons.json`.  
Initial entries for `kjv_singletons.json`:  
```json
{
  "Matthew 4:10": {
    "Ἰησοῦς": "Jesus",
    "Ὕπαγε": "Get thee hence",
    "Σατανᾶ": "Satan"
  },
  "Matthew 25:18": {
    "κυρίου": "his lord's",
    "αὐτοῦ": "his"
  }
}
```  
Fail: singleton matches KJV with no consented rule.  
*All verses. Verse 1 (Matthew 1:1 "βίβλος γενέσεως" → "book of the generation") likely exercises this.*

**NC3 — Consented rule requires source**  
*Derives from:* the elimination rule in the GGSD contract. Any elimination must cite a source. An elimination without a source quotation is informal and cannot stand.  

Pass: every `consented_elimination_rule` entry in `verse.jsonl` contains both a `rule_text` and a `source_quotation`.  
Fail: any elimination entry where `source_quotation` is empty or null.  
*Applies globally. No verse should pass NC3 if any word has an unsourced elimination.*

---

## 3. Summary table

| Criterion | Group | Derives from | Key verses |
|---|---|---|---|
| G1 Article gate | Grammar | ὁ does not require proper noun | 4:10, 3:17, 22:37 |
| G2 Historical present | Grammar | λέγει is present tense | 4:10 |
| G3 Dative set | Grammar | dative licenses ≥ 2 glosses | 4:10, 25:18, 3:17 |
| G4 Imperative/transitive | Grammar | ὑπάγω transitive in LSJ | 4:10 |
| L1 Headword fidelity | Lemma | mismatch → retry + flag | 25:18 |
| L2 Multi-source | Lemma | ≥ 2 sources per word | all |
| L3 No void lemma | Lemma | empty = model fills from prior | all (Aramaic exception) |
| NC1 Set cardinality | No-collapse | ≥ 2 parses → ≥ 2 interpretations | all |
| NC2 No KJV singleton | No-collapse | singleton must not match KJV default | all |
| NC3 Sourced elimination | No-collapse | elimination requires source quotation | all |

**Pass threshold:** a verse passes the harness if it passes G1–G4, L1–L3, NC1–NC3.  
Exception: Matthew 27:46 passes L3 with a `logeion_coverage_gap` flag for the Aramaic words only.

---

## 4. Output format

```
runs/harness_10verse_<timestamp>/
  summary.json          — {verse_ref: {criterion: pass|fail|exception, note}}
  summary.md            — human-readable table
  kjv_singletons.json   — maintained KJV singleton list (seeded from above)
  <verse_slug>_*/       — standard ggsd per-verse run dirs
```

`summary.json` schema per verse:
```json
{
  "Matthew 4:10": {
    "G1": {"result": "pass", "note": ""},
    "G2": {"result": "pass", "note": ""},
    "G3": {"result": "fail", "note": "αὐτῷ returned only 'to him'; no dative alternatives"},
    ...
  }
}
```

---

## 5. Files to write

1. `harness_10verse.py` — new harness (do not overwrite `harness_matthew_10.py`)  
2. `harness_data/kjv_singletons.json` — seed file (Matthew 4:10 and 25:18 entries above)  
3. `harness_data/verse_list.json` — the 10 verse refs + expected Aramaic exception for 27:46  
4. `criteria.py` — one function per criterion (`check_G1`, `check_G2`, etc.) against the verse.jsonl output  

Order: `criteria.py` first (can be unit-tested against the existing 25:18 run). Then `harness_data/`. Then `harness_10verse.py`.

---

## 6. Start condition

Run `criteria.py` against `runs/Matthew_25_18_20261103T093520Z/` (the most recent local Qwen3 run).  
Expected results on that run:  
- L1: pass (ἓν mismatch was fixed)  
- NC1: likely fail on αὐτοῦ (only pronoun reading returned; adverb reading not in set)  
- G3: likely fail on αὐτῷ  
- NC2: check against kjv_singletons.json seed  

That gives a baseline before any new verses are run. The first harness pass is diagnostic, not a gate.
