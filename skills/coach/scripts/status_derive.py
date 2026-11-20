#!/usr/bin/env python3
"""Derive the mechanical half of the status file from the TOPIC.md files.

Usage:
  status_derive.py [--project DIR] [--root TOPICS_DIR] [--status FILE]

Each TOPIC.md State table is the source of truth for one topic. This script
reads them all and prints the facts the status file repeats: state, overall
level, hours spent and estimated, planned weeks, next action, plus the topic
counts line and the re-test backlog. Then it compares those facts against the
topic table in the status file and prints a DRIFT section for every cell that
disagrees.

Judgment cells (Pace, Verdict, Mode, this week's outcomes) are not derivable
and are left alone - `coach` still writes them. Read-only: nothing is written
to the status file.
"""
import argparse
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "kit"))
import config as kcfg  # noqa: E402
import mdtable  # noqa: E402


def fields(path):
    """Return the Field/Value pairs of the first table under '## State'."""
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


def state_of(raw, states):
    """'**active** (locked -> ready -> ...)' -> 'active'; 'locked (js)' -> 'locked'."""
    for word in re.findall(r"[a-z]+", raw.lower()):
        if word in states:
            return word
    return "?"


def hours(raw):
    """'~7 (est., W1-2)' -> '7'; '-' or '' -> '0'."""
    m = re.search(r"\d+(?:\.\d+)?", raw or "")
    return m.group(0) if m else "0"


def status_table(path, topics_rel):
    """Topic id -> (header, cells) of its row in the status file's topic table."""
    rows, header = {}, None
    if not path.exists():
        return rows, header
    link = re.compile(rf"\|\s*\[([^\]]+)\]\({re.escape(topics_rel)}/[^)]+\)\s*\|")
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.lstrip().startswith("|"):
                continue
            c = mdtable.split_row(line)
            if mdtable.is_divider(c):
                continue
            low = [x.lower() for x in c]
            if "topic" in low and "state" in low:
                header = c
                continue
            m = link.match(line)
            if m:
                rows[m.group(1)] = c
    return rows, header


def main():
    ap = argparse.ArgumentParser()
    kcfg.add_args(ap)
    ap.add_argument("--status", default=None)
    a = ap.parse_args()

    cfg, topics_dir = kcfg.from_args(a)
    status_path = pathlib.Path(a.status) if a.status else cfg.path("paths.status_file")
    states = list(cfg.get("graph.states"))
    tf = cfg.get("layout.topic_fields")
    prefix = cfg.skip_prefix()
    topic_file = cfg.file_name("topic")
    topics_rel = str(cfg.get("paths.topics_dir"))

    topics = {}
    for path in sorted(pathlib.Path(topics_dir).glob(f"**/{topic_file}")):
        if any(p.startswith(prefix) for p in path.parts):
            continue
        name = path.parent.name
        f = fields(path)
        topics[name] = {
            "state": state_of(f.get(tf["state"].lower(), ""), states),
            "level": f.get(tf["level"].lower(), "-"),
            "spent": hours(f.get(tf["hours_spent"].lower(), "")),
            "est": hours(f.get(tf["est_hours"].lower(), "")),
            "weeks": f.get(tf["weeks"].lower(), "-"),
            "needs": f.get(tf["needs"].lower(), "-"),
            "next": f.get(tf["next_action"].lower(), "-"),
        }

    print(f"# Derived from {len(topics)} {topic_file} files under {topics_rel}/\n")
    print("| Topic | State | Level | Hours (spent/est) | Planned weeks | Needs |")
    print("|---|---|---|--:|---|---|")
    order = lambda kv: (states.index(kv[1]["state"]) if kv[1]["state"] in states else 9, kv[0])  # noqa: E731
    for name, t in sorted(topics.items(), key=order):
        print(f"| {name} | {t['state']} | {t['level']} | {t['spent']}/{t['est']} | {t['weeks']} | {t['needs']} |")

    counts = {s: sum(1 for t in topics.values() if t["state"] == s) for s in states}
    spent = sum(float(t["spent"]) for t in topics.values())
    est = sum(float(t["est"]) for t in topics.values())
    print("\nCounts " + "/".join(reversed(states)) + ": " +
          " / ".join(str(counts[s]) for s in reversed(states)))
    if est:
        print(f"Hours: {spent:g} spent / {est:g} estimated ({spent / est * 100:.0f}%)")

    print("\n## Next action per active topic")
    for name, t in sorted(topics.items()):
        if t["state"] == "active":
            print(f"- {name}: {t['next']}")

    # The re-test backlog belongs to the same picture, so reuse the one script
    # that knows how to read Re-test cells instead of parsing them again here.
    # Sibling skill first (plugin, kit repo or copied install), project skills_dir as fallback.
    due = pathlib.Path(__file__).resolve().parents[2] / "active-revise" / "scripts" / "due_reviews.py"
    if not due.exists():
        due = cfg.root / str(cfg.get("paths.skills_dir")) / "active-revise" / "scripts" / "due_reviews.py"
    if due.exists():
        print()
        sys.stdout.flush()  # keep the child's output in order with ours
        subprocess.run([sys.executable, str(due), "--project", str(cfg.root),
                        "--root", str(topics_dir), "--summary"], check=False)

    rows, header = status_table(status_path, topics_rel)
    print(f"\n## DRIFT vs {status_path.name}")
    drift = 0
    for name, t in sorted(topics.items()):
        row = rows.get(name)
        if not row:
            print(f"- {name}: missing from the {status_path.name} topic table")
            drift += 1
            continue
        if not header:
            continue
        checks = [("state", t["state"], state_of(mdtable.cell(header, row, "State"), states)),
                  ("level", t["level"].lower(), mdtable.cell(header, row, "Level").lower()),
                  ("hours", f"{t['spent']}/{t['est']}",
                   mdtable.cell(header, row, "Hours").replace("~", "").replace(" ", ""))]
        for label, mine, theirs in checks:
            if mine != theirs:
                print(f"- {name}: {label} is '{theirs}' in {status_path.name}, '{mine}' in {topic_file}")
                drift += 1
    for name in sorted(set(rows) - set(topics)):
        print(f"- {name}: in {status_path.name} but has no {topic_file} under {topics_rel}/")
        drift += 1
    if not drift:
        print(f"- none: {status_path.name} matches the {topic_file} files.")
    print(f"\n{drift} drifted cell(s). Fix {status_path.name}, or fix the {topic_file} "
          f"if the topic file is the stale one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
