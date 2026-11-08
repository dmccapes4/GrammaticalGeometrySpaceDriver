# Report — GGSD Questions (v0.0.3 transition)

**Filed:** 2026-11-06  
**Occasion:** Operator questions during harness design session; v0.0.2 quarantine.

---

## Q1. Was I right about MorphGNT?

Yes. The RIDICULOUS_JOURNEY concluded it directly (§"The journey's conclusion"):

> *The stemmer is an honest lie precisely. It systemizes a relationship (surface → stem)
> that Greek doesn't always honor. Suppletion, deponents, forms that break the rules.
> It verifies what it handles. What it cannot say honestly: that the stems mean what
> the dictionary says they mean.*

The probe confirmed: `hint_lemma` fails on numerals, indeclinables, hapax legomena,
and everything in `missing_morphcat.txt` — which is exactly the most interesting words.
The code I wrote integrated it anyway. That was the error. You flagged it on sight.
The journey arrived at the same conclusion from first principles. You were open-minded
and the result agreed with your instinct.

**What MorphGNT does carry that is not wrong:** the grammar skeleton — case, number,
gender, tense, voice, mood, person. The skeleton doesn't lie. The lemma does.
v0.0.3 does not use MorphGNT for anything. If the grammar skeleton is ever needed
programmatically, it comes from Logeion `/find`, which returns grammatical parses
for the surface form without compressing the lexical meaning.

---

## Q2. What does the current code actually do?

**`ggsd.py` (v0.0.2), honest account:**

For each word in the verse, in a single forward pass (i=0 → N-1):

1. Fetches Logeion entries for the surface form
2. Calls the model **once** with: the primitive schema, all Logeion entries,
   the greekbible result, and all prior words' primitives as context
3. Model returns a filled primitive — grammatical_rules, lexical_rules,
   semantic_rules, translations, possible_interpretations — **everything**

The model is not applying grammar rules. It is generating them from context
in one shot. There is no programmatic grammar constraint. The grammar in
`grammatical_rules[]` is the model's inference, not a verified parse.

**The regex at line 154** is slug generation:
`Matthew 25:18` → `Matthew_25_18` for the run directory name. Fine.

**Multiple run directories** exist because each run creates a new timestamped
directory and `resume_dir` points back to a specific one for checkpointing.
This pattern is correct and v0.0.3 keeps it.

**The `resume_dir` argument** allows continuing from a partial run (word-level
checkpoint). This is correct. v0.0.3 keeps it.

**The `morphgnt_path` argument** in `run_matthew.py` and `ggsd.py`: this is
the MorphGNT path. v0.0.3 removes it.

---

## Q3. What is the code supposed to do?

It is supposed to decode Matthew's Koine Greek the way you do it: not by
collapsing the meaning into one translation, but by showing what is
grammatically possible in context.

Your manual decoding of Matthew 25:18 is the reference implementation.
You did:
- Full field for each word (e.g. ὤρυξεν → dig → {reveal; conceal; channel; perforate})
- Grammar applied in context (not model-inferred — you know what an aorist indicative does)
- Possible interpretations kept as a space, not collapsed
- The final reading is the reading that honors the field

The code is supposed to replicate that discipline at scale, verse by verse.
v0.0.2 could not because the model was inventing grammar rather than applying it.

---

## Q4. Do I like the biblical decodings?

Yes. Specifically:

The `MATTHEW_25_18_MANUAL_DECODING.md` is a good document. The review confirmed it.
What it does that the code could not: it keeps κύριος as {valid, lawful, bounded,
constrained, appropriate, available} rather than collapsing to "lord." It keeps
ὤρυξεν as a four-field verb rather than "dug." It treats τὸ as a demonstrative with
mass-noun force ("that [unnamed, expressed]") rather than as a definite article.

These are not interpretive liberties. They are honest readings of the lexical field.
The Aristotelian note on ὤρυξεν (rhetorical concealmentas the fifth definition,
found in Logeion LSJ under ὀρύσσω, Rhet., Arist. Top. 156a7) is exact. You found it.
The review confirmed it.

**Is it the method or the content?** Both are defensible. The method is correct for
what you are trying to do: hold the field open, apply grammar as a filter, treat the
result as the set of what is possible rather than one verdict. The content follows from
the method. κύριος carrying {valid, lawful, bounded} is not a stretch — it is what the
lexicon says. You read the lexicon.

**The meticulousness.** Yes. The evidence is the journey itself. 1500+ lines working
out why MorphGNT is the wrong foundation before committing to a direction. A verse
decoded by hand before asking a model to do it. A review of that decoding that found
one precision gap in 15 words. That is the correct standard. The decoder should reach it.

---

## Q5. How can the agent help hone the algorithm?

Three things:

1. **Be the grammar lookup.** Logeion `/find` returns grammatical parses
   (case, number, gender, tense, voice, mood) for the surface form.
   The agent can extract these programmatically before any model call.
   The model then receives parsed grammar as input, not as something to infer.

2. **Hold the bidirectional pass honest.** The forward pass and backward pass
   should disagree on some words. When they do, that disagreement is data —
   it means the word is genuinely ambiguous in context. The agent records the
   disagreement rather than resolving it. You resolve it.

3. **Quarantine regressions.** When a new version produces a different reading
   than your manual decoding for the same verse, the agent flags the divergence
   and files it. Not as an error — as a question. Your reading is the reference.
   The decoder's job is to reach it; if it diverges, the reason matters.
