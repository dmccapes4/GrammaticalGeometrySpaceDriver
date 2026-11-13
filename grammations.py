"""
GGSD mathematical grammation — letter-by-letter candidate parsing.

Implements docs/GAMEPLAN_MORPHGNT_CADENCE_GRAMMATION_20261112.md:
  - punctuation cadence identifies math-lecture verses (gates, kai chains,
    repetitions that grow);
  - triggered words are parsed grapheme-by-grapheme under a SUGGESTED,
    versioned symbol table (status: proposed everywhere);
  - MorphGNT-required words are identified and the MorphGNT witness is
    graded against cadence and grammation — offline, deterministically.

No statistics. Counting only (whole counts, TAKE). Nothing here eliminates
a lexical, grammatical, or semantic reading.
"""
from __future__ import annotations

import unicodedata
from collections import Counter, defaultdict

SYMBOL_TABLE_VERSION = "v0.2"
STATUS = "proposed"

# Suggested symbol table (game plan section 4). Not locked.
SYMBOLS = {
    "α": "α_angle", "β": "β_square_or_double", "γ": "γ_gamma",
    "δ": "δ_variation", "ε": "ε_apply", "ζ": "ζ_curve", "η": "η_inclusive_or",
    "θ": "θ_measure", "ι": "ι_unique", "κ": "κ_index", "λ": "λ_function",
    "μ": "μ_differential", "ν": "ν_total", "ξ": "ξ_coupled", "ο": "ο_asymptotic",
    "π": "π", "ρ": "rho_decay", "σ": "σ_permutation", "ς": "ς_variable",
    "τ": "τ_field", "υ": "υ_secondary", "φ": "φ_golden", "χ": "χ_free",
    "ψ": "ψ_state", "ω": "ω_ordinal_set",
}
_SYMBOL_RICH = set("ζξφψ")               # rare operator letters only
_STRONG_SIGNALS = {"symbol_rich_letter", "internal_zeta", "transformed_iota",
                   "accented_omega", "kappa_to_nu", "mu_initial", "final_rho",
                   "alpha_tau_alpha_tail", "subscript_iota"}
_FUNCTION_BARE = {"και", "ο", "η", "οι", "αι", "το", "τα", "τω", "τη", "του",
                  "των", "τον", "την", "εν", "εισ", "εκ", "εξ"}
_PREFIX_OPS = {"ζ", "λ", "φ", "τ", "σ"}  # may open a segment as an operator


def _bare(s: str) -> str:
    n = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in n if unicodedata.category(c) != "Mn").replace("ς", "σ")


def graphemes(surface: str) -> list[dict]:
    """Split a surface into graphemes: base letter + combining marks.

    v0.2 fixes (LETTER_GRAMMATION_SUGGESTED_RULES_v0.2 section 0):
      - U+0345 COMBINING GREEK YPOGEGRAMMENI (iota subscript) is preserved
        as its own field: ᾳ/ῃ/ῳ = vowel pinned at locus iota (x_ι).
      - Rough breathing: "REVERSED COMMA ABOVE" is checked BEFORE
        "COMMA ABOVE" (the latter is a substring of the former; the old
        order labelled every rough breathing smooth).
    """
    out = []
    for ch in unicodedata.normalize("NFC", surface):
        parts = unicodedata.normalize("NFD", ch)
        base = parts[0].lower()
        accent, breathing, subscript = "none", "none", False
        for m in parts[1:]:
            name = unicodedata.name(m, "")
            if "YPOGEGRAMMENI" in name:
                subscript = True
            elif "ACUTE" in name:
                accent = "acute"
            elif "GRAVE" in name:
                accent = "grave"
            elif "PERISPOMENI" in name:
                accent = "perispomeni"
            elif "REVERSED COMMA ABOVE" in name or "DASIA" in name:
                breathing = "rough"
            elif "COMMA ABOVE" in name or "PSILI" in name:
                breathing = "smooth"
        out.append({"raw": ch, "base": base, "accent": accent,
                    "breathing": breathing, "subscript_iota": subscript})
    return out


