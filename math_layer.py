"""
GGSD mathematical layer — deterministic core over the punctuation layer.

Implements the operator's rules as PROPOSED interpretations (schema.py:
the model/driver may propose; only the operator consents; mathematical
rules may never eliminate). Division is ratio-free:
    TAKE(Q, u) = (n, r)_u   take whole units until remainder r < unit u.

See docs/GAMEPLAN_GGSD_PUNCTUATION_MATH_20261111.md §4 (rules M1-M10).
"""
from __future__ import annotations

import unicodedata

RULES = {
    "M1": "kai joins as equality claim between flanking terms",
    "M2": "; opens a conditional domain (gate); what follows is its resolution or measured absence",
    "M3": "ano teleia after a speech form = evaluate-what-follows; elsewhere strong hold",
    "M4": "mu-initial function words and oligo- forms mark infinitesimal-scale terms (nonzero, below declared unit)",
    "M5": "numerals are whole counts at a declared unit; never normalised into fractions",
    "M6": "division is TAKE(Q,u)=(n,r)_u with r<u; ratios only as derived reports carrying (n,r,u)",
    "M7": "gate typed by head: ti (unknown), tis (element), dia-ti (cause), pos (construction), pote (time), pothen (source), pou (position), eos-pote (limit), meti (loaded), ouchi (negated)",
    "M8": "gate return typed: answered | self-answered | null-refused | held-zero | volume | left-open",
    "M9": "apparatus (single/span) is a drift measurement on its term; carried, never deleted",
    "M10": "dynamis-family = potential term; question/answer sharing the root are one experiment",
}
RULE_STATUS = "proposed"  # operator promotes to "consented"; never automatic


def take_units(quantity: int, unit: int) -> dict:
    """TAKE(Q,u) = (n, r)_u. Whole takes until remainder is below the unit."""
    if unit <= 0:
        raise ValueError("unit must be a positive whole count")
    if quantity < 0:
        raise ValueError("quantity must be non-negative in this layer")
    n, r = divmod(quantity, unit)
    assert r < unit
    return {"quantity": quantity, "unit": unit, "takes": n, "remainder": r}


def _bare(s: str) -> str:
    """Accent/breathing-stripped lowercase for matching."""
    n = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in n if unicodedata.category(c) != "Mn").replace("ς", "σ")


NUMERALS = {  # bare-form -> whole count (M5)
    "εισ": 1, "μια": 1, "ενα": 1, "πρωτοσ": 1,
    "δυο": 2, "δεισ": 2, "τρεισ": 3, "τρια": 3, "τεσσαρεσ": 4,
    "πεντε": 5, "επτα": 7, "οκτω": 8, "εννεα": 9, "δεκα": 10,
    "δωδεκα": 12, "εικοσι": 20, "τριακοντα": 30, "εβδομηκοντα": 70,
    "εκατον": 100, "ενενηκοντα": 90,
}

# Homographs where accent/breathing carries the distinction the bare key
# would erase: ἐν (prep "in") vs ἕν ("one"), ἐξ (prep "out of") vs ἕξ ("six").
# These are matched on the MARKED form only; the unmarked homograph is
# recorded as ambiguous, never silently assigned a value.
MARKED_NUMERALS = {"ἕν": 1, "ἕξ": 6}
AMBIGUOUS_BARE = {"εν": "ἐν (prep) vs ἕν (one)", "εξ": "ἐξ (prep) vs ἕξ (six)"}

# M4 is about mu-initial FUNCTION words and oligo-/mikro- scale terms,
# not every mu-initial token (Μαρία is not an infinitesimal).
_MU_FUNCTION = {"μη", "μου", "μοι", "με", "μων", "μον", "μαλλον", "μητι",
                "μηπω", "μηδε", "μητε", "μην"}


def _is_mu_term(bare: str) -> bool:
    return bare in _MU_FUNCTION or bare.startswith(("ολιγ", "μικρ"))


def numeral_value(surface: str, lemma: str | None = None) -> tuple[int | None, str | None]:
    """(value, ambiguity) — value only when the marked form carries it.

    When a lemma witness is available (MorphGNT), it decides the homograph
    class: εἰς (prep, lemma εἰς) is not εἷς (one, lemma εἷς); ἐν is not ἕν.
    """
    if lemma:
        if lemma == "εἷς":
            return 1, None
        if lemma in ("εἰς", "ἐν", "ἐκ"):
            return None, None
    marked = unicodedata.normalize("NFC", surface.lower())
    if marked in MARKED_NUMERALS:
        return MARKED_NUMERALS[marked], None
    bare = _bare(surface)
    if bare in AMBIGUOUS_BARE or bare == "εισ":
        return None, AMBIGUOUS_BARE.get(bare, "εἰς (prep) vs εἷς (one)")
    return NUMERALS.get(bare), None


def _head_type(left_surfaces: list[str]) -> str:
    left = [_bare(s) for s in left_surfaces]
    joined = " ".join(left)
    if "εωσ" in left and "ποτε" in joined:
        return "limit"
    if left and left[0] in ("μητι",):
        return "loaded"
    if any(w.startswith("ινατι") for w in left):
        return "target_limit"
    for i, w in enumerate(left):
        if w == "δια" and i + 1 < len(left) and left[i + 1].startswith("τι"):
            return "cause"
    for w in left:
        if w.startswith("τισ") or w.startswith("τινεσ"):
            return "element"
        if w in ("τι", "τινα") or w.startswith("τι "):
            return "unknown"
        if w.startswith("πωσ"):
            return "construction"
        if w.startswith("ποτε"):
            return "time"
        if w.startswith("ποθεν"):
            return "source"
        if w.startswith(("που", "πη", "ποι")):
            return "position"
        if w.startswith("τι"):
            return "unknown"
    if left and left[0].startswith("ουχ"):
        return "negated"
    return "untyped"


