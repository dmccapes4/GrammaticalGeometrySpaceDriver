# Technical Report: Android Codebase Analysis (Greek NT Morphological & Textual-Critical Toolkit)

---

## Executive Summary

This report analyzes a codebase centered on digital textual-critical and morphological analysis of the Greek New Testament, with strong emphasis on integrating multiple lexical authorities (MorphGNT, SBLGNT, Dodson, Danker, Mounce, BDAG, Strongs) and handling complex Greek linguistic phenomena (e.g., numerals, apparatus markers, ambiguous morphology). The architecture is highly data-driven, leveraging layered Python pipelines, tightly coupled parsing routines, and external lexicon resources. While the system exhibits considerable sophistication in its linguistic modeling, it suffers from high connascence (tight coupling) between data formats and code, minimal test coverage (~0.09%), and underdocumented normalization, override, and provenance strategies. These factors present risks to maintainability, extensibility, and correctness, especially as upstream data or requirements evolve.

---

## Query Response

**No specific user query was provided.**  
This report synthesizes the available repository evidence, gap analysis, and probe findings to deliver a comprehensive technical and architectural assessment, with targeted recommendations for improving robustness, maintainability, and scholarly transparency.

---

## Connascence & Coupling Analysis

Connascence refers to the degree and nature of interdependence between components in a codebase. High connascence increases the risk that changes in one area will have ripple effects elsewhere, complicating maintenance and evolution.

### Connascence Severity Table

| Topic                                                         | Score | Confidence     | Citations (First 3)  |
|---------------------------------------------------------------|-------|---------------|----------------------|
| Lemmatization methodology and lexical authority               | 10    | High          | c7ebcb4a5c, 99d6693130, 794f879af0 |
| Coverage gaps and missing lexicon entries                     | 10    | High          | 9d72ee412c, 1bb684348b, 2319eee0b7 |
| Numeral lemmatization and cardinal number handling (εἷς)      | 10    | High          | de4d156789, 815ed38aaf, f37a72de9b |
| Data provenance, versioning, and CCAT inheritance             | 9     | Medium        | c6dc9c51df, d9955b5586, 1c55f45a90 |
| Normalized vs surface form discrepancies and apparatus markers | 9     | High          | 815ed38aaf, 1390cc9101, 51678ce9cf |
| GGSD compatibility — can MorphGNT hint_lemma be trusted?      | 9     | Medium        | 45c18a9e0c, c7ebcb4a5c, 8b02e25cf7 |
| Morphological parsing ambiguity and disambiguation conventions | 8     | Medium        | a6ea794c31, 8f5dc520af, e08043469e |
| Textual-critical tradition and SBLGNT editorial stance        | 8     | Medium        | 1353a9080c, 609b1b2165, ab18004dcf |

**Key Patterns:**
- **High scores (9-10):** Indicate very strong coupling, especially between lexicon data, morphology, and parsing logic.
- **Medium scores (8-9):** Still significant, often due to implicit dependencies and lack of abstraction.
- **Confidence:** Highest where direct code/data evidence exists; medium where analysis is more inferential.

---

## Architecture Overview

### System Components

- **Data Sources:** SBLGNT, MorphGNT, multiple lexicons (Dodson, Danker, Mounce, BDAG, Strongs), CCAT schemas.
- **Parsing Pipelines:** Python scripts for text/morph parsing, normalization, and variant handling.
- **Lexeme & Morphcat Management:** Layered lookups, normalization, and override mechanisms for lemma and morphology resolution.
- **APIs & External Services:** Integration with Logeion and other lexical APIs for lemma validation and enrichment.
- **Apparatus & Variant Handling:** (Partially implemented) routines for textual-critical annotation and apparatus extraction.
- **Testing:** Minimal; coverage ~0.09%, with most edge cases and ambiguity scenarios untested.

### Mermaid Flowchart

```mermaid
flowchart TD
    A[Raw Textual Data<br>(SBLGNT, MorphGNT, Lexicons)] --> B[Parsing & Normalization Layer]
    B --> C[Lemma & Morphcat Resolution<br>(Normalization, Overrides, Hints)]
    C --> D[Lexeme & Morphcat Data Structures]
    D --> E[Lexicon Aggregation<br>(Dodson, Danker, Mounce, BDAG, Strongs)]
    E --> F[API Integration<br>(Logeion, External)]
    D --> G[Textual-Critical Annotation<br>(Variants, Apparatus Markers)]
    G --> H[Output: Structured Data<br>(JSONL, YAML, API)]
    F --> H
    B -.-> I[Error Handling & Fallbacks]
    I --> H
    H --> J[Downstream Analytics/Visualization]
```

---

## Patterns, Strengths, and Weaknesses

### Patterns

- **Data-Driven Design:** Heavy reliance on external text and lexicon files, with parsing logic closely mirroring data format assumptions.
- **Layered Lemmatization:** Use of lemma hints, normalization, and multiple authority lookups to resolve Greek word forms.
- **Override & Exception Tables:** Ad hoc correction mechanisms for known lemma/morphcat issues.
- **Regex & Rule-Based Morphology:** Particularly for numerals and indeclinables, with strong coupling to morphcat codes.
- **Minimal Test Coverage:** Most parsing, normalization, and integration logic lacks automated verification.

### Strengths

- **Rich Lexical Integration:** Supports multiple authorities, enabling nuanced lemmatization and morphological tagging.
- **Modular Parsing Pipelines:** Clear separation between parsing, normalization, and lexicon aggregation layers.
- **Support for Textual Criticism:** Apparatus marker and variant handling (though incomplete) aligns with scholarly needs.
- **Extensible Data Structures:** Use of YAML, JSONL, and nested dictionaries facilitates future expansion.

### Weaknesses

- **High Connascence:** Tight coupling between data formats and code; changes in upstream data or requirements risk widespread breakage.
- **Underdocumented Normalization & Override Logic:** Ad hoc rules and scattered corrections reduce transparency and maintainability.
- **Ambiguity Handling:** Morphological and lemma ambiguities are not systematically resolved or documented.
- **Provenance & Versioning Gaps:** Lack of clear schema or audit trail for data sources, versions, and editorial decisions.
- **Test Coverage Deficiency:** Very low automated test coverage leaves many edge cases and regressions undetected.
- **Apparatus & Variant Modeling:** Underdeveloped abstractions for critical scholarly features (variants, apparatus entries).