def _render_grapheme(g: dict) -> str:
    base = g["base"]
    role = SYMBOLS.get(base, base)
    if base == "ι" and g["accent"] != "none":
        role = "ι′_transformed_unique"      # ί = ι + transform, not a new letter
    if base == "ω" and g["accent"] != "none":
        role = "ω_ordinal_set_reversed"     # accent on ω proposes reverse order
    if g.get("subscript_iota"):
        role += "_ι"                        # pinned at the unique locus iota
    if g.get("breathing") == "rough":
        role += "(+h)"                      # quantized / active-bound state
    return role


# Tier-2 composite clusters (v0.2 section I): additional segmentation
# candidates in the lattice, never replacements for grapheme candidates.
CLUSTER_RENDER = {
    "ατα": "τ_field(α_angle .. α_angle)",
    "ματα": "μ_differential · τ_field(α_angle .. α_angle)",
    "κατα": "κ_index · τ_field(α_angle .. α_angle)",
    "περι": "∮_peri(π · ε_apply · rho_decay · ι_unique)",
    "παρα": "παρα_parallel(π · α_angle · rho_decay · α_angle)",
    "ουσιν": "flow(ου→σ_permutation) ι_ν",
    "ται": "τ_field(α_angle→ι_unique)",
}
_CLUSTER_PREFIXES = ["περι", "παρα", "κατα", "μετα", "δια", "συν", "υπο",
                     "προ", "απο", "ανα", "εκ", "εξ"]
_CLUSTER_TAILS = ["ματα", "αται", "ατα", "ουσιν", "ται", "ων", "ος", "ον"]


def render_segment(segment: str) -> str:
    """Render one segment as a candidate expression string."""
    gs = graphemes(segment)
    if not gs:
        return ""
    bare_seg = "".join(g["base"] for g in gs)
    if bare_seg in CLUSTER_RENDER:
        return CLUSTER_RENDER[bare_seg]
    first = gs[0]["base"]
    if first in _PREFIX_OPS and len(gs) > 1:
        inner = " ".join(_render_grapheme(g) for g in gs[1:])
        name = {"ζ": "ζ_curve", "λ": "λ_f", "φ": "φ_golden",
                "τ": "τ_field", "σ": "Σ_sum"}[first]
        return f"{name}({inner})"
    # Medial tau is the field BETWEEN its neighbours (operator, 2026-11-12):
    # ατα = angles held in a field = an unspecified collection, "some
    # things" (ἅττα). X τ Y renders as the field spanned by X and Y.
    bases = [g["base"] for g in gs]
    if "τ" in bases[1:-1]:
        i = bases.index("τ", 1)
        left = " ".join(_render_grapheme(g) for g in gs[:i])
        right = " ".join(_render_grapheme(g) for g in gs[i + 1:])
        return f"τ_field({left} .. {right})"
    return " ".join(_render_grapheme(g) for g in gs)


