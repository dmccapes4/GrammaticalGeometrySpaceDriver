# Oration & Variation Sources for GGSD — First Pack (2026-11-11)

**Fetched:** `tools/fetch_oration.py` → `tools/oration/*.txt` (Perseus canonical-greekLit, same source family as the Homer/Pindar pack)
**Purpose:** punctuation/cadence baselines with *variation in the right directions* — delivered oration, staged dialogue, recited history, metred dialogue, and a work rendered into Greek from an Aramaic first version — to test the operator's working belief about Maththew (see §3).
**Rates:** per 1000 words, full local texts, computed 2026-11-11. Matthew rates from MorphGNT SBLGNT (`tools/matthew_verses.jsonl`).

## 1. The pack

| File | Work | Kind | Words | `,` | `·` | `.` | `;` |
|---|---|---|---:|---:|---:|---:|---:|
| `plato_apology.txt` | Plato, *Apology* (Ἀπολογία Σωκράτους) | staged forensic oration + cross-examination | 8,659 | 92.97 | 15.94 | 30.37 | **9.47** |
| `demosthenes_crown.txt` | Demosthenes, *On the Crown* (ὑπὲρ Κτησιφῶντος…) | delivered political oration | 22,516 | 94.24 | 12.17 | 29.45 | **7.99** |
| `lysias_1.txt` | Lysias, *Speech 1* (ὑπὲρ τοῦ Ἐρατοσθένους φόνου) | delivered court speech, plain style | 2,476 | 94.91 | 16.56 | 41.20 | 2.83 |
| `herodotus.txt` | Herodotus, *Histories* (Ἱστορίαι) | recited logoi, Ionic narrative prose | 185,957 | 67.56 | 17.03 | 37.32 | 0.62 |
| `josephus_war.txt` | Josephus, *Jewish War* (Ἰουδαϊκοῦ πολέμου πρὸς Ῥωμαίους) | **Aramaic-first, rendered into Greek** (author's own preface), narrative history | 125,226 | 58.55 | 12.67 | 31.59 | 1.53 |
| `euripides_tlg003.txt` | Euripides, *Medea* (Μήδεια) | metred stage dialogue | 8,041 | 88.17 | 34.45 | 57.70 | **14.92** |

Reference rows (not fetched today; already in repo / measured today from `morphgnt/sblgnt/`):

| Work | Kind | Words | `;` /kW |
|---|---|---:|---:|
| Homer (Iliad+Odyssey) | oral epic, editorial punctuation | 199,076 | 2.31 |
| Pindar (4 collections) | sung ode | 21,145 | 1.80 (collection range 0.40–3.45) |
| **Matthew** | target | 18,329 | **9.17** |
| Mark | gospel, paratactic narrative | 11,286 | 9.92 |
| Luke | gospel, literary preface + narrative | 19,446 | 7.92 |
| John | gospel, dialogue-heavy | 15,438 | 10.82 |
| Acts | narrative + speeches | 18,412 | 3.69 |
| Romans | dictated argumentative letter (diatribe questions) | 7,055 | 11.62 |
| Revelation | vision report | 9,833 | 0.81 |

## 2. First readings (labelled: counts measured; interpretations proposed)

1. **Gate rate tracks dialogic argument, not antiquity and not "Greek" in general.** Delivered/staged oratory (*Apology* 9.47, *Crown* 7.99), stage dialogue (*Medea* 14.92), the gospels (7.9–10.8) and Paul's diatribe (11.62) all live in one band; narrative history — recited (Herodotus 0.62), Aramaic-rendered (Josephus 1.53), epic (Homer 2.31), vision (Revelation 0.81) — lives in another, an order of magnitude lower. Matthew's 9.17 is **not anomalous among orators**. It is anomalous only against the narrative baseline the project started with.
2. **Translation-from-Aramaic, by itself, does not raise the gate rate.** Josephus is the control the project most needed: a work actually rendered from an Aramaic first version into Greek, by its author's own account — and it gates at 1.53. Whatever makes Matthew gate at 9.17, "the translator carried Aramaic questions over" is not sufficient. Dialogue density is the visible driver.
3. **`·` separates the genres `;` cannot.** Medea (34.45) and the gospels (37–43) hold high ano teleia; Attic oratory prose holds low (12–17) despite high commas (93–95/kW — Attic orators breathe in commas, Matthew in holds). This is a second, independent cadence axis for the classifier: *comma-breathing* (Attic prose oration) vs *hold-and-gate* (dialogue/lecture). Matthew is hold-and-gate.
4. **Intra-NT variation is itself the cheapest experiment available:** same edition family, same language moment, gate rates from 0.81 (Revelation) to 11.62 (Romans) tracking genre scene-by-scene. Before reaching for Aramaic explanations, GGSD should explain variance *inside* the NT — the variables that do that (speech density, interlocutor presence, return-type) are measurable today.

## 3. Challenge to the operator's working belief (as invited)

Belief, as stated 2026-11-11: *Maththew is Chaucian oration for parables, Feynmanic narration for math lectures; orated Aramaic translated literally into Greek Koine with perfect grammar; the cadence throws off Greek punctuation; the author coined words where translation failed or to make the reader ` . ;`*

Points where today's data presses on it:

- **"Oration" does real work; "Aramaic" does not (yet).** The gate excess is fully explained by the oratorical-dialogic register, attested in native Greek works that never touched Aramaic (Demosthenes, Plato, Euripides). Aramaic origin may still explain *other* layers — Semitic word order, lexical coinages, the double-names — but those need their own tests (Logeion source-tier already in GGSD: a coined word should show classical-absence; a literal translation should show Hebrew/Aramaic-mappable constructions). Keep the hypotheses on separate axes or they will launder each other's evidence.
- **"Cadence throws off Greek punctuation" needs re-aiming.** The punctuation in all these editions is editorial (Alexandrian-descended, modern-settled); an Aramaic cadence cannot have thrown *marks* the author never wrote. What cadence can throw is the *clause structure* editors later scored — question frequency, vocative framing, parataxis. Restate as: **orated cadence → clause/question architecture → editorial punctuation follows obediently.** The data then test the first arrow (question density per genre), which §2 already supports; the second arrow is a property of editors, common to every corpus here.
- **The belief makes a falsifiable prediction it should be proud of:** if parables are story-oration and lectures are Feynman-narration, gate density should *step* between Matthew's parable blocks (13, 20, 25), discourse blocks (5–7, 23), and narrative — and parable-internal *dialogue* should gate like dialogue while parable narration gates like Herodotus. That segmentation run is cheap (gate/words per pericope) and the plan's Phase 2 gate records make it a by-product. If the steps aren't there, the belief should change; if they are, it's a measured result, not a framing.
- **"Perfect grammar" is testable as stated.** MorphGNT parse codes + the 10-verse harness already encode several operator grammatical conditions (article-before-nominative, dative sets, historical present). Extend them over the whole text: a literal-and-perfect translation should fail *differently* from a loose one — errors clustering at untranslatable constructions (participles, article-with-infinitive), not randomly. Random solecism distribution would press hard on "perfect"; clustered failure would support "literal."
- The trailing ` . ;` of the belief is received as written: full stop, then gate. The lecture ends; the domain stays open. Noted, and — as a compositional choice in a sentence about authorial decision — appreciated by both agents who have read it so far.

## 4. Next sources, in priority order

1. **Septuagint (Genesis, Psalms, Isaiah)** — the other great Semitic→Greek literal-translation control; Perseus holds only the English for these, so source from a Greek LXX text (e.g. eliranwong/LXX or CCAT-derived) with edition recorded. This is the one comparison that can rescue or retire the Aramaic-translation arrow for *lexis*.
2. **Plato, *Gorgias* and *Phaedrus*** — Plato *on* oration, in dialogue: gates about gating.
3. **Xenophon, *Memorabilia*; Aeschines, *Against Timarchus*** — Socratic record + a second delivered orator, to check Lysias 1's low gate rate (2.83 — plain style, narrative-heavy speech) isn't "oratory is low" but "narrative inside oratory is low."
4. **Aristophanes (a comedy)** — dialogue at maximum speed, vulgar register: the far end of the gate axis.
5. **Didache / Shepherd of Hermas selections** — post-NT Koine teaching/vision prose in Matthew's own dialect neighbourhood, cheap controls for "is it just Koine?"
6. **Cicero in Greek translation / Plutarch *Lives* selections** — later literary prose, another translation direction (Latin-thinking Greek), if a fifth axis is wanted.

## 5. Housekeeping done today (operator orders, 12:13 PT)

- Remote run on hilarious_marcupial (`run_matthew.py`, Qwen3-30B-A3B) **killed** mid-word at Matthew 5:39 w18/21; Ollama model unloaded; GPU 48°C, 0%, 147 MiB.
- Remote `~/ggsd/runs/` (144 entries, 71 MB) + driver log **rsynced** to `GrammaticalGeometrySpaceDriver/quarantine/hilarious_marcupial_20261111/` with `README_QUARANTINE.md`. **Not merged** into local `runs/`. Nothing resumes until the punctuation/math phases land and the operator says go.
