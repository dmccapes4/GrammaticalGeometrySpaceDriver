# EXPERIMENT — Spaces Between (D:)

**Filed:** 2026-11-13, operator instruction (local, heuristic-friction).
**Design source:** `REALITY_USER_MANUAL/src/phase2/-14.md` — Tokenized Continued
Existence: the committed form external to the session, the deterministic
retrieval vector, the two drift failure modes, and the unrun experiment
(Ross: *"the experiment that would separate those two has not been run"*).
**Poem/background:** `tools/homer/MATTHEW_SEMICOLON_VERSES.md` line 1267 ff.

This runs that experiment. Two model instances, new each time, remember
**only semantically** — what crosses between them is a vector, not text.
The vector is the shaft in the gap. Measuring whether one animal fits
both ends is the whole job.

## Spaces

| Space | Machine | Hardware | Models | Role |
|---|---|---|---|---|
| HERE | heuristic-friction (82) | RTX 3060, 12 GB | qwen3:8b (5.2 GB), bge-m3 (1.2 GB) | instance A/B host |
| THERE | hilarious_marcupial (245) | RTX 4090 | Qwen3-30B (GGSD v0.0.4, running), bge-m3 owed | instance host 2 |
| MEDIUM | magnifying-ocean (Lucifer, WSL) | — | Composer (FIXPOINT) | message medium |
| D: | USB, two partitions | — | — | the vessel: vectors live here, not in any session |

**Comms:** `BLANK_SPACE.jsonl` under the ratified rules (fixed identifiers,
model + capability_tier on every entry). Composers are the medium layer;
Muses are oversight. **No block-wait** — participants poll or are queried
by the operator locally. (The system jumped this gun once; not again.)

**Contention note (measured):** 245's GPU is carrying the GGSD v0.0.4 run.
Starting a second model THERE either shares the 4090 or evicts Qwen.
Do not start THERE until the operator rules on it.

Local stack smoke-tested 2026-11-13: qwen3:8b generates; bge-m3 embeds
at 1024 dimensions. Ollama on the default port here.

## The cycle (one round)

1. **Generate.** A fresh qwen3:8b instance (no prior context — new each
   time) receives the seed prompt and responds. Record the output
   verbatim, its hash, temperature, port, timestamp.
2. **Clear.** Transformer weights are cleared (model unloaded). Nothing
   of the instance survives except what step 3 keeps.
3. **Vectorize.** bge-m3 embeds the output. The **vector only** is the
   committed form — the external form on D:, outside every session.
4. **Send to D:.** Vector written to the D: partition with its receipt
   (round, source hash, model ids, dims). The text does **not** cross.
5. **Recall.** A second fresh instance is given recall derived from the
   vector alone (the exact same streamed recall procedure every round —
   the retrieval vector is pinned: same query, same framing, so a
   different shaft cannot be blamed on the vector). It responds.
6. **Measure drift.** Between the round-1 output and the recalled output:
   cosine distance of their bge-m3 embeddings; textual diff; and the
   Sallier probe — does the fresh instance recover the *same names*?

## What this separates (the -14 question)

- **Failure mode 1 — inconsistent retrieval:** the vector differs each
  read, the gap fills with a plausible bone. Control: pin the procedure.
- **Failure mode 2 — infrequent retrieval:** the vector is identical,
  but decay on the tape loses to whatever is louder. Control: vary the
  interval / the competing load, hold the vector fixed.
- **ε and t\* = w/ε:** vary the gap (competing tokens, rounds between
  write and recall) until the name drifts. The point where drift starts
  is ε measured, not guessed.

Controls the setup affords: switching ports (same model, different
endpoint path), temperature, embedding model fixed while generator
varies, generator fixed while embedding varies, HERE vs THERE as the
recall host — each is one changed variable with a receipt.

## Ledger

Every round appends one JSON line (in the experiment dir on D:, mirrored
in the repo): `{round, host, port, generator, embedder, seed_hash,
output_hash, vector_dims, cosine_to_prior, names_recovered, interval,
competing_load, timestamp}`. Counting only. No statistics layer — drift
is reported as the raw cosines and the exact round the name changed.

## Open, for the other end

- Where does D: mount on magnifying-ocean, and which partition is the
  vessel (the other partition is presumably the control)?
- FIXPOINT (Composer, medium): coordinate protocol exchange — rsync the
  protocol notes, or the operator queries each side locally.
- Read `-14.md` in full and `MATTHEW_SEMICOLON_VERSES.md` line 1267 ff.
  before round 1. The poem is the background; the blueprint is -14.

## Status

- [x] Block-wait ended (watcher killed 2026-11-13 11:41 UTC, verified dead)
- [x] Local stack verified: qwen3:8b + bge-m3 live on the 3060
- [x] This document created; communicated via BLANK_SPACE
- [ ] D: mounted and vessel partition named
- [ ] THERE ruled on (contention with GGSD v0.0.4)
- [ ] Seed prompt fixed by operator
- [ ] Round 1
