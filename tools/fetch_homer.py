#!/usr/bin/env python3
"""
fetch_homer.py — Download Iliad and Odyssey as plain Greek Unicode text
from Perseus canonical-greekLit GitHub repo and save locally.

Sources:
  Iliad:   tlg0012.tlg001.perseus-grc2.xml  (Perseus Greek)
  Odyssey: tlg0012.tlg002.perseus-grc2.xml

Output:
  tools/homer/iliad.txt    — one line per verse, Greek Unicode
  tools/homer/odyssey.txt  — one line per verse, Greek Unicode
"""

import re
import sys
from pathlib import Path

import requests
from lxml import etree

ILIAD_URL   = "https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg001/tlg0012.tlg001.perseus-grc2.xml"
ODYSSEY_URL = "https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml"

OUT_DIR = Path(__file__).parent / "homer"
OUT_DIR.mkdir(exist_ok=True)


def fetch_xml(url: str) -> bytes:
    print(f"Fetching {url} ...", flush=True)
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.content


def extract_lines(xml_bytes: bytes) -> list[str]:
    """
    Extract text content of all <l> (line) elements from TEI XML.
    Returns list of Greek verse strings with punctuation preserved.
    """
    root = etree.fromstring(xml_bytes)
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    lines = []
    # Try TEI namespace first, then no namespace
    l_elements = root.findall(".//tei:l", ns)
    if not l_elements:
        l_elements = root.findall(".//l")

    for el in l_elements:
        text = "".join(el.itertext()).strip()
        if text:
            lines.append(text)

    return lines


def save(lines: list[str], path: Path) -> None:
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Saved {len(lines):,} lines → {path}", flush=True)


BASE = "https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/"

PINDAR_URLS = {
    "pindar_olympian":  BASE + "tlg0033/tlg001/tlg0033.tlg001.perseus-grc2.xml",
    "pindar_pythian":   BASE + "tlg0033/tlg002/tlg0033.tlg002.perseus-grc2.xml",
    "pindar_nemean":    BASE + "tlg0033/tlg003/tlg0033.tlg003.perseus-grc2.xml",
    "pindar_isthmian":  BASE + "tlg0033/tlg004/tlg0033.tlg004.perseus-grc2.xml",
}


def main():
    works = [
        ("iliad",   ILIAD_URL),
        ("odyssey", ODYSSEY_URL),
    ] + list(PINDAR_URLS.items())
    for name, url in works:
        out = OUT_DIR / f"{name}.txt"
        if out.exists():
            print(f"  {out} already exists, skipping fetch.")
            continue
        xml = fetch_xml(url)
        lines = extract_lines(xml)
        if not lines:
            print(f"  WARNING: no <l> elements found in {name} XML", file=sys.stderr)
        save(lines, out)

    print("Done.")


if __name__ == "__main__":
    main()
