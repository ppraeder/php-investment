#!/usr/bin/env python3
"""Require confirmed publication data and reject visible placeholders."""

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parent.parent
TEXT_FILES = [
    ROOT / "index.html",
    ROOT / "impressum.html",
    ROOT / "datenschutz.html",
    ROOT / "robots.txt",
    ROOT / "sitemap.xml",
]


def main() -> int:
    errors: list[str] = []
    approval_path = ROOT / "publication-confirmation.json"
    if not approval_path.exists():
        errors.append("publication-confirmation.json is missing; company and hosting data have not been approved")
    else:
        try:
            approval = json.loads(approval_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            errors.append("publication-confirmation.json is not valid UTF-8 JSON")
        else:
            if not isinstance(approval, dict):
                errors.append("publication-confirmation.json must contain a JSON object")
            else:
                required = ("company_details", "contact", "hosting", "log_retention", "privacy")
                missing = [key for key in required if approval.get(key) is not True]
                if missing:
                    errors.append("publication-confirmation.json is missing approvals: " + ", ".join(missing))
    for path in TEXT_FILES:
        content = path.read_text(encoding="utf-8")
        if "example.invalid" in content:
            errors.append(f"{path.name}: placeholder domain example.invalid remains")
        if path.suffix == ".html" and 'class="placeholder"' in content:
            errors.append(f"{path.name}: visible publication placeholders remain")

    if errors:
        print("Deployment blocked. Complete the publication data first:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Deployment readiness checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