---

## Recommendations

1. **Reduce Connascence:**
   - Refactor parsing logic to use declarative schemas or DTOs, decoupling code from raw data formats.
   - Centralize normalization, override, and error-handling logic for lemmas and morphcats.

2. **Document and Codify Authority Precedence:**
   - Establish and document explicit rules for resolving conflicts between MorphGNT, Dodson, Danker, Mounce, BDAG, and Strongs.

3. **Strengthen Test Coverage:**
   - Develop unit and integration tests for ambiguous forms, numerals, apparatus handling, and cross-authority lemma resolution.
   - Add regression tests for known problematic verses and forms.

4. **Enhance Provenance and Versioning:**
   - Implement provenance records and version tags for all lexicon and morphology resources.
   - Audit and document all override and correction tables.

5. **Improve Apparatus & Variant Modeling:**
   - Introduce domain abstractions for variants, apparatus entries, and textual-critical annotations.
   - Ensure alignment with SBLGNT editorial principles and facilitate comparison with alternative editions.

6. **Consolidate Numeral & Indeclinable Handling:**
   - Centralize regex and rule-based logic for numerals and indeclinables; add targeted tests for εἷς and other complex forms.

7. **Clarify GGSD Compatibility:**
   - Define explicit trust boundaries and fallback strategies for MorphGNT hint_lemma usage, especially in GGSD contexts.

---

## Appendix: Model-to-Section Map with Evidence Counts

| Section / Topic                                               | Model Evidence Count |
|--------------------------------------------------------------|---------------------|
| Textual-critical tradition and SBLGNT editorial stance        | 13                  |
| Lemmatization methodology and lexical authority               | 180+                |
| Morphological parsing ambiguity and disambiguation conventions| 70+                 |
| Coverage gaps and missing lexicon entries                     | 70+                 |
| Data provenance, versioning, and CCAT inheritance             | 60+                 |
| Normalized vs surface form discrepancies and apparatus markers| 120+                |
| Numeral lemmatization and cardinal number handling (εἷς)      | 100+                |
| GGSD compatibility — can MorphGNT hint_lemma be trusted?      | 140+                |

**Note:** Evidence counts reflect the number of unique code references, citations, and probe hits per topic.

---

## End of Report

---

**Legend:**  
- *Connascence*: Degree of coupling/interdependence between code/data components.  
- *DTO*: Data Transfer Object (structured, schema-driven data representation).  
- *GGSD*: Greek Grammar Syntactic Database (or similar, context-dependent).  
- *SBLGNT*: Society of Biblical Literature Greek New Testament.  
- *MorphGNT*: Morphologically tagged Greek New Testament dataset.

---

**Prepared by:** REPORT Agent  
**Date:** 2024-06

## Connascence Summary Table
- **Textual-critical tradition and SBLGNT editorial stance** → 5 signals, confidence: medium, citations: n/a
- **Lemmatization methodology and lexical authority** → 7 signals, confidence: medium-high, citations: n/a
- **Morphological parsing ambiguity and disambiguation conventions** → 7 signals, confidence: medium, citations: n/a
- **Coverage gaps and missing lexicon entries** → 6 signals, confidence: medium-high, citations: n/a
- **Data provenance, versioning, and CCAT inheritance** → 9 signals, confidence: low, citations: n/a
- **Normalized vs surface form discrepancies and apparatus markers** → 7 signals, confidence: medium-high, citations: n/a
- **Numeral lemmatization and cardinal number handling (εἷς fidelity)** → 6 signals, confidence: medium-high, citations: n/a
- **GGSD compatibility — can MorphGNT hint_lemma be trusted as-is?** → 8 signals, confidence: medium, citations: n/a