def segmentations(surface: str) -> list[list[str]]:
    """Candidate segmentations. All rivals are kept; no winner is chosen."""
    clean = surface.strip(",.·;—")
    gs = graphemes(clean)
    bare = [g["base"] for g in gs]
    cands: list[list[str]] = [[clean]]
    # Split before an internal zeta, and before a final -ιν tail.
    bounds = [i for i in range(1, len(gs)) if bare[i] == "ζ"]
    if bare[-2:] == ["ι", "ν"] and len(gs) >= 6:
        bounds.append(len(gs) - 2)
    if bare[-3:] == ["α", "τ", "α"] and len(gs) >= 5:
        bounds.append(len(gs) - 3)   # -ατα tail: the field-of-angles segment
    bounds = sorted(set(bounds))
    if bounds:
        segs, prev = [], 0
        for b in bounds:
            segs.append("".join(g["raw"] for g in gs[prev:b]))
            prev = b
        segs.append("".join(g["raw"] for g in gs[prev:]))
        if segs not in cands:
            cands.append(segs)
    # Tier-2 cluster candidate: split a known prefix cluster and/or a
    # known tail cluster, keeping the middle as its own segment. This is
    # an ADDITIONAL lattice candidate; the grapheme candidates above stand.
    bare_str = "".join(bare)
    pre = next((c for c in _CLUSTER_PREFIXES
                if bare_str.startswith(c) and len(bare_str) > len(c) + 1), None)
    tail = next((c for c in _CLUSTER_TAILS
                 if bare_str.endswith(c) and len(bare_str) > len(c) + 1), None)
    if pre or tail:
        segs, rest = [], clean
        if pre:
            segs.append("".join(g["raw"] for g in gs[:len(pre)]))
            gs_rest = gs[len(pre):]
        else:
            gs_rest = gs
        if tail and len(gs_rest) > len(tail):
            segs.append("".join(g["raw"] for g in gs_rest[:-len(tail)]))
            segs.append("".join(g["raw"] for g in gs_rest[-len(tail):]))
        else:
            segs.append("".join(g["raw"] for g in gs_rest))
        segs = [s for s in segs if s]
        if len(segs) > 1 and segs not in cands:
            cands.insert(1, segs)
    return cands


def word_signals(surface: str) -> list[str]:
    """Named equation-likeness signals (game plan section 5.3). No vibes."""
    gs = graphemes(surface)
    bare = [g["base"] for g in gs]
    sigs = []
    if any(b in _SYMBOL_RICH for b in bare):
        sigs.append("symbol_rich_letter")
    if any(b == "ζ" for b in bare[1:]):
        sigs.append("internal_zeta")
    if bare and bare[0] == "μ":
        sigs.append("mu_initial")
    if bare and bare[-1] == "ρ":
        sigs.append("final_rho")   # the variable rho, lower-case in prose
    if any(g["base"] == "ι" and g["accent"] != "none" for g in gs):
        sigs.append("transformed_iota")
    if any(g["base"] == "ω" and g["accent"] != "none" for g in gs):
        sigs.append("accented_omega")
    if "κ" in bare and "ν" in bare and bare.index("κ") < bare.index("ν"):
        sigs.append("kappa_to_nu")
    if bare[-3:] == ["α", "τ", "α"]:
        sigs.append("alpha_tau_alpha_tail")   # -ατα: field of angles, "some things"
    if any(g.get("subscript_iota") for g in gs):
        sigs.append("subscript_iota")         # x_ι: pinned at the unique locus
    if len(gs) >= 8:
        sigs.append("long_form")
    if len(set(bare)) < len(bare):
        sigs.append("letter_repetition")
    return sigs


def hard_triggers(surface: str, unclosed_proxy: bool = False) -> list[str]:
    """Word-level hard triggers (game plan section 5.2)."""
    gs = graphemes(surface)
    if not gs:
        return []
    bare = [g["base"] for g in gs]
    out = []
    if bare[0] == "ζ":
        out.append("W2_zeta_initial")
    if bare[0] == "σ":
        out.append("W3_sigma_initial")
    if unclosed_proxy:
        out.append("W1_lexically_unclosed_proxy")
        if bare[0] == "λ":
            out.append("W4_lambda_unclosed")
    if "κ" in bare and "ν" in bare and bare.index("κ") < bare.index("ν"):
        out.append("W5_kappa_nu")
    if len(gs) == 1 and _bare(surface) not in _FUNCTION_BARE:
        out.append("W6_single_letter")
    return out


