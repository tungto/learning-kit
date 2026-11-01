#!/usr/bin/env python3
"""Collect error-log rows from every topic, for weekly root-cause analysis.

Usage:
  collect_errors.py [--project DIR] [--root TOPICS_DIR] [--days N] [--topic SUBSTR]

Prints every row whose Date is within the window, grouped by topic, plus a
cause histogram and the repeat-question list. Read-only.
"""
import argparse
import collections
import datetime as dt
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "kit"))
import config as kcfg  # noqa: E402
import mdtable  # noqa: E402

DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def main():
    ap = argparse.ArgumentParser()
    kcfg.add_args(ap)
    ap.add_argument("--days", type=int, default=None)
    ap.add_argument("--topic", default="")
    a = ap.parse_args()

    cfg, topics = kcfg.from_args(a)
    days = a.days if a.days is not None else int(cfg.get("review.error_window_days"))
    prefix = cfg.skip_prefix()
    log_name = cfg.file_name("error_log")
    today = dt.date.today()
    since = today - dt.timedelta(days=days)

    by_topic = collections.OrderedDict()
    causes = collections.Counter()
    questions = collections.Counter()
    total = 0
    for path in sorted(pathlib.Path(topics).glob(f"**/{log_name}")):
        rel = os.path.relpath(path, topics)
        if any(p.startswith(prefix) for p in pathlib.Path(rel).parts):
            continue
        topic = path.parent.name
        if a.topic and a.topic not in topic:
            continue
        header = mdtable.header_of(path)
        if not header:
            continue
        for _, c in mdtable.read_rows(path, header):
            if len(c) < len(header):
                continue
            d = mdtable.cell(header, c, "Date")
            m = DATE.search(d)
            if not m or dt.date.fromisoformat(m.group(0)) < since:
                continue
            cause = mdtable.cell(header, c, "Cause")
            by_topic.setdefault(topic, []).append(c)
            causes[cause] += 1
            questions[mdtable.cell(header, c, "Question").lower()[:60]] += 1
            total += 1

    print(f"# Errors since {since} ({days}d): {total} rows in {len(by_topic)} topics")
    print(f"By cause: {dict(causes)}\n")
    for topic, rows in by_topic.items():
        print(f"## {topic} ({len(rows)})")
        header = cfg.table("error_log")
        for c in rows:
            print("  " + " | ".join(mdtable.cell(header, c, col) for col in
                                    ("Date", "Question", "My answer", "Correct", "Cause", "Fix drill")))
        print()
    repeats = [(q, n) for q, n in questions.items() if n > 1]
    print(f"## Repeated questions: {len(repeats)}")
    for q, n in sorted(repeats, key=lambda kv: -kv[1]):
        print(f"  {n}x {q}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
