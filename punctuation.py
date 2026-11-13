"""
GGSD punctuation layer — deterministic, no model calls.

Parses the printed Greek text (MorphGNT field 3, or any punctuated string)
into token objects carrying punctuation, apparatus, accent and breathing,
plus a verse-level cadence map. Word surfaces come from the clean field
(MorphGNT field 4) whenever available so token counts never change.

Marks (operator grammar, docs/GREEK_PUNCTUATION_BASELINE_20261111.md):
  , comma (breath) · ano teleia (strong hold / evaluate) . full stop (close)
  ; Greek gate (conditional domain) — em dash (operator grammar; absent
  from Homer/Pindar baselines, flagged) : colon (absent from corpora, flagged)
Elision (U+02BC) and koronis (U+1FBD) are NEVER cadence: excluded by design.
"""
from __future__ import annotations

import unicodedata

MARK_BY_CHAR = {
    ",": "comma",
    "·": "ano_teleia", "·": "ano_teleia",   # U+0387 == U+00B7 in Greek text
    ".": "full_stop",
    ";": "gate", ";": "gate",               # U+037E Greek question mark
    "—": "em_dash",
    ":": "colon",
}
WEIGHTS = {"comma": 1, "ano_teleia": 2, "full_stop": 3, "gate": "Q",
           "em_dash": 2, "colon": 2, "none": 0}
BASELINE_ABSENT = {"em_dash", "colon"}  # 0 occurrences in Homer/Pindar packs

_VOWELS = set("αεηιουω")
_SPEECH_LEMMAS = {"λέγω", "εἶπον", "φημί", "ἔφην"}


def _decomp(ch: str) -> list[str]:
    return [c for c in unicodedata.normalize("NFD", ch)]


def accent_profile(surface: str) -> dict:
    """Deterministic accent/breathing profile from Unicode decomposition.
    Input is NFC-normalised first so canonically equivalent encodings
    (NFC vs NFD) produce identical records; the stored surface is unchanged."""
    surface = unicodedata.normalize("NFC", surface)
    classes: list[str] = []
    breathings: list[str] = []
    vowel_groups = 0
    accented_group = None
    in_vowel = False
    for ch in surface:
        parts = _decomp(ch)
        base = parts[0].lower() if parts else ch.lower()
        is_vowel = base in _VOWELS
        if is_vowel and not in_vowel:
            vowel_groups += 1
            in_vowel = True
        elif not is_vowel:
            in_vowel = False
        for c in parts[1:]:
            name = unicodedata.name(c, "")
            if "COMBINING ACUTE" in name:
                classes.append("acute"); accented_group = vowel_groups
            elif "COMBINING GRAVE" in name:
                classes.append("grave"); accented_group = vowel_groups
            elif "PERISPOMENI" in name:
                classes.append("perispomeni"); accented_group = vowel_groups
            elif "PSILI" in name or "COMBINING COMMA ABOVE" in name:
                breathings.append("smooth")
            elif "DASIA" in name or "COMBINING REVERSED COMMA ABOVE" in name:
                breathings.append("rough")
    if not classes:
        accent_class = "none"
    elif len(set(classes)) == 1:
        accent_class = classes[0]
    else:
        accent_class = "mixed"
    if accented_group is None or vowel_groups == 0:
        syllable = None
    elif accented_group <= 1:
        syllable = "initial"
    elif accented_group >= vowel_groups:
        syllable = "final"
    else:
        syllable = "medial"
    breathing = ("rough" if "rough" in breathings else
                 "smooth" if "smooth" in breathings else "none")
    if surface[:1] in ("ῥ", "Ῥ"):
        breathing = "rough"
    return {"accent_class": accent_class, "accented_syllable": syllable,
            "breathing": breathing}


def parse_printed_token(printed: str, clean: str | None,
                        lemma: str | None, index: int) -> dict:
    """One token object from a printed form + clean surface."""
    leading_apparatus = printed.startswith("⸀")
    span_open = printed.startswith("⸂")
    span_close = "⸃" in printed
    body = printed.replace("⸀", "").replace("⸂", "").replace("⸃", "")
    trailing = "none"
    if body and body[-1] in MARK_BY_CHAR:
        trailing = MARK_BY_CHAR[body[-1]]
        body = body[:-1]
    surface = clean if clean else body
    prof = accent_profile(surface)
    return {
        "word_index": index,
        "surface": surface,
        "printed": printed,
        "lemma_hint": lemma,
        "trailing_punct": trailing,
        "leading_apparatus": leading_apparatus,
        "apparatus_span_open": span_open,
        "apparatus_span_close": span_close,
        "apparatus_span": None,  # filled by _assign_spans
        **prof,
        "baseline_absent": trailing in BASELINE_ABSENT,
    }


def _assign_spans(tokens: list[dict]) -> None:
    open_idx = None
    for t in tokens:
        if t["apparatus_span_open"]:
            open_idx = t["word_index"]
        if open_idx is not None:
            t["apparatus_span"] = {"open": open_idx,
                                    "close": t["word_index"] if t["apparatus_span_close"] else None}
        if t["apparatus_span_close"]:
            if open_idx is not None:
                for u in tokens[open_idx:t["word_index"] + 1]:
                    if u["apparatus_span"]:
                        u["apparatus_span"]["close"] = t["word_index"]
            open_idx = None


def tokenise_morph_tokens(morph_tokens: list[dict]) -> list[dict]:
    """MorphGNT tokens: field 'text' printed, 'word' clean, 'lemma' hint."""
    out = [parse_printed_token(w.get("text", w["word"]), w["word"],
                               w.get("lemma"), i)
           for i, w in enumerate(morph_tokens)]
    _assign_spans(out)
    return out


def tokenise_printed_text(text: str) -> list[dict]:
    """Fallback for raw punctuated text (no MorphGNT fields)."""
    raw = [t for t in text.replace("[", " ").replace("]", " ").split() if t]
    out = [parse_printed_token(t, None, None, i) for i, t in enumerate(raw)]
    _assign_spans(out)
    return out


def cadence_map(tokens: list[dict]) -> list[dict]:
    out = []
    for t in tokens:
        mark = t["trailing_punct"]
        if mark == "none":
            continue
        contexts = []
        lemma = (t.get("lemma_hint") or "")
        if lemma in _SPEECH_LEMMAS:
            contexts.append("speech_verb")
        if t.get("leading_apparatus") or t.get("apparatus_span"):
            contexts.append("apparatus")
        out.append({"after_word": t["word_index"], "surface": t["surface"],
                    "mark": mark, "weight": WEIGHTS[mark],
                    "context": contexts,
                    "baseline_absent": mark in BASELINE_ABSENT})
    return out


def mark_counts(tokens: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for t in tokens:
        m = t["trailing_punct"]
        if m != "none":
            counts[m] = counts.get(m, 0) + 1
    counts["apparatus_single"] = sum(1 for t in tokens if t["leading_apparatus"])
    counts["apparatus_span_tokens"] = sum(1 for t in tokens if t["apparatus_span"])
    return counts


def punctuation_block(token: dict) -> dict:
    """The per-word block stored on primitives / decoding words."""
    return {k: token[k] for k in (
        "printed", "trailing_punct", "leading_apparatus", "apparatus_span",
        "accent_class", "accented_syllable", "breathing", "baseline_absent")}
