"""
GrammaticalGeometrySpaceDriver — report writer.

The report lists:
  - the kernel (verse reference, run metadata)
  - the retrievals (sources read, URLs, timestamps)
  - the source agreements (where dictionaries converge)
  - the set that remains (translations and interpretations not eliminated)
  - what remains open (members not yet resolved)

The report does not say what the verse means while more than one member remains.
The report does not call the operator an immoral liar.
The report does not apply [his] unless explicitly requested.
The report does not apply [measured] without naming the measure.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any


def write_report(
    verse_ref: str,
    run_meta: dict[str, Any],
    primitives: list[dict[str, Any]],
    output_path: Path,
    greek_text: str = "",
    qa_results: list[dict[str, Any]] | None = None,
    cadence: list[dict[str, Any]] | None = None,
    gates: list[dict[str, Any]] | None = None,
    equations: dict[str, Any] | None = None,
    math_lines: list[str] | None = None,
) -> None:
    """Write the report markdown beside the JSONL."""
    lines = [
        f"# GGSD Report — {verse_ref}",
        "",
        f"**Run date:** {run_meta.get('started_at', '?')}",
        f"**Model:** {run_meta.get('model_id', '?')}",
        f"**Verse:** {verse_ref}",
        "",
        "---",
        "",
        "## Kernel",
        "",
        f"- Verse reference: `{verse_ref}`",
        f"- Word count: {len(primitives)}",
        f"- JSONL: `{output_path.stem}.jsonl`",
        "",
    ]

    # Sources retrieved
    lines += ["## Sources retrieved", ""]
    all_sources: dict[str, list[str]] = {}  # source_id -> urls
    for p in primitives:
        for sid, entry in p.get("source_retrievals", {}).items():
            all_sources.setdefault(sid, [])
            url = entry.get("url", "")
            if url not in all_sources[sid]:
                all_sources[sid].append(url)

    if all_sources:
        for sid, urls in sorted(all_sources.items()):
            lines.append(f"- **{sid}**")
            for u in urls:
                lines.append(f"  - {u}")
    else:
        lines.append("- No sources retrieved (check retrieval logs).")
    lines.append("")

    # Source agreements
    lines += ["## Source agreements", ""]
    any_agreement = False
    for p in primitives:
        word = p["word"]["surface"]
        agreements = [a for a in p.get("source_agreements", []) if a.get("agreement")]
        if agreements:
            any_agreement = True
            lines.append(f"**{word}**")
            for a in agreements:
                sids = ", ".join(a["source_ids"])
                lines.append(f"  - `{a['field']}` → `{a['value']}` [{sids}]")
            lines.append("")

    if not any_agreement:
        lines.append("No multi-source agreements recorded in this run.")
        lines.append("")

    # Cadence & gates (deterministic punctuation/math layers; proposed rules)
    if cadence is not None or gates is not None:
        lines += ["## Cadence & gates", ""]
        if cadence:
            lines.append("**Cadence map** (after word → mark / weight):")
            for e in cadence:
                ctx = f" [{', '.join(e['context'])}]" if e.get("context") else ""
                lines.append(f"- [{e['after_word']}] {e['surface']} → "
                             f"{e['mark']} ({e['weight']}){ctx}")
            lines.append("")
        if gates:
            lines.append("**Gates** (`;` — conditional domains; math rules proposed, not consented):")
            for g in gates:
                lines.append(f"- gate {g['gate_index']} after [{g['after_word']}]: "
                             f"head={g['head_type']}, return (proposed)={g['return_proposed']}, "
                             f"left={' '.join(g['left_terms'])}")
            lines.append("")
        elif gates is not None:
            lines += ["No gates (`;`) in this verse.", ""]
        if equations:
            eq = equations
            lines.append(f"Proposed: καὶ-equalities ×{len(eq.get('kai_equalities', []))}, "
                         f"numerals {[(n['surface'], n['value']) for n in eq.get('numerals', [])]}, "
                         f"μ-terms ×{len(eq.get('mu_terms', []))}, "
                         f"potential terms {[p['surface'] for p in eq.get('potential_terms', [])]}. "
                         f"Division primitive: TAKE(Q,u)=(n,r)_u, r<u.")
            lines.append("")
        if math_lines:
            lines.append("**Explicit mathematical translation** (script, proposed):")
            lines += [f"- {l}" for l in math_lines[1:]]
            lines.append("")

    # Per-word: the set that remains
    lines += ["## The set (per word)", ""]
    for p in primitives:
        word = p["word"]["surface"]
        lines.append(f"### {word}")
        lines.append("")
        desc = p.get("description", "").strip()
        if desc:
            lines.append(desc)
            lines.append("")

        gram = p.get("grammations") or {}
        if gram:
            cand = gram.get("segmentation_candidates", [{}])[-1]
            lines.append(f"*Math letters (proposed): {cand.get('expression', '')}*")
            lines.append("")
        grade = p.get("reference_grade") or {}
        if grade:
            lines.append(f"*MorphGNT: lemma {grade.get('lemma', '')}, "
                         f"grade {grade.get('grade_offline', '')}"
                         f"{', needs: ' + ', '.join(grade.get('morphgnt_need', [])) if grade.get('morphgnt_need') else ''}*")
            lines.append("")

        # Translations that remain (not eliminated)
        eliminated = {e["translation"] for e in p.get("eliminations", [])}
        translations = p.get("translations", [])
        standing = [
            t for t in translations
            if (t if isinstance(t, str) else t.get("value", "")) not in eliminated
        ]
        if standing:
            lines.append("**Translations standing:**")
            for t in standing:
                val = t if isinstance(t, str) else t.get("value", "")
                sid = "" if isinstance(t, str) else t.get("source_id", "")
                lines.append(f"  - {val}" + (f" ({sid})" if sid else ""))
        else:
            lines.append("*No translations recorded yet.*")

        if eliminated:
            lines.append("")
            lines.append("**Eliminated (rule-consented):**")
            for e in p.get("eliminations", []):
                lines.append(f"  - {e['translation']} — rule `{e['rule_id']}`")

        # Possible interpretations
        interps = p.get("possible_interpretations", [])
        if interps:
            lines.append("")
            lines.append("**Possible interpretations (set — not a choice):**")
            for i in interps:
                val = i if isinstance(i, str) else i.get("value", str(i))
                lines.append(f"  - {val}")

        lines.append("")

    # What remains open
    lines += ["## What remains open", ""]
    open_words = []
    for p in primitives:
        eliminated = {e["translation"] for e in p.get("eliminations", [])}
        translations = p.get("translations", [])
        standing = [
            t for t in translations
            if (t if isinstance(t, str) else t.get("value", "")) not in eliminated
        ]
        if len(standing) > 1:
            open_words.append(p["word"]["surface"])

    if open_words:
        lines.append(
            "The following words have more than one translation standing. "
            "The verse does not yet mean one thing. The set is open."
        )
        lines.append("")
        for w in open_words:
            lines.append(f"- {w}")
    elif primitives:
        lines.append(
            "Every word has one translation standing. "
            "If every elimination was made by a consented rule with a source quotation, "
            "the verse resolves to that reading. Check the eliminations."
        )
    else:
        lines.append("No words processed.")

    # Deterministic checks. No model call. See divergence.py and bold.py.
    # A failure here must not discard the report already built above.
    lines += ["", "---", "", "## Common translation, and the bold checks", ""]
    try:
        from bold import render_checks
        lines.append("```")
        lines.append(render_checks(primitives, greek_text=greek_text).rstrip())
        lines.append("```")
    except Exception as exc:
        lines.append(f"Checks did not run: {exc}")
    lines.append("")

    # Q1 / Q2 — grammatical taking and its morality
    if qa_results:
        lines += ["", "---", "", "## Grammatical taking — Q1 and Q2", ""]
        for entry in qa_results:
            q_num = entry.get("question_number", "?")
            question = entry.get("question", "")
            answer = entry.get("answer", "").strip()
            dur = entry.get("duration_s", "")
            lines.append(f"### Q{q_num}")
            lines.append("")
            lines.append(f"**{question}**")
            lines.append("")
            lines.append(answer)
            if dur:
                lines.append("")
                lines.append(f"*({dur}s)*")
            lines.append("")

    lines += [
        "",
        "---",
        "",
        f"*Generated by GrammaticalGeometrySpaceDriver v0.0.1 — "
        f"{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*",
    ]

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"report written: {output_path}")
