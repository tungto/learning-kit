#!/usr/bin/env python3
"""Append one row to the first markdown table in a file (error log / glossary / patterns).

Usage:
  append_row.py FILE CELL1 CELL2 ...          # row cells as args
  append_row.py FILE --check                  # print the profile and header, no write
  [--project DIR]                             # project root, if not inferable from FILE

Rules:
- The row must have exactly as many cells as the table header, else exit 2.
- Pipes inside a cell are escaped; newlines become spaces.
- Inserts after the last row of the FIRST table, so a "Parking lot" or any
  other section below the table stays untouched.
- Rows are validated against the table's profile before writing: an error-log
  row needs every cell filled, a Cause from the configured set and a
  YYYY-MM-DD date in Re-test; a glossary row needs a term and a definition in
  the user's own words; a patterns row needs a trigger and a move. A bad row
  exits 2 and writes nothing, so a half-remembered row has to be filled in
  instead of landing in the log.
- Skips duplicates, ignoring case, on the profile's configured key: glossary
  and patterns on the first column (one row per term, one per trigger),
  the error log on Date + Question (the same question can come back later).
"""
import argparse
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "kit"))
import config as kcfg  # noqa: E402
import mdtable  # noqa: E402

DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def validate(profile, header, cells, cfg):
    """Problems with this row; an empty list means the row is fine."""
    bad = []
    if profile == "error_log":
        for name, c in zip(header, cells):
            if not c or c == "-":
                bad.append(f"column '{name}' is empty")
        causes = [c.lower() for c in cfg.get("grading.causes")]
        cause = mdtable.cell(header, cells, "Cause")
        if cause and cause.lower() not in causes:
            bad.append(f"Cause '{cause}' is not one of {', '.join(cfg.get('grading.causes'))}")
        retest = mdtable.cell(header, cells, "Re-test")
        if retest and not DATE.search(retest):
            bad.append(f"Re-test '{retest}' has no YYYY-MM-DD date")
    elif profile == "glossary":
        if not cells[0]:
            bad.append("Term is empty")
        if len(cells) > 1 and (not cells[1] or cells[1] == "-"):
            bad.append("definition is empty - the row is worthless without the user's own words")
    elif profile == "patterns":
        if not cells[0]:
            bad.append("Trigger is empty")
        if len(cells) > 1 and (not cells[1] or cells[1] == "-"):
            bad.append("Move is empty - a pattern row is trigger -> move, in the user's words")
    return bad


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("file")
    ap.add_argument("cells", nargs="*")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--project", default=None)
    ap.add_argument("-h", "--help", action="store_true")
    a, unknown = ap.parse_known_args()
    if a.help:
        print(__doc__)
        return 0
    cells = [c for c in a.cells if c != "--check"] + [u for u in unknown if not u.startswith("--")]

    path = pathlib.Path(a.file)
    project = a.project or os.environ.get("CLAUDE_PROJECT_DIR")
    if not project:
        # walk up from the file itself, so a bare relative path still resolves
        p = path.resolve().parent
        for cand in [p, *p.parents]:
            if (cand / kcfg.CONFIG_NAME).is_file():
                project = str(cand)
                break
    cfg = kcfg.load(project)

    if not path.is_file():
        print(f"error: no such file: {path}", file=sys.stderr)
        return 2
    header = mdtable.header_of(path)
    if header is None:
        print(f"error: no table in {path}", file=sys.stderr)
        return 2
    profile = cfg.profile_for(header)

    if a.check or not cells:
        print(f"profile={profile or 'unknown'} | " + " | ".join(header))
        return 0

    if len(cells) != len(header):
        print(f"error: need {len(header)} cells ({' | '.join(header)}), got {len(cells)}", file=sys.stderr)
        return 2

    problems = validate(profile, header, cells, cfg)
    if problems:
        print("error: row rejected, nothing written:", file=sys.stderr)
        for b in problems:
            print(f"  - {b}", file=sys.stderr)
        print("Ask the user for the missing part, then re-run.", file=sys.stderr)
        return 2

    nkey = int(cfg.get(f"layout.dedupe_keys.{profile}")) if profile else 2
    status, msg = mdtable.append_row(path, cells, nkey=nkey)
    print(f"{status}: {msg}", file=sys.stderr if status == "error" else sys.stdout)
    return 2 if status == "error" else 0


if __name__ == "__main__":
    sys.exit(main())
