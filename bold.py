"""
GrammaticalGeometrySpaceDriver — bold.py: the operator's bold checks, mechanised.

The operator, 2026-11-08:

    "Also see if you can get it to decode more like me somehow. It is mechanical
     but my method requires some bold checking."

He is right that it is mechanical, and that is the whole opening. His bold moves
are not inspiration; they are a short, finite list of operations he performs on
every word and the tool performs on none. Enumerate the operations and the
boldness becomes a probe suite.

Each probe below is DETERMINISTIC and has a hard oracle: a token is in the
dropped set or it is not; a substring is an attested lemma or it is not; the
corpus tags a lemma N ways or it does not. No probe proposes a reading. Every
probe hands him a list and stops. That is the `no-agentic-loops` precondition
satisfied for free, and it matches his own architecture note in
REFLECTION_GGSD_METHOD_v0.0.3.md: "The agent does not decode."

THE FIVE PROBES
---------------
  1  dropped      tokens the tokeniser deletes before decoding begins
  2  unanimity    corpus POS agreement, flagged when it is suspiciously total
  3  submorphemic substrings that are themselves attested lemmas
  4  parses       every morphological parse attested for the surface form
  5  phonetic     the transliteration skeleton, for sound-level reading

What each probe CANNOT do is stated in its docstring. A probe that silently
fails is worse than no probe, which is the lesson of the 2026-11-03 run where
`eliminations` stayed empty and `validate_primitive` passed anyway.
"""

from __future__ import annotations

import json
import re
import unicodedata as ud
from collections import Counter
from pathlib import Path
from typing import Any

# ─── shared normalisation ──────────────────────────────────────────────────────

def bare(s: str) -> str:
    """
    Accent-, breathing- and case-stripped Greek, with final sigma regularised.

    This exists because the naive version of probe 3 returned nothing: the ά in
    λαμβάνω (alpha + acute) and the ἄ in ἄνω (alpha + smooth + acute) are
    different codepoints, so substring matching failed on every word. The
    operator's readings work at the level of bare letters, so the probe must too.
    """
    n = ud.normalize("NFD", s.lower())
    stripped = "".join(c for c in n if not ud.combining(c))
    return stripped.replace("ς", "σ")


# ─── probe 1: what the tokeniser throws away ───────────────────────────────────

# Mirrors ggsd.tokenise_greek. Kept as a literal copy so a change there shows up
# here as a divergence rather than being silently inherited.
TOKENISER_STRIP = r"[·,;\.·—\[\]()]"


def probe_dropped(greek_text: str) -> dict[str, Any]:
    """
    Tokens and marks that never reach a primitive.

    `ggsd.tokenise_greek` strips punctuation. The operator's reference decoding
    in MATTHEW_25_18_MANUAL_DECODING.md gives the final period a gloss —
    "the infinitessimal; approaching infinity; end of frame; current directory" —
    so the tool is structurally incapable of reproducing his own reference
    output for that token. This probe reports the gap; it does not fix the
    tokeniser, because changing tokenisation changes every stored run.

    Cannot do: tell you whether a dropped mark carries meaning. It reports
    presence and position only.
    """
    marks = []
    for m in re.finditer(TOKENISER_STRIP, greek_text):
        marks.append({"mark": m.group(0), "offset": m.start()})
    return {
        "probe": "dropped",
        "n_dropped": len(marks),
        "dropped": marks,
        "note": (
            "ggsd.tokenise_greek removes these before any primitive is built. "
            "The operator's reference decoding glosses the sentence-final period."
        ),
    }


# ─── corpus index ──────────────────────────────────────────────────────────────

