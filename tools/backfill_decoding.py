#!/usr/bin/env python3
"""
backfill_decoding.py — rebuild verse_grammatical_decoding.json for a
completed run WITHOUT any model calls.

What it repairs (review 2026-11-11):
  - 0.0.2-era verses: decoding gains punctuation blocks, cadence_map,
    mark_counts, gates, equations (deterministic layers, driver 0.0.3).
  - All eras: decoding gains status / incomplete_words (#6), and words
    are re-assembled in stored word-index order (#5).

What it does NOT repair: Q1/Q2 answers (model calls; separate pass) and
the word primitives themselves (they were never the defect).

Usage:
  .venv/bin/python tools/backfill_decoding.py RUN_DIR [RUN_DIR ...]
  .venv/bin/python tools/backfill_decoding.py --all runs/   # every verse dir

Writes decoding.backfill.json ALONGSIDE the original (never overwrites);
diff it, then replace when satisfied. Exit 1 if any dir fails.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sources import load_morphgnt, morphgnt_verse_tokens
from punctuation import tokenise_morph_tokens, punctuation_block
from ggsd import _build_decoding_json

MORPH_CANDIDATES = [
    ROOT / "morphgnt" / "sblgnt" / "61-Mt-morphgnt.txt",
    ROOT / "tools" / "sblgnt" / "Matthew-morphgnt.txt",
]


def load_primitives(run_dir: Path) -> list[dict]:
    prims = []
    with (run_dir / "verse.jsonl").open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = json.loads(line)
            if p.get("_model_error"):
                continue  # not a completion (A8); a resume will retry it
            prims.append(p)
    # Stored word index is the identity (#5); fall back to file order.
    prims.sort(key=lambda p: p.get("word", {}).get("index", 1 << 30))
    return prims


def backfill(run_dir: Path, morph_data) -> dict:
    meta = json.loads((run_dir / "run_meta.json").read_text(encoding="utf-8"))
    verse_ref = meta["verse_ref"]
    _, rest = verse_ref.split(" ", 1)
    ch, vs = (int(x) for x in rest.split(":"))
    prims = load_primitives(run_dir)
    morph_tokens = morphgnt_verse_tokens(morph_data, ch, vs) if morph_data else []
    punct_tokens = tokenise_morph_tokens(morph_tokens) if morph_tokens else []
    for i, p in enumerate(prims):
        if i < len(punct_tokens) and not p.get("punctuation"):
            p["punctuation"] = punctuation_block(punct_tokens[i])
    out = _build_decoding_json(verse_ref, meta.get("model_id", "?"), prims,
                               punct_tokens=punct_tokens or None)
    out["backfilled"] = True
    out["backfill_note"] = ("deterministic layers rebuilt 2026-11-12; "
                            "word primitives and Q1/Q2 unchanged")
    (run_dir / "decoding.backfill.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"run": run_dir.name, "verse": verse_ref, "words": out["word_count"],
            "status": out["status"], "gates": len(out.get("gates", []))}


def main() -> int:
    args = sys.argv[1:]
    dirs: list[Path] = []
    if args[:1] == ["--all"]:
        base = Path(args[1]) if len(args) > 1 else ROOT / "runs"
        dirs = sorted(d for d in base.glob("Matthew_*") if (d / "verse.jsonl").exists())
    else:
        dirs = [Path(a) for a in args]
    morph_path = next((p for p in MORPH_CANDIDATES if p.exists()), None)
    morph_data = load_morphgnt(morph_path) if morph_path else None
    if not morph_data:
        print("WARNING: no MorphGNT file found; punctuation backfill skipped", file=sys.stderr)
    fails = 0
    skipped = 0
    for d in dirs:
        if not (d / "run_meta.json").exists():
            skipped += 1
            print(f"  skip {d.name}: no run_meta.json (incomplete or smoke run)")
            continue
        try:
            r = backfill(d, morph_data)
            print(f"  ok {r['verse']:>15} words={r['words']:>3} gates={r['gates']} status={r['status']}")
        except Exception as e:
            fails += 1
            print(f"  FAIL {d.name}: {e}", file=sys.stderr)
    print(f"{len(dirs) - fails - skipped}/{len(dirs)} backfilled, {skipped} skipped "
          "-> decoding.backfill.json (originals untouched)")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
