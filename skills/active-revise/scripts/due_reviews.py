#!/usr/bin/env python3
"""List error-log rows whose Re-test date is due (<= today).

Usage:
  due_reviews.py [--project DIR] [--root TOPICS_DIR] [--topic SUBSTR]
                 [--ahead N] [--summary]

Walks the topics dir for every error log, skipping any path segment that
starts with the configured skip prefix. In the Re-test cell each YYYY-MM-DD is
a review date; a date carrying a result marker was already reviewed, so only
the dates after the last marked one are still scheduled. Prints due rows
(oldest first), rows coming up within --ahead days, then a COLD pool: rows
that already passed at least once, oldest last pass first, for interleaved
questions. Each row gets a TYPE hint from its Fix drill. Read-only.
"""
import argparse
import datetime as dt
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "kit"))
import config as kcfg  # noqa: E402
import dates as kdates  # noqa: E402
import mdtable  # noqa: E402


def kind(drill, types):
    d = drill.lower()
    for name, words in types.items():
        if not words:
            continue
        if any(w.lower() in d for w in words):
            return name
    return "recall"


def main():
    ap = argparse.ArgumentParser()
    kcfg.add_args(ap)
    ap.add_argument("--topic", default="")
    ap.add_argument("--ahead", type=int, default=None)
    ap.add_argument("--summary", action="store_true",
                    help="one line per topic, no questions or answers (safe to inject into context)")
    a = ap.parse_args()

    cfg, topics = kcfg.from_args(a)
    ahead = a.ahead if a.ahead is not None else int(cfg.get("review.ahead_days"))
    markers = cfg.get("review.markers")
    types = cfg.get("review.types")
    log_name = cfg.file_name("error_log")
    show = int(cfg.get("review.cold_pool_show"))

    today = dt.date.today()
    due, soon, cold = [], [], []
    for path in sorted(pathlib.Path(topics).glob(f"**/{log_name}")):
        rel = os.path.relpath(path, topics)
        if cfg.skipped(path, topics):
            continue
        topic = cfg.topic_of(path, topics)
        if a.topic and a.topic not in topic:
            continue
        header = mdtable.header_of(path)
        if not header:
            continue
        for _, c in mdtable.read_rows(path, header):
            if len(c) < len(header):
                continue
            q = mdtable.cell(header, c, "Question")
            correct = mdtable.cell(header, c, "Correct")
            cause = mdtable.cell(header, c, "Cause")
            drill = mdtable.cell(header, c, "Fix drill")
            retest = mdtable.cell(header, c, "Re-test")
            if not retest:
                continue
            pending, passed = kdates.split_retest(retest, markers)
            if passed:
                cold.append((max(passed), topic, q, correct, kind(drill, types)))
            if not pending:
                continue
            nxt = min(pending)
            row = (nxt, topic, rel, q, correct, cause, drill)
            if nxt <= today:
                due.append(row)
            elif (nxt - today).days <= ahead:
                soon.append(row)

    if a.summary:
        # Questions and answers are withheld: a summary may be pasted into a
        # session prompt, and seeing the answers would spoil the re-test.
        print(f"Re-tests as of {today}: {len(due)} due, {len(soon)} within {ahead}d, {len(cold)} in cold pool.")
        if due:
            per_topic = {}
            for nxt, topic, *_ in due:
                late = (today - nxt).days
                worst, n = per_topic.get(topic, (0, 0))
                per_topic[topic] = (max(worst, late), n + 1)
            for topic, (late, n) in sorted(per_topic.items(), key=lambda kv: -kv[1][0]):
                print(f"  {topic}: {n} due, oldest {late}d late")
            print("Run `active-revise` before new material.")
        return 0

    print(f"# Reviews due as of {today}: {len(due)} due, {len(soon)} within {ahead}d\n")
    for title, rows in (("DUE", due), ("SOON", soon)):
        for nxt, topic, rel, q, correct, cause, drill in sorted(rows):
            late = (today - nxt).days
            tag = f"{late}d late" if late > 0 else ("today" if late == 0 else f"in {-late}d")
            print(f"[{title}] {nxt} ({tag}) {topic} | cause={cause} | type={kind(drill, types)}\n"
                  f"  Q: {q}\n  Correct (hide from user): {correct}\n  Drill: {drill}\n  File: {rel}")
    print(f"\n# COLD pool (passed before, oldest last pass first): {len(cold)}")
    for last, topic, q, correct, k in sorted(cold)[:show]:
        print(f"[COLD] last pass {last} {topic} | type={k}\n  Q: {q}\n  Correct (hide from user): {correct}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