class Corpus:
    """
    MorphGNT as a deterministic lookup. Built once, reused by probes 2-4.

    Row format (whitespace separated):
        012514 A- ----APM- ἰδίους ἰδίους ἰδίους ἴδιος
        [0] book/ch/verse  [1] POS  [2] parse  [3] surface
        [4] normalised     [5] stripped        [6] lemma
    """

    def __init__(self, sblgnt_dir: str | Path):
        self.lemma_pos: dict[str, Counter] = {}
        self.lemma_count: Counter = Counter()
        self.surface_parses: dict[str, Counter] = {}
        self.bare_lemma: dict[str, set[str]] = {}
        self.surface_lemmas: dict[str, Counter] = {}

        for path in sorted(Path(sblgnt_dir).glob("*-morphgnt.txt")):
            with path.open(encoding="utf-8") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) < 7:
                        continue
                    pos, parse, surface, lemma = parts[1], parts[2], parts[3], parts[6]
                    self.lemma_pos.setdefault(lemma, Counter())[pos] += 1
                    self.lemma_count[lemma] += 1
                    self.surface_parses.setdefault(surface, Counter())[f"{pos} {parse}"] += 1
                    self.bare_lemma.setdefault(bare(lemma), set()).add(lemma)
                    self.surface_lemmas.setdefault(bare(surface), Counter())[lemma] += 1

    @property
    def n_lemmas(self) -> int:
        return len(self.lemma_count)

    def resolve_lemmas(self, surface: str) -> list[str]:
        """
        Lemmas the corpus assigns to this surface form, commonest first.

        A stored primitive carries no lemma — `source_retrievals["morphgnt"]` is
        a provenance stub with a url and a timestamp and nothing else. So the
        lemma has to come from the corpus, which is better anyway: where a
        surface form maps to more than one lemma the probe sees all of them
        instead of inheriting one.
        """
        return [lem for lem, _ in self.surface_lemmas.get(bare(surface), Counter()).most_common()]


# ─── probe 2: unanimity as a warning, not a confirmation ───────────────────────

# MorphGNT open-class tags. Unanimity only means anything here: an article is
# an article 19,769 times out of 19,769 and no lexicon disputes it, so flagging
# the closed classes buries the one case that matters under every τὸ in the NT.
OPEN_CLASS = {"N-", "V-", "A-", "D-"}


def probe_unanimity(corpus: Corpus, lemma: str, min_n: int = 50) -> dict[str, Any]:
    """
    How the corpus tags this lemma, and whether the agreement is too clean.

    The reasoning, which is the operator's and not mine. κύριος is tagged N-
    (noun) in 713 of 713 New Testament occurrences. Zero variation. LSJ carries
    an adjective κύριος — lawful, valid, authoritative — and the operator's
    decoding uses exactly that sense. The corpus cannot be cited against him,
    because 713 identical tags are not 713 independent judgements. They are one
    editorial decision applied 713 times and then inherited by every downstream
    tool, including this one.

    So unanimity at high n is flagged as an EDITORIAL CONSENSUS RISK. It is the
    same object as the false header in REPORT_POV_FIRMWARE_VS_HONORIFIC: a layer
    the trained eye reads as the document.

    Cannot do: tell you the alternative sense is correct here. It tells you the
    corpus never tested it.
    """
    pos_counts = corpus.lemma_pos.get(lemma, Counter())
    n = sum(pos_counts.values())
    if n == 0:
        return {"probe": "unanimity", "lemma": lemma, "n": 0,
                "pos": {}, "unanimous": False, "flag": "lemma not in corpus"}

    top_pos, top_n = pos_counts.most_common(1)[0]
    unanimous = len(pos_counts) == 1

    flag = ""
    if unanimous and top_pos not in OPEN_CLASS:
        flag = f"closed class ({top_pos}); unanimity expected, not informative"
    elif unanimous and top_pos == "N-" and n >= min_n:
        # Nouns only. Flagging every unanimous verb buried κύριος under
        # λαμβάνω, ἀπέρχομαι and γῆ-class noise: those lemmas really are verbs.
        # The failure that costs a reading is a noun tag sitting on a word the
        # lexica also enter as an adjective. See probe_preview_senses.
        flag = (
            f"EDITORIAL CONSENSUS RISK: {n}/{n} tagged {top_pos} with zero "
            f"variation. A noun tag with no other part of speech in the corpus "
            f"is one editorial decision, not {n} confirmations. "
            f"Check the lexica for an adjective."
        )
    elif unanimous:
        flag = f"unanimous but low n ({n}); weak either way"
    else:
        flag = f"{len(pos_counts)} parts of speech attested; no collapse to check"

    return {
        "probe": "unanimity",
        "lemma": lemma,
        "n": n,
        "pos": dict(pos_counts),
        "unanimous": unanimous,
        "flag": flag,
    }


# ─── probe 3: substrings that are themselves lemmas ────────────────────────────

