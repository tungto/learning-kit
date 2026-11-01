# `learning.config.json` reference

One file per project, at the project root next to `PLAN.md`. Every key has a default in
`kit/defaults.json`; the project file only overrides what differs, so a real project file is
~30 lines. A key absent from `defaults.json` is reported by `init_project.py --check` and
ignored at runtime — **a skill must never read a key that is not in the defaults.**

JSON, not TOML: `tomllib` needs Python ≥3.11 and this project travels between devices where
`python3` may be the system 3.9.

## How it is read

`kit/config.py` resolves the project root in this order, never from `__file__`:

1. `--project` / `--root` passed to a script
2. `$LEARNING_PROJECT_ROOT`
3. `$CLAUDE_PROJECT_DIR` (set by Claude Code, which is how the SessionStart hook finds it)
4. an upward walk from the current directory looking for `learning.config.json`

Then the project file is merged over the defaults: dicts recursively, lists and scalars replaced
whole. So overriding one phase means writing the whole `plan.phases` list.

## Who reads what

| Area | Keys | Read by |
|---|---|---|
| paths | `paths.*` | every script |
| week math, phases | `plan.start_date`, `plan.phases`, `plan.total_weeks` | `brief_context.py`, `coach` |
| effort | `plan.effort_levels`, `plan.weekly_hours`, `plan.weekly_block_bar` | `coach`, `learn-session` |
| tables | `layout.tables`, `layout.dedupe_keys`, `layout.files`, `layout.topic_fields` | `append_row.py`, `due_reviews.py`, `collect_errors.py`, `status_derive.py`, `validate.py` |
| state machine | `graph.*` | `coach`, `validate.py` |
| grading | `grading.*`, `levels.*` | `learn-session`, `active-revise`, `session-log`, `append_row.py`, `validate.py` |
| ladder and caps | `review.*` | `active-revise`, `session-log`, `due_reviews.py`, `validate.py` |
| English | `esl.*` | `learn-session`, `active-revise`, `perform-drill`, `error-diagnose` |
| roles | `roles.*` | `learn-session` |
| pressure rounds | `perform.*` | `perform-drill` |
| pace gate | `pace.*` | `coach` weekly review |
| coach behaviour | `coach.*` | `coach` and its modes |
| teach workspace | `teach.*` | `teach` |

## The dials worth thinking about

- **`esl.enabled`** — on by default. Off makes English stop counting toward the pass bar and
  removes the rewrite gate. Everything else is unaffected.
- **`review.ladder_days`** — the spacing. Shortening it raises inflow pressure; `validate.py`
  will start warning sooner.
- **`review.cap_per_run` × `review.rows_per_session`** — the two halves of the review economy.
  Raising rows per session without raising the cap is how the review slot eats a plan.
- **`graph.max_parallel_new_topics`** — 1 for a side project, 2 only when the weekly hours
  genuinely support two fronts.
- **`pace.drop_ladder` / `pace.never_dropped`** — write these while rested. They fire
  automatically when the pace gate trips, and `coach` is told not to ask permission.
- **`layout.group_dirs`** — true if topics live in `topics/<group>/<name>/`. The scripts glob
  recursively either way; this only switches on an extra `validate.py` check.

## Every key

