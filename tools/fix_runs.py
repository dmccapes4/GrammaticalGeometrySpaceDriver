#!/usr/bin/env python3
"""fix_runs.py — three operations:
1. Quarantine empty dry-run directories (no verse.jsonl or zero-byte).
2. Normalize questions: for runs with questions_v2.jsonl, overwrite questions.jsonl
   with v2 content and delete questions_v2.jsonl.
3. Regenerate report.md for every real run, now including Q1/Q2.

Usage:
    python3 tools/fix_runs.py [--dry-run]
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
RUNS_DIR = HERE / "runs"
QUARANTINE_DIR = RUNS_DIR / "_dry_run_quarantine"

sys.path.insert(0, str(HERE))
from report import write_report


def main(dry_run: bool = False) -> None:
    print(f"runs dir: {RUNS_DIR}")
    print(f"dry_run: {dry_run}")
    print()

    quarantined = normalized = regenerated = 0

    for d in sorted(RUNS_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("_") or d.name == "matthew_full":
            continue

        verse_jsonl = d / "verse.jsonl"
        is_real = verse_jsonl.exists() and verse_jsonl.stat().st_size > 10

        # ── 1. Quarantine empty dirs ──────────────────────────────────────────
        if not is_real:
            if not dry_run:
                QUARANTINE_DIR.mkdir(exist_ok=True)
                shutil.move(str(d), str(QUARANTINE_DIR / d.name))
            print(f"  quarantine: {d.name}")
            quarantined += 1
            continue

        # ── 2. Normalize questions ────────────────────────────────────────────
        q_v2   = d / "questions_v2.jsonl"
        q_main = d / "questions.jsonl"

        qa_results: list[dict] = []

        if q_v2.exists():
            # v2 is the correct grammar-first questions — promote to primary
            if not dry_run:
                shutil.copy2(str(q_v2), str(q_main))
                q_v2.unlink()
            print(f"  normalize:  {d.name}  (v2 → questions.jsonl, v2 deleted)")
            normalized += 1

        if q_main.exists():
            for line in q_main.read_text(encoding="utf-8").strip().splitlines():
                if line.strip():
                    try:
                        qa_results.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

        # ── 3. Regenerate report ──────────────────────────────────────────────
        decoding_path = d / "verse_grammatical_decoding.json"
        meta_path     = d / "run_meta.json"
        report_path   = d / "report.md"

        if not decoding_path.exists():
            print(f"  skip regen: {d.name}  (no decoding.json)")
            continue

        decoding  = json.loads(decoding_path.read_text(encoding="utf-8"))
        run_meta  = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        verse_ref = decoding.get("verse_ref", d.name)
        words     = decoding.get("words", [])

        # Reconstruct minimal primitives from decoding words for report writer
        primitives = []
        for w in words:
            p = {
                "word": {"surface": w.get("surface", "?"), "letters": list(w.get("surface", "?"))},
                "description": w.get("description", ""),
                "grammatical_rules": w.get("grammatical_rules", []),
                "lexical_rules": w.get("lexical_rules", []),
                "semantic_rules": w.get("semantic_rules", []),
                "possible_interpretations": w.get("possible_interpretations", []),
                "translations": w.get("translations", []),
                "edges": w.get("edges", []),
                "eliminations": [],
                "source_retrievals": {},
                "source_agreements": [],
            }
            primitives.append(p)

        if not dry_run:
            write_report(
                verse_ref=verse_ref,
                run_meta=run_meta,
                primitives=primitives,
                output_path=report_path,
                greek_text="",
                qa_results=qa_results if qa_results else None,
            )
        print(f"  regen:      {d.name}  ({len(qa_results)} Q entries)")
        regenerated += 1

    print()
    print(f"quarantined: {quarantined}  normalized: {normalized}  regenerated: {regenerated}")
    if dry_run:
        print("(dry-run — no files changed)")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    main(dry_run=dry)
