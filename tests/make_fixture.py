#!/usr/bin/env python3
"""(Re)build tests/fixture-project with dates relative to today.

The fixture has to exercise due / soon / cold / stale-marker paths, and all of
those are relative to the day the tests run, so the dates are stamped here
instead of being frozen in the files.
"""
import datetime as dt
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FX = HERE / "fixture-project"
TODAY = dt.date.today()
MONDAY = TODAY - dt.timedelta(days=TODAY.weekday())


def d(n):
    return (TODAY + dt.timedelta(days=n)).isoformat()


def write(rel, text):
    p = FX / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


cfg = {
    "kit_version": "0.1.0",
    "project": {"name": "fixture", "title": "Kit test fixture (2 topics)"},
    "plan": {
        "start_date": MONDAY.isoformat(),
        "total_weeks": 4,
        "weekly_hours": 2.0,
        "weekly_block_bar": 3,
        "horizon_label": "fixture only",
        "phases": [
            {"name": "Phase 1", "heading": "### Phase 1: W1-2 — alpha", "first_week": 1, "last_week": 2},
            {"name": "Phase 2", "heading": "### Phase 2: W3-4 — beta", "first_week": 3, "last_week": 4},
        ],
    },
    "pace": {"drop_ladder": [{"tier": 1, "drops": "beta becomes a reading list", "saves_hours": 1}],
             "never_dropped": ["alpha"]},
    "coach": {"slot_map": [{"slot": "morning", "days": "Mon-Fri", "minutes": 30, "use": "main topic"}]},
}
write("learning.config.json", json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")

write("topics/alpha/error-log.md", f"""# alpha error log

Cause = concept, careless or English. Re-test ladder: +2d, +7d, +16d, +35d, +90d.

| Date | Question | My answer | Correct | Cause | Fix drill | Re-test |
|---|---|---|---|---|---|---|
| {d(-6)} | what does alpha do first? | nothing | it narrows the choice | concept | implement alpha from scratch | ✓{d(-4)}, +7d {d(0)} |
| {d(-5)} | say the alpha rule aloud | drops "is" in passives | the rule is applied first | English | explain alpha aloud in 2 min | {d(-1)} |
| {d(-3)} | when is alpha wrong? | always | when the input is already sorted | concept | 5 snippets, predict the output | ✓{d(-1)} |

## Parking lot

- a bullet below the table that must survive every append
""")

write("topics/beta/error-log.md", f"""# beta error log

| Date | Question | My answer | Correct | Cause | Fix drill | Re-test |
|---|---|---|---|---|---|---|
| {d(-2)} | beta trigger? | when I feel like it | when X happens, do Y | careless | write 3 triggers | {d(2)} |
""")

write("topics/alpha/patterns.md", f"""# alpha patterns

| Trigger (when I see...) | Move (...I do) | From row |
|---|---|---|
| an already sorted input | say alpha is a no-op here | {d(-3)} |
""")

write("STATUS.md", f"""# Fixture status

**As of:** {d(0)} · **Week:** W{(TODAY - MONDAY).days // 7 + 1}

## This week (max 3 outcomes)
1. alpha subtopic 1 to L2

## Now

| Field | Value |
|---|---|
| Today | {d(0)} |
| Streak | 1 day |
| Blocks this week | 1 of 3 |
| Mode | normal |
| Next action | `/learn-session alpha` |

## Daily log (last 10)

| Date | Topic | Minutes | Outcome |
|---|---|---|---|
| {d(-1)} | alpha | 40 | subtopic 1 predicted 7/10 |

## Overall

| Field | Value |
|---|---|
| Week | W1 of 4 |
| Hours | 1.0 of 3 |
| Pace | on track |
| Next checkpoint | CP1 (W2) |

## Topics

| Topic | State | Level | Done | Needs | Hours | Planned finish | ETA | Flag |
|---|---|---|---|---|---|---|---|---|
| [alpha](topics/alpha/TOPIC.md) | active | L2 | 1/2 | - | 1.0/2 | W2 | W2 | ✅ |
| [beta](topics/beta/TOPIC.md) | locked | - | 0/2 | alpha | 0/1 | W4 | W4 | ⏳ |

## Critical path

alpha -> beta

## Milestones

| Milestone | Week | Status |
|---|---|---|
| CP1 | 2 | due |

## Weekly log

| Week | Hours | Outcomes |
|---|---|---|
""")
print(f"fixture rebuilt for {TODAY} (W1 Monday {MONDAY})")
