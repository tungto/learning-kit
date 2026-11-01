---
name: error-diagnose
description: Weekly root-cause analysis of the user's logged mistakes. Reads every topic's `error-log.md` (under the configured topics dir; skips paths starting with the skip prefix), finds recurring patterns across topics (shared misconception, careless habit, English comprehension gap), and proposes targeted drills and the next week's focus. Use whenever the user says "weekly review", "diagnose my errors", "why do I keep getting X wrong", "what am I weak at", "analyze error log", "review week", or at the weekly review block, even if they only ask "what should I fix this week". Acts as the Diagnostician role. Needs logged data; with no rows it says so instead of guessing.
---

# Error diagnose (Diagnostician)

## Why

One mistake is noise. The same kind of mistake across topics is a core misconception, and fixing it is worth more than 10 single-fact reviews. This skill only works on history the user logged (via `session-log`). No data, no diagnosis.

## Steps

1. **Collect.** Run:

```bash
python3 .claude/skills/error-diagnose/scripts/collect_errors.py --project . --days 7
```

   Use `--days 14` for a bi-weekly review, `--topic <name>` for one topic. The defaults come from `review.weekly_window_days` and `review.error_window_days`. If the user wants a different window, pass it.
2. **Check data.** Fewer than ~5 rows: say that the sample is small, give tentative hypotheses labelled as such, and suggest logging more. Zero rows: stop and say so.
3. **Look for patterns, not single mistakes.** Group by:
   - Shared idea across topics (the same assumption failing in three different places) = one misconception.
   - Cause column: mostly `careless` -> process habit (no re-read, rushing). Mostly `English` -> vocabulary or question misreading. Mostly `concept` -> missing mental model. The set and what each means: `grading.causes` and `grading.cause_help`.
   - Repeats: same Question, or a Re-test still failing.
   - Rows marked `concept` that are really a question-wording problem: flag as a possible mislabel.
4. **Present for the user to confirm.** Show 1-3 candidate root causes, each with the evidence rows (cite Date + topic). Ask the user which matches their experience. They know their own reasoning better than the table does, so do not state a root cause as fact.
5. **Prescribe.** For each confirmed cause: one 10-15 min drill (five fresh cases aimed at it), target about 80% success, re-test at the first two ladder gaps (+2d then +7d). Plus: one word list for `English` causes, one habit rule for `careless` ones.
6. **Next week.** One recommendation: what to slow down on, and what to skip. Stay inside the weekly budget (`plan.weekly_hours`, and the plan's tracks section for how it is spread). Cut, never add; the fix drill replaces work, it does not stack on top.
7. **Offer to log** the drills as Fix drill / Re-test entries via `session-log`.

## Output shape

```
Data: N rows, topics, window
Patterns (confirmed by you): ...
Evidence: date/topic of rows
Drills: ...
Next week: ...
```

Keep it short. Simple English (`esl.output_ceiling`). Put English notes for the user's own messages in a separate block at the end.
