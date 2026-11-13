# Greek Punctuation: Baseline Reference

**Filed:** 2026-11-11  
**Occasion:** operator observation that punctuation is the first defined unit of language; space = the first iota. Working document for GGSD punctuation analysis layer.

---

## 0. The Zeroth Mark: Space

> "You cannot spell without ` `."

Space is punctuation. It is the first. Before space, a text is `Youcannotspellwithout`. The word boundary IS the parse. Every lexical claim GGSD makes begins with the decision that THIS group of characters is a word. The Alexandrian editors who divided scriptio continua made lexical choices — interpretation embedded in whitespace.

**In Homeric manuscripts:** Early papyri (3rd–2nd century BCE) have no word spaces — scriptio continua. The division into words is the first layer of editorial interpretation, introduced by Alexandrian scholars (Zenodotus, Aristophanes of Byzantium, Aristarchus, c. 280–145 BCE). The spaces we read as natural are editorial.

**GGSD implication:** tokenisation is not neutral. Where we split is an inherited interpretation.

---

## I. Accent Marks (Prosodic Diacriticals)

These are pitch instructions. Ancient Greek was a **tonal pitch-accent language** — syllable melody, not stress-accent. These are not optional decorations. They are the score.

| Mark | Name | Symbol | Function |
|------|------|--------|----------|
| **Acute** | Oxeia | ά | Rising pitch on that syllable. High note. The syllable goes up. |
| **Grave** | Bareia | ὰ | Lowered/falling pitch. Typically replaces acute on a word-final syllable when another word follows in the same clause — the voice drops in connected speech. |
| **Circumflex / Perispomeni** | Perispōmenē | ᾶ | Rise-then-fall on a **long** vowel. The syllable rises then descends in one breath. Sustained emphasis. **Σατανᾶ = Satan-*ÂA*** — the voice rises then falls on the final syllable. The operator's `~` is exactly right. This is not emphasis in the English-stress sense — it is a melodic gesture. |

**Only long vowels (η, ω, or long α/ι/υ or diphthongs) can carry the circumflex.** The short vowels (ε, ο) cannot. This is phonological, not stylistic.

**The acute vs grave rule:** a word that would end in an acute accent loses it to a grave when the next word follows immediately. The grave on word-final position is a *flowing* mark — it means the voice moves on without a full high landing. An acute at word-end (before a pause or stop) means the voice actually lands high there.

---

## II. Breathing Marks

| Mark | Name | Symbol | Function |
|------|------|--------|----------|
| **Smooth** | Psile | ᾿ | No aspiration. Vowel-initial word pronounced without /h/. |
| **Rough** | Dasia | ῾ | Aspiration. Vowel-initial word pronounced with /h/. Also always on ρ at word start (ῥ = rh). |
| **Diaeresis** | Dialytika | ΐ / ϊ | Two adjacent vowels are **not** a diphthong — they are pronounced separately. αι = diphthong; αΐ with diaeresis = two beats, not one. |

---

## III. Sentence-Level Punctuation

Introduced systematically by **Aristophanes of Byzantium** (~200 BCE) — three stops for reading aloud, indicating breath length. This is the system inherited by NT scribes. Pre-Alexandrian Homer had none of these.

| Mark | Name | Symbol | Equivalent | Function |
|------|------|--------|------------|----------|
| **Comma** | Hypodiastolē | , | Comma | Shortest pause. Phrase boundary, breath. In oration: a beat. |
| **High stop / Ano teleia** | Teleia stigmē | · | Semicolon or strong pause | Strong internal pause. Heavier than comma. A clause is complete but the sentence continues. In oration: a full breath, a held moment. |
| **Full stop** | Stigmē | . | Period | Sentence end. |
| **Greek question mark** | Erōtēmatikon | ; | **? (not semicolon)** | ⚠ The SEMICOLON character marks a **question** in Greek. The English semicolon is the Greek question mark. This is a live source of confusion in Unicode: U+003B `;` is the Latin semicolon used as Greek question mark. — But note: "question" may be the wrong English gloss entirely. See §IX. |
| **Colon** | — | : | Varies | Used in some manuscripts for paragraph-level stops. Not standardised in ancient texts. |