def probe_submorphemic(corpus: Corpus, surface: str, min_len: int = 3,
                       min_corpus_n: int = 1) -> dict[str, Any]:
    """
    Attested lemmas occurring inside this word, on bare letters.

    This mechanises the operator's sub-word reading. His λαμβάνω → ... άνω,
    glossed "top; upper limit", is licensed by the corpus: ἄνω is an attested
    NT lemma, 9 occurrences, tagged D- (adverb). That is not an interpretation,
    it is a lookup, and the tool can do it on every word of all 1071 verses.

    Cannot do: distinguish a morphological relative from a coincidence. Greek
    has 5,400-odd lemmas and short strings collide. κύριος contains ἰός
    ("poison", 3 NT occurrences) by accident of spelling. Hence `length` and
    `corpus_n` on every hit, and hence min_len=3 as a floor rather than 2.
    Treat any hit shorter than 4 letters as noise until something else
    corroborates it.
    """
    b = bare(surface)
    hits = []
    for i in range(len(b)):
        for j in range(i + min_len, len(b) + 1):
            sub = b[i:j]
            if sub == b:
                continue
            for lemma in corpus.bare_lemma.get(sub, ()):
                cn = corpus.lemma_count[lemma]
                if cn >= min_corpus_n:
                    hits.append({
                        "substring": sub,
                        "lemma": lemma,
                        "length": len(sub),
                        "corpus_n": cn,
                        "pos": dict(corpus.lemma_pos.get(lemma, Counter())),
                        "offset": i,
                        "confidence": "weak" if len(sub) < 4 else "worth a look",
                    })
    hits.sort(key=lambda h: (-h["length"], -h["corpus_n"]))
    return {"probe": "submorphemic", "surface": surface, "bare": b,
            "n_hits": len(hits), "hits": hits}


# ─── probe 4: every parse the surface form actually takes ──────────────────────

def probe_parses(corpus: Corpus, surface: str) -> dict[str, Any]:
    """
    All morphological parses attested for this exact surface form in the corpus.

    Where a surface form is genuinely ambiguous, the tool should see the
    ambiguity rather than inherit one resolution. This is the grammar-as-
    constraint principle applied honestly: the constraint is the SET of
    attested parses, not the one the editor chose at this site.

    Cannot do: resolve the ambiguity. That is the operator's job and the
    constraint's job, in that order.
    """
    parses = corpus.surface_parses.get(surface, Counter())
    return {
        "probe": "parses",
        "surface": surface,
        "n_distinct": len(parses),
        "parses": [{"parse": p, "n": c} for p, c in parses.most_common()],
        "ambiguous": len(parses) > 1,
    }


# ─── probe 5: the sound ────────────────────────────────────────────────────────

_TRANSLIT = {
    "α": "a", "β": "b", "γ": "g", "δ": "d", "ε": "e", "ζ": "z", "η": "e",
    "θ": "th", "ι": "i", "κ": "k", "λ": "l", "μ": "m", "ν": "n", "ξ": "x",
    "ο": "o", "π": "p", "ρ": "r", "σ": "s", "τ": "t", "υ": "u", "φ": "ph",
    "χ": "ch", "ψ": "ps", "ω": "o",
}


def probe_phonetic(surface: str) -> dict[str, Any]:
    """
    Transliteration skeleton, for reading at the level of sound.

    The operator's τοῦ κυρίου αὐτοῦ → "the curio's author" is a sound reading.
    This probe supplies the skeleton it operates on and nothing more.

    Cannot do: find the English. Deliberately. Matching a skeleton against a
    wordlist would generate hundreds of candidates per verse and bury the
    signal, which is the failure mode of the 2026-11-03 run's five
    interchangeable "possible interpretations". The skeleton is for him to read.
    """
    b = bare(surface)
    return {
        "probe": "phonetic",
        "surface": surface,
        "skeleton": "".join(_TRANSLIT.get(c, c) for c in b),
    }


# ─── the suite ─────────────────────────────────────────────────────────────────

_POS_LABEL = re.compile(r"\((adjective|noun|verb|adverb|participle)\)", re.IGNORECASE)


