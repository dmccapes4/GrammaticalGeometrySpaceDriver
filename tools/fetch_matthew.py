#!/usr/bin/env python3
"""
fetch_matthew.py — Download Matthew from Perseus canonical-greekLit
and save as plain Greek Unicode text (one verse per line).

Source: Perseus tlg0031.tlg001.perseus-grc2.xml (NT Greek)
Output: tools/homer/matthew.txt  — one verse line, Greek with punctuation
"""

from pathlib import Path
import requests
from lxml import etree

URL = "https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0031/tlg001/tlg0031.tlg001.perseus-grc2.xml"
OUT = Path(__file__).parent / "homer" / "matthew.txt"


def fetch_xml(url: str) -> bytes:
    print(f"Fetching {url} ...", flush=True)
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.content


def extract_verses(xml_bytes: bytes) -> list[tuple[str, str]]:
    """
    Extract (ref, text) tuples from TEI XML.
    NT TEI typically uses <ab> or <milestone> + text nodes for verses.
    Returns list of (ref_label, verse_text).
    """
    root = etree.fromstring(xml_bytes)
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    verses = []

    # Strategy 1: <ab n="verse_ref"> elements
    ab_els = root.findall(".//tei:ab", ns)
    if ab_els:
        print(f"  Found {len(ab_els)} <ab> elements")
        for el in ab_els:
            text = "".join(el.itertext()).strip()
            ref = el.get("n", "")
            if text:
                verses.append((ref, text))
        return verses

    # Strategy 2: <l> elements
    l_els = root.findall(".//tei:l", ns)
    if l_els:
        print(f"  Found {len(l_els)} <l> elements")
        for el in l_els:
            text = "".join(el.itertext()).strip()
            ref = el.get("n", "")
            if text:
                verses.append((ref, text))
        return verses

    # Strategy 3: collect all text under <body>
    body = root.find(".//tei:body", ns)
    if body is not None:
        text = "".join(body.itertext()).strip()
        # Split on newlines as verse approximation
        for i, line in enumerate(text.splitlines()):
            line = line.strip()
            if line:
                verses.append((str(i + 1), line))
        print(f"  Fell back to body text: {len(verses)} lines")

    return verses


def main():
    if OUT.exists():
        print(f"{OUT} already exists. Delete to re-fetch.")
        return

    xml = fetch_xml(URL)
    verses = extract_verses(xml)

    if not verses:
        print("WARNING: no verse text extracted")
        return

    # Write: ref TAB text
    lines = [f"{ref}\t{text}" for ref, text in verses]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Saved {len(verses)} verses → {OUT}")

    # Show first 5
    print("\nSample:")
    for ref, text in verses[:5]:
        print(f"  [{ref}] {text[:80]}")


if __name__ == "__main__":
    main()
