# Challenge Run — Orated Aramaic / Two-Oration Belief vs the Data

**Filed:** 2026-11-11 (second pack + challenge, operator order: "run the next sources and then run the challenge on the belief. I call failures datum.")
**Belief under test (operator, 2026-11-11):** *Maththew is Chaucian oration for parables and Feynmanic narration for math lectures. Orated Aramaic translated literally to Greek Koine using perfect grammar. The cadence throws off Greek punctuation. The author exercised authorial decision to coin words when translation failed, or when it wanted to make the reader `. ;`*
**Method:** pre-registered-style. Each component was turned into a measurement *before* looking at its result; failures are recorded as datum with the same prominence as confirmations (§5 is a ledger, not a graveyard). Counts measured in full from local files, 2026-11-11; interpretations proposed.

---

## 1. Second source pack (fetched today)

`tools/fetch_oration.py` (extended), `tools/oration/`:

| Work | Kind | Words | `,` | `·` | `.` | `;` /kW |
|---|---|---:|---:|---:|---:|---:|
| Plato, *Gorgias* (Γοργίας) | dialogue **about oration** | 27,355 | 87.22 | 13.85 | 80.50 | **24.02** |
| Xenophon, *Memorabilia* (Ἀπομνημονεύματα) | Socratic record, dialogue | 36,035 | 103.04 | 14.54 | 30.14 | **18.34** |
| Aristophanes, *Clouds* (Νεφέλαι) | stage comedy dialogue | 9,670 | 64.22 | 19.44 | 70.01 | **30.82** |
| Aeschines, *Against Timarchus* | delivered oration #2 | 15,056 | 96.11 | 13.08 | 43.77 | 4.85 |
| Didache (Tauber, Apostolic Fathers) | Koine teaching instruction | 2,300 | 98.26 | 34.78 | 89.57 | 1.30 |
| Hermas, *Shepherd* | Koine vision + dialogue | 29,357 | 91.26 | 26.77 | 93.03 | 6.10 |

**LXX (Swete, via chadmonahan/septuagint-swete TSV — Perseus holds only English for these; see Failure F1)** — per book, `;` /kW:

| Book | Kind | `;` /kW | | Book | Kind | `;` /kW |
|---|---|---:|---|---|---|---:|
| Genesis | narrative + dialogue | 4.20 | | Psalms | poetry | 4.61 |
| Exodus | narrative | 2.35 | | Isaiah | prophecy + dialogue | 6.64 |
| Ruth | story-dialogue | 6.29 | | Jeremiah | prophecy | 6.05 |
| 1 Samuel | narrative-dialogue | 6.49 | | Ezekiel | vision-prophecy | 2.69 |
| Proverbs | gnomic | 2.89 | | Jonah | story (n=1,080w) | 8.33 |
| **Job** | **dialogue (translated from Hebrew)** | **20.95** | | | | |

## 2. What the second pack does to the picture

The gate axis now has a clean gradient, and it is **turn-taking density**, end to end:

```
vision/instruction/narrative:   Rev 0.81 · Herodotus 0.62 · Didache 1.30 · Josephus 1.53
                                Homer 2.31 · LXX narrative 2.35–4.20 · Hermas 6.10
delivered oration:              Lysias 2.83 (narrative-heavy) · Aeschines 4.85 · Demosthenes 7.99
gospel teaching/dialogue:       Luke 7.92 · Matthew 9.17 · Apology 9.47 · Mark 9.92 · John 10.82
diatribe/dialogue proper:       Romans 11.62 · Medea 14.92 · Xenophon 18.34 · Job-LXX 20.95
                                Gorgias 24.02 · Clouds 30.82
```

Three consequences, stated before the Matthew test so they can't be accused of being built to fit it:

1. **Written dialogue is the gate-maximum genre in Greek, full stop.** Socrates out-gates everyone. Any theory of Matthew's 9.17 must first beat the null "he writes live question-answer scenes," and the null is now very strong.
2. **Translated dialogue gates high too (Job 20.95).** So translation does not *suppress* gates — content (dialogue) survives translation and carries its rate with it. This keeps a *translation* hypothesis alive for Matthew's texture while killing "translation explains the rate": the rate follows the scenes, in any source language yet tested.
3. **Didache (1.30) is a precious null:** Koine, teaching, apostolic neighbourhood, *no interlocutors* — and no gates. Being early Christian instructional Koine explains nothing. Being a scene with a second voice explains almost everything so far.

## 3. The challenge proper — Matthew segmented (deduped; see Failure F4)

Gate rates per 1000 words, Matthew by block (segments defined before counting; boundaries = traditional pericope structure):

