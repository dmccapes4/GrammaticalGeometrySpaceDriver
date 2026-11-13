#!/usr/bin/env python3
"""harness_grammations.py — v0.2 letter-layer fixtures. Deterministic."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from grammations import graphemes, render_segment, segmentations, \
    grammations_for_word, SYMBOL_TABLE_VERSION
from sources import load_morphgnt, morphgnt_verse_tokens
from punctuation import tokenise_morph_tokens
from math_layer import math_for_verse

results = []


def check(pid, ok, detail):
    results.append((pid, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {pid}: {detail}")


def main() -> int:
    print(f"symbol table {SYMBOL_TABLE_VERSION}")
    # G1 — iota subscript preserved as its own field (958 words in Matthew)
    g = graphemes("τῷ")[-1]
    check("G1 subscript-iota", g["subscript_iota"] and g["base"] == "ω",
          f"τῷ final grapheme: {g}")
    # G2 — rough breathing actually records rough (order bug fixed)
    check("G2 rough-breathing",
          graphemes("ἕν")[0]["breathing"] == "rough"
          and graphemes("ἐν")[0]["breathing"] == "smooth",
          f"ἕν={graphemes('ἕν')[0]['breathing']}, ἐν={graphemes('ἐν')[0]['breathing']}")
    # G3 — πέτρᾳ carries _ι in its rendering (Mt 16:18 fixture)
    r = grammations_for_word("πέτρᾳ", in_math_verse=True)
    exprs = [c["expression"] for c in r["segmentation_candidates"]] if r else []
    check("G3 petra-subscript", bool(r) and any("_ι" in e for e in exprs),
          f"πέτρᾳ -> {exprs}")
    # G4 — Πέτρος ends on the active variable; -ατα cluster renders as field
    check("G4 clusters",
          render_segment("ατα") == "τ_field(α_angle .. α_angle)"
          and "ατα" in [s[-1] for s in segmentations("πράγματα")],
          f"ατα -> {render_segment('ατα')}; πράγματα segs {segmentations('πράγματα')}")
    # G5 — θερίζουσιν operator segmentation survives v0.2 (Mt 6:26 fixture)
    data = load_morphgnt(ROOT / "morphgnt" / "sblgnt" / "61-Mt-morphgnt.txt")
    toks = tokenise_morph_tokens(morphgnt_verse_tokens(data, 6, 26))
    vm = math_for_verse(toks, "Matthew 6:26")
    ther = [v for v in vm["grammations"].values()
            if v["surface"] == "θερίζουσιν"]
    seg = ther[0]["segmentation_candidates"][-1]["segments"] if ther else []
    check("G5 therizousin", seg == ["θερί", "ζουσ", "ιν"],
          f"θερίζουσιν segments {seg}")
    # G6 — ἱνατί gate head now types (Mt 27:46)
    toks = tokenise_morph_tokens(morphgnt_verse_tokens(data, 27, 46))
    vm = math_for_verse(toks, "Matthew 27:46")
    heads = [g["head_type"] for g in vm["gates"]]
    check("G6 hinati-head", "target_limit" in heads, f"27:46 heads {heads}")
    # G7 — subscript-bearing words count in the real corpus (regression datum)
    n_sub = sum(1 for words in data.values() for w in words
                if any(g["subscript_iota"] for g in graphemes(w["word"])))
    check("G7 corpus-subscript", n_sub == 958, f"{n_sub} words carry _ι")

    fails = [p for p, ok in results if not ok]
    print(f"{len(results) - len(fails)}/{len(results)} passed")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
