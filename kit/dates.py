#!/usr/bin/env python3
"""Week math, the review ladder, and result-marker parsing.

split_retest() is lifted verbatim (logic and rationale) from interview-v2's
due_reviews.py:split_cell. It is load-bearing: without it a row that was
reviewed but not passed keeps its old dates and reports as overdue forever.
"""
import datetime as dt
import re

DATE_RE = r"\d{4}-\d{2}-\d{2}"


def marker_re(markers):
    """Regex matching an optional result marker in front of a date."""
    alts = "|".join(re.escape(m) for m in markers if m)
    return re.compile(rf"({alts})?\s*({DATE_RE})")


def split_retest(cell, markers):
    """Return (pending, passed) dates from a Re-test cell.

    A date carrying a result marker (pass / shaky / fail) was reviewed on that
    day. Everything at or before the last reviewed date is history, so only the
    dates after it are still scheduled.
    """
    pass_marker = markers.get("pass", "✓")
    rx = marker_re([markers.get("pass"), markers.get("shaky"), markers.get("fail")])
    found = list(rx.finditer(cell))
    last_done = -1
    for i, m in enumerate(found):
        if m.group(1):
            last_done = i
    pending = [dt.date.fromisoformat(m.group(2)) for m in found[last_done + 1:]]
    passed = [dt.date.fromisoformat(m.group(2)) for m in found if m.group(1) == pass_marker]
    return pending, passed


def unmarked_past(cell, markers, today):
    """Dates already in the past that carry no marker and no marker after them.

    These are the rows that report overdue forever. validate.py warns on them.
    """
    pending, _ = split_retest(cell, markers)
    return [d for d in pending if d < today]


def week_of(today, start_date):
    """1-based week number of a plan that started on start_date (a Monday).

    Returns 0 before the plan starts, so a project can be seeded the weekend
    before W1 without the brief claiming week 1 has begun.
    """
    if not start_date:
        return 0
    start = dt.date.fromisoformat(str(start_date)) if not isinstance(start_date, dt.date) else start_date
    if today < start:
        return 0
    return (today - start).days // 7 + 1


def phase_of(week, phases):
    for p in phases:
        if int(p.get("first_week", 0)) <= week <= int(p.get("last_week", 0)):
            return p
    return None


def rung_index(cell, markers, ladder):
    """How many rungs of the ladder this row has already passed."""
    _, passed = split_retest(cell, markers)
    return len(passed)


def next_rung(cell, markers, ladder, today, result="pass", shaky_days=3, fail_days=1):
    """The updated Re-test cell after a review today.

    pass  -> mark today with the pass marker, append today + the next ladder gap
    shaky -> mark today 'shaky', append today + shaky_days
    fail  -> mark today 'fail', append today + fail_days
    Returns (new_cell, label) where label is like '+7d' or 'retired'.
    """
    pending, passed = split_retest(cell, markers)
    marker = markers.get(result if result in ("shaky", "fail") else "pass")
    base = cell.rstrip().rstrip(",")
    stamped = re.sub(rf"(?<![\w✓]){re.escape(today.isoformat())}", f"{marker}{today.isoformat()}", base, count=1)
    if stamped == base:
        stamped = f"{base}, {marker}{today.isoformat()}" if base else f"{marker}{today.isoformat()}"
    if result == "pass":
        n = len(passed) + 1
        if n >= len(ladder):
            return stamped, "retired"
        gap = ladder[n]
    elif result == "shaky":
        gap = shaky_days
    else:
        gap = fail_days
    nxt = today + dt.timedelta(days=gap)
    return f"{stamped}, +{gap}d {nxt.isoformat()}", f"+{gap}d"


def first_rung(today, ladder):
    """The Re-test cell a brand-new row starts with: today+rung0, then rung1 noted."""
    d0 = today + dt.timedelta(days=ladder[0])
    d1 = today + dt.timedelta(days=ladder[1]) if len(ladder) > 1 else None
    cell = d0.isoformat()
    if d1:
        cell += f", +{ladder[1]}d {d1.isoformat()}"
    return cell
