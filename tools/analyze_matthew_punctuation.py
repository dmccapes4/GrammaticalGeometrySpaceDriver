#!/usr/bin/env python3
"""
analyze_matthew_punctuation.py — Punctuation frequency analysis on Matthew JSONL.
Compare against the Homer + Pindar baseline from punctuation_baseline.json.
"""

import json
from pathlib import Path

JSONL  = Path(__file__).parent / "matthew_verses.jsonl"
BASE   = Path(__file__).parent / "homer" / "punctuation_baseline.json"
REPORT = Path(__file__).parent / "homer" / "PUNCTUATION_MATTHEW_REPORT.md"


def analyze(verses: list[dict]) -> dict:
    all_text = " ".join(v["greek_text"] for v in verses)
    n_lines  = len(verses)

    comma_c = all_text.count(",")
    ano_c   = all_text.count("·")
    stop_c  = all_text.count(".")
    semi_c  = all_text.count(";")

    f = 100 / n_lines
    return {
        "label":       "Matthew (SBLGNT/MorphGNT)",
        "lines":       n_lines,
        "total_chars": len(all_text),
        "counts": {
            "comma":       comma_c,
            "ano_teleia":  ano_c,
            "full_stop":   stop_c,
            "semicolon":   semi_c,
        },
        "per_100": {
            "comma":       round(comma_c * f, 2),
            "ano_teleia":  round(ano_c   * f, 2),
            "full_stop":   round(stop_c  * f, 2),
            "semicolon":   round(semi_c  * f, 2),
        },
        "semi_verses": [
            {"ref": v["verse_ref"], "text": v["greek_text"]}
            for v in verses if ";" in v["greek_text"]
        ],
    }


def load_baseline():
    if not BASE.exists():
        return None
    with open(BASE, encoding="utf-8") as f:
        return json.load(f)


def get_baseline_rate(baseline: dict, corpus_key: str, mark_char: str) -> float | str:
    """Extract per_100_lines rate from baseline JSON structure."""
    c = baseline.get(corpus_key, {})
    marks = c.get("marks", {})
    return marks.get(mark_char, {}).get("per_100_lines", "—")


def write_report(mat: dict, baseline: dict):
    lines = []
    lines.append("# Punctuation Analysis: Matthew vs Homer + Pindar")
    lines.append("")
    lines.append("**Source:** MorphGNT SBLGNT (local), field 3 (word form with trailing punctuation)  ")
    lines.append("**Date:** 2026-11-11")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Corpus Sizes")
    lines.append("")
    lines.append("| Corpus | Lines/Verses |")
    lines.append("|--------|-------------|")
    corpus_display = [
        ("iliad",          "Iliad"),
        ("odyssey",        "Odyssey"),
        ("homer_combined", "Homer combined"),
        ("pindar",         "Pindar"),
        ("all_combined",   "Homer+Pindar"),
    ]
    for key, label in corpus_display:
        n = baseline.get(key, {}).get("total_lines", "?")
        lines.append(f"| {label} | {n:,} |" if isinstance(n, int) else f"| {label} | {n} |")
    lines.append(f"| Matthew | {mat['lines']:,} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Mark Frequency Table (per 100 lines/verses)")
    lines.append("")

    # marks: (display name, character in text)
    mark_list = [
        ("comma",       ","),
        ("ano teleia",  "·"),
        ("full stop",   "."),
        ("semicolon ;", ";"),
    ]

    header = "| Mark | Iliad | Odyssey | Homer | Pindar | Homer+Pindar | **Matthew** |"
    sep    = "|------|-------|---------|-------|--------|-------------|------------|"
    lines.append(header)
    lines.append(sep)

    for mark_name, mark_char in mark_list:
        row = f"| {mark_name} |"
        for key, _ in corpus_display:
            val = get_baseline_rate(baseline, key, mark_char)
            row += f" {val} |"
        mat_val = mat["per_100"].get({
            ",":  "comma",
            "·":  "ano_teleia",
            ".":  "full_stop",
            ";":  "semicolon",
        }[mark_char], "—")
        row += f" **{mat_val}** |"
        lines.append(row)

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Semicolon (`;`) Gate — All Occurrences in Matthew")
    lines.append("")
    lines.append(f"**Total verses with `;`:** {len(mat['semi_verses'])} / {mat['lines']}  ")
    lines.append(f"**Rate:** {mat['per_100']['semicolon']} per 100 verses  ")
    lines.append("")
    lines.append("| Ref | Text |")
    lines.append("|-----|------|")
    for sv in mat["semi_verses"]:
        txt = sv["text"].replace("|", "\\|")
        lines.append(f"| {sv['ref']} | {txt[:120]} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")

    homer_semi  = get_baseline_rate(baseline, "homer_combined", ";")
    pindar_semi = get_baseline_rate(baseline, "pindar", ";")
    mat_semi    = mat["per_100"]["semicolon"]

    lines.append(f"- Homer baseline: **{homer_semi}** `;` per 100 lines")
    lines.append(f"- Pindar baseline: **{pindar_semi}** `;` per 100 lines")
    lines.append(f"- Matthew rate: **{mat_semi}** `;` per 100 verses")
    lines.append("")

    if isinstance(mat_semi, (int, float)) and isinstance(homer_semi, (int, float)):
        ratio = mat_semi / homer_semi if homer_semi > 0 else float("inf")
        lines.append(f"Matthew uses `;` at **{ratio:.1f}×** the Homeric rate.")
        lines.append("")
        if ratio > 2:
            lines.append("> **Signal:** Matthew deploys the conditional gate at significantly higher")
            lines.append("> frequency than the pre-Christian literary baseline. The `;` is not")
            lines.append("> ornamental — it is structural. Nearly every instance marks a rhetorical")
            lines.append("> question that frames the conditional domain for what follows.")
        elif ratio < 0.5:
            lines.append("> **Signal:** Matthew deploys the conditional gate far less than Homer.")
        else:
            lines.append("> Within range of the pre-Christian literary baseline.")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Notes on MorphGNT punctuation fidelity")
    lines.append("")
    lines.append("The MorphGNT field 3 carries the **word as it appears in the SBLGNT** including")
    lines.append("any trailing punctuation mark. This is the same text base greekbible.com serves.")
    lines.append("The MorphGNT file was used directly because greekbible.com is a SvelteKit app")
    lines.append("that renders client-side — the Greek text is not in the SSR HTML response.")

    return "\n".join(lines)


def main():
    verses = [json.loads(l) for l in JSONL.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"Loaded {len(verses)} Matthew verses")

    mat = analyze(verses)
    print(f"\nMark frequencies (per 100 verses):")
    for k, v in mat["per_100"].items():
        print(f"  {k:<15} {v}")
    print(f"\nVerses with `;`: {len(mat['semi_verses'])}")

    baseline = load_baseline()
    if not baseline:
        print("No baseline file found — skipping comparison")
        return

    report = write_report(mat, baseline)
    REPORT.write_text(report, encoding="utf-8")
    print(f"\nReport → {REPORT}")

    # Also append matthew data to baseline
    baseline["Matthew"] = {
        "label": mat["label"],
        "lines": mat["lines"],
        "per_100": mat["per_100"],
        "counts": mat["counts"],
    }
    BASE.write_text(json.dumps(baseline, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Baseline updated → {BASE}")


if __name__ == "__main__":
    main()
