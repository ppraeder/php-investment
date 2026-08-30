#!/usr/bin/env python3
"""Fail safely when publication placeholders are still present."""

from pathlib import Path
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
