# How to use the AI system

Guide for the human. What to type, when, and what the AI is allowed to touch.
Rules the AI follows: [../CLAUDE.md](../CLAUDE.md). Why those rules: [principles.md](principles.md).
Every number named here lives in `learning.config.json` ([CONFIG.md](CONFIG.md) documents it).

## 1. The two learning methods

There are two teaching skills. They are **not** alternatives. They fit different stages of knowing the same thing.

| | `/teach` | `/learn-session` |
|---|---|---|
| Use when | I know almost nothing about it | I have seen it before, even badly |
| Method | guided: cited sources, worked example, one small win | retrieval: I attempt first, AI reveals after |
| Difficulty | the enemy - it eats working memory | the tool - effort is what makes it stick |
| AI posture | explains, shows, scaffolds | withholds, quizzes, hunts the gap |
| Output | a lesson + a reference one-pager I keep | error rows, levels, re-test dates |
| Builds | knowledge | skill and retention |

Why both: a novice given hard retrieval just fails and learns nothing (principles 1.5b - below the band). Someone who already has the knowledge and is given an explanation feels smooth and remembers nothing (1.1). **Guidance first, then take the guidance away.** Picking the wrong one wastes the slot.

Rule of thumb: if I cannot write three true sentences about the thing, it is a `/teach` job. If I can, it is a `/learn-session` job.

## 2. The ladder per subtopic

Four stages. A subtopic walks down the ladder once, then lives in revise forever.

| Stage | Skill | Done when |
|---|---|---|
| 1 Knowledge | `/teach <subtopic>` | I can state what problem it solves and the main rule, from the lesson |
| 2 Skill | `/learn-session` | I passed cold: right on the substance, right English, confidence 3 |
| 3 Retention | `/active-revise` | it survives the ladder: +2d, +7d, +16d, +35d |
| 4 Perform | `/perform-drill` | it holds under time pressure and pushback |

Stage 1 is skipped when I already have the knowledge - most subtopics start at stage 2. Do not run stage 1 on something I half-know: that is re-reading, the most popular useless study method.

Logging is not a stage. `/session-log` closes **every** session, stage 1 included.

## 3. Skill map

| I want | I type | Skill does |
|---|---|---|
| What to do today | `/coach today` | Picks topic + block from the plan, asks my time budget, books min/target/stretch |
| First exposure to a new thing | `/teach <subtopic>` | Finds trusted sources, builds one cited lesson + a printable reference page |
| Learn / be quizzed | `/learn-session` | One active session, I answer first, on one `active` topic |
| Re-test due items | `/active-revise` | Quizzes error-log rows past their Re-test date, from memory, no notes |
| Wrap up | `/session-log` | Writes error-log, glossary, deep-dive, hours, next re-test dates |
| Weekly analysis | `/error-diagnose` | Finds repeated causes across topics, proposes drills |
| Pressure test | `/perform-drill` | Timed round, pushback on vague answers, scripted debrief |
| Report the day | `/coach done` or `/coach skipped` | Writes the status file (streak, daily log, next action) |
| Big picture | `/coach status` | Reads the status file, recomputes ETA and on-track flags |
| One topic | `/coach topic <name>` | That topic's state, levels, next step |
| Weekly review | `/coach weekly review` | Levels, state changes, unlocks, next week's outcomes (I choose them) |
| Change device | `/sync-progress save` / `resume` | `HANDOFF.md` + git push / pull |

## 4. Standard day

```
/coach today          -> get the block, say how many minutes I have
/active-revise        -> only if re-tests are due (the session banner says)
/teach <subtopic>     -> only if today's subtopic is new to me
/learn-session        -> the main block, every day
/session-log          -> before I close the laptop
/coach done           -> one line result
```

Order matters. Revise before new material: a due item not re-tested today is a loss, and clearing the backlog is cheap. `/teach` before `/learn-session`, never after - after is re-reading.

Skip `session-log` and the day is lost: no error rows, no re-test dates, no hours. The streak is not the point; the logs are.

Time is short, pick in this order: **revise > learn > teach**. Cutting `/teach` costs one day of progress. Cutting revise costs items I already paid for.

## 5. Standard week

The slots come from `coach.slot_map`. The shape:

| Day | Run |
|---|---|
| Weekdays | the standard day above |
| One weekend block | `/error-diagnose`, then drills on the worst cause |
| One weekend block | `/coach weekly review`, pick max `coach.weekly_outcome_cap` outcomes for next week |

The last day of a topic: `/perform-drill` instead of `/learn-session`.

## 6. Review load: the arithmetic I must respect

Every error row costs **five** future reviews (+2d, +7d, +16d, +35d, +90d: `review.ladder_days`). `active-revise` runs `review.cap_per_run` items a run (default **8**). So:

| New rows per session | Future reviews created | Sustainable? |
|--:|--:|---|
| 4 | 20 | yes |
| 10 | 50 | no - backlog grows every day |

Rules that keep it finite:

