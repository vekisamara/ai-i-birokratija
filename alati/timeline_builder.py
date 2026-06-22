#!/usr/bin/env python3
"""Generator hronologije predmeta iz CSV fajla."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

DATE_FORMATS = ["%Y-%m-%d", "%d.%m.%Y", "%d.%m.%Y."]


def parse_date(value: str) -> datetime:
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return datetime.max


def read_field(row: dict[str, str], names: list[str], default: str = "") -> str:
    for name in names:
        value = row.get(name)
        if value:
            return value
    return default


def build_timeline(csv_path: Path, output: Path | None = None) -> str:
    with csv_path.open("r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    rows.sort(key=lambda row: parse_date(read_field(row, ["date", "document_date", "datum"])))
    lines = ["# Hronologija predmeta", ""]

    for row in rows:
        date_value = read_field(row, ["date", "document_date", "datum"], "bez datuma")
        event = read_field(row, ["event", "document_name", "predmet", "note"], "stavka")
        institution = read_field(row, ["institution", "organ"])
        source = read_field(row, ["source", "document_number", "id"])
        details = []
        if institution:
            details.append(institution)
        if source:
            details.append(source)
        extra = f" ({'; '.join(details)})" if details else ""
        lines.append(f"- {date_value} — {event}{extra}")

    result = "\n".join(lines) + "\n"
    if output:
        output.write_text(result, encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Napravi Markdown hronologiju iz CSV evidencije.")
    parser.add_argument("csv", help="CSV fajl")
    parser.add_argument("--output", help="Markdown izlaz")
    args = parser.parse_args()
    result = build_timeline(Path(args.csv), Path(args.output) if args.output else None)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
