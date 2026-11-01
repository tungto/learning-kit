#!/usr/bin/env python3
"""Check a learning project's layout invariants and its topic state machine.

Usage:
  validate.py [--project DIR] [--root TOPICS_DIR] [--plan FILE] [--topic SUBSTR]

Guardrails, all read-only:

1. Format. Every topic folder has its TOPIC.md, error log and glossary with the
   columns the config declares, one Cause from the allowed set, a parseable
   date in each Re-test cell, and the required TOPIC.md State fields.
2. Ladder hygiene. A Re-test date already in the past with no result marker
   before it makes the row report as overdue forever, so it is a warning.
3. Unlocks. A topic may be active/passed/kept only when every prerequisite from
   the plan's graph table is passed or kept (a `lite` prerequisite needs only
   the configured minimum level).
4. Inflow. New error rows x the ladder length must stay under what the review
   cap can absorb; above that, the review slot eats the plan.

Prints ERROR lines (exit 1) and WARN lines (exit 0 if alone).
"""
import argparse
import datetime as dt
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "kit"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / ".claude" / "kit"))
import config as kcfg  # noqa: E402
import dates as kdates  # noqa: E402
import mdtable  # noqa: E402

DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
LEVEL = re.compile(r"\bL(\d+)\b")

problems = []


def say(kind, where, msg):
    problems.append((kind, f"{kind}: {where}: {msg}"))


def check_table(path, want):
    header = mdtable.header_of(path)
    if header is None:
        say("ERROR", path, "no table found")
        return
    if [h.lower() for h in header] != [w.lower() for w in want]:
        say("ERROR", f"{path}:1", f"columns are {header}, expected {want}")
    for n, c in mdtable.read_rows(path, header):
        if len(c) != len(want):
            say("ERROR", f"{path}:{n}", f"{len(c)} cells, expected {len(want)}")
            continue
        yield n, dict(zip(want, c))


def check_error_log(path, cfg, today, counter):
    causes = {c.lower() for c in cfg.get("grading.causes")}
    markers = cfg.get("review.markers")
    window = int(cfg.get("review.weekly_window_days"))
    for n, row in check_table(path, cfg.table("error_log")):
        if not DATE.fullmatch(row["Date"]):
            say("ERROR", f"{path}:{n}", f"Date {row['Date']!r} is not YYYY-MM-DD")
        elif (today - dt.date.fromisoformat(row["Date"])).days <= window:
            counter.append(row["Date"])
        if row["Cause"].lower() not in causes:
            say("ERROR", f"{path}:{n}", f"Cause {row['Cause']!r} not in {cfg.get('grading.causes')}")
        found = DATE.findall(row["Re-test"])
        if not found:
            say("ERROR", f"{path}:{n}", "Re-test cell has no date")
        for d in found:
            try:
                dt.date.fromisoformat(d)
            except ValueError:
                say("ERROR", f"{path}:{n}", f"Re-test date {d} is not a real date")
        stale = kdates.unmarked_past(row["Re-test"], markers, today)
        if len(stale) > 1 or (stale and stale[0] < today - dt.timedelta(days=window)):
            say("WARN", f"{path}:{n}",
                f"Re-test has {len(stale)} past date(s) with no result marker ({stale[0]}); "
                f"mark the date you reviewed on or the row reports overdue forever")


def check_glossary(path, cfg):
    for n, row in check_table(path, cfg.table("glossary")):
        if not row[cfg.table("glossary")[0]]:
            say("ERROR", f"{path}:{n}", "empty Term")


def check_patterns(path, cfg):
    cols = cfg.table("patterns")
    for n, row in check_table(path, cols):
        if not row[cols[0]] or not row[cols[1]]:
            say("ERROR", f"{path}:{n}", "a pattern row needs both a trigger and a move")


def read_topic_fields(path):
    """Field/Value pairs of the first 2-column table under '## State'."""
    out = {}
    in_state = False
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("## "):
                if in_state:
                    break
                in_state = line.strip().lower() == "## state"
                continue
            if in_state and line.lstrip().startswith("|"):
                c = mdtable.split_row(line)
                if len(c) == 2 and c[0].lower() not in ("field", "") and not mdtable.is_divider(c):
                    out[c[0].lower()] = c[1]
    return out


