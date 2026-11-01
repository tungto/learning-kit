#!/usr/bin/env python3
"""Header-driven markdown-table read / append / dedupe.

One implementation for every kit script. It fixes two bugs the three
interview-v2 copies had between them:

- the writer split cells on a plain "|" while the readers split on
  (?<!\\)\| , so a cell holding the escaped \| that the writer itself
  produces was split wrongly on the dedupe path: a row containing a pipe
  could silently duplicate. Both sides now use the escaped split.
- the dedupe key was inferred from the first header cell ("Term" -> 1 cell,
  anything else -> 2 cells), so patterns.md keyed on Trigger + Move and two
  phrasings of the same Move both landed. The key is now configured per
  table profile (layout.dedupe_keys).
"""
import re

CELL_SPLIT = re.compile(r"(?<!\\)\|")


def split_row(line):
    """Cells of one markdown table row, honouring escaped pipes."""
    return [c.strip() for c in CELL_SPLIT.split(line.strip().strip("|"))]


def escape(value):
    return str(value).replace("|", r"\|").replace("\n", " ").strip()


def is_divider(cells):
    return bool(cells) and all(set(c) <= set("-: ") and c for c in cells)


def find_table(lines):
    """(start, end) line indexes of the FIRST table, or (None, None).

    Only the first table is ever written to, so a "Parking lot" section or
    any prose below it survives an append untouched.
    """
    start = next((i for i, l in enumerate(lines) if l.lstrip().startswith("|")), None)
    if start is None:
        return None, None
    end = start
    while end + 1 < len(lines) and lines[end + 1].lstrip().startswith("|"):
        end += 1
    return start, end


def read_rows(path, header=None):
    """Yield (lineno, cells) for every data row of the first table in path."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    start, end = find_table(lines)
    if start is None:
        return []
    out = []
    for i in range(start + 1, end + 1):
        cells = split_row(lines[i])
        if is_divider(cells):
            continue
        if header and [c.lower() for c in cells] == [h.lower() for h in header]:
            continue
        out.append((i + 1, cells))
    return out


def header_of(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    start, _ = find_table(lines)
    if start is None:
        return None
    return split_row(lines[start])


def index_of(header, column):
    """Index of a column by name, case-insensitive, prefix-tolerant."""
    low = [h.strip().lower() for h in header]
    want = column.strip().lower()
    if want in low:
        return low.index(want)
    for i, h in enumerate(low):
        if h.startswith(want):
            return i
    return None


def cell(header, cells, column, default=""):
    i = index_of(header, column)
    if i is None or i >= len(cells):
        return default
    return cells[i]


def append_row(path, cells, nkey=2):
    """Append one row after the first table. Returns (status, message).

    status: "ok" | "skip" | "error"
    """
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")
    start, end = find_table(lines)
    if start is None:
        return "error", f"no table in {path}"
    header = split_row(lines[start])
    if len(cells) != len(header):
        return "error", f"need {len(header)} cells ({' | '.join(header)}), got {len(cells)}"
    cells = [escape(c) for c in cells]
    key = [c.lower() for c in cells[:nkey]]
    for i in range(start + 1, end + 1):
        existing = split_row(lines[i])
        if is_divider(existing):
            continue
        if [c.lower() for c in existing[:nkey]] == key:
            return "skip", f"row already present (key: {' | '.join(cells[:nkey])}) - enrich that row instead"
    lines.insert(end + 1, "| " + " | ".join(cells) + " |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return "ok", f"appended to {path}"


def render_table(header):
    """A header-only table, as the topic templates ship it."""
    return "| " + " | ".join(header) + " |\n|" + "|".join("---" for _ in header) + "|\n"
