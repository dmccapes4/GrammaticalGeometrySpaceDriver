#!/usr/bin/env python3
"""
fetch_oration.py — Fetch oration / translated-oration Greek corpora for GGSD
punctuation baselines, from Perseus canonical-greekLit (same source family as
fetch_homer.py). Extracts <p> (prose) and <l> (verse) blocks, one per line,
punctuation preserved. Verse-drama speaker tags are dropped; text only.

Works chosen for variation (see docs/ORATION_SOURCES_20261111.md):
  plato_apology      Plato, Apology          — staged forensic oration, Q&A gates
  demosthenes_crown  Demosthenes, On Crown   — delivered political oration
  lysias_1           Lysias, Speech 1        — delivered court speech, plain style
  herodotus          Herodotus, Histories    — recited logoi, Ionic prose
  josephus_war       Josephus, Jewish War    — Aramaic-first, rendered into Greek
  euripides_tlg003   Euripides work tlg003   — metred dialogue (title read from TEI)
"""
import sys
from pathlib import Path

import requests
from lxml import etree

BASE = "https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/"
WORKS = {
    "plato_apology":     BASE + "tlg0059/tlg002/tlg0059.tlg002.perseus-grc2.xml",
    "demosthenes_crown": BASE + "tlg0014/tlg018/tlg0014.tlg018.perseus-grc2.xml",
    "lysias_1":          BASE + "tlg0540/tlg001/tlg0540.tlg001.perseus-grc2.xml",
    "herodotus":         BASE + "tlg0016/tlg001/tlg0016.tlg001.perseus-grc2.xml",
    "josephus_war":      BASE + "tlg0526/tlg004/tlg0526.tlg004.perseus-grc2.xml",
    "euripides_tlg003":  BASE + "tlg0006/tlg003/tlg0006.tlg003.perseus-grc2.xml",
    # second pack (2026-11-11b): oration-about-oration, Socratic record,
    # second delivered orator, stage comedy
    "plato_gorgias":     BASE + "tlg0059/tlg023/tlg0059.tlg023.perseus-grc2.xml",
    "xenophon_memorabilia": BASE + "tlg0032/tlg002/tlg0032.tlg002.perseus-grc2.xml",
    "aeschines_timarchus":  BASE + "tlg0026/tlg001/tlg0026.tlg001.perseus-grc2.xml",
    "aristophanes_tlg003":  BASE + "tlg0019/tlg003/tlg0019.tlg003.perseus-grc2.xml",
}
OUT_DIR = Path(__file__).parent / "oration"
NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def fetch(url: str) -> bytes:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    return r.content


def extract(xml_bytes: bytes) -> tuple[str, list[str]]:
    root = etree.fromstring(xml_bytes)
    titles = root.findall(".//tei:titleStmt/tei:title", NS)
    title = " ".join(titles[0].itertext()).strip() if titles else ""
    blocks: list[str] = []
    body = root.find(".//tei:body", NS)
    scope = body if body is not None else root
    for el in scope.iter():
        if not isinstance(el.tag, str):
            continue
        if etree.QName(el).localname in ("p", "l"):
            text = " ".join("".join(el.itertext()).split())
            if text:
                blocks.append(text)
    return title, blocks


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    for name, url in WORKS.items():
        out = OUT_DIR / f"{name}.txt"
        if out.exists():
            print(f"  {out} exists, skipping")
            continue
        print(f"Fetching {name} ...", flush=True)
        try:
            title, blocks = extract(fetch(url))
        except Exception as e:  # keep going; report at end
            print(f"  ERROR {name}: {e}", file=sys.stderr)
            continue
        out.write_text("\n".join(blocks), encoding="utf-8")
        (OUT_DIR / f"{name}.title").write_text(title + "\n", encoding="utf-8")
        print(f"  {name}: {len(blocks):,} blocks | TEI title: {title[:90]}")


if __name__ == "__main__":
    main()