| Block | Label given before counting | Verses | Gate/kW |
|---|---|---:|---:|
| A (1–4) | intro narrative | 90 | 1.82 |
| B (5–7) | Sermon discourse | 111 | 9.57 |
| C (8–9) | miracle narrative/dialogue | 72 | 8.13 |
| D (10) | mission discourse | 42 | **1.39** |
| E (11–12) | controversy dialogue | 80 | **14.30** |
| F (13:1–52) | parables chapter | 52 | 5.16 |
| G (13:53–17) | narrative/dialogue | 135 | 12.63 |
| H (18) | community discourse | 34 | 8.97 |
| I (19–22) | controversy dialogue | 156 | **15.38** |
| J (23) | woes discourse | 39 | 6.11 |
| K (24–25) | eschatological discourse | 97 | 4.44 |
| L (26–28) | passion narrative | 161 | 9.32 |
| **All discourse-labelled (B,D,H,J,K)** | | 323 | **6.60** |
| **All narrative-labelled (A,C,L)** | | 323 | **6.78** |
| Parable verses (all books of them) | | 128 | 6.42 |
| Non-parable verses | | 941 | 9.54 |
| Verses **with** a speech verb (λέγ-/εἶπ-/ἔφη) | | 374 | **15.71** |
| Verses **without** | | 695 | 5.12 |
| Ch.13 frame dialogue (why-parables? understood?) | | 18 | 21.41 |
| Parable **story only** | | 107 | 7.89 |
| Parable **explanation** (13:18–23, 36–43) | | 14 | **0.00** |
| Parable-story verses with speech verb | | 39 | 12.43 |
| Parable-story verses without | | 68 | 4.76 |

## 4. Verdicts, component by component

**B1. "Two orations: parables told (Chaucian), lectures narrated (Feynmanic)." — PARTIALLY SUPPORTED, INVERTED IN AN INTERESTING WAY.**
The naive form fails: discourse-as-labelled does not out-gate narrative-as-labelled (6.60 vs 6.78 — a coin toss), because the labels are too coarse. But the *finer* prediction hiding inside the belief does well: parable **explanation** — the lecturer decoding his own simulation, students silent — gates at **0.00** (n=281 words; small, recorded with its n), while the frame dialogue around the parables ("why do you speak in parables?") gates at 21.41, and controversy dialogue tops the book (14–15). Parables sit mid-low (story 7.89). So the text does switch registers exactly where the belief says it switches — but the switch is not story-vs-lecture. It is **scene-with-a-second-voice vs single-voice-of-any-kind**: mission instructions (ch.10, discourse with no interlocutor) gate at 1.39, lower than most narrative; passion *narrative* gates at 9.32 because it is full of trials, i.e. interrogations. Refined belief that survives contact: *Matthew is written in scenes; gate rate is the scene's interlocutor density; parable-telling is a single-voice scene even when its content is a story with talkers inside it* (story-without-speech-verb 4.76 vs story-with 12.43 — even *inside* parables, the driver is whether a speech act is on stage, not that a parable is playing).

**B2. "Orated Aramaic, translated literally." — NOT SUPPORTED AS THE GATE EXPLANATION; UNTESTED AS A LEXICAL CLAIM.**
Josephus (Aramaic-first) 1.53 and LXX-narrative (~2–4) show translation does not import gate density; *Gorgias/Xenophon/Clouds* show Greek dialogue needs no Aramaic to exceed Matthew fivefold-to-threefold. If Aramaic oration stands behind Matthew, its gate signature is indistinguishable from ordinary Greek dialogue practice — which means the gate data *cannot be evidence for it*. The claim retreats, properly, to lexis and syntax, where it was always testable and hasn't been tested yet (§6).

**B3. "Perfect grammar" — NOT YET TESTED; proxy attempted, proxy failed honestly.**
No grammar-error census was run (that needs MorphGNT parse-code anomaly work, a day of care, not an afternoon). What was run as a cheap stand-in — NT-hapax lemma rate as a *coinage* proxy — returns: Matthew 6.0% (100/1,680), Mark 5.9%, John 7.2%, **Luke 14.2%** (290/2,046). If Matthew's author coined at unusual rates, this proxy cannot see it; and if the proxy means anything, Luke is the coiner. Recorded as a **failure of the proxy**, and weak evidence against unusual Matthean coinage — not a verdict on coinage itself (a coinage may be classically attested, a hapax may be ordinary rare vocabulary; Logeion-tier absence, already in GGSD's source system, is the sharper instrument).

