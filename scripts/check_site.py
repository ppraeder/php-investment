#!/usr/bin/env python3
"""Dependency-free structural and internal-link checks for the static site."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys


ROOT = Path(__file__).resolve().parent.parent
HTML_FILES = sorted(ROOT.glob("*.html"))


class PageParser(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.local_sources: list[str] = []
        self.title_depth = 0
        self.title_text: list[str] = []
        self.h1_count = 0
        self.lang = ""
        self.has_viewport = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                raise ValueError(f"{self.path.name}: duplicate id #{element_id}")
            self.ids.add(element_id)

        if tag == "html":
            self.lang = values.get("lang") or ""
        elif tag == "title":
            self.title_depth += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta" and values.get("name", "").lower() == "viewport":
            self.has_viewport = True

        if tag in {"a", "link"} and values.get("href"):
            self.links.append(values["href"] or "")
        if tag in {"img", "script", "iframe", "source", "video", "audio"}:
            source = values.get("src")
            if source:
                self.local_sources.append(source)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text.append(data)


def parse_pages() -> dict[Path, PageParser]:
    pages: dict[Path, PageParser] = {}
    for path in HTML_FILES:
        parser = PageParser(path)
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
        pages[path.resolve()] = parser
    return pages


def resolve_local(page: Path, value: str) -> tuple[Path, str] | None:
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or value.startswith(("mailto:", "tel:")):
        return None
    target = unquote(parsed.path)
    target_path = page if not target else (page.parent / target).resolve()
    if target_path.is_dir():
        target_path /= "index.html"
    return target_path, unquote(parsed.fragment)


def main() -> int:
    errors: list[str] = []
    if not HTML_FILES:
        errors.append("No HTML files found")
    pages = parse_pages()

    for path, parser in pages.items():
        if parser.lang != "de":
            errors.append(f"{path.name}: expected lang=de")
        if not "".join(parser.title_text).strip():
            errors.append(f"{path.name}: missing non-empty title")
        if parser.h1_count != 1:
            errors.append(f"{path.name}: expected exactly one h1, found {parser.h1_count}")
        if not parser.has_viewport:
            errors.append(f"{path.name}: missing viewport meta tag")

        for value in parser.links + parser.local_sources:
            resolved = resolve_local(path, value)
            if not resolved:
                continue
            target, fragment = resolved
            if not target.exists():
                errors.append(f"{path.name}: broken local reference {value}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = pages.get(target.resolve())
                if target_parser is None or fragment not in target_parser.ids:
                    errors.append(f"{path.name}: missing fragment target {value}")

        for value in parser.local_sources:
            if urlsplit(value).scheme or value.startswith("//"):
                errors.append(f"{path.name}: external resource is not allowed: {value}")

    for required in ("favicon.svg", "robots.txt", "sitemap.xml", ".htaccess"):
        if not (ROOT / required).is_file():
            errors.append(f"Missing required file: {required}")

    if errors:
        print("Site checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Site checks passed for {len(pages)} HTML pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
