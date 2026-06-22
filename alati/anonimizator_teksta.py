#!/usr/bin/env python3
"""Lokalna osnovna anonimizacija tekstualnih fajlova.

Alat koristi regularne izraze i nije savrsen. Rezultat treba rucno pregledati.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PATTERNS = [
    ("JMBG", re.compile(r"\b\d{13}\b"), "[ANONIMIZOVANO_JMBG]"),
    ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[ANONIMIZOVANO_EMAIL]"),
    ("PHONE", re.compile(r"(?<!\d)(?:\+?387|0)?\s?\d{2}\s?\d{3}\s?\d{3,4}(?!\d)"), "[ANONIMIZOVANO_TELEFON]"),
    ("ID_NUMBER", re.compile(r"\b(?:LK|licna karta|lična karta|broj lične karte)\s*[:#-]?\s*[A-Z0-9-]{5,}\b", re.IGNORECASE), "[ANONIMIZOVANO_DOKUMENT]"),
]


def anonymize(text: str) -> tuple[str, dict[str, int]]:
    stats: dict[str, int] = {}
    result = text
    for name, pattern, replacement in PATTERNS:
        result, count = pattern.subn(replacement, result)
        stats[name] = count
    return result, stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Osnovna lokalna anonimizacija TXT/MD fajla.")
    parser.add_argument("input", help="Ulazni TXT ili MD fajl")
    parser.add_argument("--output", help="Izlazni fajl; ako nije naveden, dodaje se .anonimizovano")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print("Ulazni fajl ne postoji.")
        return 1

    output_path = Path(args.output) if args.output else input_path.with_suffix(input_path.suffix + ".anonimizovano")
    text = input_path.read_text(encoding="utf-8")
    result, stats = anonymize(text)
    output_path.write_text(result, encoding="utf-8")

    print(f"Kreiran anonimizovani fajl: {output_path}")
    print("Statistika zamjena:")
    for key, value in stats.items():
        print(f"- {key}: {value}")
    print("Upozorenje: automatska anonimizacija nije dovoljna za javnu objavu. Obavezan je rucni pregled.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