def parse_plan(plan, cfg):
    """{topic: [(prereq, lite?), ...]} from the plan's graph table, by column name.

    Header-driven on purpose: the original keyed on fixed cell positions, so
    inserting a column made it return nothing and silently skip the whole
    unlock check.
    """
    needs = {}
    header = None
    with open(plan, encoding="utf-8") as f:
        for line in f:
            if not line.lstrip().startswith("|"):
                continue
            c = mdtable.split_row(line)
            if mdtable.is_divider(c):
                continue
            low = [x.lower() for x in c]
            if "topic" in low and "needs" in low:
                header = c
                continue
            if not header or len(c) != len(header):
                continue
            name = re.sub(r"^\[([^\]]+)\].*", r"\1", mdtable.cell(header, c, "Topic")).strip()
            if not name:
                continue
            raw = mdtable.cell(header, c, "Needs").strip()
            if raw in ("-", ""):
                needs[name] = []
                continue
            items = []
            for part in raw.split(","):
                part = part.strip()
                items.append((re.sub(r"\(.*\)", "", part).strip(), "lite" in part))
            needs[name] = items
    return needs


def main():
    ap = argparse.ArgumentParser()
    kcfg.add_args(ap)
    ap.add_argument("--plan", default=None)
    ap.add_argument("--topic", default="")
    a = ap.parse_args()

    cfg, topics_dir = kcfg.from_args(a)
    plan = pathlib.Path(a.plan) if a.plan else cfg.path("paths.plan_file")
    states_order = list(cfg.get("graph.states"))
    done = set(cfg.get("graph.done_states"))
    started = done | {"active"}
    lite_min = int(cfg.get("graph.lite_min_level"))
    prefix = cfg.skip_prefix()
    fnames = cfg.get("layout.files")
    today = dt.date.today()
    recent_rows = []

    needs = parse_plan(plan, cfg) if plan.exists() else {}
    if not needs:
        say("WARN", str(plan), "no topic table parsed, skipping the unlock check")

    states, levels, found = {}, {}, []
    for topic_md in sorted(pathlib.Path(topics_dir).glob(f"**/{fnames['topic']}")):
        if any(p.startswith(prefix) for p in topic_md.parts):
            continue
        folder = topic_md.parent
        name = folder.name
        if a.topic and a.topic not in name:
            continue
        found.append(name)

        for key, check in (("error_log", lambda p: check_error_log(p, cfg, today, recent_rows)),
                           ("glossary", lambda p: check_glossary(p, cfg))):
            p = folder / fnames[key]
            if p.exists():
                check(p)
            else:
                say("ERROR", str(folder), f"missing {fnames[key]}")
        p = folder / fnames["patterns"]
        if p.exists():
            check_patterns(p, cfg)

        f = read_topic_fields(topic_md)
        tf = cfg.get("layout.topic_fields")
        for key, label in tf.items():
            if label.lower() not in f:
                say("ERROR", str(topic_md), f"State table has no '{label}' field")
        raw = f.get(tf["state"].lower(), "")
        state = next((s for s in states_order if s in raw.split("(")[0]), None)
        if state is None:
            say("ERROR", str(topic_md), f"State {raw!r} names none of {states_order}")
        states[name] = state
        m = LEVEL.search(f.get(tf["level"].lower(), ""))
        levels[name] = int(m.group(1)) if m else 0

        if cfg.get("layout.group_dirs"):
            want_group = folder.parent.name
            if f.get("group", "") != want_group:
                say("ERROR", str(topic_md), f"Group {f.get('group')!r} but folder says {want_group}")
        if name in needs:
            listed = ", ".join(n for n, _ in needs[name]) or "-"
            got = re.sub(r"\s*\(.*?\)", "", f.get(tf["needs"].lower(), "")).strip()
            if got != listed:
                say("ERROR", str(topic_md), f"Needs {got!r} but {plan.name} says {listed!r}")
        elif needs:
            say("WARN", str(topic_md), f"{name} is not in the {plan.name} graph table")

    for name in found:
        if states.get(name) not in started:
            continue
        for prereq, lite in needs.get(name, []):
            if prereq not in states:
                say("WARN", name, f"prerequisite {prereq} has no {fnames['topic']} here")
            elif lite:
                if levels.get(prereq, 0) < lite_min and states.get(prereq) not in done:
                    say("ERROR", name, f"{name} is {states[name]} but lite prerequisite {prereq} is below L{lite_min}")
            elif states.get(prereq) not in done:
                say("ERROR", name, f"{name} is {states[name]} but prerequisite {prereq} is {states[prereq]}")

    ladder = len(cfg.get("review.ladder_days"))
    cap = int(cfg.get("review.cap_per_run"))
    window = int(cfg.get("review.weekly_window_days"))
    inflow = len(recent_rows) * ladder
    throughput = cap * window
    if inflow > throughput:
        say("WARN", "inflow", f"{len(recent_rows)} new rows in {window}d x {ladder} rungs = {inflow} future "
                              f"reviews against a throughput of {throughput}: merge rows by pattern or lower the cap")

    for _kind, line in problems:
        print(line)
    errors = sum(1 for k, _ in problems if k == "ERROR")
    warns = len(problems) - errors
    print(f"\n{len(found)} topics checked: {errors} errors, {warns} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
