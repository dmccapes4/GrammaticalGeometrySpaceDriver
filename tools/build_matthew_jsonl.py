#!/usr/bin/env python3
"""
build_matthew_jsonl.py — Build matthew_verses.jsonl from the local MorphGNT file.

MorphGNT format (space-separated, 7 fields):
  BCVV  POS  parsing-tag  word-WITH-punct  word-no-punct  normalized  lemma

Field 3 (0-indexed) = word form WITH trailing punctuation marks.
Joining field-3 per verse gives the verse text with punctuation.

Output: tools/matthew_verses.jsonl
  {"verse_ref": "Matthew 1:1", "chapter": 1, "verse": 1, "greek_text": "...", "source": "morphgnt"}
"""

import json
from pathlib import Path

MORPHGNT = Path(__file__).parent.parent / "morphgnt" / "sblgnt" / "61-Mt-morphgnt.txt"
OUT      = Path(__file__).parent / "matthew_verses.jsonl"


def ref_to_label(ref: str) -> tuple[int, int, int]:
    """Convert '010101' to (book=1, chapter=1, verse=1)."""
    b = int(ref[0:2])
    c = int(ref[2:4])
    v = int(ref[4:6])
    return b, c, v


def main():
    verses: dict[str, list[str]] = {}
    order: list[str] = []

    with open(MORPHGNT, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 5:
                continue
            ref    = parts[0]            # e.g. '010101'
            word   = parts[3]            # word WITH trailing punct

            if ref not in verses:
                verses[ref] = []
                order.append(ref)
            verses[ref].append(word)

    print(f"Loaded {len(verses)} verses from MorphGNT.")

    records = []
    for ref in order:
        b, c, v = ref_to_label(ref)
        verse_label = f"Matthew {c}:{v}"
        greek_text  = " ".join(verses[ref])
        records.append({
            "verse_ref":  verse_label,
            "chapter":    c,
            "verse":      v,
            "morphgnt_ref": ref,
            "greek_text": greek_text,
            "source":     "morphgnt_sblgnt",
        })

    OUT.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
        encoding="utf-8"
    )
    print(f"Wrote {len(records)} verse records → {OUT}")

    # Show sample
    print("\nSample verses:")
    for r in records[:3]:
        print(f"  {r['verse_ref']}: {r['greek_text'][:80]}")
    print(f"  ...")
    print(f"  {records[-1]['verse_ref']}: {records[-1]['greek_text'][:80]}")


if __name__ == "__main__":
    main()