def build_gates(tokens: list[dict]) -> list[dict]:
    """One record per ';' (gate) in the verse."""
    gates = []
    clause_start = 0
    for i, t in enumerate(tokens):
        if t["trailing_punct"] in ("full_stop", "ano_teleia", "gate") and t is not tokens[-1]:
            if t["trailing_punct"] != "gate":
                clause_start = i + 1
        if t["trailing_punct"] != "gate":
            continue
        left = tokens[clause_start:i + 1]
        # return: terms until next full stop (or verse end)
        j = i + 1
        following = []
        while j < len(tokens):
            following.append(tokens[j])
            if tokens[j]["trailing_punct"] == "full_stop":
                break
            j += 1
        last = (i == len(tokens) - 1)
        if last or not following:
            ret = "left-open"
        elif any((w.get("lemma_hint") or "") in ("λέγω", "εἶπον") for w in following):
            ret = "answered-in-scene"
        else:
            ret = "continues"
        gates.append({
            "gate_index": len(gates),
            "after_word": i,
            "head_type": _head_type([w["surface"] for w in left]),
            "left_terms": [w["surface"] for w in left],
            "following_terms": [w["surface"] for w in following],
            "kai_positions": [w["word_index"] for w in left
                              if _bare(w["surface"]) == "και"],
            "mu_terms": [w["surface"] for w in left
                         if _is_mu_term(_bare(w["surface"]))],
            "numerals": [{"surface": w["surface"], "value": v}
                         for w in left
                         if (v := numeral_value(w["surface"],
                                                w.get("lemma_hint"))[0]) is not None],
            "apparatus_in_span": [w["surface"] for w in left
                                  if w["leading_apparatus"] or w["apparatus_span"]],
            "return_proposed": ret,
            "rules": ["M2", "M7", "M8"],
            "status": RULE_STATUS,
        })
        clause_start = i + 1
    return gates


def build_equations(tokens: list[dict]) -> dict:
    """kaì-equality claims, numeral counts, mu-terms, potential terms."""
    kai = []
    numerals = []
    ambiguous = []
    mu_terms = []
    potential = []
    for i, t in enumerate(tokens):
        b = _bare(t["surface"])
        if b == "και":
            kai.append({
                "word_index": i,
                "left": tokens[i - 1]["surface"] if i > 0 else None,
                "right": tokens[i + 1]["surface"] if i + 1 < len(tokens) else None,
                "rule": "M1", "status": RULE_STATUS,
            })
        value, amb = numeral_value(t["surface"], t.get("lemma_hint"))
        if value is not None:
            numerals.append({"word_index": i, "surface": t["surface"],
                             "value": value, "rule": "M5",
                             "status": RULE_STATUS})
        elif amb:
            ambiguous.append({"word_index": i, "surface": t["surface"],
                              "ambiguity": amb, "rule": "M5",
                              "status": RULE_STATUS})
        if _is_mu_term(b):
            mu_terms.append({"word_index": i, "surface": t["surface"],
                             "rule": "M4", "status": RULE_STATUS})
        if "δυνα" in b:
            potential.append({"word_index": i, "surface": t["surface"],
                              "rule": "M10", "status": RULE_STATUS})
    return {"kai_equalities": kai, "numerals": numerals,
            "numerals_ambiguous": ambiguous,
            "mu_terms": mu_terms, "potential_terms": potential,
            "rules": RULES, "status": RULE_STATUS}


def math_for_verse(tokens: list[dict], verse_ref: str = "",
                   morph_stats: dict | None = None) -> dict:
    from grammations import (grammations_for_word, classify_math_lecture,
                             explicit_math_translation, cadence_roles,
                             morphgnt_need)
    gates = build_gates(tokens)
    equations = build_equations(tokens)
    lecture = classify_math_lecture(tokens, gates, equations)
    grammations: dict[int, dict] = {}
    for t in tokens:
        unclosed = False
        if morph_stats is not None:
            fake_word = {"lemma": t.get("lemma_hint") or "",
                         "word": t["surface"], "text": t.get("printed", ""),
                         "parse": "x"}
            unclosed = "lemma_hapax_in_matthew" in morphgnt_need(fake_word,
                                                                 morph_stats)
        rec = grammations_for_word(
            t["surface"], in_math_verse=lecture["is_math_lecture"],
            unclosed_proxy=unclosed)
        if rec:
            grammations[t["word_index"]] = rec
    return {"gates": gates, "equations": equations,
            "grammations": {str(k): v for k, v in grammations.items()},
            "math_lecture": lecture,
            "cadence_roles": {str(k): v for k, v in
                              cadence_roles(tokens).items()},
            "explicit_math_translation": explicit_math_translation(
                verse_ref, tokens, gates, equations, grammations),
            "division_primitive": "TAKE(Q,u)=(n,r)_u, r<u (M6)"}
