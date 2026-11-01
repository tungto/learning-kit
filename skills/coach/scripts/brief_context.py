#!/usr/bin/env python3
"""Print the whole context one coach mode needs, in a single tool call.

Usage:
  brief_context.py [today|status|weekly|topic <name>] [--project DIR] [--root TOPICS_DIR]

Replaces reading the status file and the plan whole plus three separate script
runs. Every path, week number and section heading comes from the project
config, so nothing here is specific to one plan.
"""
import argparse
import datetime
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "kit"))
import config as kcfg  # noqa: E402
import dates as kdates  # noqa: E402


def section(text, start_re, stop_re):
    out, on = [], False
    for ln in text.splitlines():
        if re.match(start_re, ln):
            on = True
        elif on and re.match(stop_re, ln):
            break
        if on:
            out.append(ln)
    return "\n".join(out).strip()


def row_weeks(line):
    """'| 1-2 | ...' -> {1, 2}; a non-week row returns None."""
    cell = line.strip("| ").split("|")[0].strip()
    m = re.fullmatch(r"(\d+)(?:\s*-\s*(\d+))?", cell)
    if not m:
        return None
    a, b = int(m.group(1)), int(m.group(2) or m.group(1))
    return set(range(a, b + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="today",
                    choices=["today", "status", "weekly", "topic"])
    ap.add_argument("name", nargs="?", default="")
    kcfg.add_args(ap)
    a = ap.parse_args()

    cfg, topics_dir = kcfg.from_args(a)
    mode = a.mode
    root = cfg.root
    skills = root / str(cfg.get("paths.skills_dir"))
    if not (skills / "active-revise").exists():  # running straight out of the kit repo
        skills = pathlib.Path(__file__).resolve().parents[2]

    def read(rel):
        f = root / str(rel)
        return f.read_text(encoding="utf-8") if f.exists() else ""

    def run(cmd):
        try:
            r = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=120)
            return (r.stdout + r.stderr).strip()
        except Exception as e:  # script missing or broken: say so, never guess
            return f"[{pathlib.Path(cmd[1]).name} failed: {e}]"

    today = datetime.date.today()
    week = kdates.week_of(today, cfg.get("plan.start_date"))
    print(f"## date\n{today} {today.strftime('%A')} · W{week}\n")

    if mode == "topic":
        hits = sorted(pathlib.Path(topics_dir).glob(f"**/{a.name}/{cfg.file_name('topic')}")) or \
               sorted(pathlib.Path(topics_dir).glob(f"**/*{a.name}*/{cfg.file_name('topic')}"))
        if not hits:
            sys.exit(f"no topic matching {a.name!r} under {topics_dir}")
        for t in hits:
            print(f"## {t.relative_to(root)}\n{t.read_text(encoding='utf-8').strip()}\n")
            log = t.parent / cfg.file_name("error_log")
            if log.exists():
                print(f"## {log.relative_to(root)}\n{log.read_text(encoding='utf-8').strip()}")
        return 0

    status_name = str(cfg.get("paths.status_file"))
    status = read(status_name)
    keep = cfg.get(f"coach.status_sections.{mode}")
    print(f"## {status_name}")
    for h in keep:
        s = section(status, re.escape(h), r"^## ")
        if s:
            print(s + "\n")

    plan_name = str(cfg.get("paths.plan_file"))
    plan = read(plan_name)
    phases = cfg.get("plan.phases")
    phase = kdates.phase_of(week, phases) or (phases[0] if phases else None)
    want = {week} | ({week + 1, week + 2} if mode == "weekly" else set())
    phases_label = "\u00a7" + str(cfg.get("plan.sections.phases")).lstrip("# ").rstrip(".")
    if phase:
        rows = []
        for ln in section(plan, re.escape(phase.get("heading", "")), r"^###|^## ").splitlines():
            w = row_weeks(ln)
            if w is None or w & want:
                rows.append(ln)
        print(f"## {plan_name} {phases_label} ({phase.get('name', '')}, this week's rows)\n"
              + "\n".join(rows).strip() + "\n")
    if mode == "weekly":
        cp = cfg.get("plan.sections.checkpoints")
        cp_label = "\u00a7" + str(cp).lstrip("# ").rstrip(".")
        print(f"## {plan_name} {cp_label}\n" + section(plan, rf"^{re.escape(cp)}", r"^## ") + "\n")

    print("## status_derive.py\n" + run([sys.executable, str(skills / "coach/scripts/status_derive.py"),
                                        "--project", str(root), "--root", str(topics_dir)]) + "\n")

    days = int(cfg.get("review.weekly_window_days")) if mode == "weekly" \
        else int(cfg.get("review.error_window_days"))
    errs = run([sys.executable, str(skills / "error-diagnose/scripts/collect_errors.py"),
                "--project", str(root), "--root", str(topics_dir), "--days", str(days)])
    due = run([sys.executable, str(skills / "active-revise/scripts/due_reviews.py"),
               "--project", str(root), "--root", str(topics_dir)])
    # due rows always come as headlines: active-revise loads the full rows itself
    due = "\n".join(l for l in due.splitlines() if not l.startswith("  "))
    if mode != "weekly":
        errs = errs.split("\n## ")[0]  # counts only; error-diagnose loads the rows
    print(f"## errors (last {days}d)\n{errs}\n")
    print("## due reviews (headlines; run due_reviews.py for the rows)\n" + due)
    if mode == "weekly":
        val = root / str(cfg.get("paths.validate_script"))
        if not val.exists():
            val = pathlib.Path(__file__).resolve().parents[3] / "scripts" / "validate.py"
        print("\n## validate.py\n" + run([sys.executable, str(val), "--project", str(root)]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
