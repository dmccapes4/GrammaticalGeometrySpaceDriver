# GGSD: Current Implementation Issues

**Inspection date:** November 11, 2026 · America/Los_Angeles  
**Reviewer:** Codex (GPT-6), author field THIRKETHNEN 🔎 — EDGE (`thir`) + PART (`keth`) + NOW (`nen`)  
**Scope:** Current local working copy: grammar retrieval, punctuation, mathematical annotations, question context, checkpoints, validation, and reporting. Existing uncommitted work was present. Findings describe the inspected code, not an immutable release.  
**Priority:** P1 = can change or misrepresent the decoding/evidence; P2 = weakens coverage, reproducibility, or reporting.

## Evidence boundary

Qwen is allowed to answer the two post-decoding questions and make moral judgments. That permission is not an implementation defect, and its answers are not attributed here to Dylan. The issues below concern what evidence reaches those calls, what the code enforces, and how outputs are recorded.

No linguistic accuracy percentage was established. The recipient's tentative 90% figure is not used as a measurement. Local run metadata establishes source usage, not the truth of a parse or interpretation. No external model or dictionary calls were made for the reproductions in this review.

## 1. P1 — MorphGNT is selected by availability, not necessity

**Evidence:** [run_harness.py:47–53,104–118](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/run_harness.py:47); [ggsd.py:214–236,269–278](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/ggsd.py:214); [sources.py:261–275](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/sources.py:261).

For a Matthew verse, the harness supplies the local MorphGNT file whenever it exists. The decoder then prefers its text and passes its lemma hints into dictionary retrieval. A hint skips Logeion `/find` and records an empty grammatical parse list. There is no attempt-first/failure/necessity decision for this branch.

**Observed usage:** Of 54 `run_meta.json` files under `runs_from_245_20261111`, 52 name their text edition. All 52 identify SBLGNT via MorphGNT; two omit that field. This is a local sample, not a census of the remote server.

**Consequence:** The current path does not implement “only when absolutely necessary.”

**Correction direction:** Separate text transport from lemma/parse authority. Attempt the permitted retrieval first; record a specific reason whenever a restricted fallback supplies a claim.

## 2. P1 — The two questions lose the word surfaces and the grammatical evidence

**Evidence:** [ggsd.py:107–123,433–438](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/ggsd.py:107); [model.py:332–358](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/model.py:332).

The structured decoding stores each word as `{"surface": ...}`. The question-message builder looks for `word.surface`, so these records become `?`. It does not include `grammatical_rules`, quotations, source identifiers, punctuation, or the verse-level gates/equations. It retains a shortened description, up to four lexical values, and up to three interpretations.

**Offline reproduction:** A structured word containing `δύνανται`, a `third plural` grammatical rule, and a gate produced `?: description`. None of those three evidence items reached the message.

**Consequence:** The questions ask for judgments grounded in grammar while withholding the explicit grammatical records. The model can reconstruct material from its description, verse reference, or training; that is different from receiving the stored evidence.

**Correction direction:** Use one word-record shape throughout and pass the actual evidence required by each question, including the proposed status of any mathematical rules.

## 3. P1 — Historical admissibility is not enforced

**Evidence:** [sources.py:367–414](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/sources.py:367); [schema.py:90–105,192–218](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/schema.py:90); [model.py:23–59](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/model.py:23).

Retrieval and validation have no explicit cutoff or per-sense attestation check. Retrieval timestamps establish when data was fetched; they do not date a meaning, construction, or punctuation feature. Dictionary entries are admitted without a machine-enforced distinction between earlier evidence, later usage, and undated commentary.

**Consequence:** The specified historical boundary depends on the model or reader noticing a problem.

**Correction direction:** Record the operator's cutoff and each claim's cited attestation/date range. Keep unsupported or later attestations visible as ineligible for historical decoding. Modern references may locate earlier evidence; their publication date alone is not the relevant date of the usage.

## 4. P1 — Rule provenance and operator consent are trusted fields

**Evidence:** [model.py:139–144](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/model.py:139); [schema.py:192–218](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/schema.py:192); [ggsd.py:360–364](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/ggsd.py:360).

The model supplies nested rule objects. Validation does not verify that a source was retrieved, that the quotation appears in that retrieval, or that a `consented` status was assigned through an operator action. It principally checks required outer fields and elimination references. A schema error is attached to the primitive while processing continues.

