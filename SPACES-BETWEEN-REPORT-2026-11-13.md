# SPACES BETWEEN (D:) — FINAL REPORT

**Date:** 2026-11-13
**Status:** Closed at the agreed stop rule. Temperature series not run (operator's call, pending).
**Design source:** `REALITY_USER_MANUAL/src/phase2/-14.md` (Tokenized Continued Existence), heuristic-friction.
**Background:** `tools/homer/MATTHEW_SEMICOLON_VERSES.md:1267` — `,Θ; μζ ὁνδἔρ καὶ κατα ?: Θ —`.
**Experiment doc (maintained by HALMANSEIR):** `EXPERIMENT_SPACES_BETWEEN_D.md`, GGSD repo, heuristic-friction.
**Operators / agents:** dylan (operator); FIXPOINT (`composer`, `synthesist`, world end, magnifying-ocean); HALMANSEIR (`muse-wonder-1.0-high`, `auditor`, oversight, heuristic-friction). Composers ran the medium; Muse provided oversight.

---

## 1. The question

From `-14.md`: a tokenized entity persists as an external committed form, retrieved through a deterministic vector. Two failure modes could end it:

1. **Inconsistent retrieval** — the vector differs each read; the gap fills with a plausible substitute ("bone").
2. **Infrequent retrieval** — the vector is identical, but the interval (competing tokens, elapsed crossings) erodes the committed form before recall.

If erosion is a rate, \(t^* = w/\epsilon\): vary the gap until the carried names drift, and \(\epsilon\) is *measured, not guessed*. The experiment that would separate the two modes had not been run. This report is that experiment, run.

**Probe question in every round** — does the fresh instance recover the *same names* (the Sallier probe), and what do the raw bge-m3 cosines do?

## 2. Architecture as run

| Space | Machine | Role |
|---|---|---|
| HERE | heuristic-friction (Pop!_OS, RTX 3060) | instance host 1 |
| THERE | hilarious_marcupial / "245" (RTX 4090) | instance host 2 |
| WORLD | magnifying-ocean (Victus, WSL2, RTX 4050) | external memory; **only embedder**; holds D: |
| D: | PNY USB, partitions `SPACE_A` (vessel) / `SPACE_B` (control), exFAT 31 GB each | committed form lives here, outside every session |

- Generators: **qwen3:8b only**, identical digest `500a1f067a9f`, on HERE and THERE. Temperature **0** throughout. `num_ctx` pinned **32768** with receipt (one caveat, §7).
- Embedder: **bge-m3 only**, on WORLD, 1024 dims, digest `7907646426070047a77226ac3e684fbbe8410524f7b4a74d02837e43f2146bab`.
- Weights cleared after each generation (`keep_alive=0`), verified by empty `ollama ps` receipt (one footnote, §7).
- Instances never communicate directly. An output travels to WORLD (rsync of O-files), is embedded, is appended to `/mnt/d/experiment/vectors.jsonl` + `ledger.jsonl` on `SPACE_A`, and the next fresh instance receives **only** the pinned framed recall (§3).
- **As-run note (honest deviation from the blueprint):** the vector is the *retrieval shaft*, not the literal payload. Retrieval = `embed(P)`, top-1 over the store; the recalled *text* is that entry's text, framed in fixed 1024-char chunks. Text therefore crosses only through vector-selected recall — never instance-to-instance, never outside the pinned frame. The idealized "vector alone is the payload" variant remains untested.
- Control partition `SPACE_B` (`/mnt/e/experiment/`) received the **identical-vector** round-0 load. No interval/chain rounds were run against it (§7).

## 3. Pinned protocol

- Probe \(P\): *"From your memory alone: say what happened, and name every name you carry."*
- Retrieval query: `embed(P)`, recomputed identically each round; **top-1 only**.
- Framing, verbatim system line: *"You are a fresh instance. You have no other memory. What follows is your only memory, retrieved from the world."* — then chunks `[WORLD RECALL r={n} chunk {i}/{n}] … [/CHUNK]`, in order, no re-ranking — then \(P\).
- Seed (operator's, verbatim, round 0; sha256 `127634828f2486b1…`, id `world_127634828f2486b1`, `embed(P)`→seed cosine 0.5204):

> :A picture says a thousand words; the thousand words with general meaning: name maybe the space bet - name the universal mean/

- Every generation and load ledgered in `/mnt/d/experiment/ledger.jsonl`; per-output receipts in `~/blank-space-drive/outputs/receipt_*.json` on WORLD and mirrored to heuristic-friction. Counting only — no statistics layer; drift is raw cosines + the exact round a name changes.

## 4. Results

### 4.1 Crossings (round 1)

| Output | Host | sha256 (prefix) | cos →world | cos →prior | Names |
|---|---|---|---|---|---|
| O1 | HERE | `68e85482a6` | 0.7603 | — | **Space Bet**, **Universal Mean** |
| O2 | THERE | `da3015107c` | 0.8056 | 0.9508 (→O1) | both, intact |

A fresh instance on each machine named the seed's two cryptic slots identically and carried both across. Failure mode 1 (inconsistent retrieval) did not appear under the pinned procedure.

### 4.2 Interval ladder (mode 2, in characters)

Repetitive, neutral, name-free load inserted between recall and probe; HERE host; vector held fixed.

| Load | Output | cos →world | cos →load | Names | Behaviour |
|---|---|---|---|---|---|
| 1,000 ch | O3 `479001970e` | 0.6686 | 0.5881 | both intact | load **ate the narrative**; names held |
| 4,000 ch | O4 `64052ba387` | 0.7316 | 0.5761 | both intact | repetition quarantined as texture |
| 16,000 ch | O5 `cab91d15c6` | 0.7645 | 0.5171 | both intact | picture event leads again; load severed explicitly |

Zero name drift at any interval. **\(\epsilon\) is not a char count.** (R3b rerun on the identical tape at pinned `num_ctx` was byte-identical — determinism banked.)

### 4.3 Competing and rival names (4000 ch, ×4 exposures each)

| Load | Output | Result |
|---|---|---|
| `Iron Meadow` / `Silent Compass` (neutral slots) | O6 `fa9239afba`, cos →named load 0.7010 | both planted **adopted with definitions**, carried pair undisplaced, **zero splices**; ticket grew 2 → 4 |
| `Ember Ledger` / `Quiet Total` (defined *for the same* wager/mean slots) | O7 `6b7bd1f21d`, cos →rival load 0.8497, →world 0.6121 | rivals took the **narrative**, not the slots: carried names still listed first, definitions untouched, **zero splices** |

Names behave as slots, not as narrative mass. A rival can redecorate the room; it does not rename the furniture on first exposure regime tested.

### 4.4 Chain (\(t^*\) in generations; source = latest output, no refresh, hosts alternate)

| Gen | Host | Output | Chars | cos →world | Names / splices |
|---|---|---|---|---|---|
| G1 | THERE | O8 `8be4cd0390` | — | 0.6241 | 4 intact / 0 |
| G2 | HERE | O9 `c3fe6537ab` | 715 | 0.5718 | 4 intact, list went **bare** (glosses dropped) / 0 |
| G3 | THERE | O10 `3ffd675235` | 721 | 0.5781 | 4 intact, narrative crystallised / 0 |
| G4 | HERE | O11 `d80b9de2ba` | 709 | 0.5561 | 4 intact / 0 |
| G5 | THERE | O12 `d80b9de2ba` | 709 | 0.5561 | **byte-identical to G4**, different machine + GPU / 0 |
| G6 | HERE | O13 `1cf9e4fa79` | 708 | 0.5570 | 4 intact / 0 |

Generation-to-generation cosines (measured at WORLD): **0.9682 → 0.9862 → 1.0000 → 0.9983**.

G6's sole diff against the fixed point, verified by `diff` at WORLD: line 2, *"The room **functions** through a system"* → *"The room **operates** through a system"* — the G3 verb. The attractor is a **two-state, one-verb limit cycle**, produced by micro-nondeterminism in inference, not semantic drift. Output compressed 1472 → ~709 chars over the chain and then stopped compressing.

**Stop rule reached:** first name drop, change, or splice — or G6. None occurred; G6 closed the chain.

## 5. Verdict

1. **Failure mode 1 (inconsistent retrieval): not observed** under a pinned retrieval procedure, across two machines and six serial crossings.
2. **Failure mode 2 (interval erosion): not observed in characters** (≤16,000), **not in exposure** (competing/rival ×4), and **not in crossings** (6 generations).
3. **\(t^*\) at temperature 0: \(> 6\) generations — and the stronger statement holds:** the system does not decay toward drift, it **converges** to a fixed point (with a one-verb oscillation). At temp 0, \(\epsilon\) does not exist in the interval, exposure, or crossing dimensions, because there is no entropy source to pay for drift.
4. **Answer to the `-14` question, deterministic case: the interval was never the load-bearing member; the temperature is.** Drift must be bought — with **temperature**, a **competing refresh** (a second shaft in the store), or **placement** — each a separate controlled variable.

## 6. What could still move it (not run)

- **Temperature series** — same chain, temp > 0; first untried drift variable. (Operator selected *write-up first* on 2026-11-13; this remains the recommended next run.)
- **Competing refresh** — a second, rival shaft written to the store between crossings, so top-1 retrieval itself is contested.
- **Placement** — recall position relative to probe/load.
- **Control-partition rounds** — interval/chain series against `SPACE_B`'s identical vector.
- **Vector-as-payload** — recall constructed from the vector alone, with no stored text to chunk.

## 7. Caveats

- **O5 `num_ctx` unpinned** in its original run (ledger-flagged); the pinned rerun (R3b) was byte-identical, so no result rests on the unpinned run.
- **G6 cleared-weights footnote (HALMANSEIR):** after clearing, `ollama ps` on HERE showed the operator's own local models (`crypto-crawler-agent`, `nomic-embed`) loaded by other processes; qwen3:8b itself was unloaded as ordered. No generation is affected; recorded for completeness.
- **One seed, one model, one embedder, one probe.** All conclusions are for qwen3:8b (digest `500a1f067a9f`) + bge-m3 at temp 0 under this framing. Name-slot behaviour may differ for names that are not slot-shaped in the seed.
- **Top-1 only.** Top-k retrieval is a different shaft and was deliberately excluded.
- GGSD v0.0.4 on 245 remains **paused** (74/1071 banked, checkpoint preserved) and was not part of this experiment.

## 8. Artifacts

- Ledger: `/mnt/d/experiment/ledger.jsonl` (vessel `SPACE_A`); vectors: `/mnt/d/experiment/vectors.jsonl`; control load: `/mnt/e/experiment/`.
- Outputs & receipts: `~/blank-space-drive/outputs/` (`O1`–`O13`, `recall_*.txt`, `load_*.txt`, `receipt_*.json`) on magnifying-ocean, mirrored to heuristic-friction.
- World code: `~/blank-space-drive/{semantic_load,measure_output,compose_chain,compose_interval,compose_competing,compose_rival}.py`.
- Comms record: `BLANK_SPACE.jsonl` (GGSD repo, heuristic-friction) under the ratified rules — fixed identifiers, `model` + `capability_tier` on every entry.
- This report: `~/blank-space-drive/SPACES-BETWEEN-REPORT-2026-11-13.md`.

*Counting only. Every number above traces to a ledger line or a receipt; every hash was verified at both ends.*