| `kit_version` | string | `"0.1.0"` |
| `project.name` | string | `""` |
| `project.title` | string | `""` |
| `project.notes` | string | `""` |
| `paths.topics_dir` | string | `"topics"` |
| `paths.plan_file` | string | `"PLAN.md"` |
| `paths.status_file` | string | `"STATUS.md"` |
| `paths.about_file` | string | `"ABOUT-ME.md"` |
| `paths.handoff_file` | string | `"HANDOFF.md"` |
| `paths.sessions_dir` | string | `"sessions"` |
| `paths.source_dir` | string | `"source"` |
| `paths.skills_dir` | string | `".claude/skills"` |
| `paths.validate_script` | string | `"scripts/validate.py"` |
| `paths.skip_prefix` | string | `"_"` |
| `plan.start_date` | string | `""` |
| `plan.total_weeks` | int | `12` |
| `plan.horizon_label` | string | `""` |
| `plan.weekly_hours` | float | `3.0` |
| `plan.weekly_block_bar` | int | `4` |
| `plan.phases` | list | `[]` |
| `plan.sections.goal` | string | `"## 1."` |
| `plan.sections.graph` | string | `"## 2."` |
| `plan.sections.parallel_rule` | string | `"### 2.2"` |
| `plan.sections.bars` | string | `"## 3."` |
| `plan.sections.phases` | string | `"## 4."` |
| `plan.sections.tracks` | string | `"## 5."` |
| `plan.sections.effort_levels` | string | `"### 5.1"` |
| `plan.sections.pace_gate` | string | `"### 5.2"` |
| `plan.sections.checkpoints` | string | `"## 6."` |
| `plan.effort_levels.minimum_day_minutes` | int | `10` |
| `plan.effort_levels.minimum_minutes` | int | `20` |
| `plan.effort_levels.target_minutes` | int | `40` |
| `plan.effort_levels.stretch_minutes` | int | `70` |
| `layout.group_dirs` | boolean | `false` |
| `layout.files.topic` | string | `"TOPIC.md"` |
| `layout.files.error_log` | string | `"error-log.md"` |
| `layout.files.glossary` | string | `"glossary.md"` |
| `layout.files.patterns` | string | `"patterns.md"` |
| `layout.files.deep_dive` | string | `"deep-dive.md"` |
| `layout.tables.error_log` | list | `["Date", "Question", "My answer", "Correct", "Cause", "Fix drill", ...` |
| `layout.tables.glossary` | list | `["Term", "Simple definition (my words)", "Code", "Related / not sam...` |
| `layout.tables.patterns` | list | `["Trigger (when I see...)", "Move (...I do)", "From row"]` |
| `layout.dedupe_keys.error_log` | int | `2` |
| `layout.dedupe_keys.glossary` | int | `1` |
| `layout.dedupe_keys.patterns` | int | `1` |
| `layout.topic_fields.state` | string | `"State"` |
| `layout.topic_fields.level` | string | `"Overall level"` |
| `layout.topic_fields.needs` | string | `"Needs"` |
| `layout.topic_fields.unlocks` | string | `"Unlocks"` |
| `layout.topic_fields.bar` | string | `"Bar category"` |
| `layout.topic_fields.weeks` | string | `"Planned weeks"` |
| `layout.topic_fields.est_hours` | string | `"Est. hours"` |
| `layout.topic_fields.hours_spent` | string | `"Hours spent"` |
| `layout.topic_fields.last_retest` | string | `"Last re-test"` |
| `layout.topic_fields.next_action` | string | `"Next action"` |
| `graph.states` | list | `["locked", "ready", "active", "passed", "kept"]` |
| `graph.done_states` | list | `["passed", "kept"]` |
| `graph.lite_min_level` | int | `2` |
| `graph.max_parallel_new_topics` | int | `1` |
| `graph.allow_standalone` | boolean | `true` |
| `levels.count` | int | `6` |
| `levels.names` | list | `["recognize", "predict", "do alone", "spot the failure mode", "expl...` |
| `grading.confidence_scale` | list | `[1, 3]` |
| `grading.pass_confidence` | int | `3` |
| `grading.pass_bar` | string | `"right idea, in my own words, with the key term, said in clear Engl...` |
| `grading.shaky_bar` | string | `"any one of those missing - wrong or missing term, English that blo...` |
| `grading.fail_bar` | string | `"wrong or blank after one best-guess nudge"` |
| `grading.causes` | list | `["concept", "careless", "English"]` |
| `grading.cause_help.concept` | string | `"the model itself is missing or wrong"` |
| `grading.cause_help.careless` | string | `"knew it, answered before reading the question"` |
| `grading.cause_help.English` | string | `"wording blocked the idea (principles 1.3 'comprehension')"` |
| `grading.depth_note` | string | `"depth is shown by naming where the model fails, not by reciting it...` |
| `review.ladder_days` | list | `[2, 7, 16, 35, 90]` |
| `review.shaky_days` | int | `3` |
| `review.fail_days` | int | `1` |
| `review.markers.pass` | string | `"✓"` |
| `review.markers.shaky` | string | `"shaky"` |
| `review.markers.fail` | string | `"fail"` |
| `review.cap_per_run` | int | `8` |
| `review.rows_per_session` | int | `5` |
| `review.rows_per_long_session` | int | `6` |
| `review.ahead_days` | int | `3` |
| `review.cold_items_per_run` | int | `3` |
| `review.cold_pool_show` | int | `10` |
| `review.pattern_line_from_rung` | int | `16` |
| `review.error_window_days` | int | `14` |
| `review.weekly_window_days` | int | `7` |
| `review.fail_streak_escalate` | int | `3` |
| `review.types.skill` | list | `["implement", "rebuild", "re-build", "write code", "build", "from s...` |
| `review.types.speak` | list | `["aloud", "say ", "explain", "speak", "record", "teach back"]` |
| `review.types.recall` | list | `[]` |
| `esl.enabled` | boolean | `true` |
| `esl.level` | string | `"B1"` |
| `esl.output_ceiling` | string | `"B2"` |
| `esl.max_corrections` | int | `3` |
| `esl.rewrite_gate` | boolean | `true` |
| `esl.pass_bar_includes_english` | boolean | `true` |
| `esl.accept_chat_abbreviations` | boolean | `true` |
| `esl.new_words_cap` | int | `5` |
| `esl.purpose` | string | `"explain an idea clearly to another person, in English, without notes"` |
| `esl.frames` | list | `["The mechanism is...", "When I see X, the move is Y", "I'd estimat...` |
| `roles.arc` | list | `[{"day": 1, "label": "Orient", "roles": ["Scoper", "Mapmaker"], "no...` |
| `roles.target_hit_rate` | list | `[0.6, 0.95]` |
| `perform.mode` | string | `"application"` |
| `perform.questions` | list | `[5, 8]` |
| `perform.default_seconds_per_answer` | int | `90` |
| `perform.dials` | list | `["time limit", "persona: friendly -> neutral -> hostile", "pushback...` |
| `perform.scenarios` | list | `[]` |
| `perform.exit_bar` | string | `"the answer holds under the time limit and two rounds of pushback"` |
| `pace.gate_fraction` | float | `0.6` |
| `pace.lookback_weeks` | int | `2` |
| `pace.drop_ladder` | list | `[]` |
| `pace.never_dropped` | list | `[]` |
| `coach.status_sections.today` | list | `["## Now", "## This week", "## Daily log", "## Topics"]` |
| `coach.status_sections.status` | list | `["## Now", "## This week", "## Overall", "## Topics", "## Milestones"]` |
| `coach.status_sections.weekly` | list | `["## Now", "## This week", "## Daily log", "## Overall", "## Topics...` |
| `coach.status_sections.topic` | list | `["## Now", "## Topics"]` |
| `coach.daily_log_keep` | int | `10` |
| `coach.minimum_day` | string | `"one recall item + one error-log row"` |
| `coach.streak_rule` | string | `"a day counts if one session or the minimum day happened"` |
| `coach.priority` | list | `["overdue re-tests", "main topic", "second topic", "standalone topi...` |
| `coach.weekly_outcome_cap` | int | `3` |
| `coach.slot_map` | list | `[]` |
| `teach.workspace_root` | string | `"topics/<name>"` |
| `teach.allow` | list | `["MISSION.md", "RESOURCES.md", "NOTES.md", "lessons/", "reference/"...` |
| `teach.lesson_theme` | string | `"light"` |
| `teach.require_citations` | boolean | `true` |
| `sync.git` | boolean | `true` |
| `sync.branch` | string | `"main"` |
| `sync.transcripts` | boolean | `true` |

`plan.phases`, `pace.drop_ladder`, `coach.slot_map` and `perform.scenarios` default to empty and
are meant to be filled per project. Their shapes:

```jsonc
"plan": { "phases": [ { "name": "Phase 1 Hardware",
                        "heading": "### Phase 1: W1-3 — hardware",   // matched in PLAN.md §4
                        "first_week": 1, "last_week": 3 } ] },
"pace": { "drop_ladder": [ { "tier": 1, "drops": "<what stops>", "saves_hours": 2 } ],
          "never_dropped": ["<topic>"] },
"coach": { "slot_map": [ { "slot": "weekday morning", "days": "Mon-Fri",
                           "minutes": 30, "use": "main topic, learn-session" } ] },
"perform": { "scenarios": [ { "name": "cold application",
                              "prompt": "a real decision from my week, no notes" } ] }
```
