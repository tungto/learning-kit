## Mode: weekly review

1. Run `python3 <coach-dir>/scripts/brief_context.py weekly --project .` — one call: the status
   file, plan §4 (this week + next 2) and §6, `status_derive.py`, the error rows for
   `review.weekly_window_days`, the due headlines and `validate.py`. Then read only the
   `active`/`passed` `TOPIC.md` files. Any ERROR line: report it and fix the named file before step 2,
   because levels, states and ETAs read those cells. WARN lines: mention in one line and continue.
2. **Per topic** (active, passed): level with evidence, hours this week, decision: continue / review / deepen / pass. Ask the user for evidence on any bar; do not assume.
3. **State changes and unlocks:** apply the state machine; list newly `ready` topics.
4. **Recompute the topic table:** hours spent (sum from `TOPIC.md`), `ETA = today + (est − spent) / avg weekly hours on that topic over the last 2 weeks` (no hours yet → planned dates), and flags: ✅ ETA ≤ planned finish · ⚠️ ETA up to 1 week late · ❌ more than 1 week late, or a checkpoint missed · ⏳ not started by plan. Update "Done" and "Needs more effort" per topic in one short line each.
5. **Critical path check:** if a topic on the plan's critical path (plan §2.1) is ⚠️/❌, say what it pushes.
6. **Pace gate (plan §5.2) — run it, do not debate it.** Sum realized hours over the last `pace.lookback_weeks` weeks (`TOPIC.md` hours, or the status weekly log) and divide. The plan is `plan.weekly_hours` per week; the gate is `plan.weekly_hours × pace.gate_fraction`.
   - At or above the gate: say the number, continue.
   - Below the gate for `pace.lookback_weeks` running: **fire the next tier of `pace.drop_ladder`.** Say which tier, what it drops, the hours it saves and the new h/week needed. Record it in the status **Mode** field (e.g. `tier 2 live`). Do not ask permission to fire a tier - the rule was agreed; ask only which of two equal items inside a tier goes first, if the tier offers a choice. Already at the last tier and still below → that is the replan conversation (step 8 verdict), not another cut.
   - Back at or above plan for two weeks → un-fire the newest tier, one tier at a time, and say what returns.
   - `pace.never_dropped` is never cut, at any tier.
   - A fired tier changes est hours: recompute those topics' est in the table, then redo the ETAs in step 4.
7. **Checkpoint branch (plan §6).** A checkpoint due this week and missed: apply its failure branch verbatim, say which topics change state and which dates move. Never improvise the branch.
8. **Verdict (3 lines):** on track / behind / ahead vs `plan.horizon_label`. Behind → propose the cut. Two checkpoint misses → replan conversation.
9. **Next week:** main + second topic and up to `coach.weekly_outcome_cap` outcomes from plan §4. Write to the status file after the user approves. Add the weekly log row.