**The critical trap:** `Ὕπαγε, Σατανᾶ·` — the `·` is the ano teleia, a strong pause. If you read the `;` (semicolon) as a pause instead, you have now turned the statement into a question: *"Go under, Satan?"* — which is the opposite of the verse.

---

## IV. Scribal / Critical Marks (Alexandrian tradition, in margins)

These appear in scholarly manuscripts, not in performed texts — but they are how we received Homer.

| Mark | Name | Function |
|------|------|----------|
| **Diple** | `>` | Marks a notable passage, a citation from another author, or a disputed line. |
| **Antisigma** | `Ͻ` | Marks lines that Aristarchus thought were transposed or should be rearranged. |
| **Paragraphos** | `⸗` or horizontal line | Marks a new section, speaker change, or topic break in papyri. |
| **Coronis** | Ϫ-like mark | End of a book or major section. |
| **Obelos** | `—` in margin | Line Aristarchus considered spurious. |

---

## V. Maththew 4:10 Fully Scored

```
Ἰησοῦς,  Ὕπαγε,  Σατανᾶ·
```

| Word | Accent | Punctuation after | Reading |
|------|--------|-------------------|---------|
| Ἰησοῦς | Perispomeni on -οῦ (long diphthong) | Comma | The name is stated with melodic fall on its long syllable. Then a breath: the speaker has identified who speaks. |
| Ὕπαγε | Acute on Ὕ-, grave on final -ε (before next word... but here comma intervenes, so the acute holds) | Comma | The command is stated with a rising pitch on its first syllable, landing clearly. The comma after says: the command is given — now the addressee. |
| Σατανᾶ | Perispomeni on final -ᾶ | Ano teleia (·) | The addressee is named with rise-fall pitch on the final long vowel. Then the strong pause closes it. **Satan-AH·** — complete. |

The operator's notation `'  " ,"  ,  ~.` maps exactly:
- `'` — the opening breath / smooth breathing on Ἰ-
- `"` — the quotation / statement of the name
- `,` — comma after Ἰησοῦς
- `"` — the imperative stated
- `,` — comma after Ὕπαγε
- `~` — perispomeni on ᾶ
- `.` — the ano teleia `·` (strong stop, not a period, but the operator writes it as `.` since the full-close is the event)

---

## VI. Homer and Pindar as Baseline

**Why Homer:**
- Aristophanes of Byzantium's stop system was designed *for* Homeric texts — the stops were invented to notate oration performance of Homer
- The accent marks in Homer encode the actual pitch of spoken Greek before later traditions flattened it
- Homer's punctuation is oration-native; it is not theological addition

**Why Pindar:**
- Odes are metrically scored — strophe/antistrophe/epode structure means the cadence marks are embedded in meter
- Every pause in Pindar is a metrical pause — the punctuation and the rhythm are the same thing
- A Pindaric comma is not editorial whim; it is where the metrical foot requires breath

**The Maththew situation:**
Maththew's oration register uses pause as meter — but Maththew is not in a fixed metrical scheme. The commas and stops are the substitute for meter: they are the breathing score of the original Aramaic delivery transcribed into Greek punctuation. This is why the marks are non-negotiable data.

---

## VII. GGSD Plan: Punctuation Preservation Layer

**What to add:**

1. `tokenise_greek()` currently strips marks and returns word strings. Change it to return token objects:
   ```python
   {
     "surface": "Σατανᾶ",
     "trailing_punct": "·",          # comma | high_stop | full_stop | question | none
     "accent_class": "perispomeni",  # acute | grave | circumflex | none | mixed
     "accented_syllable": "final",   # initial | medial | final
     "breathing": "smooth",          # smooth | rough | none
   }
   ```

2. **Cadence map per verse** — an output field alongside the word list: a sequence of `(word, beat_weight)` tuples where beat_weight is derived from trailing punctuation:
   - `none` = 0 (flows to next word)
   - `comma` = 1 (breath)
   - `high_stop` = 2 (held pause)
   - `full_stop` = 3 (complete close)
   - `question` = Q (rising close)

