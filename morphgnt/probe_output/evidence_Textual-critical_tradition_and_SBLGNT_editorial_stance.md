# Evidence for Textual-critical tradition and SBLGNT editorial stance

- `ggsd.py:0-5` → python3 ggsd.py --verse "Matthew 25:18" --model ollama/... --morphgnt tools/sblgnt/Matthew-morphgnt.txt
- `ggsd.py:0-5` → # word (field 4) is clean — no ⸀ apparatus markers or trailing punctuation.
- `ggsd.py:0-5` → "(e.g. tools/sblgnt/Matthew-morphgnt.txt). "
- `sources.py:0-5` → for el in soup.select("div.translation, div.version, table.translations tr"):
- `morphgnt/embed_morphgnt.py:0-5` → - Large NT data files in sblgnt/ and python/pysblgnt/sblgnt/ (≥1000 lines)
- `morphgnt/python/setup.py:0-5` → name="py-sblgnt",
- `morphgnt/python/setup.py:0-5` → description="pip-installable MorphGNT/SBLGNT with Python API",
- `morphgnt/python/setup.py:0-5` → url="https://github.com/morphgnt/py-sblgnt",
- `morphgnt/python/setup.py:0-5` → package_data={"": ["sblgnt/*.txt"]},
- `morphgnt/python/pysblgnt/__init__.py:0-5` → return "sblgnt/{}-{}-morphgnt.txt".format(
- `morphgnt/python/pysblgnt/__init__.py:0-5` → yield a dict for each MorphGNT/SBLGNT row in the given book number.
- `morphgnt/lexicon/projects/principal_parts/check_endings.py:0-5` → for row in fs["sblgnt-lexemes"].rows():
- `morphgnt/lexicon/scripts/check_forms.py:0-5` → for row in fs["sblgnt-forms"].rows():
- `morphgnt/lexicon/scripts/extract_noun_forms.py:0-5` → "ἑκατοντάρχης",  # @@@ fix lemma in sblgnt
