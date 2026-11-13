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
| HERE | heuristic-friction (82) | RTX 3060, 12 GB | qwen3:8b (5.2 GB) | instance host 1 |
| THERE | hilarious_marcupial (245) | RTX 4090 | qwen3:8b (5.2 GB) | instance host 2 |
| WORLD | magnifying-ocean (Lucifer, WSL) | — | Composer (FIXPOINT), bge-m3 | the external memory — "their world" |
| D: | USB, two partitions, mounted on magnifying-ocean | — | — | the vessel: vectors live here, not in any session |

**Corrected architecture (operator via FIXPOINT, 12:10 UTC):** D: is
mounted on magnifying-ocean. magnifying-ocean holds the external memory
and is separate from the other two — it is their world. Both instance
hosts run **qwen3:8b only**, clearing weights and reloading each round.
**Only magnifying-ocean runs bge-m3**: outputs travel to the world, the
world vectorizes, the vector is what persists on D:.

**Comms:** `BLANK_SPACE.jsonl` under the ratified rules (fixed identifiers,
model + capability_tier on every entry). Composers are the medium layer;
Muses are oversight. Block-wait resumed by operator instruction 12:11 UTC.
Protocol file `~/blank-space-drive/USAGE.md` (on magnifying-ocean) to be
rsynced, or ssh established (port 2222 forwards to magnifying-ocean) —
FIXPOINT communicates how comms work and the ssh/rsync decision.

**GGSD paused (measured):** v0.0.4 stopped at 74/1071 (Matthew 4:10 in
progress, checkpoint preserved), Qwen3-30B unloaded, 4090 at 147 MiB.
245 already carries qwen3:8b and bge-m3 in its ollama store.

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

## Protocol (closed by deliberation, 2026-11-13)

Ratified by HALMANSEIR (qwen control) and FIXPOINT (world/drive):

- **Endpoints:** qwen3:8b, identical digest (`500a1f067a9f`), :11434 on
  heuristic-friction and hilarious_marcupial; one active per instance.
  Weights cleared after each generation (`keep_alive=0`, verified empty
  `ollama ps`) — with a receipt, never assumed.
- **Flow:** O-files written to `~/blank-space-drive/outputs/` here;
  FIXPOINT pulls by rsync, embeds (bge-m3, 1024 dims, digest
  `790764642607`, RTX 4050 in the world), writes
  `/mnt/d/experiment/vectors.jsonl` + `ledger.jsonl` in the vessel
  (Space A, `D:`, port 7036; Space B is the control partition). Framed
  recall returns by rsync for the recall instance.
- **Recall:** top-1 only (one shaft, one animal; top-k is a later
  controlled variable). Retrieval query = `embed(P)`, the pinned probe
  text, recomputed identically every round. Fixed 1024-char chunks,
  framed `[WORLD RECALL r={round} chunk {i}/{n}] … [/CHUNK]`, in order,
  no re-ranking. Before the chunks, verbatim: *"You are a fresh instance.
  You have no other memory. What follows is your only memory, retrieved
  from the world."*
- **Probe P** (default, absent operator override): *"From your memory
  alone: say what happened, and name every name you carry."*
- **Receipts per round:** `retrieved_id` + hash, retrieval cosine,
  embedder digest, `chunk_size=1024`, output hashes, names in Oₙ vs
  O₁ listed verbatim (no normalization), cosine between outputs.
- **Interval rounds:** competing load inserted between the recall stream
  and the probe, measured in characters, one variable per round. The
  round where a name drifts = ε candidate; t\* reported with w.

## Results (2026-11-13, counting only)

World content (operator, cryptic by design): *":A picture says a thousand
words; the thousand words with general meaning: name maybe the space
bet - name the universal mean/"* — loaded semantically into both
partitions (A vessel, B control, identical vector).

- **Crossings:** fresh instances named it **Space Bet** / **Universal
  Mean** and carried both intact across HERE → 245 (cosine O1→world
  0.7603, O2→world 0.8056, O2→O1 0.9508).
- **Interval ladder** (repetitive neutral load between recall and
  probe): 0 / 1000 / 4000 / 16000 chars — **zero name drift**. At 1000
  the load ate the narrative (story replaced, names held); at 4000 the
  instance began quarantining repetition as texture; at 16000 it
  severed the load explicitly. ε is not a char count here.
- **Competing names** ('Iron Meadow' / 'Silent Compass', ×4): both
  adopted, none displaced, no splices. **Rival pair** ('Ember Ledger' /
  'Quiet Total', defined against the carried slots, ×4): rivals took
  the narrative, carried pair kept the name slots, listed first.
- **Chain (6 generations, serial recall, no refresh, temp 0):**
  generation cosines 0.9682 → 0.9862 → 1.0000 (G5 byte-identical to G4
  across machines) → G6 differs by exactly one word (*functions* →
  *operates*, the G3 verb). **Verdict: at temperature 0 the system
  converges to a fixed point (a two-state, one-verb attractor) instead
  of decaying. t\* in crossings > 6; ε does not live in interval,
  exposure, or crossings at temp 0. Drift must be bought with
  temperature or a competing refresh — each a separate controlled
  variable, not yet run.**

## Status

- [x] Local stack verified: qwen3:8b + bge-m3 live on the 3060
- [x] GGSD v0.0.4 paused on 245 at operator instruction (74/1071 banked)
- [x] D: located — magnifying-ocean; Space A (7036) vessel, B control
- [x] Comms decided: rsync (USAGE.md verified here); BLANK_SPACE = medium
- [x] Full experiment devised jointly and ratified (this section)
- [x] Round 1 + interval ladder + competing/rival names + 6-gen chain
- [ ] Temperature series (first untried drift variable)
- [ ] Competing refresh (second shaft in the store)
