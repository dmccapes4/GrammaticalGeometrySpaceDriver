#!/usr/bin/env python3
"""
build_prerun_context.py — the v0.0.3 pre-run stage.

Runs BEFORE any Qwen call. For every Matthew verse, deterministically:
  1. punctuation cadence extraction        (punctuation.py)
  2. mathematical identification           (math-lecture classification)
  3. mathematical grammation               (gates, kai chains, TAKE counts)
  4. mathematical letter-by-letter         (grammations.py, table v0.2)
  5. MorphGNT grading                      (need identification + grade
                                            vs cadence and grammations)

Output: prerun/matthew_prerun_context.json — one entry per verse, consumed
by ggsd.py (--prerun) so Qwen begins each verse with all of it available.
Verses absent from SBLGNT/MorphGNT (17:21, 18:11, 23:14) are recorded as
absent; the driver falls back to computing context live for those.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sources import load_morphgnt, morphgnt_verse_tokens
from punctuation import tokenise_morph_tokens, cadence_map, mark_counts
from math_layer import math_for_verse
from grammations import corpus_stats, morphgnt_need, grade_morphgnt_word

MORPH = ROOT / "morphgnt" / "sblgnt" / "61-Mt-morphgnt.txt"
OUT = ROOT / "prerun" / "matthew_prerun_context.json"
ABSENT_IN_SBLGNT = ["Matthew 17:21", "Matthew 18:11", "Matthew 23:14"]


def main() -> int:
    data = load_morphgnt(MORPH)
    stats = corpus_stats(data)
    verses: dict[str, dict] = {}
    need_counter: Counter = Counter()
    grade_counter: Counter = Counter()
    n_lecture = n_gram = 0

    for (ch, vs) in sorted(data):
        ref = f"Matthew {ch}:{vs}"
        morph_words = morphgnt_verse_tokens(data, ch, vs)
        toks = tokenise_morph_tokens(morph_words)
        vm = math_for_verse(toks, ref, morph_stats=stats)
        if vm["math_lecture"]["is_math_lecture"]:
            n_lecture += 1
        n_gram += len(vm["grammations"])

        words = []
        for i, w in enumerate(morph_words):
            need = morphgnt_need(w, stats)
            for r in need:
                need_counter[r] += 1
            gram = vm["grammations"].get(str(i))
            grade = grade_morphgnt_word(w, need, toks[i], gram)
            grade_counter[grade["grade_offline"]] += 1
            words.append({
                "index": i, "surface": w["word"], "printed": w["text"],
                "lemma": w["lemma"], "pos": w["pos"],
                "parse_code": w["parse"], "normalized": w["normalized"],
                "punctuation": toks[i]["trailing_punct"],
                "cadence_role": vm["cadence_roles"].get(str(i), {}),
                "reference_grade": grade, "grammations": gram,
            })

        verses[ref] = {
            "verse_ref": ref,
            "cadence_map": cadence_map(toks),
            "mark_counts": mark_counts(toks),
            "math_lecture": vm["math_lecture"],
            "gates": vm["gates"], "equations": vm["equations"],
            "explicit_math_translation": vm["explicit_math_translation"],
            "words": words,
        }

    census = {
        "verses_in_sblgnt": len(verses),
        "absent_in_sblgnt": ABSENT_IN_SBLGNT,
        "math_lecture_verses": n_lecture,
        "grammation_words": n_gram,
        "morphgnt_need_reasons": dict(need_counter),
        "grade_counts_offline": dict(grade_counter),
        "symbol_table_version": "v0.2",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"census": census, "verses": verses},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(census, ensure_ascii=False, indent=2))
    print(f"-> {OUT}  ({OUT.stat().st_size/1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
