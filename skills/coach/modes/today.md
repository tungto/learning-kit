## Mode: today

1. Run one call:
   ```bash
   python3 .claude/skills/coach/scripts/brief_context.py today --project .
   ```
   It prints the date and week, the status-file sections (Now, this week, daily log, topics),
   the plan §4 rows for this week, `status_derive.py`, the error counts for the last
   `review.error_window_days` and the due-review headlines. Read no other file. Full error rows or
   due rows: only if you need one, run `collect_errors.py --project .` or `due_reviews.py --project .`.

   `status_derive.py` reads every `TOPIC.md` and prints the facts the status file
   repeats - state, level, hours, next action, re-test backlog - then a DRIFT
   section for each cell where the two disagree. Trust the script over
   the status file for those cells, and fix the drift before briefing. Pace,
   Verdict, Mode and this week's outcomes are judgment: they stay yours.
2. Today's topics = the `active` topics, placed in the slots from `coach.slot_map` (which slot, which days, how many minutes, what it is for). A topic with no slot today does not get invented time.
3. Read the chosen topic's `TOPIC.md`: the first subtopic below its bar = today's focus.
4. Yesterday missing in the daily log: say "yesterday is unreported", ask done or skipped.
5. Brief, one screen (~20 lines):

```
W{n} · {weekday} {date} · {phase.name}
Streak {x} · this week {done}/{plan.weekly_block_bar} · mode {normal|cut-scope}
Yesterday: {done/minimum/skipped/unreported}
Active topics: {list} — {flags}
Needs work: {1-2 items from error logs, topic + count}

TODAY
 {slot}  {minutes} → `learn-session`: "start session: topic {name}, subtopic {x}, {role}"
 {slot}  → {from coach.slot_map}
 Revise  → {n} due, {m} overdue → `active-revise` (first if ≥3 overdue)
 After   → `session-log` (topic {name})
Level → {minimum|target|stretch}; minimum = {observable result}
Unlock watch: {topic} unlocks when {need} passes ({what's left})
Next up: {tomorrow}
```
