## Mode: done / skipped

1. Read the status file only (you edit it). Update its **Now** block (date, streak, blocks, next action) and add a daily log row (keep the last `coach.daily_log_keep`): date, result (`done`/`minimum`/`skipped`), topic, level reached, one-line note.
2. Streak: `coach.streak_rule` - a day counts if the main session or the minimum day (`coach.minimum_day`) happened. The weekly bar is `plan.weekly_block_bar` days.
3. Skipped: assign the minimum day, count it, do not double up. Two skipped main slots in a row → mode `cut-scope`, propose the cut now (rule 2).
4. If the user reports a bar met with evidence → apply the state change (state machine).
5. Mistakes or new words mentioned → suggest `session-log` with the topic.
6. End in ~6 lines: streak, next step, when.
