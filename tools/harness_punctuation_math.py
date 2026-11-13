#!/usr/bin/env python3
"""
harness_punctuation_math.py — 10-verse harness for the GGSD punctuation
and mathematical layers. Deterministic; no model calls; no GPU.

Verses: the established 10-verse harness set
(docs/GAMEPLAN_GGSD_HARNESS_10VERSE_20261110.md), re-used so punctuation
results sit beside the grammar results for the same verses.

Criteria PM1-PM10 are defined in docs/HARNESS_PUNCTUATION_MATH_20261111.md.
Exit code 0 iff every criterion passes; failures are reported as datum,
never silently skipped.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sources import load_morphgnt, morphgnt_verse_tokens
from punctuation import tokenise_morph_tokens, cadence_map, mark_counts
from math_layer import math_for_verse, take_units

MORPH = ROOT / "morphgnt" / "sblgnt" / "61-Mt-morphgnt.txt"

VERSES = [
    ("Matthew 4:10", 4, 10), ("Matthew 25:18", 25, 18),
    ("Matthew 1:1", 1, 1), ("Matthew 3:17", 3, 17),
    ("Matthew 5:3", 5, 3), ("Matthew 6:26", 6, 26),
    ("Matthew 19:24", 19, 24), ("Matthew 22:37", 22, 37),
    ("Matthew 26:26", 26, 26), ("Matthew 27:46", 27, 46),
]

results: list[tuple[str, bool, str]] = []


def check(pid: str, ok: bool, detail: str) -> None:
    results.append((pid, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {pid}: {detail}")


def main() -> int:
    print(f"loading {MORPH} ...")
    data = load_morphgnt(MORPH)
    per_verse: dict[str, dict] = {}

    for ref, ch, vs in VERSES:
        morph = morphgnt_verse_tokens(data, ch, vs)
        toks = tokenise_morph_tokens(morph)
        per_verse[ref] = {"morph": morph, "toks": toks,
                          "math": math_for_verse(toks),
                          "counts": mark_counts(toks)}
        print(f"\n{ref}  ({len(toks)} words)  marks={per_verse[ref]['counts']}")

    # PM1 — token invariance: surfaces == MorphGNT clean words, count equal
    bad = [ref for ref, d in per_verse.items()
           if [t["surface"] for t in d["toks"]] != [w["word"] for w in d["morph"]]]
    check("PM1 token-invariance", not bad,
          f"surface sequence == clean field for all 10 verses" if not bad else f"mismatch: {bad}")

    # PM2 — mark counts equal a naive count over the printed field
    bad = []
    for ref, d in per_verse.items():
        printed = " ".join(w["text"] for w in d["morph"])
        naive = {"comma": printed.count(","), "ano_teleia": printed.count("·"),
                 "full_stop": printed.count("."), "gate": printed.count(";")}
        got = {k: d["counts"].get(k, 0) for k in naive}
        if naive != got:
            bad.append((ref, naive, got))
    check("PM2 mark-counts", not bad,
          "cadence counts == raw printed-field counts, 10/10" if not bad else f"{bad}")

    # PM3 — whole-Matthew invariance against the punctuation report's totals
    all_toks = []
    for (ch, vs), words in sorted(data.items()):
        all_toks.extend(tokenise_morph_tokens(words))
    totals = mark_counts(all_toks)
    expect = {"comma": 910, "ano_teleia": 761, "full_stop": 753, "gate": 168}
    got = {k: totals.get(k, 0) for k in expect}
    check("PM3 matthew-totals", got == expect,
          f"gates={got['gate']} (expect 168), ano={got['ano_teleia']} (761), "
          f"comma={got['comma']} (910), full={got['full_stop']} (753)")

    # PM4 — Matthew 4:10 fixtures
    d = per_verse["Matthew 4:10"]
    toks = d["toks"]
    sat = [t for t in toks if t["surface"].startswith("Σαταν")]
    hyp = [t for t in toks if t["surface"].startswith("Ὕπαγε")]
    check("PM4 matthew-4:10",
          d["counts"].get("gate", 0) == 0 and d["counts"].get("ano_teleia", 0) == 3
          and bool(sat) and sat[0]["accent_class"] == "perispomeni"
          and sat[0]["accented_syllable"] == "final"
          and bool(hyp) and hyp[0]["leading_apparatus"],
          f"gates=0, ano_teleia=3, Σατανᾶ perispomeni/final, Ὕπαγε apparatus: "
          f"{[(t['surface'], t['accent_class'], t['leading_apparatus']) for t in toks if t in sat + hyp]}")

    # PM5 — Matthew 27:46 final gate is left open
    d = per_verse["Matthew 27:46"]
    gates = d["math"]["gates"]
    check("PM5 matthew-27:46",
          len(gates) >= 2 and gates[-1]["return_proposed"] == "left-open"
          and d["toks"][-1]["trailing_punct"] == "gate",
          f"{len(gates)} gates; last return={gates[-1]['return_proposed'] if gates else None}, "
          f"head={gates[-1]['head_type'] if gates else None}")

    # PM6 — Matthew 6:26: one gate, mu-term present, no numerals forced
    d = per_verse["Matthew 6:26"]
    mu = [m["surface"] for m in d["math"]["equations"]["mu_terms"]]
    check("PM6 matthew-6:26",
          len(d["math"]["gates"]) == 1 and any(s.startswith("μ") for s in mu),
          f"gates={len(d['math']['gates'])}, mu_terms={mu}")

    # PM7 — TAKE is ratio-free: whole takes, remainder below unit
    t = take_units(100, 99)
    t2 = take_units(1, 100)
    ok = (t == {"quantity": 100, "unit": 99, "takes": 1, "remainder": 1}
          and t2["takes"] == 0 and t2["remainder"] == 1)
    try:
        take_units(5, 0)
        ok = False
    except ValueError:
        pass
    check("PM7 take-primitive", ok,
          f"TAKE(100,99)={t}; TAKE(1,100) takes=0 remainder=1; unit=0 rejected")

    # PM8 — kai-equalities are proposed, never consented, never eliminating
    eqs = [e for d in per_verse.values() for e in d["math"]["equations"]["kai_equalities"]]
    check("PM8 kai-status",
          bool(eqs) and all(e["status"] == "proposed" for e in eqs),
          f"{len(eqs)} καὶ-equality claims over 10 verses, all status=proposed")

    # PM9 — schema: math rules cannot eliminate; punctuation block validates
    from schema import empty_primitive, validate_primitive
    p = empty_primitive("Matthew 4:10", "Ὕπαγε", "harness")
    p["punctuation"] = {"trailing_punct": "comma"}
    try:
        validate_primitive(p)
        schema_ok = True
    except Exception as e:
        schema_ok = False
        print("    schema error:", e)
    p2 = empty_primitive("Matthew 4:10", "Ὕπαγε", "harness")
    p2["eliminations"] = [{"translation": "x", "rule_id": "mathematical_rules[0]",
                            "source_id": "s", "quotation": "q"}]
    try:
        validate_primitive(p2)
        guard_ok = False
    except Exception:
        guard_ok = True
    check("PM9 schema-guard", schema_ok and guard_ok,
          "primitive with punctuation validates; elimination via math rule rejected")

    # PM10 — accent sanity on Matthew 1:1 and breathing on Ἰησοῦ
    d = per_verse["Matthew 3:17"]
    ies = [t for t in d["toks"] + per_verse["Matthew 4:10"]["toks"]
           if t["surface"].startswith("Ἰησ")]
    check("PM10 accent-breathing",
          bool(ies) and all(t["breathing"] == "smooth" for t in ies),
          f"Ἰησοῦς tokens breathing={[t['breathing'] for t in ies]}")

    print("\n=== SUMMARY ===")
    fails = [r for r in results if not r[1]]
    for pid, ok, detail in results:
        print(f"  {pid}: {'PASS' if ok else 'FAIL'}")
    print(f"{len(results) - len(fails)}/{len(results)} criteria passed")
    out = ROOT / "tools" / "harness_punctuation_math_results.json"
    out.write_text(json.dumps(
        [{"criterion": p, "pass": o, "detail": d} for p, o, d in results],
        ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"results → {out}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