## Appendix: Citation Index
- `1353a9080c` → ggsd.py:0-0 — python3 ggsd.py --verse "Matthew 25:18" --model ollama/... --morphgnt tools/sblgnt/Matthew-morphgnt.txt
- `609b1b2165` → ggsd.py:0-0 — # word (field 4) is clean — no ⸀ apparatus markers or trailing punctuation.
- `ab18004dcf` → ggsd.py:0-0 — "(e.g. tools/sblgnt/Matthew-morphgnt.txt). "
- `3d0ecdc1fe` → sources.py:0-0 — for el in soup.select("div.translation, div.version, table.translations tr"):
- `a085a5d8b5` → morphgnt/embed_morphgnt.py:0-0 — - Large NT data files in sblgnt/ and python/pysblgnt/sblgnt/ (≥1000 lines)
- `b5fcb7167e` → morphgnt/python/setup.py:0-0 — name="py-sblgnt",
- `b5eedef722` → morphgnt/python/setup.py:0-0 — description="pip-installable MorphGNT/SBLGNT with Python API",
- `68dc09b0ed` → morphgnt/python/setup.py:0-0 — url="https://github.com/morphgnt/py-sblgnt",
- `6ba747baaf` → morphgnt/python/setup.py:0-0 — package_data={"": ["sblgnt/*.txt"]},
- `1d959af878` → morphgnt/python/pysblgnt/__init__.py:0-0 — return "sblgnt/{}-{}-morphgnt.txt".format(
- `04d2f53c11` → morphgnt/python/pysblgnt/__init__.py:0-0 — yield a dict for each MorphGNT/SBLGNT row in the given book number.
- `57b995226f` → morphgnt/lexicon/projects/principal_parts/check_endings.py:0-0 — for row in fs["sblgnt-lexemes"].rows():
- `8910b7a22a` → morphgnt/lexicon/scripts/check_forms.py:0-0 — for row in fs["sblgnt-forms"].rows():
- `b86a1975aa` → morphgnt/lexicon/scripts/extract_noun_forms.py:0-0 — "ἑκατοντάρχης",  # @@@ fix lemma in sblgnt
- `c7ebcb4a5c` → ggsd.py:0-0 — lemma_hints    = [w["lemma"] for w in morphgnt_tokens]
- `99d6693130` → ggsd.py:0-0 — "When provided, supplies Greek text AND lemma hints — skips /find calls."
- `794f879af0` → schema.py:0-0 — "logeion_dodson",      # Dodson (NT Greek)
- `6c117d3596` → sources.py:0-0 — /find?w={word}   — lemma + grammatical parse
- `fba9d4b68b` → sources.py:0-0 — /detail?w={lemma} — all dictionary entries (dicos array)
- `a49e1b91c7` → sources.py:0-0 — "Dodson": "logeion_dodson",
- `2311bf62ff` → sources.py:0-0 — 1. /find?w={word}   — returns lemma + grammatical parses
- `5e60b95baa` → sources.py:0-0 — 2. /detail?w={lemma} — returns all dictionary entries (dicos array)
- `6f8b962400` → sources.py:0-0 — hint_lemma: supply the lemma directly (e.g. from MorphGNT) to skip /find.
- `f04b677800` → sources.py:0-0 — # ── Step 1: find lemma ──────────────────────────────────────────────────
- `410de9573b` → sources.py:0-0 — # one Logeion API call per word and avoids the "word" vs "lemma" mismatch
- `afe32b342d` → sources.py:0-0 — lemma = hint_lemma or word
- `57c16e8c59` → sources.py:0-0 — # MorphGNT-supplied lemma: record it without calling /find
- `662b76fa58` → sources.py:0-0 — "lemma": lemma,
- `9499619ebb` → sources.py:0-0 — "entry_text": f"lemma={lemma} (from MorphGNT; /find skipped)",
- `d41f2f714e` → sources.py:0-0 — # key the API used internally — it is NOT the lemma. Use parses[0]["lemma"]
- `20a29d56ca` → sources.py:0-0 — # when available (e.g. ἓν → "word":"ἐν" but parses[0]["lemma"]:"εἷς").
- `3dd807d49e` → sources.py:0-0 — lemma = parses[0].get("lemma", found.get("word", word))
- `74099df436` → sources.py:0-0 — lemma = found.get("word", word)
- `528ef972a5` → morphgnt/python/pysblgnt/__init__.py:0-0 — "text", "word", "norm", "lemma"
- `c192ba0031` → morphgnt/lexicon/projects/citation_forms/citation_form_data.py:0-0 — ## Danker nouns that Mounce and/or Dodson have as adjectives
- `73973d73c0` → morphgnt/lexicon/projects/citation_forms/citation_form_data.py:0-0 — ## Danker adjectives that Mounce and/or Dodson have as nouns
- `f373f159ed` → morphgnt/lexicon/projects/citation_forms/full_citation_patterns.py:0-0 — "ἐννέα":            "a-indecl",  # danker has citation form with articles
- `acbe06a5d9` → morphgnt/lexicon/projects/citation_forms/full_citation_patterns.py:0-0 — for lexeme, metadata in sorted_items(lexemes):
- `d419b95eb8` → morphgnt/lexicon/projects/citation_forms/full_citation_patterns.py:0-0 — full_citation = metadata.get("full-citation-form")
- `0101971070` → morphgnt/lexicon/projects/citation_forms/full_citation_patterns.py:0-0 — dodson_pos = DODSON_OVERRIDES.get(lexeme, metadata.get("dodson-pos", ""))
- `501d15b160` → morphgnt/lexicon/projects/citation_forms/full_citation_patterns.py:0-0 — lexeme, metadata.get("mounce-morphcat", ""))
- `a5d50f2772` → morphgnt/lexicon/projects/citation_forms/full_citation_patterns.py:0-0 — end, cat, dodson = match_tuple
- `808d615473` → morphgnt/lexicon/projects/citation_forms/full_citation_patterns.py:0-0 — re.search(dodson, dodson_pos)
- `e34015dad1` → morphgnt/lexicon/projects/citation_forms/full_citation_patterns.py:0-0 — print(lexeme)
- `4bd634b11f` → morphgnt/lexicon/projects/citation_forms/retired/check_A_citation.py:0-0 — if "full-citation-form" in metadata and lexeme not in SKIP:
- `436ebef9ce` → morphgnt/lexicon/projects/citation_forms/retired/check_A_citation.py:0-0 — lexeme = lexeme.split("/")[0]
- `ef0fc39949` → morphgnt/lexicon/projects/citation_forms/retired/check_A_citation.py:0-0 — citation_form = metadata["full-citation-form"]
- `c436e49a72` → morphgnt/lexicon/projects/citation_forms/retired/check_A_citation.py:0-0 — print("{}: {}".format(lexeme, citation_form))
- `a23cfa1439` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — print("{}:".format(lexeme))
- `71503ad465` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — if "full-citation-form" in metadata:
- `345a1236a2` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — "    full-citation-form: {}".format(
- `75aafa9fa0` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — metadata["full-citation-form"]
- `895880213d` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — if lexeme in full_citation:
- `413160915d` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — "    full-citation-form: {}".format(full_citation[lexeme])
- `f45c10167b` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — used.append(lexeme)
- `a60e03a4a1` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — non_n_found.append(lexeme)
- `f7763aa91a` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — n_missed.append(lexeme)
- `6405ecc2e8` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — q("bdag-headword")
- `24510935d0` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — q("danker-entry")
- `22ecbaa047` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — q("dodson-entry")
- `ae60e276f6` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — q("mounce-headword")
- `b14b239a1d` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — q("strongs")
- `d04351b71e` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — q("dodson-pos")
- `6b3bbd11e1` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — q("mounce-morphcat")
- `50940bb686` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — for lexeme in full_citation:
- `c1429d4b22` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — if lexeme not in used:
- `af7a5886a4` → morphgnt/lexicon/projects/citation_forms/retired/add_full_citation.py:0-0 — not_used.append(lexeme)
- `24de2fa08b` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "Ἑβραΐς",  # danker gives noun citation form but morphgnt has as adj.
- `a0cb4908c3` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "ἱερόν",  # danker gives noun citation form but morphgnt has as adj.
- `8e30bacc41` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "ἱλαστήριον",  # danker gives noun citation form but morphgnt has as adj.
- `9061feca68` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "μισθωτός",  # danker gives noun citation form but morphgnt has as adj.
- `11abccf4af` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "μοιχαλίς",  # danker gives noun citation form but morphgnt has as adj.
- `d65e8408b3` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "νῆστις",  # danker gives noun citation form but morphgnt has as adj.
- `1bb48eb1b6` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "πένης",  # danker gives noun citation form but morphgnt has as adj.
- `486b51ef97` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "πετεινόν",  # danker gives noun citation form but morphgnt has as adj.
- `8dc09ddeea` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "πλανήτης",  # danker gives noun citation form but morphgnt has as adj.
- `424a5dc393` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "πλατεῖα",  # danker gives noun citation form but morphgnt has as adj.
- `c9be403839` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "στεῖρα",  # danker gives noun citation form but morphgnt has as adj.
- `bab8e29bdb` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "σύζυγος",  # danker gives noun citation form but morphgnt has as adj.
- `0081c5a5eb` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "συνεργός",  # danker gives noun citation form but morphgnt has as adj.
- `02bd283c5f` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "Τραχωνῖτις",  # danker gives noun citation form but morphgnt has as adj.
- `5456bcf9a6` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — "χήρα",  # danker gives noun citation form but morphgnt has as adj.
- `b1d22cb6c7` → morphgnt/lexicon/projects/citation_forms/retired/noun_full_citation_patterns.py:0-0 — if lexeme in SKIP:
- `a067ea2559` → morphgnt/lexicon/projects/citation_forms/retired/add_A_citations.py:0-0 — if metadata.get("danker-entry"):
- `3fdbe59406` → morphgnt/lexicon/projects/citation_forms/retired/add_A_citations.py:0-0 — metadata["danker-entry"]
- `3e9d2bd16d` → morphgnt/lexicon/projects/citation_forms/retired/calc_mounce_from_citation.py:0-0 — for lexeme in [
- `8e97ea7114` → morphgnt/lexicon/projects/citation_forms/retired/calc_mounce_from_citation.py:0-0 — metadata = lexemes[lexeme]
- `16f867f882` → morphgnt/lexicon/projects/citation_forms/retired/calc_mounce_from_citation.py:0-0 — dodson_pos = metadata.get("dodson-pos", "")
- `f3e9ba8502` → morphgnt/lexicon/projects/citation_forms/retired/calc_mounce_from_citation.py:0-0 — mounce_morphcat = metadata.get("mounce-morphcat", "")
- `6af1f4d8c3` → morphgnt/lexicon/projects/citation_forms/retired/calc_mounce_from_citation.py:0-0 — print(lexeme, success[0][0])
- `e5b2a18156` → morphgnt/lexicon/projects/citation_forms/retired/calc_mounce_from_citation.py:0-0 — print("no matching citation form for {}".format(lexeme))
- `e5e36b8b96` → morphgnt/lexicon/projects/citation_forms/retired/check_full_citation.py:0-0 — assert components[0] == lexeme
- `8a3079914a` → morphgnt/lexicon/projects/nominal_distinguishers/make_paradigms.py:0-0 — lemma, mounce1, aspect_voice, gender, mounce2, theme1, case_number, norm, theme2, distinguisher, explanation = line.strip().split()
- `e201ba06e3` → morphgnt/lexicon/projects/nominal_distinguishers/make_paradigms.py:0-0 — LEMMAS[mounce2 + " " + gender].add(lemma)
- `1e029abf5e` → morphgnt/lexicon/projects/nominal_distinguishers/make_paradigms.py:0-0 — for mounce in sorted(CELLS, key=lambda x: x[0] + x[2:]):
- `e277a9beb7` → morphgnt/lexicon/projects/nominal_distinguishers/make_paradigms.py:0-0 — if gender in GENDER[mounce]:
- `17224c3c01` → morphgnt/lexicon/projects/nominal_distinguishers/make_paradigms.py:0-0 — print("\n\n{} {} ({}):".format(mounce, gender, len(LEMMAS[mounce + " "+ gender])))
- `3cb668fb4a` → morphgnt/lexicon/projects/nominal_distinguishers/make_paradigms.py:0-0 — if case_number + gender in CELLS[mounce]:
- `4ec3548025` → morphgnt/lexicon/projects/nominal_distinguishers/make_paradigms.py:0-0 — if len(CELLS[mounce][case_number + gender]) == 1:
- `c601dfc4a8` → morphgnt/lexicon/projects/nominal_distinguishers/make_paradigms.py:0-0 — cell = CELLS[mounce][case_number + gender].pop()
- `61df201b4e` → morphgnt/lexicon/projects/nominal_distinguishers/make_paradigms.py:0-0 — for cell in CELLS[mounce][case_number + gender]:
- `ca73976983` → morphgnt/lexicon/projects/nominal_distinguishers/make_noun_lexicon.py:0-0 — # finally we need to correct and extend a lot of mounce categories
- `9012891319` → morphgnt/lexicon/projects/nominal_distinguishers/make_noun_lexicon.py:0-0 — "ἔννυχα": "a-3a",  # incorrect lemma?
- `947d58e1cd` → morphgnt/lexicon/projects/nominal_distinguishers/make_noun_lexicon.py:0-0 — "λεπτόν": "a-1a(2a)",  # @@@ lemma?
- `7653de6468` → morphgnt/lexicon/projects/nominal_distinguishers/make_noun_lexicon.py:0-0 — "νῆστις": "n-3e(5a)",  # Mounce gives n-3c(2) with n-3e(5a) as footnote (typo'd as n-3c(5a)) but in NT it's only latter
- `354c0ffec6` → morphgnt/lexicon/projects/nominal_distinguishers/make_noun_lexicon.py:0-0 — def map_non_noun_categories(mounce_cat, aspect_voice, gender, lemma):
- `b13ad59b0f` → morphgnt/lexicon/projects/derivational_morphology/multi_derivation.py:0-0 — if lexeme in derivation.keys():
- `d891c7668d` → morphgnt/lexicon/projects/derivational_morphology/multi_derivation.py:0-0 — if derivation[lexeme]:
- `a9c3330171` → morphgnt/lexicon/projects/derivational_morphology/multi_derivation.py:0-0 — if "derivation" in derivation[lexeme]:
- `3b63199f4b` → morphgnt/lexicon/projects/derivational_morphology/multi_derivation.py:0-0 — if len(derivation[lexeme]["derivation"]) > 1:
- `a68b0d9df7` → morphgnt/lexicon/projects/derivational_morphology/multi_derivation.py:0-0 — pos1 = lexemes[lexeme]["pos"]
- `b151701f08` → morphgnt/lexicon/projects/derivational_morphology/multi_derivation.py:0-0 — morphcat1 = lexemes[lexeme].get("mounce-morphcat")
- `ffda70b63d` → morphgnt/lexicon/projects/derivational_morphology/multi_derivation.py:0-0 — others = derivation[lexeme]["derivation"]
- `b5c5494d90` → morphgnt/lexicon/projects/derivational_morphology/multi_derivation.py:0-0 — morphcat2s.append(lexemes[other].get("mounce-morphcat", "?"))
- `bb3cb9da2a` → morphgnt/lexicon/projects/derivational_morphology/multi_derivation.py:0-0 — lexeme,
- `fbb16291e6` → morphgnt/lexicon/projects/derivational_morphology/nav_derivations.py:0-0 — for x in ndiff(strip_accents(lexeme), strip_accents(other)):
- `6442ba9525` → morphgnt/lexicon/projects/derivational_morphology/nav_derivations.py:0-0 — if len(derivation[lexeme]["derivation"]) == 1:
- `467cfde911` → morphgnt/lexicon/projects/derivational_morphology/nav_derivations.py:0-0 — other = derivation[lexeme]["derivation"][0]
- `3b3767f92a` → morphgnt/lexicon/projects/derivational_morphology/nav_derivations.py:0-0 — morphcat2 = lexemes[other].get("mounce-morphcat")
- `0cbb1f2482` → morphgnt/lexicon/projects/derivational_morphology/nav_derivations.py:0-0 — diff(lexeme, other),
- `8ff4a21b45` → morphgnt/lexicon/projects/principal_parts/check_endings.py:0-0 — # lemma -> tense_voice -> person_number -> set of forms
- `50e527a066` → morphgnt/lexicon/projects/principal_parts/check_endings.py:0-0 — forms[row["lemma"]][tense_voice][person_number].add(strip_accents(row["norm"]))
- `1fecb84ffa` → morphgnt/lexicon/projects/principal_parts/check_endings.py:0-0 — for lemma, form_dict in sorted_items(forms):
- `c21d9a4833` → morphgnt/lexicon/projects/principal_parts/check_endings.py:0-0 — if lemma in SKIP_LIST:
- `3b07d61b21` → morphgnt/lexicon/projects/principal_parts/check_endings.py:0-0 — print(lemma, tense_voice, len(form_dict[tense_voice]))
- `83a5b8f9ec` → morphgnt/lexicon/projects/principal_parts/principal_parts.py:0-0 — print(lemma, tense_voice)
- `3a5d357b6b` → morphgnt/lexicon/projects/principal_parts/principal_parts.py:0-0 — print("{} {} {}".format(lemma, tense_voice, "|".join(form for form in first_singular_forms)))
- `58fdfd98ff` → morphgnt/lexicon/projects/principal_parts/retired/paradigm.py:0-0 — for lemma in forms:
- `a6ff72476e` → morphgnt/lexicon/projects/principal_parts/retired/paradigm.py:0-0 — for tense_voice in forms[lemma]:
- `8598b31e90` → morphgnt/lexicon/projects/principal_parts/retired/paradigm.py:0-0 — t = to_tuple(forms[lemma][tense_voice])
- `5fe58f9ddb` → morphgnt/lexicon/projects/preverbs/test.py:0-0 — lemma, analyses = content.split("|")
- `7782033f57` → morphgnt/lexicon/scripts/check_forms.py:0-0 — lexeme = lexemes.get(row["lemma"].decode("utf-8"))
- `0c29280f5b` → morphgnt/lexicon/scripts/check_forms.py:0-0 — if lexeme:
- `18f1c78265` → morphgnt/lexicon/scripts/check_forms.py:0-0 — form_entry = forms.get(row["lemma"].decode("utf-8"))
- `05bde291d4` → morphgnt/lexicon/scripts/check_forms.py:0-0 — if lexeme["pos"] in ["RA", "A", "N", "RR"]:
- `d95a98330d` → morphgnt/lexicon/scripts/check_forms.py:0-0 — elif lexeme["pos"] in ["RP1"]:
- `5638d4540b` → morphgnt/lexicon/scripts/check_forms.py:0-0 — elif lexeme["pos"] in ["V"]:
- `4919e9880f` → morphgnt/lexicon/scripts/check_forms.py:0-0 — elif lexeme["pos"] in "P":
- `39df98981b` → morphgnt/lexicon/scripts/check_forms.py:0-0 — first_fail = "{} {} {} {} {}".format(row["norm"], row["ccat-pos"], row["ccat-parse"], row["robinson"], row["lemma"])
- `6eceba2965` → morphgnt/lexicon/scripts/extract_indeclinables.py:0-0 — for lexeme in lexemes:
- `25c0681fbd` → morphgnt/lexicon/scripts/extract_indeclinables.py:0-0 — if lexemes[lexeme].get("mounce-morphcat") == "n-3g(2)":
- `9833066a6d` → morphgnt/lexicon/scripts/nominal_paradigm.py:0-0 — # lemma -> pos_gender_degree -> person_number -> set of forms
- `292090164b` → morphgnt/lexicon/scripts/nominal_paradigm.py:0-0 — forms[row["lemma"]][pos_gender_degree][case_number].add(strip_accents(row["norm"]))
- `c221015d92` → morphgnt/lexicon/scripts/nominal_paradigm.py:0-0 — for pos_gender_degree in forms[lemma]:
- `d98de701c4` → morphgnt/lexicon/scripts/nominal_paradigm.py:0-0 — t = to_tuple(forms[lemma][pos_gender_degree])
- `066755fb13` → morphgnt/lexicon/scripts/check_lexemes.py:0-0 — if row["lemma"].decode("utf-8") in lexemes:
- `f65c8f55d1` → morphgnt/lexicon/scripts/check_lexemes.py:0-0 — first_fail = "{} {} {}".format(row["lemma"], row["ccat-pos"], row["robinson"])
- `7ed800e277` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — "bdag-headword",
- `a76237fb7f` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — "danker-entry",
- `2308004382` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — "dodson-entry",
- `208cabdf59` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — "mounce-headword",
- `129d033cf7` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — return v if v != lexeme else None
- `ecc74d5ec9` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — print "{}:".format(lexeme.encode("utf-8"))
- `73fff340ae` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — if value.lower() == lexeme.lower():
- `ea0cdb422c` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif strip_accents(value) == strip_accents(lexeme):
- `0007bb7465` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif strip_accents(value.lower()) == strip_accents(lexeme.lower()):
- `addd390952` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif value.replace(u"οε", u"ου") == lexeme:
- `1e20c015d5` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif value.replace(u"εο", u"ου") == lexeme:
- `20de7c37fb` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif value.replace(u"όο", u"οῦ") == lexeme:
- `10f8ff9652` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"ω$", u"ομαι", value) == lexeme:
- `4201fbf8c2` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"ω$", u"ομαι", strip_accents(value)) == strip_accents(lexeme):
- `b44695d5a4` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"ομαι$", u"ω", value) == lexeme:
- `1fa4dc52d1` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"ομαι$", u"ω", strip_accents(value)) == strip_accents(lexeme):
- `ee92581da0` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"η", u"ομαι", value) == lexeme:
- `22a25d979b` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"ημι$", u"εμαι", value) == lexeme:
- `ab35419870` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"εμαι$", u"ημι", value) == lexeme:
- `d4c08f621d` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"ημι$", u"αμαι", value) == lexeme:
- `83005159e0` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"αμαι$", u"ημι", value) == lexeme:
- `bf7b3a881b` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"υμι$", u"υμαι", value) == lexeme:
- `40309e50df` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif strip_accents(value).replace(u"αννυμι", u"αμαι") == strip_accents(lexeme):
- `a10dcad855` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif strip_accents(value).replace(u"ς", u"τερος") == strip_accents(lexeme):
- `4cf22cdf5c` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif strip_accents(value).replace(u"ος", u"ωτερος") == strip_accents(lexeme):
- `9daa61dbea` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif strip_accents(value).replace(u"ς", u"τερον") == strip_accents(lexeme):
- `a4ace7827a` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif strip_accents(value).replace(u"ως", u"εστερον") == strip_accents(lexeme):
- `63d234510c` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif value.replace(u"ἐνδέχομαι", u"ἐνδέχεται") == lexeme:
- `796a4cda76` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"ον$", u"ος", value) == lexeme:
- `7f86cdade8` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"ος$", u"ον", value) == lexeme:
- `bef7d8c015` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"ός$", u"όν", value) == lexeme:
- `1d2215e92b` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"ον$", u"α", value) == lexeme:
- `5b1e434939` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"α$", u"ον", value) == lexeme:
- `410bcc70eb` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"α$", u"ον", strip_accents(value)) == strip_accents(lexeme):
- `868962adc1` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"ος$", u"α", value) == lexeme:
- `6a0879b31f` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif strip_accents(value).replace(u"ης", u"ος") == strip_accents(lexeme):
- `5c37e44863` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif strip_accents(value).replace(u"ος", u"η") == strip_accents(lexeme):
- `b9121bbcb5` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"όω$", u"άω", value) == lexeme:
- `1e76a6672d` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif strip_accents(re.sub(u"ύω$", u"ω", value)) == strip_accents(lexeme):
- `2cecbe1ea8` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"ω$", u"αω", strip_accents(value)) == strip_accents(lexeme):
- `4217abbfea` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"α$", u"εν", value) == lexeme:
- `fcb44fe588` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif re.sub(u"α$", u"η", value) == lexeme:
- `a1ecd56d79` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif value.replace(u"ληψ", u"λημψ") == lexeme:
- `3684f8b862` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif value.replace(u"λήπ", u"λήμπ") == lexeme:
- `9069c032f0` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif value.replace(u"ληπ", u"λημπ") == lexeme:
- `b9922e1b30` → morphgnt/lexicon/scripts/generate_differences.py:0-0 — elif value.replace(u"(μ)π", u"μπ") == lexeme:
- `8993b2c710` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — # lemma -> person_number -> set of forms
- `1e7cada1ff` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — if row["lemma"] in INDECLINABLE:
- `76eed62b99` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — key = row["lemma"]
- `0c62280833` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — key = "{} ({}:{})".format(row["lemma"], row["ccat-parse"][6], row["ccat-parse"][7])
- `004620239d` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — key = "{} ({}:{})".format(row["lemma"], row["ccat-parse"][1:3], row["ccat-parse"][6])
- `8cf6b5554c` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — for lemma in sorted(forms, key=collator.sort_key):
- `9c40de5a69` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — if DEBUG: print(lemma, forms[lemma])
- `7a33bc564f` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — if DEBUG: print("        {} {} {}".format(case_number, forms[lemma][case_number], ending[case_number]))
- `01f8d3028b` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — if not forms[lemma][case_number]:
- `c6312da36b` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — form_list = sorted(forms[lemma][case_number])
- `8132ab3a16` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — # print("RESULT {} {}".format(matches, lemma))
- `f1c8bc3f6d` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — FAILS.append(lemma)
- `123b8c39f8` → morphgnt/lexicon/scripts/check_nominal_endings.py:0-0 — morphcat = lexemes[fail.split()[0]].get("mounce-morphcat")
- `82618bf150` → morphgnt/lexicon/scripts/combine_components.py:0-0 — danker = load_yaml("../data-cleanup/danker-concise-lexicon/components.yaml")
- `1fc2dbcbd4` → morphgnt/lexicon/scripts/combine_components.py:0-0 — words = [n(word) for word in set(danker.keys()).union(set(greenlee.keys()))]
- `e21cf8baf6` → morphgnt/lexicon/scripts/combine_components.py:0-0 — if word in danker:
- `d78453b85d` → morphgnt/lexicon/scripts/combine_components.py:0-0 — print "    danker-full-entry: \"{}\"".format(danker[word]["full-entry"].encode("utf-8"))
- `e822f9494b` → morphgnt/lexicon/scripts/combine_components.py:0-0 — print "    danker-components: \"{}\"".format(danker[word]["components"].encode("utf-8"))
- `5fced1d502` → morphgnt/lexicon/scripts/basic_noun_ending_regex2.py:0-0 — form1, mounce, parses, count = line.strip().split("|")
- `5492d8adac` → morphgnt/lexicon/scripts/basic_noun_ending_regex2.py:0-0 — if not mounce.startswith("n-"):
- `e8d8ba7fd4` → morphgnt/lexicon/scripts/basic_noun_ending_regex2.py:0-0 — if re.match(mounce_re, mounce):
- `8e971d4018` → morphgnt/lexicon/scripts/basic_noun_ending_regex2.py:0-0 — print(form, mounce, parses, count, form_match, solution_match)
- `05b93270d8` → morphgnt/lexicon/scripts/basic_noun_ending_regex2.py:0-0 — print(parses, mounce, form, form1)
- `0b6a787cdc` → morphgnt/lexicon/scripts/extract_nouns2.py:0-0 — # lemma -> form -> cng -> count
- `d15db686c4` → morphgnt/lexicon/scripts/extract_nouns2.py:0-0 — forms[row["lemma"]][row["norm"]][row["ccat-parse"][4:7]] += 1
- `25d861f89d` → morphgnt/lexicon/scripts/extract_nouns2.py:0-0 — lexemes_entry = lexemes.get(lemma, {"mounce-morphcat": None})
- `469ef40485` → morphgnt/lexicon/scripts/extract_nouns2.py:0-0 — morphcat = lexemes_entry.get("mounce-morphcat")
- `f62aa5365a` → morphgnt/lexicon/scripts/extract_nouns2.py:0-0 — for form in forms[lemma]:
- `84ed25c191` → morphgnt/lexicon/scripts/extract_nouns2.py:0-0 — for parse in forms[lemma][form]:
- `ceb35c7902` → morphgnt/lexicon/scripts/extract_nouns2.py:0-0 — form, parse, forms[lemma][form][parse]
- `247014dbc2` → morphgnt/lexicon/scripts/extract_nouns2.py:0-0 — print("{}|{}|{}".format(lemma, morphcat, "/".join(form_list)))
- `ebea21d7a6` → morphgnt/lexicon/scripts/indeclinable-nouns.py:0-0 — danker = metadata.get("danker-entry", "")
- `d3b4852af8` → morphgnt/lexicon/scripts/indeclinable-nouns.py:0-0 — lexeme in already or
- `ec97424b7f` → morphgnt/lexicon/scripts/indeclinable-nouns.py:0-0 — danker,
- `cb5547f4a2` → morphgnt/lexicon/scripts/indeclinable-nouns.py:0-0 — "yes" if lexeme in already else "no",
- `1625a4f0f0` → morphgnt/lexicon/scripts/indeclinable-nouns.py:0-0 — if lexeme in already:
- `af6eabb7c7` → morphgnt/lexicon/scripts/indeclinable-nouns.py:0-0 — already.remove(lexeme)
- `cc1a0172cc` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — dodson = defaultdict(list)
- `aee0f4215a` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — with open("../data-cleanup/dodson-lexicon/dodson_lexicon.txt") as f:
- `c54aba7b7f` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — strongs, gk, pos, greek, short_gloss, long_gloss = line.strip().decode("utf-8").split("\t")
- `d0c7499e29` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — dodson[head_word].append({
- `64da7efdc5` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — "strongs": strongs,
- `5aedc4d8fc` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — if lexeme in dodson or metadata.get("bdag-headword") in dodson:
- `6645bd3151` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — if lexeme in dodson:
- `4223bfc1f0` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — data = dodson[lexeme]
- `064491e7f9` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — data = dodson[metadata["bdag-headword"]]
- `323b5e3f1f` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — not_in_dodson.add(lexeme.encode("utf-8"))
- `6aeb6c5d50` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — p("dodson-entry", "greek")
- `45100eb34d` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — p("strongs", "strongs")
- `5c10a5fa49` → morphgnt/lexicon/scripts/add_dodson.py:0-0 — p("dodson-pos", "pos")
- `92effd3e33` → morphgnt/lexicon/scripts/add_bdag_headword.py:0-0 — with open("../data-cleanup/bdag-headwords/bdag_headwords.txt") as f:
- `00c5c72f6f` → morphgnt/lexicon/scripts/add_bdag_headword.py:0-0 — if "bdag-headword" in metadata:
- `42b17a3c0a` → morphgnt/lexicon/scripts/add_bdag_headword.py:0-0 — print "    bdag-headword: {}".format(metadata["bdag-headword"].encode("utf-8"))
- `d29242f074` → morphgnt/lexicon/scripts/add_bdag_headword.py:0-0 — if metadata["bdag-headword"] not in headwords:
- `b604747ffd` → morphgnt/lexicon/scripts/add_bdag_headword.py:0-0 — existing_not_in_headwords.append(metadata["bdag-headword"].encode("utf-8"))
- `df659f9dc8` → morphgnt/lexicon/scripts/add_bdag_headword.py:0-0 — if lexeme in headwords:
- `42436367c9` → morphgnt/lexicon/scripts/add_bdag_headword.py:0-0 — print "    bdag-headword: {}".format(lexeme.encode("utf-8"))
- `deb4c22b90` → morphgnt/lexicon/scripts/add_bdag_headword.py:0-0 — added.append(lexeme.encode("utf-8"))
- `3d9f3f2458` → morphgnt/lexicon/scripts/add_bdag_headword.py:0-0 — missing_not_in_headwords.append(lexeme.encode("utf-8"))
- `32b886a01c` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — lemma = row["lemma"].decode("utf-8")
- `b921a02cc3` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — lexeme = lexemes.get(lemma)
- `4b0827f5f1` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — if lexeme is None:
- `f8eda032fd` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — lemma = "{}/{}".format(row["lemma"], row["ccat-pos"].strip("-")).decode("utf-8")
- `f5fcab7c0b` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — if isinstance(lexeme["pos"], list):
- `0eedc44cfd` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — print >> sys.stderr, lexeme
- `8e06a683f6` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — form_list = forms.setdefault(lemma, {}).setdefault(gender, {}).setdefault(case_number, {}).setdefault("forms", [])
- `e0a5b957f0` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — form_list = forms.setdefault(lemma, {}).setdefault(case_number, {}).setdefault("forms", [])
- `9807183933` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — form_list = forms.setdefault(lemma, {}).setdefault(tense_voice_mood, {}).setdefault("forms", [])
- `9d8c23f0a0` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — form_list = forms.setdefault(lemma, {}).setdefault(tense_voice_mood, {}).setdefault(person_number, {}).setdefault("forms", [])
- `8d1c2008a8` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — form_list = forms.setdefault(lemma, {}).setdefault(tense_voice_mood, {}).setdefault(gender, {}).setdefault(case_number, {}).setdefault("forms", [])
- `ad84ecd394` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — elif lexeme["pos"] in ["P", "X"]:
- `bdf3077049` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — form_list = forms.setdefault(lemma, {}).setdefault("forms", [])
- `667859791b` → morphgnt/lexicon/scripts/generate_forms.py:0-0 — print >>sys.stderr, "lexemes file doesn't have {}".format(row["lemma"])
- `bae2cde7cd` → morphgnt/lexicon/scripts/check_pos.py:0-0 — # verbs missing in dodson
- `eabc162e69` → morphgnt/lexicon/scripts/check_pos.py:0-0 — # verbs missing in dodson and morphcat
- `1fbd5411ec` → morphgnt/lexicon/scripts/check_pos.py:0-0 — # compound verbs missing in dodson
- `46c9085d34` → morphgnt/lexicon/scripts/check_pos.py:0-0 — # compound verbs that dodson thinks can be adjectives
- `8fc6925c14` → morphgnt/lexicon/scripts/check_pos.py:0-0 — # adjective missing in dodson
- `68fda6e480` → morphgnt/lexicon/scripts/check_pos.py:0-0 — # adjective missing in dodson and morphcat
- `03ce241e7d` → morphgnt/lexicon/scripts/check_pos.py:0-0 — # adjectives that dodson has as adverbs
- `37b1445189` → morphgnt/lexicon/scripts/check_pos.py:0-0 — # adjectives that mounce has as adverbs
- `8939f1c249` → morphgnt/lexicon/scripts/check_pos.py:0-0 — # nouns with multiple genders (according to dodson)
- `85a9e8204d` → morphgnt/lexicon/scripts/check_pos.py:0-0 — # nouns missing in dodson
- `1d816dfc7b` → morphgnt/lexicon/scripts/check_pos.py:0-0 — # nouns missing in dodson and morphcat
- `857b25acd9` → morphgnt/lexicon/scripts/extract_nouns.py:0-0 — counts[row["lemma"]] += 1
- `da29b8f2f8` → morphgnt/lexicon/scripts/extract_nouns.py:0-0 — for lemma, count in sorted(
- `99d932f765` → morphgnt/lexicon/scripts/extract_nouns.py:0-0 — lexemes_entry = lexemes.get(lemma, {"gloss": None})
- `9e91365f7e` → morphgnt/lexicon/scripts/extract_nouns.py:0-0 — print("{}|{}|{}".format(lemma, count, gloss))
- `1735b6464d` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — mounce = defaultdict(list)
- `76cdc23ead` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — with open("../data-cleanup/mounce-morphcat/mounce-tauber-morphcat-utf8.txt") as f:
- `2a623d9b18` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — mounce[greek].append({
- `789d00b11d` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — if not q("mounce-morphcat"):
- `f61ba5d861` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — if lexeme in missing_morphcat:
- `eea19b1354` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — if lexeme in mounce:
- `7ebb74692c` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — source = lexeme
- `647e21ea8a` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — elif metadata.get("bdag-headword") in mounce:
- `a8d04ffd3f` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — source = metadata["bdag-headword"]
- `916f246618` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — if len(mounce[source]) == 1:
- `52801af2de` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — gk = int(mounce[source][0]["gk"])
- `3e0c9902c2` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — print "    mounce-morphcat: {}".format(mounce[source][0]["morphcat"])
- `5118b00bfd` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — problems.append("{} len({}) > 1".format(source.encode("utf-8"), mounce[source]))
- `44d5817541` → morphgnt/lexicon/scripts/add_mounce_morphcat.py:0-0 — problems.append("{} not found (gk={})".format(lexeme.encode("utf-8"), metadata.get("gk")))
- `921fb0fcf4` → morphgnt/lexicon/scripts/basic_noun_ending_regex.py:0-0 — form, mounce, parses, count = line.strip().split("|")
- `8a358e83b5` → morphgnt/lexicon/scripts/basic_noun_ending_regex.py:0-0 — re.match(mounce_re, mounce) and re.match(form_re, form):
- `10af18d4ac` → morphgnt/lexicon/scripts/basic_noun_ending_regex.py:0-0 — print(form, mounce, parses, mounce_re, parses_re, count)
- `a5b0539186` → morphgnt/lexicon/scripts/basic_noun_ending_regex.py:0-0 — #     parses, mounce, form))
- `b86a1975aa` → morphgnt/lexicon/scripts/extract_noun_forms.py:0-0 — "ἑκατοντάρχης",  # @@@ fix lemma in sblgnt