def grammations_for_word(surface: str, *, in_math_verse: bool,
                         unclosed_proxy: bool = False) -> dict | None:
    """Letter-by-letter record for one word, or None if no trigger fires."""
    if _bare(surface) == "και":
        return None  # καὶ is the join operator itself, not an operand
    hard = hard_triggers(surface, unclosed_proxy)
    sigs = word_signals(surface)
    eligible = in_math_verse and (
        (len(sigs) >= 2 and bool(_STRONG_SIGNALS.intersection(sigs)))
        or "subscript_iota" in sigs)
    if not hard and not eligible:
        return None
    segs = segmentations(surface)
    return {
        "surface": surface,
        "triggered_by": hard or ["verse_math_eligible"],
        "signals": sigs,
        "symbol_table_version": SYMBOL_TABLE_VERSION,
        "graphemes": [g["base"] for g in graphemes(surface)],
        "segmentation_candidates": [
            {"segments": s,
             "expression": " | ".join(render_segment(x) for x in s)}
            for s in segs
        ],
        "status": STATUS,
    }


# ─── verse-level: cadence -> math lecture identification ───────────────────

def kai_chains(tokens: list[dict]) -> list[dict]:
    """καὶ chains per cadence domain (domains end at full stops)."""
    chains, current = [], []
    def flush():
        if len(current) >= 2:
            chains.append({"kai_positions": list(current),
                           "member_joins": len(current)})
    for t in tokens:
        if _bare(t["surface"]) == "και":
            current.append(t["word_index"])
        if t["trailing_punct"] == "full_stop":
            flush(); current = []
    flush()
    return chains


def growth_sequences(tokens: list[dict]) -> list[dict]:
    """Repetitions that grow (game plan section 6): shared-frame sequences."""
    out = []
    suffix_groups: dict[str, list[str]] = defaultdict(list)
    for t in tokens:
        b = _bare(t["surface"])
        if len(b) >= 6:
            suffix_groups[b[-4:]].append(t["surface"])
    for suffix, words in suffix_groups.items():
        if len(words) >= 3:
            out.append({"pattern": "G3_frame_growth", "frame": f"-{suffix}",
                        "members": words, "count": len(words)})
    kai_counts = [c["member_joins"] for c in kai_chains(tokens)]
    if len(kai_counts) >= 2 and kai_counts == sorted(kai_counts) \
            and len(set(kai_counts)) > 1:
        out.append({"pattern": "G4_chain_growth", "chain_lengths": kai_counts})
    return out


def classify_math_lecture(tokens: list[dict], gates: list[dict],
                          equations: dict) -> dict:
    """A verse is a math-lecture verse when cadence opens the math door."""
    reasons = []
    if gates:
        reasons.append("V1_gate_present")
    chains = kai_chains(tokens)
    if any(c["member_joins"] >= 3 for c in chains):
        reasons.append("V2_kai_chain>=3")
    growth = growth_sequences(tokens)
    if growth:
        reasons.append("V3_repetition_grows")
    nums = equations.get("numerals", [])
    if len(nums) >= 2 and chains:
        reasons.append("V4_numerals_in_chain")
    return {"is_math_lecture": bool(reasons), "reasons": reasons,
            "kai_chains": chains, "growth_sequences": growth,
            "status": STATUS}


def explicit_math_translation(verse_ref: str, tokens: list[dict],
                              gates: list[dict], equations: dict,
                              grammations: dict[int, dict]) -> list[str]:
    """Script-rendered explicit mathematical translation lines for a verse."""
    lines = [f"{verse_ref} — explicit mathematical translation (proposed)"]
    marks = [(t["word_index"], t["surface"], t["trailing_punct"])
             for t in tokens if t["trailing_punct"] != "none"]
    lines.append("cadence: " + (" ".join(
        f"[{i}]{s}:{m}" for i, s, m in marks) or "no marks"))
    for e in equations.get("kai_equalities", []):
        lines.append(f"  {e.get('left')} = {e.get('right')}   (καὶ, M1 proposed)")
    for n in equations.get("numerals", []):
        lines.append(f"  count: {n['surface']} = {n['value']} (whole count, M5)")
    for g in gates:
        lines.append(f"  GATE[{g['gate_index']}] head={g['head_type']} "
                     f"return={g['return_proposed']}: "
                     f"{' '.join(g['left_terms'])} ; => "
                     f"{' '.join(g['following_terms'])}")
    for idx in sorted(grammations):
        rec = grammations[idx]
        cand = rec["segmentation_candidates"][-1]
        lines.append(f"  {rec['surface']} -> {' | '.join(cand['segments'])}"
                     f" -> {cand['expression']}  [{', '.join(rec['triggered_by'])}]")
    return lines