3. **Accent annotation in verse.jsonl** — each word record gets the accent class and position. This feeds into oration analysis: where the pitch peaks in a verse is where the speaker emphasised.

**The run continues.** The current decode data (word open sets, Logeion results, Q1/Q2) is valid. Punctuation is an enrichment pass — it doesn't invalidate any existing decode, it adds the cadence layer on top.

---

## VIII. Matthew 25:18 — Noted

> "The one who had received one [talent] went and dug in the ground and hid his master's money."

The operator flags this as **entirely lifecycle**: seed → earth → burial → waiting. The word ἔκρυψεν (hid, concealed) from κρύπτω — to hide, to conceal, but also the root of *cryptic* and *crypt* (underground chamber). The lifecycle reading: the talent goes underground not as hoarding but as the seed phase of the cycle. To be decoded fully when the run reaches it.

---

---

## IX. The `?` Is Not a Question — Computing as Witness

The operator's observation (2026-11-11): the Greek `;` survived into computing as `?`, and it kept the **Greek function**, not the English one.

**The URL query string:**
```
[protocol]subdomain.domain.topleveldomain?[key=value&]n
```
The `?` opens a **qualification namespace**. What follows modifies what the resource resolves to. Remove the query string and you get a different or null response. The key-value pairs are not flavor — deep links are load-bearing. The `?` is not asking anything. It is a **gateway into a dependent domain**.

This is the Greek `;` function: introducing a clause that qualifies or depends on what came before. The Greek `;` was never only an "asking" mark — it separated a main clause from its conditional resolution.

**The ternary operator `?:`:**
```
condition ? branch_true : branch_false
```
Not a question. A conditional branch operator. The `?` gates entry into the resolution domain. `?:` is everyone's favorite operator precisely because it is maximally expressive with minimal characters: *if the condition resolves, enter this domain, else enter that one.*

**Optional chaining `?.` (TypeScript, etc.):**
```
object?.property
```
*Does this exist? If so, proceed into this qualified namespace. If not, return null.* Same gate structure.

**The lineage:**
```
Greek ;  →  URL ?  →  ternary ?:  →  optional chaining ?.  →  regex ? (zero-or-one qualifier)
```
All of these introduce a **conditional or qualified domain**. The Greek `;` did not become the English question mark — they diverged. The English `?` asks for information. The computing `?` routes into a qualified domain. Computing inherited the Greek function.

### The Elvis Operator

`?:` is called the Elvis operator. Two visual readings are in circulation — which one is correct has not been settled (2026-11-11, operator note: "I am going to find images of Elvis to settle this once and for all").

**Reading A — quiff and face (standard citation):** Rotate `?:` 90° counterclockwise. The rounded top of `?` is Elvis's pompadour/quiff. The straight descender is the face. The dot is the chin. The `:` is unexplained.

**Reading B — performance pose (operator's read, confirmed 2026-11-11):** Elvis performing. Left hand on the mic, right arm active and raised, body leaning in toward it. The `?` is the active side of the body — curve = reaching arm or leaning torso, hook = elbow or hand, dot = grounded foot or fist. The `:` is the microphone — round head, stand below. This is a complete composition; Reading A leaves the `:` unaccounted for.

**Final mapping (operator, confirmed against photos):**

- `?` — right side of the body: the arc at the top is the raised right arm sweeping overhead; the descending hook is the torso/body leaning in; the dot at the bottom is the right foot planted on the stage.
- `:` — left side of the body: the top dot is the left hand holding the microphone (or the mic head itself); the bottom dot is the left foot.

`?:` together is Elvis's complete performance silhouette — `?` is the dynamic sweep of the raised arm and leaning body, `:` is the two anchor points (hand+mic, foot) holding the ground. The whole pose in two characters.

**Verdict:** Reading B, precisely specified. The quiff reading doesn't account for `:` and doesn't match performance photos. The full-body silhouette reading accounts for every mark.

**GGSD implication:** when a verse ends in `;`, the standard gloss "question" may be wrong. The correct function may be "conditional dependent clause" — what follows (or what is implied to follow) is the qualification on what was stated. This changes the register of every interrogative sentence in the corpus.

---

*Working reference. Not final. Punctuation analysis layer pending implementation.*
