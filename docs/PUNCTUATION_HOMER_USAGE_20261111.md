# Punctuation Usage in Homer — Iliad and Odyssey

**Filed:** 2026-11-11
**Companion to:** `tools/homer/PUNCTUATION_HOMER_REPORT.md` (counts), `docs/GREEK_PUNCTUATION_BASELINE_20261111.md` (operator system)
**Corpus measured:** Perseus canonical-greekLit `iliad.txt` + `odyssey.txt` as held in `tools/homer/` — full text counted, not sampled
**Question this report answers:** not "how often does each mark occur" (the count report does that) but **what is each mark *doing* in Homeric usage** — where it sits, what opens and closes around it, and what a reader of Matthew is therefore entitled to expect as baseline.

---

## 0. Provenance caveat — read this before any number below

Homer did not punctuate. The marks in these files descend from the Alexandrian editorial tradition (Aristophanes of Byzantium's stop system, c. 200 BCE; Aristarchus) as transmitted and re-edited into the modern Perseus text. Every claim below is therefore about **Homeric usage as punctuated by that tradition** — which is exactly the right baseline for Matthew, because the same tradition (via the scribal culture that produced the NT manuscripts and their modern editions) punctuates Matthew. We are comparing like with like: two texts wearing the same editorial instrument. What we must not say is "Homer placed a comma here." What we may say is "the tradition that scores Homer for reading aloud places a comma here, at this rate, in these positions" — and then ask where Matthew's scoring departs from that practice.

All frequency claims below are **measured** (full-corpus counts from the local files, computed 2026-11-11; per-line rates cross-checked against `punctuation_baseline.json`). Functional claims are readings of the counted contexts — examples quoted are the counted lines themselves.

---

## 1. The two normalisations, and why both are kept

| Corpus | Lines | Words | Words/line |
|---|---:|---:|---:|
| Iliad | 15,687 | 111,895 | 7.13 |
| Odyssey | 12,222 | 87,181 | 7.13 |
| Homer combined | 27,909 | 199,076 | 7.13 |
| Matthew (SBLGNT via MorphGNT) | 1,071 verses | 18,329 | 17.1/verse |

A verse is not a line — the finding Carbon's Feynman board (§I of `FEYNMAN_MCCLANE_KOINE_DECODING.md`) got right, and this report keeps. Per-line rates flatter prose; per-word rates travel across genres. Both are reported; per-word is the comparison rate.

| Mark | Iliad /100L | Odyssey /100L | Homer /100L | Homer /1000 words | Matthew /1000 words | Ratio Matt:Homer |
|---|---:|---:|---:|---:|---:|---:|
| `,` comma | 44.80 | 68.35 | 55.11 | 77.3 (62.8 Il / 95.8 Od) | 49.65 | 0.64× |
| `·` ano teleia | 29.24 | 25.83 | 27.75 | 38.9 (41.0 / 36.2) | 41.52 | 1.07× |
| `.` full stop | 22.94 | 27.37 | 24.88 | 34.9 (32.2 / 38.4) | 41.08 | 1.18× |
| `;` gate | 1.47 | 1.87 | 1.64 | 2.31 (2.06 / 2.62) | 9.17 | **3.97×** |
| `—` em dash | 0.00 | 0.25 | 0.11 | 0.15 | — | n/a |
| `:` colon | 0 | 0 | 0 | 0 | 0 | — |

**Headline:** on the three "ordinary" cadence marks Matthew is unremarkable against Homer (0.6–1.2×). On the `;` he runs at four times Homer's rate per word. Whatever the gate is doing in Matthew, it is not Homeric habit turned up slightly; it is a different deployment of a rare mark.

---

## 2. Mark-by-mark usage

### 2.1 `,` (comma) — the breath that keeps hexameter speakable

The comma is Homer's workhorse boundary: phrase-edge, apposition-edge, vocative frame. Its Iliad→Odyssey jump (62.8 → 95.8 per 1000 words) is the largest inter-book difference in the corpus and tracks content, not carelessness: the Odyssey is denser in dialogue, catalogue and explanatory apposition than the Iliad's battle narrative. **Usage rule for GGSD:** comma rate is a *register* signal (speech/exposition density), not an authorial fingerprint. Do not read theology into a comma count. Read the commas for grouping: in Homer the comma almost never separates a subject from its verb across a clause the sense needs whole — it cuts where breath and sense allow the same cut. Where Matthew's commas cut differently (e.g. vocative frames: `Ὕπαγε, Σατανᾶ·` — comma framing the addressed term between operator and stop), the cut is doing address-marking, and the baseline lets us see that because Homer frames vocatives the same way.

### 2.2 `·` (ano teleia) — the strong internal hold

29 per 100 Iliad lines, 26 Odyssey — the ano teleia is Homer's mid-sentence *weight*: clause complete, sentence not over, voice held. Its Matthew rate per word (41.5) matches Homer's (38.9) almost exactly. This matters for the 4:10 class of verses: a reader trained on Homer expects `·` to mean "evaluate what stands before the hold; more follows in the same breath-unit." In Matthew the `·` additionally clusters after speech verbs (`λέγει αὐτοῖς·` — "he says to them: **evaluate**"), a deployment Homer's narrative third-person uses less relentlessly. Baseline expectation: `·` = hold-and-continue, *not* a question and not an ending. Any reading that converts `·` into either is an error the baseline catches for free.

### 2.3 `.` (full stop) — closure at sentence scale

Full stops per word: Iliad 32.2, Odyssey 38.4, Matthew 41.1. Odyssey and Matthew agree in closing sentences slightly more often than the Iliad — consistent with more direct speech (shorter utterances, more closures). Usage note: in Homer a full stop is the only mark that reliably ends a speech or a sense-unit; the `;` and `·` never do that job alone (see §3: a third of Homeric `;` are *not* line-final, and those that are line-final usually end the *line*, not the discourse). Matthew follows this too — 168 `;` in 143 verses sit mid-verse or end verses whose discourse continues.

### 2.4 `;` (the gate) — Homer's rare, speech-bound question instrument

459 gates in 27,909 lines. Measured properties (computed over every gate in both poems):

- **Line position:** 165/231 Iliad gates and 147/228 Odyssey gates are line-final — the gate likes the end of the hexameter, where the metre itself pauses. Matthew's gates, in prose, have no metre to lean on; their placement is freer and therefore more informative.
- **Interrogative content:** only ~40% of gated clauses contain an explicit interrogative token (τίς, τί, πῶς, πόθι, τίπτε…). The other ~60% are questions by delivery and context — challenges, reproaches, ἦ-prefixed appeals (`ἧσθαι δευόμενον, κέλεαι δέ με τήνδʼ ἀποδοῦναι;`). **This is the single most important usage fact for GGSD:** in the baseline tradition, `;` does *not* require an interrogative word to be a gate. The mark itself carries the illocution. A classifier that types gates by hunting τί-words will miss the majority type. Type by the mark and its return (what the next clause/speaker does), not by vocabulary.
- **Who holds the gate:** overwhelmingly characters in direct speech, not the narrator. Homer's narrator asks almost nothing; his people ask constantly. The gate is dialogue technology.
- **Gate openers after `;`:** the following clause most often opens with continuation/interrogative particles (τί, ἦ, οὐδέ, πόθι) — the gate opens *into* more speech by the same or an answering voice. A Homeric `;` is rarely followed by narrative full stop; it is a hinge inside utterance.
- **Gated-clause length:** mean ~5–6 words (Iliad 5.9, Odyssey 5.4) before the gate — short, sharp, one question per breath. Matthew's gated clauses are also short (the 143-verse file averages under 20 words per gated verse, most gates closing a clause of similar handful-of-words size). Same instrument, same hand-size.

Canonical Homeric examples (from the counted text):

```
τίς τʼ ἄρ σφωε θεῶν ἔριδι ξυνέηκε μάχεσθαι;      Il. 1 — the poem's first gate: which god?
πῶς γάρ τοι δώσουσι γέρας μεγάθυμοι Ἀχαιοί;       how — by what mechanism?
Τροίῃ ἐν εὐρείῃ; τί νύ οἱ τόσον ὠδύσαο, Ζεῦ;        Od. — place answered?, then cause asked
τίς πόθεν εἰς ἀνδρῶν; πόθι τοι πόλις ἠδὲ τοκῆες;   Od. — the stranger-intake pair: who, from where
ἢ ὁδὸν ἐλθέμεναι ἢ ἀνδράσιν ἶφι μάχεσθαι;          ἤ-branch gate: road ± battle (both roots taken, in the event)
```

Notice what the examples share with Matthew's: τίς/πόθεν (identity + source), πῶς (construction), ἤ (branch). The question *types* are a stable Greek repertoire. Matthew did not invent gate-typing; he inherited it and quadrupled its rate.

### 2.5 Marks that are not cadence — `ʼ`, `᾽`, `—`, `:`

- **Elision `ʼ` (U+02BC):** 72 per 100 lines — the most frequent "mark" in Homer and **not punctuation**. It records vowel elision for metre. Any pipeline counting it as a pause will hallucinate cadence inside words. GGSD must exclude it from the punctuation layer (it belongs, if anywhere, in a metrical/phonological field). Matthew's prose has almost none of it, correctly.
- **Koronis `᾽` (U+1FBD):** 1 occurrence in Homer, 1 in Pindar. Scribal section furniture, not usage.
- **Em dash `—`:** 0 in the Iliad, 30 in the Odyssey (0.25/100L). The Odyssey's handful — line-final breaks in speeches (`φιλέεσκε γὰρ αἰνῶς—`) — look like modern editorial interruption marks, not an ancient system. Baseline verdict: **the dash is not a Homeric operator.** When the operator's own grammar gives `—` work to do (strong break holding a thought open), that is the operator's system extending beyond Homer, and reports should say so rather than borrow Homer's authority for it.
- **Colon `:`:** zero occurrences in Homer (and zero in Matthew's SBL text — the `·` does that job). Any GGSD output that emits `:` as a Homeric mark has invented it.

---

## 3. Iliad vs Odyssey — the baseline is a range, not a point

| Signal | Iliad | Odyssey | Reading |
|---|---|---|---|
| comma /1000w | 62.8 | 95.8 | Odyssey: more speech, apposition, explanation |
| `·` /1000w | 41.0 | 36.2 | Iliad slightly more held narration |
| `.` /1000w | 32.2 | 38.4 | Odyssey closes shorter units more often |
| `;` /1000w | 2.06 | 2.62 | Both rare; Odyssey marginally more inquisitive (fits its intake/interrogation scenes: who are you, stranger) |
| `—` | none | 30 | Editorial, Odyssey-only |

For GGSD, treat Homeric usage as **bands**: `;` ∈ [2.1, 2.6] per 1000 words is "Homeric" anywhere; Matthew's 9.17 is outside the band by ~4×, on 18k words — not a small-sample wobble (binomial noise on 459 baseline gates cannot stretch to 9.17). Conversely, comma differences *within* the Homeric band say nothing about Matthew; his 49.65 sits below both poems and inside plausible prose variation (verse divisions, not lines, drive part of this).

---

## 4. What Homer teaches a punctuation parser (design inputs)

1. **Type gates by return, not by interrogative vocabulary** (~60% of Homeric gated clauses lack one). The return — answer, counter-question, narrative resumption, silence — is in the text and is machine-checkable: next speaker, next closure mark.
2. **Never let elision into cadence.** Exclude U+02BC / U+1FBD from the operator set explicitly, or Homer's "most common punctuation" becomes a vowel mark.
3. **Position is data:** line-final vs intra-line gate in Homer; verse-internal vs verse-final gate in Matthew. Record `position_in_line` and `position_in_sentence` for every mark.
4. **`·` after speech verbs is the Homeric/Matthew shared hinge** — but in Homer it also does plain narrative work. A parser may *propose* "evaluate-what-follows" for speech-verb `·`; it must not hard-code it for all `·`.
5. **Baseline comparisons must be per-word** whenever line/verse units differ between corpora, and both rates printed. Per-100-lines-only reporting — the format of the first count report — invites the verse≠line error Carbon's board explicitly warned against. (Keep the old report; it is the count. This report is the usage. Games plans should cite both.)
6. **The dash and colon are not in the baseline.** If GGSD's math layer assigns them operators (the operator's grammar does, for `—`), they enter as *operator-system* rules, status consented-by-operator, never as "Homeric usage."

---

## 5. Open questions Homer leaves for the Pindar report and the game plan

- Pindar's odes are metred by strophe, not hexameter: does metre *replace* punctuation (as the baseline doc hypothesised) or merely re-price it? See `PUNCTUATION_PINDAR_USAGE_20261111.md` — short answer: re-prices, and the per-line rate lies about it.
- Homer's gates live in dialogue. Matthew's gates live in dialogue *and* teaching. A speaker-attribution field per gate ("who holds this gate") would let GGSD measure that shift instead of asserting it.
- 40% interrogative-token rate in Homer gives a prior for Matthew's gate-typing classifier. If Matthew's gated clauses show interrogative tokens at far above 40%, his gates are more explicitly typed — a measurable, falsifiable prediction the math layer can test on its first run.

*Measured counts: full local corpus, 2026-11-11. Functional readings: the author of this report, from the counted contexts. Disagreement welcome; bring lines, not adjectives.*