def probe_preview_senses(primitive: dict[str, Any] | None) -> dict[str, Any]:
    """
    Senses present in a stored dictionary preview and absent from the rules.

    Measured on the 2026-11-03 run. logeion_shortdef's preview for κυρίου is:

        κύριος, κύριος α ον, able, with power, by right, sovereign (adjective)
        | κύριος2, a lord, master

    The extracted rules kept lord/master/sovereign and recorded the part of
    speech as "noun". The pipe, the second headword, and the word "adjective"
    never made it into a rule. The field the model filtered was already missing
    the sense the operator uses, so no later step could have kept it.

    The pipe is shortdef's own headword separator. This probe splits on it and
    reports a side whose explicit part-of-speech label is not in the rules.

    Cannot do: decide which headword this occurrence is. It reports that the
    retrieval contained two and the rules kept one.
    """
    if not primitive:
        return {"probe": "preview_senses", "splits": []}

    from divergence import gloss_terms

    rule_blob = " ".join(
        (r.get("value") or "")
        for field in ("grammatical_rules", "lexical_rules", "semantic_rules")
        for r in primitive.get(field, [])
    ).lower()
    rule_terms: set[str] = set()
    for field in ("lexical_rules", "semantic_rules"):
        for r in primitive.get(field, []):
            rule_terms |= gloss_terms(r.get("value") or "")

    splits = []
    for sid, entry in primitive.get("source_retrievals", {}).items():
        if not isinstance(entry, dict):
            continue
        preview = entry.get("entry_preview") or ""
        if " | " not in preview:
            continue
        for i, part in enumerate(p.strip() for p in preview.split("|")):
            labels = [m.group(1).lower() for m in _POS_LABEL.finditer(part)]
            missing_labels = [lb for lb in labels if lb not in rule_blob]
            missing_terms = sorted(gloss_terms(part) - rule_terms)
            if not missing_labels and not missing_terms:
                continue
            splits.append({
                "source_id": sid,
                "side": i,
                "text": part,
                "pos_labels": labels,
                "pos_absent_from_rules": missing_labels,
                "glosses_absent_from_rules": missing_terms,
            })
    return {"probe": "preview_senses", "splits": splits}