def cadence_roles(tokens: list[dict]) -> dict[int, dict]:
    """Per-token cadence role: gate left/return, chain member, held, closed."""
    roles: dict[int, dict] = {}
    domain = 0
    gate_seen = False
    for t in tokens:
        i = t["word_index"]
        role = "gate_return_term" if gate_seen else "plain_term"
        if _bare(t["surface"]) == "και":
            role = "kai_join"
        if t["trailing_punct"] == "gate":
            role = "gate_boundary"
        if t["trailing_punct"] == "ano_teleia":
            role = "held_term"
        roles[i] = {"role": role, "domain": domain, "status": STATUS}
        if t["trailing_punct"] == "gate":
            gate_seen = True
        if t["trailing_punct"] == "full_stop":
            domain += 1
            gate_seen = False
    return roles


# ─── MorphGNT: who needs it, and how it grades ─────────────────────────────

def corpus_stats(morph_data: dict) -> dict:
    lemma_counts: Counter = Counter()
    bare_lemma: dict[str, set] = defaultdict(set)
    bare_surface: dict[str, set] = defaultdict(set)
    for words in morph_data.values():
        for w in words:
            lemma_counts[w["lemma"]] += 1
            bare_lemma[_bare(w["lemma"])].add(w["lemma"])
            bare_surface[_bare(w["word"])].add(w["lemma"])
    return {"lemma_counts": lemma_counts, "bare_lemma": bare_lemma,
            "bare_surface": bare_surface}


def morphgnt_need(word: dict, stats: dict) -> list[str]:
    """Reasons this word requires the MorphGNT witness (offline criteria)."""
    reasons = []
    if stats["lemma_counts"].get(word["lemma"], 0) <= 1:
        reasons.append("lemma_hapax_in_matthew")
    if len(stats["bare_surface"].get(_bare(word["word"]), set())) > 1:
        reasons.append("bare_form_ambiguous")
    if "⸀" in word["text"] or "⸂" in word["text"] or "⸃" in word["text"]:
        reasons.append("apparatus_carrier")
    if "?" in word.get("parse", "") or not word.get("parse"):
        reasons.append("parse_unclosed")
    bl, bs = _bare(word["lemma"]), _bare(word["word"])
    if not (bs.startswith(bl[:4]) or bl.startswith(bs[:4])):
        reasons.append("lemma_surface_divergent")
    return reasons


def grade_morphgnt_word(word: dict, need: list[str], token: dict,
                        grammations: dict | None) -> dict:
    """Grade the MorphGNT witness against cadence and grammation.

    Grades describe witness closure, not truth (game plan section 3).
    Offline grade: Logeion is the runtime second witness (source_retrievals).
    """
    conflicts = []
    if "?" in word.get("parse", ""):
        conflicts.append("morphgnt_parse_unclosed")
    if token["surface"] != word["word"]:
        conflicts.append("cadence_token_mismatch")
    if conflicts:
        grade = "R1_offline_conflicted"
    elif need:
        grade = "R2_offline_witness_needed"
    else:
        grade = "R3_offline_consistent"
    return {
        "lemma": word["lemma"], "pos": word.get("pos", ""),
        "parse_code": word.get("parse", ""),
        "morphgnt_need": need, "grade_offline": grade,
        "conflicts": conflicts,
        "cadence_mark": token["trailing_punct"],
        "grammations_fired": grammations is not None,
        "note": "offline grade vs cadence/grammation; Logeion witness "
                "grades at runtime in source_retrievals",
        "status": STATUS,
    }
