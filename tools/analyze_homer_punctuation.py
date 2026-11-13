#!/usr/bin/env python3
"""
analyze_homer_punctuation.py — Punctuation frequency and context analysis
of Iliad + Odyssey as the Homeric baseline for GGSD.

Outputs:
  tools/homer/punctuation_baseline.json   — machine-readable counts + examples
  tools/homer/PUNCTUATION_HOMER_REPORT.md — human-readable report
"""

import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

HOMER_DIR = Path(__file__).parent / "homer"
ILIAD   = HOMER_DIR / "iliad.txt"
ODYSSEY = HOMER_DIR / "odyssey.txt"
PINDAR_FILES = [
    HOMER_DIR / "pindar_olympian.txt",
    HOMER_DIR / "pindar_pythian.txt",
    HOMER_DIR / "pindar_nemean.txt",
    HOMER_DIR / "pindar_isthmian.txt",
]

# ── Punctuation marks to track ───────────────────────────────────────────────
# Each entry: (unicode_char, name, ipa_note)
MARKS = [
    (",",  "comma",          "phrase boundary / breath pause"),
    ("·",  "ano_teleia",     "high stop — strong internal pause (semicolon equivalent)"),
    (".",  "full_stop",      "sentence end"),
    (";",  "question_mark",  "Greek question mark — conditional/dependent clause gate"),
    ("·",  "middle_dot",     "middle dot — check overlap with ano_teleia U+00B7"),
    (":",  "colon",          "colon — section or clause separator"),
    ("ʼ",  "elision_mark",   "elided vowel (U+02BC MODIFIER LETTER APOSTROPHE)"),
    ("᾽",  "coronis",        "coronis / elision (U+1FBD GREEK KORONIS) — end of section mark"),
    ("—",  "em_dash",        "em dash — parenthetical or editorial"),
    ("-",  "hyphen",         "hyphen — compound or editorial"),
]

# Deduplicate (ano_teleia and middle_dot are often the same char)
MARK_MAP = {}
for char, name, note in MARKS:
    if char not in MARK_MAP:
        MARK_MAP[char] = (name, note)

# ── Load corpus ───────────────────────────────────────────────────────────────

def load_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()

# ── Analysis ──────────────────────────────────────────────────────────────────

def analyze(lines: list[str], label: str) -> dict:
    counts: Counter = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    total_chars = 0
    total_lines = len(lines)

    for line in lines:
        total_chars += len(line)
        for char in line:
            if char in MARK_MAP:
                counts[char] += 1
                if len(examples[char]) < 5:
                    examples[char].append(line.strip())

    return {
        "label": label,
        "total_lines": total_lines,
        "total_chars": total_chars,
        "marks": {
            char: {
                "name": MARK_MAP[char][0],
                "note": MARK_MAP[char][1],
                "count": counts[char],
                "per_100_lines": round(counts[char] / total_lines * 100, 2),
                "examples": examples[char],
            }
            for char in MARK_MAP
            if counts[char] > 0
        },
    }


def unicode_name_safe(c: str) -> str:
    try:
        return unicodedata.name(c)
    except ValueError:
        return f"U+{ord(c):04X}"


# ── Report ────────────────────────────────────────────────────────────────────

