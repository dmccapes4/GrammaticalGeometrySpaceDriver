"""
GrammaticalGeometrySpaceDriver — divergence: words with no common translation.

The operator's rule (2026-11-08):

    "Have it simply identify all words which do not have a common translation.
     Those are almost always equations (limited data set, but it is reliable)."

A word whose independent dictionary witnesses do not converge on a shared gloss
is not a word with one meaning that we failed to find. It is a word carrying a
relation between its senses. ὤρυξεν holds reveal/conceal/channel/perforate at
once; that is four terms of a circuit, not four candidate translations.

WHY THIS IS NOT schema.compute_agreements
-----------------------------------------
`compute_agreements` compares whole rule values with string equality. Each
dictionary writes its own sentence, so two witnesses essentially never produce
a byte-identical value. Measured on the Matthew 25:18 run of 2026-11-03, it
reports zero cross-witness agreement for 11 of 15 words — including καὶ and
the articles. A measure that says "no common translation" for every word cannot
identify the words that have no common translation.

This module compares at GLOSS level instead: the content terms inside each
witness's statement. Agreement is then countable.

Everything here is deterministic. No model call. One witness either uses a
gloss term or it does not.

MEASURED RESULT, AND IT CAME OUT BACKWARDS
------------------------------------------
Run on the Matthew 25:18 primitives of 2026-11-03 (15 words, 6-14 witnesses
each), the consensus ranking is the reverse of what the operator's rule
predicts. ὤρυξεν — the word he decodes as four simultaneous senses, the word
that IS the equation — has the HIGHEST consensus in the verse (0.67, "dig"
used by 4 of 6 witnesses). καὶ ranks top for divergence at 0.09.

So absence of consensus does not pick out his equations in this data. The
dictionaries agree perfectly well that ὤρυξεν means "dig". Reading the fields
shows why, and the why is more useful than the measure:

  ὤρυξεν field:  dig(4) trench(3) hole(2) through(2) canal bury dug ground
                 landform material plant quarried stones
  καὶ field:     additive assertion comparative consequence contrastive
                 copulative disjunctive emphasis emphatic sequence too

καὶ's eleven glosses are eleven names for one grammatical function. ὤρυξεν's
are an action, three incompatible results (a trench is not a hole is not a
canal), and a material operation. The equation signature is not low consensus.
It is a field whose members are different KINDS of thing while a single gloss
sits on top of them.

Two further facts from the same measurement, both of which matter more than
the ranking:

  1. His four senses are not all retrieved. "channel" and "perforate" are in
     the field as canal/trench and through/hole. "reveal" and "conceal" are
     NOT in it at all, from any of the twelve witnesses. His arrow in
     MATTHEW_25_18_MANUAL_DECODING.md — `dig-> {reveal; conceal; channel;
     perforate}` — is doing real work on two of the four, and the tool has no
     path to them.

  2. κυρίου's field is fifteen terms of lordship: master(3) authority(2)
     lord(2) power(2) sovereign(2) supreme ordained divinities appointed. The
     adjectival sense he uses — lawful, valid, bounded and constrained — is
     absent from every witness the run queried. The collapse to "lord" was not
     the model overriding the field. The field never contained the alternative.
     That is a retrieval failure, and `bold.probe_unanimity` is where it gets
     caught: the corpus tags κύριος N- in 713 of 713 occurrences.

What this module is therefore GOOD for, on the evidence: finding words where
retrieval failed. λαβὼν, τοῦ and the second τὸ have zero witnesses in that run
— no lexical rules at all — and λαβὼν is a content word the operator has
decoded at length. Separating "no witnesses" from "no agreement" is the first
thing `equation_candidates` reports, for that reason.

Deciding whether the field holds one kind or several needs a semantic measure.
`tools/sem_sim.py` is the right instrument and `sentence_transformers` is not
installed in this project's venv, so that measure is NOT implemented here and
NOT claimed. `opposition_pairs` below is the cheap stand-in: a seeded antonym
list, which on this verse found nothing, because the antonyms the operator uses
are the two senses the lexica never supplied.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

# ─── what is not a gloss ───────────────────────────────────────────────────────

# Function words and lexicographic furniture. These appear in every dictionary's
# prose and would create false agreement if counted as glosses.
STOP = {
    "a", "an", "the", "of", "to", "in", "on", "at", "by", "for", "with", "from",
    "and", "or", "but", "as", "is", "are", "was", "were", "be", "been", "being",
    "it", "its", "this", "that", "these", "those", "there", "here", "which",
    "who", "whom", "whose", "what", "when", "where", "how", "why",
    "not", "no", "nor", "so", "than", "then", "also", "only", "even", "ever",
    "esp", "especially", "usually", "generally", "often", "sometimes", "freq",
    "frequently", "etc", "cf", "ie", "eg", "viz", "sc", "pl", "sg", "sing",
    "plur", "gen", "dat", "acc", "nom", "voc", "masc", "fem", "neut",
    "word", "words", "sense", "senses", "meaning", "meanings", "use", "used",
    "usage", "form", "forms", "term", "terms", "see", "also", "above", "below",
    "one", "two", "any", "all", "some", "more", "most", "very", "much", "many",
    "may", "can", "must", "would", "could", "should", "will", "shall",
    "have", "has", "had", "do", "does", "did", "make", "makes", "made",
    "lat", "latin", "greek", "gr", "homer", "hom", "nt", "lxx", "attic",
    "originally", "properly", "prop", "lit", "literally", "metaph",
    "metaphorically", "absol", "absolutely", "with", "without", "something",
    "someone", "thing", "things", "person", "persons",
}

_WORD_RE = re.compile(r"[a-z]+")


def _normalise(text: str) -> str:
    """Lower-case, strip accents, drop bracketed asides."""
    text = re.sub(r"\([^)]*\)", " ", text)
    text = re.sub(r"\[[^\]]*\]", " ", text)
    nfkd = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def gloss_terms(text: str, min_len: int = 3) -> set[str]:
    """
    Content terms from one witness's statement.

    Latin-script only on purpose: the Greek inside an LSJ entry is citation,
    not gloss, and counting it would make every witness agree on the headword.
    """
    norm = _normalise(text)
    return {
        w for w in _WORD_RE.findall(norm)
        if len(w) >= min_len and w not in STOP
    }


# ─── witness support ───────────────────────────────────────────────────────────

def _rule_fields(primitive: dict[str, Any]) -> Iterable[tuple[str, str]]:
    """Yield (source_id, text) for every witness statement in a primitive."""
    for field in ("lexical_rules", "semantic_rules"):
        for rule in primitive.get(field, []):
            sid = rule.get("source_id", "")
            val = rule.get("value", "")
            if sid and val:
                yield sid, val

    for t in primitive.get("translations", []):
        if isinstance(t, dict) and t.get("value"):
            yield t.get("source_id", "unknown"), t["value"]


def witness_support(primitive: dict[str, Any]) -> dict[str, set[str]]:
    """
    gloss term -> set of source_ids that use it.

    A source is counted once per term however many times it repeats it, so a
    verbose dictionary cannot outvote a terse one.
    """
    support: dict[str, set[str]] = defaultdict(set)
    for sid, text in _rule_fields(primitive):
        for term in gloss_terms(text):
            support[term].add(sid)
    return dict(support)


def witnesses(primitive: dict[str, Any]) -> set[str]:
    """Every source that made any statement about this word."""
    return {sid for sid, _ in _rule_fields(primitive)}


# ─── the measure ───────────────────────────────────────────────────────────────

def common_translation(primitive: dict[str, Any], top: int = 5) -> dict[str, Any]:
    """
    Does a common translation exist for this word?

    Returns:
      n_witnesses      how many sources spoke
      best             the most widely supported gloss term, or None
      best_support     how many sources used it
      consensus        best_support / n_witnesses, in [0, 1]
      has_common       consensus >= 0.5 AND best_support >= 2
      leaders          the top-N terms with their support counts
    """
    support = witness_support(primitive)
    wits = witnesses(primitive)
    n = len(wits)

    if not support or n == 0:
        return {
            "n_witnesses": n, "best": None, "best_support": 0,
            "consensus": 0.0, "has_common": False, "leaders": [],
        }

    ranked = sorted(support.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    best, best_sources = ranked[0]
    best_support = len(best_sources)
    consensus = best_support / n

    return {
        "n_witnesses": n,
        "best": best,
        "best_support": best_support,
        "consensus": round(consensus, 3),
        "has_common": consensus >= 0.5 and best_support >= 2,
        "leaders": [(t, len(s)) for t, s in ranked[:top]],
    }


def equation_candidates(primitives: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Rank a verse's words by absence of a common translation.

    The operator's claim is that the words at the top of this list are almost
    always equations. The ranking is the claim's test surface, not its proof.
    """
    rows = []
    for i, p in enumerate(primitives):
        ct = common_translation(p)
        # A word nobody spoke about is a retrieval failure, not a divergent
        # word. The first version of this function scored both as 0.0 consensus
        # and so put λαβὼν — which has no witnesses at all — at the top of a
        # list of words whose witnesses disagree. Those are different findings
        # and they need different work.
        rows.append({
            "index": i,
            "surface": p.get("word", {}).get("surface", "?"),
            "n_witnesses": ct["n_witnesses"],
            "best": ct["best"],
            "best_support": ct["best_support"],
            "consensus": ct["consensus"],
            "has_common": ct["has_common"],
            "divergence": round(1.0 - ct["consensus"], 3),
            "status": "NO WITNESSES" if ct["n_witnesses"] == 0 else "measured",
            "leaders": ct["leaders"],
        })
    # Un-retrieved words sort first and are labelled, rather than being mixed
    # into the divergence ranking where they would look like a result.
    return sorted(
        rows,
        key=lambda r: (r["n_witnesses"] != 0, -r["divergence"], r["surface"]),
    )


