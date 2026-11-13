#!/usr/bin/env python3
"""
GGSD batch harness runner.

Runs GGSD on a list of verses in order, with checkpoint/resume per verse.
Each verse gets its own run directory under runs/.
A batch summary is written to runs/harness_<slug>_<timestamp>/summary.md

Usage:
    python3 run_harness.py --verses Matthew1:1-10 --model claude-opus-4-5-20251101
    python3 run_harness.py --verses Matthew1:1-10 --model claude-opus-4-5-20251101 --dry-run
    python3 run_harness.py --verses Matthew1:1-10 --model ollama/dengcao/Qwen3-30B-A3B-Instruct-2507:Q4_K_M

Verse list options:
    Matthew1:1-10       first 10 verses of Matthew (1:1 through 1:10)
    Matthew4:10         single verse
    --verse-file <path> JSON array of verse refs, e.g. ["Matthew 1:1", "Matthew 4:10"]

MorphGNT:
    Automatically resolved to morphgnt/sblgnt/61-Mt-morphgnt.txt for Matthew verses.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

# ── resolve script location ───────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
MORPHGNT_MATTHEW = HERE / "morphgnt" / "sblgnt" / "61-Mt-morphgnt.txt"

# ── import ggsd run() ─────────────────────────────────────────────────────────
sys.path.insert(0, str(HERE))
from ggsd import run as ggsd_run


# ─── helpers ──────────────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat() + "Z"


def _morphgnt_for_verse(verse_ref: str) -> str:
    """Return the MorphGNT path for a verse reference, or '' if unknown."""
    book = verse_ref.strip().split()[0].lower() if verse_ref.strip() else ""
    if book in ("matthew", "matt", "mt"):
        if MORPHGNT_MATTHEW.exists():
            return str(MORPHGNT_MATTHEW)
    return ""


def _expand_range(spec: str) -> list[str]:
    """
    Expand a verse range spec into a list of 'Book C:V' strings.

    Formats:
        Matthew1:1-10   ->  ["Matthew 1:1", "Matthew 1:2", ..., "Matthew 1:10"]
        Matthew4:10     ->  ["Matthew 4:10"]
    """
    # Normalise: allow "Matthew 1:1-10" or "Matthew1:1-10"
    spec = spec.strip()
    # Insert space between book and chapter if missing
    spec = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", spec, count=1)

    m = re.match(r"([A-Za-z]+)\s+(\d+):(\d+)(?:-(\d+))?$", spec)
    if not m:
        print(f"WARNING: could not parse verse spec '{spec}'; treating as single verse ref")
        return [spec]

    book = m.group(1).capitalize()
    chapter = int(m.group(2))
    start = int(m.group(3))
    end = int(m.group(4)) if m.group(4) else start

    return [f"{book} {chapter}:{v}" for v in range(start, end + 1)]


# ─── batch run ────────────────────────────────────────────────────────────────

def run_batch(
    verses: list[str],
    model_id: str,
    dry_run: bool = False,
    stop_on_error: bool = False,
) -> None:
    ts = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
    slug = re.sub(r"[^a-zA-Z0-9]", "_", verses[0]) if verses else "empty"
    batch_dir = HERE / "runs" / f"harness_{slug}_{ts}"
    batch_dir.mkdir(parents=True, exist_ok=True)

    print(f"harness: {len(verses)} verse(s)")
    print(f"model:   {model_id}")
    print(f"batch:   {batch_dir}")
    if dry_run:
        print("[dry-run mode — no model calls]")
    print()

    results: list[dict] = []

    for i, verse_ref in enumerate(verses, 1):
        morphgnt_path = _morphgnt_for_verse(verse_ref)
        print(f"══ [{i}/{len(verses)}] {verse_ref} ══")
        if morphgnt_path:
            print(f"  MorphGNT: {morphgnt_path}")
        else:
            print(f"  MorphGNT: not found — will fall back to greekbible.com")

        try:
            run_dir = ggsd_run(
                verse_ref=verse_ref,
                model_id=model_id,
                dry_run=dry_run,
                morphgnt_path=morphgnt_path,
            )
            status = "dry-run" if dry_run else "ok"
            error = None
        except SystemExit as e:
            status = "error"
            error = str(e)
            run_dir = None
            print(f"  FATAL: {e}")
            if stop_on_error:
                print("  --stop-on-error set; aborting batch.")
                break
        except Exception as e:
            status = "error"
            error = str(e)
            run_dir = None
            print(f"  ERROR: {e}")
            if stop_on_error:
                print("  --stop-on-error set; aborting batch.")
                break

        results.append({
            "verse_ref":  verse_ref,
            "status":     status,
            "run_dir":    str(run_dir) if run_dir else None,
            "error":      error,
        })
        print()

    # ── summary ──────────────────────────────────────────────────────────────
    ok    = sum(1 for r in results if r["status"] in ("ok", "dry-run"))
    errs  = sum(1 for r in results if r["status"] == "error")

    summary_lines = [
        f"# Harness run — {ts}",
        f"",
        f"model: `{model_id}`  ",
        f"verses: {len(verses)}  ok: {ok}  errors: {errs}  ",
        f"",
        f"| # | Verse | Status | Run dir |",
        f"|---|-------|--------|---------|",
    ]
    for i, r in enumerate(results, 1):
        rd = Path(r["run_dir"]).name if r["run_dir"] else "—"
        err = f" `{r['error'][:60]}`" if r["error"] else ""
        summary_lines.append(
            f"| {i} | {r['verse_ref']} | {r['status']}{err} | `{rd}` |"
        )

    summary_lines += [
        "",
        "## Next step",
        "",
        "Run `criteria.py` against this batch to score each verse against the harness criteria.",
        "See `docs/GAMEPLAN_GGSD_HARNESS_10VERSE_20261110.md` for criterion definitions.",
    ]

    summary_md = batch_dir / "summary.md"
    summary_md.write_text("\n".join(summary_lines), encoding="utf-8")

    summary_json = batch_dir / "summary.json"
    summary_json.write_text(
        json.dumps({"ts": ts, "model": model_id, "results": results}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"batch done.  ok={ok}  errors={errs}")
    print(f"  summary: {summary_md}")
    print(f"  json:    {summary_json}")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="GGSD batch harness — run multiple verses in sequence."
    )

    verse_group = parser.add_mutually_exclusive_group(required=True)
    verse_group.add_argument(
        "--verses",
        help=(
            'Verse range, e.g. "Matthew1:1-10" or "Matthew4:10". '
            "Range format: BookC:V-V, e.g. Matthew1:1-10."
        ),
    )
    verse_group.add_argument(
        "--verse-file",
        metavar="PATH",
        help='JSON file containing an array of verse refs, e.g. ["Matthew 1:1", "Matthew 4:10"]',
    )

    parser.add_argument(
        "--model", required=True,
        help='Model ID, e.g. "claude-opus-4-5-20251101" or "ollama/..."',
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Tokenise each verse and exit without calling the model.",
    )
    parser.add_argument(
        "--stop-on-error", action="store_true",
        help="Abort the batch on first verse error (default: continue).",
    )

    args = parser.parse_args()

    if args.verse_file:
        path = Path(args.verse_file)
        if not path.exists():
            sys.exit(f"verse file not found: {path}")
        verses = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(verses, list):
            sys.exit("verse file must be a JSON array of strings")
    else:
        verses = _expand_range(args.verses)

    if not verses:
        sys.exit("no verses to run")

    print(f"verses expanded ({len(verses)}):")
    for v in verses:
        print(f"  {v}")
    print()

    run_batch(
        verses=verses,
        model_id=args.model,
        dry_run=args.dry_run,
        stop_on_error=args.stop_on_error,
    )


if __name__ == "__main__":
    main()
