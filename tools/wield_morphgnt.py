#!/usr/bin/env python3
"""
wield_morphgnt — act directly on the MorphGNT lexicon fork with GGSD's two
deterministic layers, no model in the loop.

The stemmer's end_rule mini-language is already punctuation cadence:

    A|B>C<D|E
    | | | | |
    | | | | +- optional tail   (after the second | : the part actually matched)
    | | | +--- named ending    (after < : a gate that NAMES, does not constrain)
    | | +----- alternant       (thal, between > and < : what the surface shows)
    | +------- graft cut       (> : stem-final is replaced by the alternant)
    +--------- alternative pre-stem fragments (ora-yog | ora-threl)

and '.' is the identity rule (form IS the stem). Mathematical grammation then
letter-parses the Greek alternants themselves: the surface letters are
compounds — ξ = velar + σ, ψ = labial + σ — so a rule κ>ξ<ς reads, letter by
letter, as "stem-final κ, surfaced as κ+σ fused, before ending ς".

Three outputs, each carrying WHERE and HOW:
  1. a generated test matrix comparing Tauber's utils.stemmer against the
     Velora stemmer in morphgnt/__init__.py (the fork's own __main__ stops
     mid-thought at '# A|B>C<D|E' — this finishes the thought by generation);
  2. a cadence+grammation census of every rule in nominal-endings.txt;
  3. a stem ledger: every nominal paradigm in forms.yaml tried against every
     ending line, recording lemma/gender/case (where), the rule's cadence
     parse and proposed stem (how), and where the paradigm refuses all lines.

Nothing here eliminates a lexical reading. A proposed stem is proposed.
"""
import itertools
import json
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEXICON = ROOT / "morphgnt" / "lexicon"
sys.path.insert(0, str(LEXICON))

from morphgnt.utils import stemmer as tauber_stemmer  # noqa: E402
from morphgnt import stemmer as velora_stemmer  # noqa: E402  (fork __init__.py)

CASES = ["NS", "GS", "AS", "DS", "VS", "NP", "GP", "AP", "DP", "VP"]

# ---------------------------------------------------------------- cadence ---

def parse_rule(rule):
    """Parse an end_rule as punctuation cadence. Returns its operator anatomy."""
    if rule == ".":
        return {"rule": rule, "kind": "identity",
                "cadence": ". = form is the stem (no cut)"}
    if ">" in rule and "<" in rule:
        gt, lt = rule.find(">"), rule.find("<")
        pre, thal, post = rule[:gt], rule[gt + 1:lt], rule[lt + 1:]
        ora = pre.split("|") if "|" in pre else ["", pre]
        ending, _, optional = post.partition("|")
        return {
            "rule": rule, "kind": "graft",
            "ora_alternatives": ora,        # before-fragments (ora-yog | ora-threl)
            "thal": thal,                   # alternant between > and <
            "named_ending": ending,         # after < : names, does not constrain
            "optional_tail": optional,      # after | : actually matched
            "matched_tail": ora[0] + thal + optional,
            "cadence": (f"graft: stem-final {'|'.join(ora)!r} > surfaced {thal!r} "
                        f"< ending named {ending!r}"
                        + (f" | optional tail {optional!r}" if optional else "")),
        }
    if "/" in rule:
        return {"rule": rule, "kind": "alternative-suffix",
                "alternatives": rule.split("/"),
                "cadence": "/ = rival suffixes, tried as separate plain rules"}
    return {"rule": rule, "kind": "plain-suffix",
            "cadence": f"plain suffix {rule!r}: strip if final"}


# ------------------------------------------------------------- grammation ---

# compound surface letters, letter-parsed (his: ξ/ψ are fusions, not atoms)
FUSIONS = {"ξ": "velar + σ", "ψ": "labial + σ", "ζ": "σ + dental (fused)"}
STOP_CLASS = {}
for ch in "κγχ":
    STOP_CLASS[ch] = "velar"
for ch in "πβφ":
    STOP_CLASS[ch] = "labial"
for ch in "τδθ":
    STOP_CLASS[ch] = "dental"


