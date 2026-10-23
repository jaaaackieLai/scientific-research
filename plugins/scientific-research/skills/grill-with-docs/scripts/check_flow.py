#!/usr/bin/env python3
"""Check a grill-with-docs flow.html.

Runs diagram-design's self-check, then two flow-page rules from references/session-files.md:
each form of each drawing keeps to the node budget, and no grid container mixes direct text
with inline tags (each inline tag would become its own row).
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "diagram-design" / "scripts"))
import self_check as dd  # noqa: E402

NODE_BUDGET = 9
FORMS = ("form-current", "form-planned")
GRID_RE = re.compile(r"display\s*:\s*(?:inline-)?grid\b")
INLINE_TAGS = {"a", "b", "code", "em", "i", "kbd", "small", "span", "strong", "sub", "sup"}
VOID_TAGS = {"br", "img", "input", "meta", "link", "hr", "wbr", "source"}


def grid_subjects(source: str) -> list[tuple[str, set[str], set[str], set[str]]]:
    """Selector subjects of stylesheet rules that set display grid."""
    styles = re.findall(r"<style\b[^>]*>(.*?)</style\s*>", source, re.IGNORECASE | re.DOTALL)
    sheet = dd.CSS_KEYFRAMES_RE.sub("", dd.CSS_COMMENT_RE.sub("", "\n".join(styles)))
    return [
        subject
        for selector, declarations in dd.CSS_RULE_RE.findall(sheet)
        if GRID_RE.search(declarations)
        for subject in dd.selector_subjects(selector)
    ]


@dataclass
class Element:
    tag: str
    grid_label: str | None
    text: bool = False
    inline: bool = False


@dataclass
class SvgElement:
    unpainted: bool
    form: str  # the FORMS class of the enclosing group, or "" for parts both forms share


class FlowParser(HTMLParser):
    """Node boxes (rect rx=6, the node grammar) per form of each accessible SVG, and mixed grid containers."""

    def __init__(self, grids: list[tuple[str, set[str], set[str], set[str]]]) -> None:
        super().__init__(convert_charrefs=True)
        self.grids = grids
        self.svgs: list[dict[str, set[tuple[str, ...]]]] = []
        self.mixed: dict[str, None] = {}
        self._svg: list[SvgElement] = []
        self._hidden = False
        self._stack: list[Element] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key.casefold(): value or "" for key, value in attrs}
        if tag == "svg" and not self._svg:
            self._hidden = data.get("aria-hidden", "").casefold() == "true"
            self.svgs.append({})
            self._svg.append(SvgElement(False, ""))
            return
        if self._svg:
            parent = self._svg[-1]
            form = next((name for name in FORMS if name in data.get("class", "").split()), parent.form)
            self._svg.append(SvgElement(parent.unpainted or tag in dd.UNPAINTED_TAGS, form))
            if tag == "rect" and not self._svg[-1].unpainted and not self._hidden and data.get("rx", "").strip() == "6":
                # A mask rect and its box share geometry, so they count once.
                box = tuple(data.get(key, "") for key in ("x", "y", "width", "height"))
                self.svgs[-1].setdefault(form, set()).add(box)
            return
        if tag in VOID_TAGS:
            return
        if self._stack and self._stack[-1].grid_label and tag in INLINE_TAGS:
            self._stack[-1].inline = True
        grid = any(dd.matches_subject(tag, data, subject) for subject in self.grids)
        label = tag + "".join("." + name for name in sorted(data.get("class", "").split()))
        self._stack.append(Element(tag, label if grid else None))

    def handle_endtag(self, tag: str) -> None:
        if self._svg:
            self._svg.pop()
            return
        for index in range(len(self._stack) - 1, -1, -1):
            element = self._stack[index]
            if element.tag == tag:
                if element.grid_label and element.text and element.inline:
                    self.mixed[element.grid_label] = None
                del self._stack[index:]
                return

    def handle_data(self, data: str) -> None:
        if not self._svg and self._stack and self._stack[-1].grid_label and data.strip():
            self._stack[-1].text = True


def flow_errors(source: str, budget: int = NODE_BUDGET) -> list[str]:
    parser = FlowParser(grid_subjects(source))
    parser.feed(source)
    parser.close()
    errors = []
    for number, forms in enumerate(parser.svgs, 1):
        shared = forms.pop("", set())
        # The switch shows one form at a time, so each form is one drawing.
        for form, boxes in (forms or {"": set()}).items():
            count = len(shared | boxes)
            if count > budget:
                where = f"svg {number} {form}".rstrip()
                errors.append(
                    f"{where} has {count} node boxes; the budget is {budget} "
                    "(split into an overview and a detail diagram)"
                )
    errors += [
        f"<{label}> is display grid and mixes text with inline elements; "
        "each inline element becomes its own row. Wrap the text in one <p>"
        for label in parser.mixed
    ]
    return errors


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    argument_parser.add_argument("files", nargs="+", type=Path)
    argument_parser.add_argument("--node-budget", type=int, default=NODE_BUDGET)
    args = argument_parser.parse_args()
    failed = False
    for path in args.files:
        try:
            errors = dd.verify(path) + flow_errors(path.read_text(encoding="utf-8"), args.node_budget)
        except (OSError, UnicodeError) as exc:
            errors = [str(exc)]
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
