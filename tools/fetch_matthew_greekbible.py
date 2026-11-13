#!/usr/bin/env python3
"""
fetch_matthew_greekbible.py — Fetch every verse of Matthew from greekbible.com
and store as JSONL. One JSON object per line. One line per verse.

Output: tools/matthew_verses.jsonl

Resume-safe: skips verses already in the file.
Rate-limited: 1 request/sec to be polite.
"""

import json
import sys
import time
from pathlib import Path

# Add parent dir so we can import sources.py
sys.path.insert(0, str(Path(__file__).parent.parent))
from sources import fetch_greekbible

OUT = Path(__file__).parent / "matthew_verses.jsonl"

# Matthew chapter verse counts (standard)
MATTHEW_CHAPTERS = {
    1: 25, 2: 23, 3: 17, 4: 25, 5: 48, 6: 34, 7: 29,
    8: 34, 9: 38, 10: 42, 11: 30, 12: 50, 13: 58, 14: 36,
    15: 39, 16: 28, 17: 27, 18: 35, 19: 30, 20: 34, 21: 46,
    22: 46, 23: 39, 24: 51, 25: 46, 26: 75, 27: 66, 28: 20,
}


def load_done() -> set[str]:
    done = set()
    if OUT.exists():
        with open(OUT, encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                    done.add(d["verse_ref"])
                except Exception:
                    pass
    return done


def main():
    done = load_done()
    total = sum(MATTHEW_CHAPTERS.values())
    remaining = [(ch, v) for ch, vmax in MATTHEW_CHAPTERS.items()
                 for v in range(1, vmax + 1)
                 if f"Matthew {ch}:{v}" not in done]

    print(f"Matthew: {total} verses total. {len(done)} already fetched. {len(remaining)} to go.")

    if not remaining:
        print("All verses already fetched.")
        return

    with open(OUT, "a", encoding="utf-8") as out_f:
        for i, (ch, v) in enumerate(remaining):
            ref = f"Matthew {ch}:{v}"
            try:
                result = fetch_greekbible(ref)
                greek = result.get("greek_text", "").strip()
                record = {
                    "verse_ref": ref,
                    "chapter": ch,
                    "verse": v,
                    "greek_text": greek,
                    "url": result.get("url", ""),
                    "retrieved_at": result.get("retrieved_at", ""),
                }
                out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
                out_f.flush()
                status = "ok" if greek else "EMPTY"
                print(f"  [{i+1}/{len(remaining)}] {ref}: {status} — {greek[:60]}")
            except Exception as e:
                print(f"  [{i+1}/{len(remaining)}] {ref}: ERROR {e}")
                # Write error record so we can inspect later
                record = {
                    "verse_ref": ref,
                    "chapter": ch,
                    "verse": v,
                    "greek_text": "",
                    "error": str(e),
                }
                out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
                out_f.flush()

            time.sleep(1.0)

    done_now = load_done()
    filled = sum(1 for ref in done_now
                 if json.loads(open(OUT).read().split('\n')[0]).get("greek_text"))
    print(f"\nDone. {len(done_now)} records in {OUT}")


if __name__ == "__main__":
    main()