def grammate_rule(parsed):
    """Letter-parse a graft rule's alternation: stem-final -> surface thal."""
    if parsed["kind"] != "graft":
        return None
    thal = parsed["thal"]
    fragments = [a for a in parsed["ora_alternatives"] if a]
    if not fragments:
        return None
    if not thal:
        return {"stem_finals": fragments, "surface": "",
                "reading": "empty thal: stem-final fragment deleted on the surface"}
    surface = thal[-1]
    sigma = "σ" if surface == "ς" else surface  # ς is σ in final position
    notes = []
    for frag in fragments:
        sf, cls = frag[-1], STOP_CLASS.get(frag[-1])
        if len(thal) > 1:
            notes.append(f"{frag} → {thal} [cluster simplified, vowel of thal "
                         f"lengthened: {thal}]")
        elif sigma in FUSIONS and cls in ("velar", "labial"):
            notes.append(f"{sf} ({cls}) + σ → {surface} [{FUSIONS[sigma]}]")
        elif sigma == "σ" and cls == "dental":
            notes.append(f"{sf} (dental) + σ → {surface} [dental absorbed]")
        elif sigma == "σ" and sf == "ν":
            notes.append(f"ν + σ → {surface} [nasal absorbed]")
        elif surface == sf:
            notes.append(f"{sf} → {surface} [no alternation]")
        else:
            notes.append(f"{sf} ({cls or '?'}) → {surface} [unclassified]")
    return {"stem_finals": [f[-1] for f in fragments], "surface": surface,
            "reading": "; ".join(notes)}


# ------------------------------------------------------- generated matrix ---

MATRIX_RULES = ["A>B<C", "A><", "A>B<C|D", "A|B><", "A|B>C<D|E",
                ".", "C", "><", "A>B<", ">B<C", "ς", "κ>ξ<ς", "π>ψ<σ|ι(ν)"]


def generated_matrix():
    alphabet = ["A", "B", "C", "D", "E", "X"]
    forms = [""] + ["".join(t) for n in (1, 2, 3)
                    for t in itertools.product(alphabet, repeat=n)]
    forms += ["φύλαξ", "φύλακς", "κόψις", "κόψιν"]  # real-shape graft bait
    rows, divergences = [], []
    for rule in MATRIX_RULES:
        for form in forms:
            t, v = tauber_stemmer(form, rule), velora_stemmer(form, rule)
            row = {"rule": rule, "cadence": parse_rule(rule)["cadence"],
                   "form": form, "tauber": t, "velora": v, "agree": t == v}
            rows.append(row)
            if t != v:
                row["how"] = divergence_cause(rule, form, t, v)
                divergences.append(row)
    return rows, divergences


def divergence_cause(rule, form, t, v):
    parsed = parse_rule(rule)
    if parsed["kind"] == "graft" and not parsed["matched_tail"]:
        return ("zero-length matched tail: utils computes form[:-0] == '' and "
                "loses the form; the Velora stemmer returns form + fragments")
    return "unclassified divergence — inspect manually"


# ------------------------------------------------------------ wield forms ---

ACUTE, GRAVE, CIRC = "\u0301", "\u0300", "\u0342"

def strip_accents(w):
    return "".join(
        unicodedata.normalize("NFC", "".join(
            c for c in unicodedata.normalize("NFD", ch)
            if c not in [ACUTE, GRAVE, CIRC]))
        for ch in w)


def load_endings():
    endings = []
    for num, line in enumerate(
            (LEXICON / "nominal-endings.txt").read_text(encoding="utf-8").splitlines(), 1):
        body = line.split("#")[0].strip()
        if not body:
            continue
        parts = body.split()
        if len(parts) < 10:
            continue
        row = dict(zip(CASES, [p.strip() for p in parts[:10]]))
        row["line_num"] = num
        row["comment"] = line.split("#", 1)[1].strip() if "#" in line else ""
        endings.append(row)
    return endings


def nominal_paradigms(forms_yaml):
    """lemma -> gender -> case -> set(stripped forms); nominals only."""
    out = {}
    for lemma, by_gender in forms_yaml.items():
        if not isinstance(by_gender, dict):
            continue
        genders = {}
        for gender, by_case in by_gender.items():
            if gender not in ("M", "F", "N") or not isinstance(by_case, dict):
                continue
            cases = {}
            for case, cell in by_case.items():
                if case not in CASES or not isinstance(cell, dict):
                    continue
                found = {strip_accents(e["form"]) for e in cell.get("forms", [])
                         if isinstance(e, dict) and "form" in e}
                if found:
                    cases[case] = found
            if cases:
                genders[gender] = cases
        if genders:
            out[lemma] = genders
    return out