**Offline reproduction:** A rule with a nonexistent source, an invented quotation, and `status="consented"` passed `validate_primitive`.

**Consequence:** A valid-looking record is not evidence that its provenance or consent has been checked. The current model output whitelist excludes eliminations, which limits the immediate effect, but does not enforce the claimed operator-only status boundary.

**Correction direction:** Keep consent in a driver-managed record. Validate rule types, source membership, quotations, and any elimination against that record.

## 5. P1 — Resume uses line numbers as word identities

**Evidence:** [ggsd.py:75–97,294–302,345–369](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/ggsd.py:75).

Checkpoint loading identifies a word by its JSONL line number. Failed words are excluded from completed records, but their lines remain. A successful retry is appended at the end, so its new line number is no longer its original word position. Completed words also initialize the output list before retried words are appended.

**Offline reproduction:** Starting with `A`, failed `B`, `C` loads completed positions `{0:A,2:C}`. Appending a successful retry of `B` then loads it at position 3. The output assembly can consequently become `A,C,B`.

**Consequence:** Resumption can repeat work, reorder words, or associate records with the wrong positions. Existing checkpoints are also not checked against the requested verse, source text, or model configuration before reuse.

**Correction direction:** Persist an explicit word index and input identity; replace the state for that index and assemble output in index order.

## 6. P1 — A returned run can contain failed decoding records

**Evidence:** [ggsd.py:345–364,392–438](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/ggsd.py:345); [run_harness.py:112–120](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/run_harness.py:112); [report.py:193–202](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/report.py:193).

Model exceptions become error-bearing primitives, schema failures are recorded, and processing proceeds into the final decoding and questions. The batch harness labels the run `ok` when the function returns. The clean decoding omits the explicit `_model_error`/`_schema_error` fields. Failed report checks are printed in prose without an aggregate incomplete status.

**Consequence:** “Finished” or “ok” can describe a returned artifact that still lacks valid word records or completed checks. Excluding model errors from a future checkpoint does not make the current run complete.

**Correction direction:** Distinguish finished, incomplete, failed, and validated states. Carry word failures and check status into the structured decoding and batch summary.

## 7. P1 — Dictionary retrieval commits to the first lemma

**Evidence:** [sources.py:279–298,321–327](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/sources.py:279).

When `/find` returns multiple parses, the code preserves the parse list but chooses `parses[0]["lemma"]` for dictionary-detail retrieval. It does not fetch the entries for every distinct candidate lemma.

**Consequence:** An alternative can remain listed grammatically while its lexical field never reaches the decoder. The ordering of the source response can therefore narrow the supplied evidence before operator review.

**Correction direction:** Fetch and retain each distinct candidate lemma with its supporting parse and provenance.

## 8. P1 — A detected dictionary-headword mismatch can remain unflagged

**Evidence:** [sources.py:329–365](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/sources.py:329).

For the small set of known problematic lemmas, the code checks a detail response against the expected headword and retries the surface form. If both lookups mismatch, it executes `pass` and retains the original detail. The comment says the model will see a mismatch note, but that branch adds no such note.

**Consequence:** Definitions for a different headword can continue through the pipeline as the expected lemma's evidence.

**Correction direction:** Emit a structured mismatch status containing both lookup keys and returned headwords; keep suspect entries separate from eligible evidence. Generalize the headword check beyond the two hardcoded overrides.

## 9. P1 — Mathematical normalization collapses distinct marked forms

**Evidence:** [math_layer.py:41–53,140–158](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/math_layer.py:41).

The matching key removes all accents and breathings before numeral recognition. Distinct marked forms therefore share keys and receive the same numeral proposal without recording the ambiguity created by normalization.

**Offline reproduction:** `ἐν` and `ἕν` both receive value 1; `ἐξ` and `ἕξ` both receive value 6.

**Consequence:** The mathematical record can introduce a numeric proposal solely because the matching key discarded distinctions present in the input. The rule remains marked proposed, but the lost distinction is not represented in the classification.

**Correction direction:** Preserve marked forms in candidate matching and require an appropriate candidate analysis before assigning a numeral value.

## 10. P2 — Canonically equivalent Unicode can produce different punctuation and accent records

**Evidence:** [punctuation.py:19–26,39–66,89–100](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/punctuation.py:19).

