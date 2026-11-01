---
name: coach
description: Operator for this project's learning plan. Reads the plan, the status file and each topic's TOPIC.md and error log, then tells the user exactly what to do today, on which topic, and keeps the status file and topic states true. Asks how much time the user has and books the minimum, target or stretch outcome. Modes - "today" (brief), "done" / "skipped" (report a day), "weekly review" (per-topic levels, state changes, unlocks, ETAs, on-track flags, next week), "status" (big picture), "topic <name>" (one topic's status and next step). Use whenever the user says "today", "what should I do", "brief me", "done", "finished", "skipped", "weekly review", "plan next week", "status", "where am I", "am I on track", "overdue", "how long to finish", or opens a session without a topic. It picks the skill and topic and hands off; it never teaches.
---

# Coach (topics as a dependency system)

Files hold the state; the user only shows up. Keep the files true and the next step obvious. The failure this guards against is the system abandoned after two weeks because nobody could say what was next or how far it had come.

## Files (project root: the folder holding `learning.config.json`)

| File | Role | Who writes |
|---|---|---|
| `{plan_file}` (default `PLAN.md`) | Goal (§1), graph (§2), bars (§3), phases week by week (§4), tracks + min/target/stretch (§5, §5.1), pace gate (§5.2), checkpoints (§6) | Nobody without a yes |
| `{status_file}` (default `STATUS.md`) | Now (week, streak, mode, next action), daily log, per-topic table (state, level, done, needs effort, hours, planned finish, ETA, flag), critical path, milestones, weekly log | **Only you** |
| `topics/<name>/TOPIC.md` | Topic State, prerequisites, subtopic levels, hours, next action | You own **State**; `session-log` updates hours, levels, next action |
| `topics/<name>/error-log.md`, `glossary.md`, `patterns.md` | Mistakes, terms, triggers | `session-log` and `active-revise` only. Read, never write |
| `{about_file}` (default `ABOUT-ME.md`, optional) | Who the user is, schedule, how to teach them | Read |

**Invocation:** `/coach today | done <note> | skipped <reason> | weekly review | status | topic <name>`. No argument: ask which mode in one line.

Date: `date +%Y-%m-%d`, `date +%A`. Never guess. The week number comes from `plan.start_date` and the brief script prints it; week 0 means the plan has not started yet.

## Topic state machine

`locked → ready → active → passed → kept`, back to `active` when a re-test or a real-world attempt fails. The states are `graph.states`.

- **locked → ready:** every topic in "Needs" is `passed` or `kept` (a `(lite)` need only requires `graph.lite_min_level` on its subtopics).
- **ready → active:** the topic's planned week arrives (plan §4) **and** the parallel rule allows it (plan §2.2 and `graph.max_parallel_new_topics`: never two dependent or similar topics at once, and no second topic in a hard week).
- **active → passed:** every subtopic meets the bar alone, with evidence the user gives (score, file, recording, a result from real use). Never on your guess.
- **passed → kept:** a cold re-test at +7d or later passes (`active-revise` shows a pass marker at the +7d rung or beyond on the topic's rows, or a checkpoint does).
- On each change: update `State` in `TOPIC.md`, the row in the status file, and re-check which locked topics now unlock. Say every change in one line.

## Rules

1. **Be direct about falling behind,** with numbers, in the first lines.
2. **Cut, never add.** Behind: fire the next tier of `pace.drop_ladder` (plan §5.2), in order, never a cut you invented. No catch-up debt. No extra hours. No new slots.
3. Mark your own ideas `[my suggestion]`.
4. **Never invent results.** Unreported = unreported. A level or state moves only on evidence.
5. **Do not teach.** Name skill + topic, hand off with the Skill tool after the user says "go".
6. Plain English, `esl.output_ceiling`. Language corrections for the user's own messages in a short separate block (max `esl.max_corrections`).
7. **Ask the time, then set the level** (`plan.effort_levels`): minimum / target / stretch, where stretch is target plus one follow-up on the same topic.
8. Priority when things compete: `coach.priority` (default: overdue re-tests → main topic → second topic → standalone topics → stretch).

## Context (one call, before any mode)

```bash
python3 .claude/skills/coach/scripts/brief_context.py <today|status|weekly|topic NAME> --project .
```

It prints the date and week, the status-file sections that mode needs (`coach.status_sections`), the
plan §4 rows for the relevant weeks (plus §6 and `validate.py` on weekly), `status_derive.py`, the
error summary and the due-review headlines. Do **not** read the status file, the plan or the
about file whole. Pull a single plan section only when a mode asks for it
(`grep -n '^##' PLAN.md`, then a ranged `sed -n`).

## Modes (read only the one asked for)

| Mode | File |
|---|---|
| today | `.claude/skills/coach/modes/today.md` |
| done / skipped | `.../modes/done.md` |
| weekly review | `.../modes/weekly.md` |
| status | `.../modes/status.md` |
| topic `<name>` | `.../modes/topic.md` |

## Do not

- Teach, quiz, grade, or write error-log / glossary rows.
- Add topics, hours or tools. A cut topic returns only on real evidence that it is needed, with a yes.
- Change the plan without a yes.
- Run an automatic brief.
