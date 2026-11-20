---
name: active-revise
description: Spaced active revision of what the user already learned. Finds error-log rows whose Re-test date is due, quizzes them from memory (no notes), mixes in interleaved cold questions from older topics, and reschedules each item by pass or fail along the configured ladder (+2d, +7d, +16d, +35d, +90d by default). Use whenever the user says "revise", "review", "what is due", "spaced repetition", "re-test", "warm-up", "recall what I learned", "test me on old stuff", or when `coach` reports overdue re-tests, even if they do not say spaced. Not for learning a new topic (`learn-session`), timed performance rounds (`perform-drill`) or logging new mistakes (`session-log`).
---

# Active revise (Reviser)

Goal: make old knowledge stick by forcing recall at growing gaps. The user answers first, always. Same rule as `learn-session`: no answer or hint before an honest attempt.

Config: `review.*` in `learning.config.json` holds the ladder, the caps and the markers. The numbers quoted below are the defaults.

## Learning style (user's own rules)

Follow `paths.style_file` from `learning.config.json` (default `LEARNING-STYLE.md`, project root; skip silently if absent). Here: on a fail, give a hint before the answer and let the user try once more; when an item fails again, re-explain with a different example or angle than last time (check the row's Fix drill). Feedback says what is right, what is wrong, why, how to improve. No empty praise. A memorized definition is not a pass: ask the user to apply or explain it.

## Steps

1. **Find what is due.** Run:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/due_reviews.py --project .
```

   It lists rows with a pending Re-test date ≤ today (oldest first), rows due within `review.ahead_days`, and a COLD pool (rows already passed once, oldest last pass first). Each row has a `type` hint: `recall`, `skill` or `speak`. The "Correct" line is for you, never show it before the attempt. If nothing is due, say so, then go to step 3 only.
2. **Quiz due items.** One question per message, `review.cap_per_run` items max per run (default 8; oldest first, substance rows before English rows).

   **When more is due than the cap (triage, in this order):**
   1. Rows already marked `fail` or `shaky` on their last review - a broken item left waiting decays further.
   2. Rows latest by days overdue (oldest-late first).
   3. Rows at the low rungs (+2d, +7d), because they are the least secure.
   4. Everything else; leave it due, tomorrow's run takes it.

   **Batch the English rows.** Several language patterns due in one run become **one** item: the user rewrites one short answer that has to fix all of them, and each row is graded from that rewrite. English rows count as one item against the cap, not several.

   Say the split in one line at the start ("8 today, 12 stay due") so a backlog reads as pacing, not failure. If the backlog is still growing after three runs, the problem is inflow, not throughput: tell the user to tighten the `session-log` row cap, and flag it for `error-diagnose`. No notes, no peeking at the log. Free recall only: never multiple choice or yes/no, which test recognition, not memory. Match the review to the type:
   - `recall`: ask the Question again in new words, or give a fresh case on the same idea. Do not repeat the original wording.
   - `skill` (build, compute, apply): the user rebuilds from blank or works a fresh instance. Judge the process, never do it for them.
   - `speak`: the user answers aloud or in a 2-min written script, no notes. Use the `learn-session` Listener rules.
   - **Confidence first:** before each answer ask "confidence 1-3?" (1 guess, 3 sure). Confidence is part of the grade, not a comment. Confident but wrong (3 then fail) is the most valuable catch: name it in the close, and explain that these stick best once fixed.
   - **Pass** = `grading.pass_bar`: right idea, in the user's own words, with the key term, **said in correct English**, at **confidence 3**. Substance and English are one bar, not two: an answer a listener could not follow is not a pass, however right the idea. **Shaky** = `grading.shaky_bar`: any one of those missing - wrong or missing term, English that would make a listener stumble, or confidence 1-2 even when the answer is right. **Fail** = wrong or blank after one best-guess nudge.
   - **Gap hunt - run it on every shaky and every fail, never skip it.** Giving the correct answer is not the end of the item. Ask 1-3 narrow follow-up questions to find the exact step where it broke, then say the gap in one specific sentence. Specific means the missing piece, not the topic: a sentence another person could test, never "weak on X". For an English shaky, the gap is the pattern: "drops `is` in passives", not "English". Hand every named gap to `session-log` so it becomes its own row with its own schedule.
   - **Close the item before moving on.** After the explanation, ask the user in one line whether the item is clear and whether they want to add anything. Only move to the next item after they confirm. Never open a new question while a follow-up of yours is unanswered.
   - On fail: give the narrowest hint, then ask again. Only after a second attempt, explain the stuck step, then the user redoes it from zero (Zero-to-One loop). Do not end the item until the user has recalled it correctly once in this run (the redo counts). Then the reschedule below still applies.
   - ESL (when `esl.enabled`): same as `learn-session`. Feedback on the substance first, then max `esl.max_corrections` English corrections. Rewrite gate: after feedback, the user rewrites the answer in correct English before the next question. It applies to every answer that has an explanation in sentences (the "why"), and to all `speak` items. Skip it only for answers that are a bare prediction or a bare computation with no explanation.
3. **Interleave `review.cold_items_per_run` cold questions** (default 2-3), taken from the COLD pool (things the user got right, so correct knowledge is also spaced), oldest last pass first. If the pool is empty, use `glossary.md` terms from older topics. Mix topics and put them between due items, not in a block at the end, so the user must first identify the kind of problem. A cold item that fails becomes a new mistake: hand it to `session-log` (it gets a fresh row and schedule). A cold item that passes: add the pass marker plus today's date and the next gap to its Re-test cell, same as step 4.
4. **Log the gaps as you find them.** Every gap named in a gap hunt, and every cold item that fails, becomes a row *in this run* - do not carry it to the wrap-up. Append with the session-log script, which validates the row and skips duplicates:

```bash
python3 ${CLAUDE_SKILL_DIR}/../session-log/scripts/append_row.py topics/<name>/error-log.md \
  "<today>" "<question>" "<my answer>" "<correct>" "<cause from grading.causes>" "<fix drill>" "<today>, +1d <date>"
python3 ${CLAUDE_SKILL_DIR}/../session-log/scripts/append_row.py topics/<name>/glossary.md \
  "<term>" "<definition in the user's words>" "<example>" "<related / not same as>" "<no>"
```

   Write the row only from what the user actually said: their answer in their words, and a definition they produced. Never invent a definition for the glossary; if the user has not said it in their own words yet, ask them for one line first. Say in one line which rows you wrote. A glossary row for a term the user only heard from you is `no` in "Said aloud?" until they use it.

5. **Reschedule** each reviewed row with the script. It rewrites only the Re-test cell and computes the date from the config, so never edit the cell by hand:

```bash
python3 ${CLAUDE_SKILL_DIR}/../session-log/scripts/append_row.py topics/<name>/error-log.md \
  --retest "<words from the row's Question>" pass|shaky|fail
```

| Result | What the script writes |
|---|---|
| Pass | Marks today with `✓` and adds the next gap along `review.ladder_days` (+2d → +7d → +16d → +35d → +90d), counting only passes since the last fail. After the last rung the row is retired. |
| Shaky | Marks today with `shaky` and adds a date at `review.shaky_days` (default +3d). |
| Fail | Marks today with `fail` and adds a date at `review.fail_days` (default +1d). The row drops back to the first rung (`docs/principles.md` 1.6). Suggest the row's Fix drill now. |

   If the Question words match 0 or 2+ rows, the script exits 2 and lists them. Use more words and re-run. Example of a pass: `2026-10-20, +7d 2026-10-25` → `✓2026-10-20, +7d 2026-10-25, ✓2026-10-25, +16d 2026-11-10`.

   **A pass at `review.pattern_line_from_rung` (default +16d) or later earns a pattern line.** The ladder proves the item; the pattern sheet keeps what it taught once the row retires. Ask the user for one line in their own words (`docs/principles.md` 1.4: experts store "when I see X, the move is Y"), then append it. The script dedupes on the Trigger column, and `--init` creates the file if it is missing:

```bash
python3 ${CLAUDE_SKILL_DIR}/../session-log/scripts/append_row.py topics/<name>/patterns.md --init
python3 ${CLAUDE_SKILL_DIR}/../session-log/scripts/append_row.py topics/<name>/patterns.md \
  "<trigger, user's words>" "<move, user's words>" "<row date>"
```

   One line per row, never a paragraph. Skip it if the pattern is already in the file.

   If the same row fails `review.fail_streak_escalate` times (default 3), flag it as a concept gap for `error-diagnose` instead of looping.
   A right answer at confidence 1 or 2 is shaky, not a pass: the user guessed or half-guessed, so the row keeps its place on the ladder.
6. **Close.** Report: items passed / shaky / failed, confident-but-wrong items, **every gap named in the gap hunt** (one line each, specific), next due date, and the one weakest idea. Do not praise in general terms. Remind: same-day success is fluency; only passes at the later gaps (+7d and beyond) count as learned.

## Do not

- Show the Correct column before the user attempts.
- Write any error-log cell other than the Re-test cell (through `--retest`) and new rows you append, or any `TOPIC.md` cell. Levels, states and hours stay with `session-log` and `coach`.
- Quiz more than `review.cap_per_run` due items in one run. Leave the rest due; tomorrow's run picks them up.
- Write a `patterns.md` line in your own words, or for a row that has not reached the pattern rung yet.
- Track real time. Pacing is by content, not clock.