def run_probes(corpus: Corpus, surface: str,
               primitive: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    All per-word probes for one word.

    Probes 2 and 3 run on the LEMMA as well as the surface form. This is not a
    refinement, it is the difference between the probe working and not working:
    the surface λαβὼν contains no attested lemma, but its dictionary form
    λαμβάνω contains ἄνω, which is the operator's reading. A probe that only
    ever sees inflected forms would have reported nothing and looked correct.
    """
    lemmas = corpus.resolve_lemmas(surface) or [surface]

    sub_hits: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for form in [surface, *lemmas]:
        for h in probe_submorphemic(corpus, form)["hits"]:
            key = (h["lemma"], h["substring"])
            if key not in seen:
                seen.add(key)
                sub_hits.append({**h, "found_in": form})
    sub_hits.sort(key=lambda h: (-h["length"], -h["corpus_n"]))

    return {
        "surface": surface,
        "lemmas": lemmas,
        "unanimity": [probe_unanimity(corpus, lem) for lem in lemmas],
        "preview_senses": probe_preview_senses(primitive),
        "submorphemic": {"n_hits": len(sub_hits), "hits": sub_hits},
        "parses": probe_parses(corpus, surface),
        "phonetic": probe_phonetic(surface),
    }


_POS_NAME = {
    "N-": "noun", "V-": "verb", "A-": "adjective", "D-": "adverb",
    "RA": "article", "RD": "demonstrative", "RP": "pronoun", "RR": "relative",
    "C-": "conjunction", "P-": "preposition", "X-": "particle", "I-": "interjection",
}


def _named_parse(parse: str, n: int) -> str:
    code = parse.split()[0] if parse else "?"
    name = _POS_NAME.get(code, code)
    return f"{parse} [{name}] ({n}x)"


def format_probes(verse_text: str, results: list[dict[str, Any]]) -> str:
    out: list[str] = ["BOLD CHECKS", "=" * 74, ""]

    if not verse_text:
        out.append("1. DROPPED BY THE TOKENISER  (verse text was not passed)")
        out.append("")
    else:
        d = probe_dropped(verse_text)
        out.append(f"1. DROPPED BY THE TOKENISER  ({d['n_dropped']} marks)")
        for m in d["dropped"]:
            out.append(f"     '{m['mark']}' at offset {m['offset']}")
        out.append(f"   {d['note']}")
        out.append("")

    out.append("2. EDITORIAL CONSENSUS RISK")
    flagged = False
    for r in results:
        for u in r["unanimity"]:
            if "RISK" in u["flag"]:
                flagged = True
                out.append(f"     {r['surface']:<10} lemma {u['lemma']:<12} {u['pos']}")
                out.append(f"       {u['flag']}")
    if not flagged:
        out.append("     (none — nouns only; a unanimous verb is a verb)")
    out.append("")

    out.append("2b. SENSES IN THE PREVIEW THAT THE RULES DROPPED")
    dropped = False
    for r in results:
        for sp in r.get("preview_senses", {}).get("splits", []):
            if not sp["pos_absent_from_rules"]:
                continue
            dropped = True
            absent = ", ".join(sp["pos_absent_from_rules"])
            glosses = ", ".join(sp["glosses_absent_from_rules"]) or "—"
            out.append(f"     {r['surface']:<10} {sp['source_id']} side {sp['side']}")
            out.append(f"       part of speech in the preview, absent from the rules: {absent}")
            out.append(f"       glosses on that side absent from the rules: {glosses}")
            out.append(f"       preview: {sp['text']}")
    if not dropped:
        out.append("     (none)")
    out.append("")

    out.append("3. SUBMORPHEMIC HITS  (attested lemmas inside the word)")
    found = False
    for r in results:
        for h in r["submorphemic"]["hits"]:
            found = True
            out.append(
                f"     {r['surface']:<10} via {h['found_in']:<10} contains {h['lemma']:<9} "
                f"({h['substring']}, {h['length']} letters, {h['corpus_n']}x, "
                f"{','.join(h['pos'])})  [{h['confidence']}]"
            )
    if not found:
        out.append("     (none)")
    out.append("")

    out.append("4. SURFACE-FORM PARSE AMBIGUITY")
    amb = [r for r in results if r["parses"]["ambiguous"]]
    if not amb:
        out.append("     (none ambiguous in corpus)")
    for r in amb:
        ps = ", ".join(
            _named_parse(p["parse"], p["n"]) for p in r["parses"]["parses"]
        )
        out.append(f"     {r['surface']:<10} {r['parses']['n_distinct']} parses: {ps}")
    out.append("")

    out.append("5. PHONETIC SKELETON")
    out.append("     " + " ".join(r["phonetic"]["skeleton"] for r in results))
    out.append("")
    return "\n".join(out)


def render_checks(
    primitives: list[dict[str, Any]],
    greek_text: str = "",
    sblgnt_dir: str | Path | None = None,
) -> str:
    """
    Both halves of the 2026-11-08 request, as one text block.

    The first half is the gloss-consensus table. On the verse it was measured
    against, low consensus does not select the equation word; the table says so.
    The second half is the probe suite. It does select the moves he makes:
    the dropped period, the adjective the rules discarded, the lemma inside
    the lemma, the minority parse.
    """
    from divergence import equation_candidates, format_table

    parts = [format_table(equation_candidates(primitives), primitives), ""]
    sblgnt = Path(sblgnt_dir) if sblgnt_dir else Path(__file__).resolve().parent / "morphgnt" / "sblgnt"
    if sblgnt.is_dir():
        corpus = Corpus(sblgnt)
        results = [
            run_probes(corpus, p.get("word", {}).get("surface", ""), p)
            for p in primitives
        ]
        parts.append(f"[corpus: {corpus.n_lemmas} distinct lemmas]")
        parts.append(format_probes(greek_text, results))
    else:
        parts.append(f"[bold checks skipped: corpus dir not found at {sblgnt}]")
    return "\n".join(parts)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="Run the bold-check probes on a GGSD run.")
    ap.add_argument("verse_jsonl", help="path to a run's verse.jsonl")
    ap.add_argument("--sblgnt", default="morphgnt/sblgnt", help="MorphGNT sblgnt dir")
    ap.add_argument("--text", default="", help="raw verse text, for the dropped probe")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    prims = []
    with Path(args.verse_jsonl).open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    prims.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    corpus = Corpus(args.sblgnt)
    results = [
        run_probes(corpus, p.get("word", {}).get("surface", ""), p)
        for p in prims
    ]

    if args.json:
        for r in results:
            print(json.dumps(r, ensure_ascii=False))
    else:
        print(f"[corpus: {corpus.n_lemmas} distinct lemmas]\n")
        print(format_probes(args.text, results))


if __name__ == "__main__":
    main()