# ─── opposition inside one field ───────────────────────────────────────────────

# Curated. These are oppositions the operator's own decodings turn on, plus the
# obvious physical pairs. This list is NOT derived from data and is NOT complete;
# it is a seed, and a miss here is a false negative, never a false positive.
# An agent may extend it only with the operator's consent, per schema.py.
OPPOSITION_SEED: list[tuple[str, str]] = [
    ("reveal", "conceal"), ("reveal", "hide"), ("disclose", "conceal"),
    ("open", "close"), ("open", "shut"), ("uncover", "cover"),
    ("give", "take"), ("receive", "give"), ("add", "subtract"),
    ("rise", "fall"), ("ascend", "descend"), ("above", "below"),
    ("inside", "outside"), ("enter", "exit"), ("come", "depart"),
    ("come", "leave"), ("arrive", "depart"), ("begin", "end"),
    ("bind", "loose"), ("bound", "free"), ("gather", "scatter"),
    ("join", "separate"), ("build", "destroy"), ("light", "dark"),
    ("full", "empty"), ("increase", "decrease"), ("grow", "shrink"),
    ("remember", "forget"), ("find", "lose"), ("buy", "sell"),
    ("push", "pull"), ("attract", "repel"), ("positive", "negative"),
]


def opposition_pairs(primitive: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Seeded oppositions both present in this word's field.

    A word whose witnesses assert both X and not-X is not ambiguous. It is a
    relation between X and not-X — which is what makes ὤρυξεν a circuit rather
    than a mis-translated verb. This is the sharper signal of the two in this
    module, and the weaker one by coverage, because the seed list is short.
    """
    support = witness_support(primitive)
    found = []
    for a, b in OPPOSITION_SEED:
        if a in support and b in support:
            found.append({
                "pair": [a, b],
                "sources_a": sorted(support[a]),
                "sources_b": sorted(support[b]),
            })
    return found


# ─── run-directory entry points ────────────────────────────────────────────────

def load_verse_primitives(verse_jsonl: str | Path) -> list[dict[str, Any]]:
    """Read a run's verse.jsonl into a list of primitives, in word order."""
    out = []
    with Path(verse_jsonl).open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def format_table(rows: list[dict[str, Any]], primitives: list[dict] | None = None) -> str:
    """
    Two lists, because they are different findings.

    A word with no witnesses was not retrieved. A word whose witnesses disagree
    has a field. On the 2026-11-03 verse the equation word sits at the BOTTOM
    of the second list, so this table does not title itself "equation
    candidates". The field under each row is what he actually reads.
    """
    lines = ["RETRIEVAL FAILURES  (no witness stated a gloss)", ""]
    missing = [r for r in rows if r["status"] == "NO WITNESSES"]
    if missing:
        for r in missing:
            lines.append(f"  {r['surface']}")
    else:
        lines.append("  (none)")

    lines += [
        "",
        "GLOSS CONSENSUS  (lowest first — low consensus is not the equation marker;",
        "see the module docstring, MEASURED RESULT)",
        "",
        f"{'word':<11}{'wit':>4}{'best gloss':>16}{'sup':>5}{'cons':>7}{'common?':>9}",
        "-" * 54,
    ]
    for r in rows:
        if r["status"] == "NO WITNESSES":
            continue
        best = (r["best"] or "—")[:15]
        lines.append(
            f"{r['surface']:<11}{r['n_witnesses']:>4}{best:>16}"
            f"{r['best_support']:>5}{r['consensus']:>7.2f}"
            f"{('yes' if r['has_common'] else 'NO'):>9}"
        )
        if r["leaders"]:
            field = "  ".join(f"{t}({n})" for t, n in r["leaders"])
            lines.append(f"             {field}")

    if primitives:
        lines += ["", "OPPOSITIONS INSIDE ONE FIELD (seeded list; misses are false negatives)", ""]
        any_found = False
        for r in rows:
            pairs = opposition_pairs(primitives[r["index"]])
            if pairs:
                any_found = True
                for pr in pairs:
                    a, b = pr["pair"]
                    lines.append(
                        f"  {r['surface']:<11} {a} / {b}"
                        f"   [{len(pr['sources_a'])} vs {len(pr['sources_b'])} witnesses]"
                    )
        if not any_found:
            lines.append("  (none in the seed list)")

    return "\n".join(lines)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(
        description="Identify words with no common translation in a GGSD run."
    )
    ap.add_argument("verse_jsonl", help="path to a run's verse.jsonl")
    ap.add_argument("--json", action="store_true", help="emit JSON lines")
    args = ap.parse_args()

    prims = load_verse_primitives(args.verse_jsonl)
    rows = equation_candidates(prims)

    if args.json:
        for r in rows:
            r["oppositions"] = opposition_pairs(prims[r["index"]])
            print(json.dumps(r, ensure_ascii=False))
    else:
        print(format_table(rows, prims))


if __name__ == "__main__":
    main()