**B4. "Cadence throws off Greek punctuation." — REFRAMED, THEN SUPPORTED IN REFRAMED FORM.**
As established (Homer report §0): the marks are editorial in every corpus here. What survives testing: the *clause architecture* the editors scored differs by register in a way punctuation rates faithfully track across six independent editorial traditions (Perseus Homer, Pindar, Attic prose, drama, Swete LXX, SBLGNT). Editors are not conspiring across 2,000 years to fake a dialogue gradient in texts this different. The cadence is in the composition; the punctuation is its obedient shadow. **Supported as: orated/dialogic cadence → question architecture → editorial marks.**

**B5. "Coin words where translation failed, or to make the reader `. ;`" — the second clause is compositional, and the data wink at it.**
Explanation-verses at 0.00 gates followed by frame-dialogue at 21.41 is the rhythm of a lecturer who stops (`.`) and then opens the floor (`;`) — the belief's own syntax, enacted by its text at ch.13. I record this as *consistency*, not proof, and note the operator wrote the belief in the same cadence. Datum, filed.

## 5. Failures ledger (datum, per operator instruction)

| # | Failure | What it cost / taught |
|---|---|---|
| F1 | Perseus canonical-greekLit holds **no Greek LXX** (English only under tlg0527) | Swete TSV sourced instead (chadmonahan/septuagint-swete); edition now differs from the Perseus pack and is named wherever LXX rates are used. Sourcing rule for the project: *a corpus without punctuation is not a corpus for us* (that is also why eliranwong's tokenised LXX was rejected). |
| F2 | First Josephus fetch crashed the extractor (`QName` on an XML comment node) | Fixed (`isinstance(el.tag, str)` guard). Lesson generalised: TEI iterators meet comments; all future extractors carry the guard. |
| F3 | Hermas/Didache absent from Perseus canonical | Fetched from jtauber/apostolic-fathers; different edition lineage, named in tables. Didache then produced the pack's most valuable null (1.30). |
| F4 | **`tools/matthew_verses.jsonl` contains 336 duplicated verse records** (Matthew 22:7 onward appended twice; 1,407 rows, 1,069 unique) | All segmentation above rerun deduped. Any past statistic computed row-wise over that file (not from MorphGNT directly) is inflated ~1.3× in late chapters. **Recommend:** rebuild the file in Phase 1 of the game plan and diff; treat this as a pipeline bug datum, not a text fact. |
| F5 | Naive belief segmentation (discourse vs narrative labels) shows **no step** (6.60 vs 6.78) | The belief's coarse form failed; the refined interlocutor-density form was then derived *from the failure* and fits every block including the awkward ones (D low, L high). This is the run's main product. Failures that refine are the best kind. |
| F6 | Parable-explanation gate rate 0.00 on n=281 words | Too small to bear weight alone; filed as suggestive datum awaiting the Phase-2 gate records (which will enlarge it: explanations exist at 13, 15, 21, 24–25 and can be pooled). |
| F7 | Hapax-as-coinage proxy cannot distinguish Matthew (6.0% ≈ Mark; Luke 14.2%) | Proxy retired. Coinage question moves to Logeion-tier absence test (game plan, §6 below). |
| F8 | "Perfect grammar" untested by this run | Not papered over: no error census exists yet. A claim this central gets its own run or none of our confidence. |

## 6. Next measurements (each small, each capable of failing)

1. **Logeion-tier coinage test:** for Matthew's 100 NT-hapax lemmas, check classical-tier attestation (Cunliffe/Slater/Autenrieth/LSJ-full) in existing run source-retrievals (Matt 1–5 already fetched; extend to quarantined runs under operator review). Coinage candidates = absent from classical tiers, present in NT-specific tiers.
2. **Grammar census ("perfect grammar"):** MorphGNT parse anomalies + article-with-nominative and dative-set conditions (10-verse harness G1–G4) run book-wide; test whether anomalies *cluster* at untranslatable constructions (literal-translation signature) or scatter (ordinary variation signature).
3. **Interlocutor density as a variable:** Phase-2 gate records give per-verse (speech verbs, named speakers, answerer). Regress gate presence on those across Matthew + Mark + Hermas: the refined B1 predicts interlocutor presence ≈ all of the variance. If residue remains that tracks "parable vs lecture," the original belief gets its share back — measured, not argued.
4. **Rebuild `matthew_verses.jsonl`** (F4) and re-issue any statistic that ever used it.

## 7. One-line summary for the board

> The gate does not mark where Matthew is translated, or where he is inspired, or where he is Greek. It marks where somebody else is in the room. Everything else — Aramaic, coinage, perfection — is still on the table, but it will be measured at the lexical bench, where it lives, or not at all.

*Counts: deduped local corpora as listed. Segment boundaries declared before counting. n attached to every small claim. Failures: 8, all retained.*