def write_report(iliad: dict, odyssey: dict, combined: dict, out: Path,
                 pindar: dict | None = None, all_combined: dict | None = None) -> None:
    lines = [
        "# Homeric Punctuation Baseline",
        "",
        "**Source:** Perseus canonical-greekLit (PerseusDL/canonical-greekLit, GitHub)",
        "**Generated:** GGSD tools/analyze_homer_punctuation.py",
        "**Purpose:** Baseline punctuation distribution for Maththew GGSD analysis",
        "",
        "---",
        "",
        "## Corpus",
        "",
        f"| Work | Lines | Chars |",
        f"|------|-------|-------|",
        f"| Iliad | {iliad['total_lines']:,} | {iliad['total_chars']:,} |",
        f"| Odyssey | {odyssey['total_lines']:,} | {odyssey['total_chars']:,} |",
        f"| **Combined** | **{combined['total_lines']:,}** | **{combined['total_chars']:,}** |",
        "",
        "---",
        "",
        "## Punctuation Frequency (Combined Iliad + Odyssey)",
        "",
        "| Mark | Name | Count | Per 100 lines | Function |",
        "|------|------|-------|---------------|----------|",
    ]

    for char, data in sorted(
        combined["marks"].items(),
        key=lambda x: -x[1]["count"]
    ):
        uname = unicode_name_safe(char)
        lines.append(
            f"| `{char}` ({uname}) | {data['name']} | {data['count']:,} | "
            f"{data['per_100_lines']} | {data['note']} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Per-Work Comparison",
        "",
        "| Mark | Name | Iliad count | Iliad/100L | Odyssey count | Odyssey/100L |",
        "|------|------|-------------|------------|---------------|--------------|",
    ]

    all_chars = set(iliad["marks"]) | set(odyssey["marks"])
    for char in sorted(all_chars, key=lambda c: -(
        iliad["marks"].get(c, {}).get("count", 0) +
        odyssey["marks"].get(c, {}).get("count", 0)
    )):
        name = MARK_MAP[char][0]
        ic = iliad["marks"].get(char, {})
        oc = odyssey["marks"].get(char, {})
        lines.append(
            f"| `{char}` | {name} | {ic.get('count',0):,} | {ic.get('per_100_lines',0)} | "
            f"{oc.get('count',0):,} | {oc.get('per_100_lines',0)} |"
        )

    lines += ["", "---", "", "## Context Examples", ""]

    for char, data in sorted(
        combined["marks"].items(),
        key=lambda x: -x[1]["count"]
    ):
        if not data["examples"]:
            continue
        uname = unicode_name_safe(char)
        lines.append(f"### `{char}` — {data['name']} ({uname})")
        lines.append("")
        for ex in data["examples"][:5]:
            lines.append(f"- `{ex}`")
        lines.append("")

    if pindar and all_combined:
        lines += [
            "",
            "---",
            "",
            "## Homer vs Pindar Comparison",
            "",
            "Pindar's odes are metrically structured (strophe/antistrophe/epode triads).",
            "In Pindar, the metrical boundary IS the cadence mark — punctuation follows",
            "the strophic structure. A comma in Pindar often marks a colon boundary",
            "(metrical unit), not just a breath pause.",
            "",
            f"**Pindar corpus:** {pindar['total_lines']:,} lines across 4 ode collections",
            f"(Olympian {sum(1 for _ in open(HOMER_DIR / 'pindar_olympian.txt'))},",
            f" Pythian, Nemean, Isthmian).",
            "",
            "| Mark | Name | Homer/100L | Pindar/100L | Δ |",
            "|------|------|-----------|------------|---|",
        ]
        all_chars = set(combined["marks"]) | set(pindar["marks"])
        for char in sorted(all_chars, key=lambda c: -(combined["marks"].get(c, {}).get("count", 0))):
            hd = combined["marks"].get(char, {})
            pd_d = pindar["marks"].get(char, {})
            h_rate = hd.get("per_100_lines", 0)
            p_rate = pd_d.get("per_100_lines", 0)
            delta = round(p_rate - h_rate, 2)
            delta_str = f"+{delta}" if delta > 0 else str(delta)
            name = hd.get("name", pd_d.get("name", "?"))
            uname = unicode_name_safe(char)
            lines.append(
                f"| `{char}` ({uname}) | {name} | {h_rate} | {p_rate} | {delta_str} |"
            )

    lines += [
        "",
        "---",
        "",
        "## Notes on Homeric Punctuation",
        "",
        "The punctuation in the Perseus transmission of Homer reflects the Alexandrian",
        "editorial tradition (Aristophanes of Byzantium, c. 200 BCE; Aristarchus).",
        "It is NOT original to Homer's composition but is the oldest systematic",
        "punctuation applied to these texts, pre-dating the NT by ~200 years.",
        "",
        "**The elision mark** (`ʼ` U+02BC) is not punctuation in the cadence sense —",
        "it marks vowel elision at word boundaries, a phonological feature of Greek",
        "that affects how lines are scanned metrically.",
        "",
        "**Key distinction for Maththew comparison:**",
        "- Where Maththew's punctuation matches Homeric frequency → standard oration convention",
        "- Where Maththew diverges significantly → potential signal / authored emphasis",
        "",
        "*Generated by GGSD tools/analyze_homer_punctuation.py*",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Report → {out}")


# ── Combine two result dicts ──────────────────────────────────────────────────

def combine(a: dict, b: dict) -> dict:
    combined_marks = {}
    all_chars = set(a["marks"]) | set(b["marks"])
    for char in all_chars:
        ad = a["marks"].get(char, {"count": 0, "per_100_lines": 0, "examples": [], "name": MARK_MAP[char][0], "note": MARK_MAP[char][1]})
        bd = b["marks"].get(char, {"count": 0, "per_100_lines": 0, "examples": [], "name": MARK_MAP[char][0], "note": MARK_MAP[char][1]})
        total_count = ad["count"] + bd["count"]
        total_lines = a["total_lines"] + b["total_lines"]
        combined_marks[char] = {
            "name": ad["name"],
            "note": ad["note"],
            "count": total_count,
            "per_100_lines": round(total_count / total_lines * 100, 2),
            "examples": (ad["examples"] + bd["examples"])[:5],
        }
    return {
        "label": "combined",
        "total_lines": a["total_lines"] + b["total_lines"],
        "total_chars": a["total_chars"] + b["total_chars"],
        "marks": combined_marks,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Loading Iliad...", flush=True)
    iliad_lines   = load_lines(ILIAD)
    print("Loading Odyssey...", flush=True)
    odyssey_lines = load_lines(ODYSSEY)

    print("Loading Pindar...", flush=True)
    pindar_lines: list[str] = []
    for p in PINDAR_FILES:
        pindar_lines.extend(load_lines(p))

    print("Analyzing...", flush=True)
    iliad_result   = analyze(iliad_lines,   "Iliad")
    odyssey_result = analyze(odyssey_lines, "Odyssey")
    homer_combined = combine(iliad_result, odyssey_result)
    homer_combined["label"] = "Homer (combined)"

    pindar_result  = analyze(pindar_lines,  "Pindar (all odes)")
    all_combined   = combine(homer_combined, pindar_result)
    all_combined["label"] = "Homer + Pindar"

    json_out = HOMER_DIR / "punctuation_baseline.json"
    json_out.write_text(
        json.dumps({
            "iliad": iliad_result,
            "odyssey": odyssey_result,
            "homer_combined": homer_combined,
            "pindar": pindar_result,
            "all_combined": all_combined,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"  JSON → {json_out}")

    md_out = HOMER_DIR / "PUNCTUATION_HOMER_REPORT.md"
    write_report(iliad_result, odyssey_result, combined=homer_combined, out=md_out,
                 pindar=pindar_result, all_combined=all_combined)

    print("\nTop marks — Homer vs Pindar:")
    print(f"  {'Mark':8s} {'Name':20s} {'Homer/100L':>12s} {'Pindar/100L':>12s}")
    all_chars = set(homer_combined["marks"]) | set(pindar_result["marks"])
    for char in sorted(all_chars, key=lambda c: -(homer_combined["marks"].get(c, {}).get("count", 0))):
        hd = homer_combined["marks"].get(char, {})
        pd = pindar_result["marks"].get(char, {})
        print(f"  {repr(char):8s} {hd.get('name', pd.get('name','?')):20s} {hd.get('per_100_lines',0):>12}  {pd.get('per_100_lines',0):>12}")


if __name__ == "__main__":
    main()