- `session-log` writes **~4-5 rows a session** (`review.rows_per_session`), one per *gap pattern*. Two misses from the same missing piece = one row. Surplus gaps fold into that row's Fix drill, so nothing is lost.
- `active-revise` triages when more is due than the cap: fail/shaky rows first, then most overdue, then low rungs. The rest stays due. **A backlog is pacing, not failure.**
- English patterns batch into one rewrite item, not one item per slip.
- A pass at **+16d or later** (`review.pattern_line_from_rung`) earns one line in `topics/<name>/patterns.md`: *trigger -> move*, my words. That sheet is what survives when rows retire, and it is what I actually reread before performing.
- `validate.py` checks this arithmetic: new rows x ladder length against the cap's weekly throughput, and it warns before the slot is eaten.

If the backlog still grows after three runs, the fix is **fewer rows in**, not more reviews out.

## 6b. Pace gate (what happens when I fall behind)

The plan needs `plan.weekly_hours` per week. Every weekly review, `coach` computes realized hours over the last `pace.lookback_weeks` weeks:

| Realized | What happens |
|---|---|
| ≥ `plan.weekly_hours × pace.gate_fraction` | nothing, it says the number and continues |
| below the gate, two reviews running | the **next tier** of `pace.drop_ladder` fires, automatically, no discussion |
| back at plan for two reviews | the newest tier un-fires |

`pace.never_dropped` survives every tier. Firing a tier is a re-plan, not a failure, and it creates no catch-up debt. The point of writing the ladder down in advance is that the decision is not made while tired and behind.

## 7. Where `teach` output goes

`/teach` builds a workspace inside the topic folder: `teach.workspace_root` (default `topics/<name>`), and `teach.allow` lists what it may create there - typically `MISSION.md`, `RESOURCES.md`, `NOTES.md`, `lessons/`, `reference/`, `drills/`, `assets/`, `learning-records/`.

Writing the lesson file itself is `/create-lesson`'s job - same workspace, same `teach.allow` bounds - so `/teach` decides what to teach and hands the authoring over. Every page it writes follows one house style - `skills/create-lesson/references/style-guide.md`, with a shared `lesson.css`/`lesson.js` copied into the topic's `assets/` and two skeletons (short lesson; rail-and-parts reference page for reports and tutorials).

It never writes the plan, the status file or a `TOPIC.md` cell, and a lesson is never evidence for a level change. New files get listed under **Sources** in `TOPIC.md`.

If this project wants `teach` output to land somewhere else, or wants some of those files suppressed (because the error log and deep-dive already do that job), narrow `teach.allow` - do not argue with the skill each time.

## 8. Who writes what

| File | Only writer |
|---|---|
| the status file, `State` in `TOPIC.md` | `coach` |
| `TOPIC.md` hours, subtopic levels, next action | `session-log` |
| `error-log.md`, `glossary.md` | `session-log`, `active-revise` (via `append_row.py`) |
| `topics/*/patterns.md` | `active-revise` (one line when a row passes the pattern rung) |
| `MISSION.md`, `RESOURCES.md`, `NOTES.md`, `learning-records/` | `teach` |
| `lessons/`, `assets/`, `reference/`, the folder `index.html` files | `create-lesson` (called by `teach`, or directly) |
| the plan, `ABOUT-ME.md` | the AI, only when I ask |

If the AI writes a file outside this table, it broke the rules. Tell it to revert.

## 9. What I check in AI output

- **Facts that age.** Anything version- or date-sensitive needs a web search, not memory.
- **Citations in `teach` lessons.** A lesson claim with no link is the AI's memory, not knowledge. Ask for the source.
- **Own ideas marked.** The AI's own opinions carry `[my suggestion]`. Unmarked = should be sourced.
- **Level changes.** A subtopic level rises only on independent evidence (I answered it cold in `learn-session` or `active-revise`), never from a `teach` lesson. Reading a good lesson is zero evidence.
- **No new systems.** New topics, folders or trackers only if I asked. Say no to scope creep.

## 10. Prompting this system

Good: `/learn-session <topic> <subtopic>, 40 minutes, I keep failing <the specific thing>`.
Bad: `teach me <topic>`. The skill then guesses the topic, the time and the gap.

Give three things: **topic, minutes, my current pain**. Everything else the skills read from the project.

When an answer feels too easy, ask for the deeper layer: trade-offs, failure modes, behaviour at the edges.

## 11. English

`esl.enabled` is on by default and `esl.level` says where I am. If a sentence is unclear, say "simpler" - that is data, not weakness. A miss caused by wording is logged with cause `English`, not `concept`, and it gets a different fix drill.

## 12. When it goes wrong

| Symptom | Fix |
|---|---|
| AI explains before I attempt in `learn-session` | Stop it. "I attempt first." Restart the question |
| `teach` lesson feels obvious | Wrong stage. It is a `/learn-session` subtopic, not a `/teach` one |
| `learn-session` keeps failing me at 0-2 of 5 | Wrong stage the other way. Drop to `/teach` for that one subtopic, then retry cold |
| `teach` writes outside its workspace | Stop it, point at §7 and `teach.allow` |
| Wrong topic picked | `/coach topic <name>` to see state; only `active` topics may be studied |
| Re-tests pile up | Normal: triage runs (§6). Growing after 3 runs = cut rows in, not reviews out |
| The status file looks stale | `/coach status` recomputes; it is written at review time, not live |
| A row reports overdue forever | Its Re-test cell has an unmarked past date. `validate.py` names it; add the `✓`/`shaky`/`fail` marker |