def wield(paradigms, endings):
    ledger, fails = [], []
    for lemma in sorted(paradigms):
        for gender, by_case in paradigms[lemma].items():
            matches = []
            for ending in endings:
                stem, how, ok = None, [], True
                for case in CASES:
                    if case not in by_case:
                        continue
                    form_list = sorted(by_case[case])
                    end_list = sorted(ending[case].split("/"))
                    if len(form_list) != len(end_list):
                        ok = False
                        break
                    for form, end in zip(form_list, end_list):
                        proposed = tauber_stemmer(form, end)
                        if proposed is None:
                            ok = False
                            break
                        if stem is None:
                            stem = proposed
                        if stem != proposed:
                            ok = False
                            break
                        how.append({"case": case, "form": form, "rule": end,
                                    "cadence": parse_rule(end),
                                    "grammation": grammate_rule(parse_rule(end)),
                                    "proposed_stem": proposed})
                    if not ok:
                        break
                if ok and stem is not None:
                    matches.append({"lemma": lemma, "gender": gender,
                                    "ending_line": ending["line_num"],
                                    "comment": ending["comment"],
                                    "stem": stem, "how": how})
            if matches:
                ledger.extend(matches)
            else:
                fails.append({"lemma": lemma, "gender": gender,
                              "cases": {c: sorted(s) for c, s in by_case.items()}})
    return ledger, fails


# -------------------------------------------------------------------- main ---

def main():
    import yaml
    out_dir = LEXICON / "wield_output"
    out_dir.mkdir(exist_ok=True)

    matrix, divergences = generated_matrix()
    (out_dir / "generated_matrix.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in matrix), encoding="utf-8")
    (out_dir / "divergences.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in divergences), encoding="utf-8")

    endings = load_endings()
    rule_census, grammation_census = Counter(), Counter()
    for ending in endings:
        for case in CASES:
            parsed = parse_rule(ending[case])
            rule_census[parsed["kind"]] += 1
            g = grammate_rule(parsed)
            if g:
                grammation_census[g["reading"]] += 1

    forms_yaml = yaml.safe_load((LEXICON / "forms.yaml").read_text(encoding="utf-8"))
    paradigms = nominal_paradigms(forms_yaml)
    ledger, fails = wield(paradigms, endings)
    (out_dir / "stem_ledger.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in ledger), encoding="utf-8")
    (out_dir / "paradigm_fails.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in fails), encoding="utf-8")

    matched = {(r["lemma"], r["gender"]) for r in ledger}
    cells_per = Counter()
    for r in ledger:
        key = (r["lemma"], r["gender"])
        cells_per[key] = max(cells_per[key], len(r["how"]))
    sparse = sum(1 for v in cells_per.values() if v <= 2)
    dense = sum(1 for v in cells_per.values() if v >= 8)
    lines = [
        "# WIELD REPORT — stemmer on the fork, cadence + grammation",
        "",
        f"Generated matrix: {len(matrix)} (rule, form) pairs over {len(MATRIX_RULES)} rules; "
        f"tauber vs velora agree on {len(matrix) - len(divergences)}, diverge on {len(divergences)}.",
        "",
        "## Divergences (where and how)",
    ]
    for d in divergences[:20]:
        lines.append(f"- rule `{d['rule']}` form `{d['form']}`: tauber={d['tauber']!r} "
                     f"velora={d['velora']!r} — {d.get('how', '')}")
    lines += ["", "## Rule census (nominal-endings.txt, all case cells)",
              *[f"- {k}: {v}" for k, v in rule_census.most_common()],
              "", "## Grammation census (graft alternations, letter-parsed)",
              *[f"- {k}: {v}" for k, v in grammation_census.most_common()],
              "", "## Wielding on forms.yaml nominals",
              f"- paradigms tried: {sum(len(g) for g in paradigms.values())} "
              f"(lemma x gender) over {len(endings)} ending lines",
              f"- paradigm matches (lemma, gender, ending line): {len(ledger)}",
              f"- paradigms matched at least once: {len(matched)}",
              f"- paradigms refusing every line (the honest register): {len(fails)}",
              f"- caveat, counted: {sparse} matched paradigms rest on <=2 attested "
              f"case cells ('not refused', not verified); {dense} rest on >=8 cells. "
              "forms.yaml is attestation-sparse where Tauber's checker used the "
              "full SBLGNT fileset — sparse matches are proposals, dense ones hold.",
              "", "Full ledger: stem_ledger.jsonl — every row carries where "
              "(lemma/gender/case/form, ending line) and how (rule, cadence parse, "
              "grammation, proposed stem). Fails: paradigm_fails.jsonl."]
    (out_dir / "WIELD_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
