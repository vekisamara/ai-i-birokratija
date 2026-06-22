#!/usr/bin/env python3
"""Generator osnovnog case.json fajla za Civic Forensics predmete."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def build_case(args: argparse.Namespace) -> dict:
    return {
        "case_id": args.case_id,
        "case_title": args.title,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "institution": args.institution,
        "issue_type": args.issue_type,
        "public_interest": args.public_interest,
        "risk_level": args.risk_level,
        "summary": args.summary or "",
        "legal_basis": split_csv(args.legal_basis),
        "documents": [],
        "timeline": [],
        "findings": [],
        "recommended_action": args.recommended_action or "",
        "privacy_note": "Sensitive personal data should be minimized or anonymized before public use.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Napravi osnovni case.json za predmet građanske forenzike.")
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--institution", required=True)
    parser.add_argument("--issue-type", required=True, help="npr. cutanje_uprave, formalizam, kontradikcija, metapodaci")
    parser.add_argument("--public-interest", required=True)
    parser.add_argument("--risk-level", default="medium", choices=["low", "medium", "high", "critical"])
    parser.add_argument("--summary")
    parser.add_argument("--legal-basis", help="Zarezom odvojeni propisi ili akti")
    parser.add_argument("--recommended-action")
    parser.add_argument("--output", default="case.json")
    args = parser.parse_args()

    data = build_case(args)
    Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Kreiran fajl: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