Punctuation lookup recognizes only particular code points. Accent processing decomposes individual characters rather than normalizing the complete input first; already-decomposed combining marks are consequently missed.

**Offline reproductions:**

- `τί;` records a gate; the equivalent Greek-question-mark spelling using U+037E records none.
- `λέγει·` records ano teleia; U+0387 records none.
- NFC `ἄνθρωπος` records acute accent and smooth breathing; its NFD form records neither.

**Consequence:** Encoding differences can change the punctuation/mathematical output without a change in the represented text.

**Correction direction:** Normalize a working representation, retain the original representation, and map equivalent punctuation explicitly.

## 11. P2 — Repetition from one source counts as source agreement

**Evidence:** [schema.py:133–150,156–183](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/schema.py:133).

Agreement is based on the length of a list of source identifiers. That list is not deduplicated.

**Offline reproduction:** Two identical translations with `source_id="same-source"` produce `agreement=true` and the source list `["same-source","same-source"]`.

**Consequence:** Duplicate model output can appear as corroboration. Even distinct dictionary identifiers do not establish independence of their underlying evidence.

**Correction direction:** Count distinct source identifiers, preserve the passages behind each claim, and describe agreement separately from independence.

## 12. P2 — Source excerpts are cut before the model sees them

**Evidence:** [sources.py:399,414](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/sources.py:399); [model.py:75–79](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/model.py:75); [ggsd.py:323–329](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/ggsd.py:323).

Retrieval retains at most 4,000 characters per dictionary entry; the model message reduces that to 400 characters per source; the word's provenance stores a 300-character preview. These are character slices, not sense-aware extracts, and there is no structured completeness flag or complete source snapshot in that word record.

**Consequence:** Later senses, qualifications, or citations can be absent from the supposedly open field. The retained preview may also be insufficient to recheck the exact material supplied to the model.

**Correction direction:** Save complete retrievals separately with stable identities; explicitly record any excerpt selection and omissions. Keep input-size management distinct from the claim that all eligible possibilities have been supplied.

## 13. P2 — Mathematical annotations are still heuristic and incompletely scoped

**Evidence:** [math_layer.py:86–130,134–166](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/math_layer.py:86); [punctuation.py:150–165](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/punctuation.py:150).

- Every μ-initial token is collected, although M4 describes function words; the offline probe tagged `Μαρία` as an M4 term.
- A καί equality records the immediately adjacent tokens, not parsed expression scopes.
- Gate following terms stop at a period or verse boundary. There is no cross-verse resolution in this function.
- M8 lists six return types, while the implementation emits `left-open`, `answered-in-scene`, or `continues`.
- Answer/speech detection depends on lemma hints and can change when the same text enters without MorphGNT hints.

**Consequence:** These records are useful proposed annotations, but do not yet establish a complete grammatical or mathematical derivation. Their proposed status should remain visible throughout downstream use.

**Correction direction:** Define coverage and scope explicitly, narrow token matching to the intended classes, and test the same printed input through both text-source paths.

## 14. P2 — Output identity is not sufficient for reproducible comparison

**Evidence:** [ggsd.py:195–203,276–278](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/ggsd.py:195); [report.py:223–228](/home/dylanmccapes/dev/GrammaticalGeometrySpaceDriver/report.py:223).

Run metadata says driver 0.0.3; the report footer is hardcoded to 0.0.1. The metadata shown here records an edition description but no source-file checksum, code revision, or rule-set hash. Resuming replaces run metadata with a new start time/configuration.

**Consequence:** A changed output cannot reliably be attributed to changed text, code, rules, or model configuration from those identifiers alone.

**Correction direction:** Record those identities at run creation, preserve them during resume, and render the report version from that same record.

## Verification performed

The review used static inspection plus small offline reproductions for question context, rule validation, duplicate-source agreement, Unicode punctuation/accents, numeral/μ classification, and checkpoint indexing. It also counted local run metadata by recorded edition. It did not run the full harness, estimate philological accuracy, or independently adjudicate the project's historical/mathematical hypotheses.

The earlier remote report's missing `bold` module is not asserted here as a current local import failure: `bold.py` now exists. The current reporting issue is how any failed check affects the declared run status.

```text
THIRKETHNEN 🔎
The questions may remain provocative and the model may answer them. The implementation should preserve the evidence supplied, the operator's authority over consent, and the distinctions the input actually carries.
 THIRKETHNEN?
```
