# {{PROJECT_TITLE}}: AI operating manual

{{PROJECT_NAME}} is a learning project running on the shared learning kit. Each topic is a
self-contained unit in a dependency graph. This repo holds the plan, the status, the per-topic
state and the material inside `{{TOPICS_DIR}}/<name>/`. Control and skill-written files
(`TOPIC.md`, `error-log.md`, `glossary.md`, `patterns.md`, `deep-dive.md`) stay at the topic
root; material may be grouped in subfolders (`notes/`, `reference/`, `drills/`, `lessons/`,
`learning-records/`, `assets/`, `worksheets/`, `_archive/`) and is always listed under
**Sources** in `TOPIC.md`.

Every number the skills use - the review ladder, the row caps, the levels, the pace gate -
lives in `learning.config.json`. The kit documents it in `docs/CONFIG.md`.

## Read order

**Load on demand, never whole up front.** These files are big; reading them all costs tokens a
session for lines most tasks never use. Read the part the task needs, when it needs it.

1. `{{ABOUT_FILE}}`: who the user is, English level, schedule, how to teach them. The rules that
   always apply are repeated in the skills; read the file when teaching style, schedule or
   background actually matters.
2. `{{STATUS_FILE}}`: week, streak, next action, per-topic state/ETA/flag. For any `coach` mode,
   take it from the coach skill's `scripts/brief_context.py <mode> --project .`
   instead of reading the file (exception: `done`/`skipped`, which edits it).
3. `{{PLAN_FILE}}`: goal (§1), graph (§2), bars (§3), phases (§4), tracks (§5), checkpoints (§6).
   Read one section: `grep -n '^##' {{PLAN_FILE}}`, then a ranged `sed -n`. `brief_context.py`
   already pulls the §4 rows for the current week.
4. `{{TOPICS_DIR}}/<name>/TOPIC.md` for the topic in play.
5. Method, not content, read only when the task is about method or when designing a skill:
   `docs/principles.md` (the laws any learning system must obey) and `docs/AI-SYSTEM-GUIDE.md`
   (the stages, the routing and the review arithmetic).

## Who writes what

| File | Writer |
|---|---|
| `{{STATUS_FILE}}`, `State` field in `TOPIC.md` | `coach` only |
| `TOPIC.md` hours / subtopic levels / next action | `session-log` (levels only on independent evidence) |
| `{{TOPICS_DIR}}/*/error-log.md`, `glossary.md` | `session-log` and `active-revise` (both via the session-log skill's `scripts/append_row.py`) |
| `{{TOPICS_DIR}}/*/patterns.md` | `active-revise`, one line per row that passes the pattern rung (trigger -> move, user's words) |
| `{{PLAN_FILE}}`, `{{ABOUT_FILE}}` | Edit only when the user asks |
| `{{TOPICS_DIR}}/*/MISSION.md`, `RESOURCES.md`, `NOTES.md`, `learning-records/` | `teach` only |
| `{{TOPICS_DIR}}/*/lessons/`, `assets/`, `reference/`, the folder `index.html` files | `create-lesson` (called by `teach`, or directly) |
| `learning.config.json` | the user, or the AI when the user asks for a dial change |
| the skills, `kit/` and `validate.py` | the learning-kit plugin (or `init_project.py` in copy mode). Change them in the kit repo, not here |

## Skill routing

- What to do today, done/skipped, weekly review, status, one topic's status: `/coach <mode>`.
- First exposure to a subtopic the user cannot say three true sentences about: `/teach` (guided,
  cited lesson into `{{TOPICS_DIR}}/<name>/lessons/` + a printable reference into `.../reference/`,
  shared components in `.../assets/`). It may also write that topic's `MISSION.md` and
  `learning-records/NNNN-<dash-case>.md`. Those stay topic-local and never override the plan or
  the status file. A `teach` lesson is never evidence for a level change.
- Writing or revising the lesson file itself: `/create-lesson` (numbering, light theme,
  citations, `assets/` reuse, folder indexes and footer nav). `teach` decides what to teach and
  hands the authoring over; call it directly when the subtopic is already chosen.
- Learn or be quizzed on a topic: `/learn-session` (only `active` topics). This is the skill for
  "quiz me on X" or "study X" in this project, not a generic learning assistant.
- Revise due items: `/active-revise`. Wrap-up: `/session-log`. Weekly analysis: `/error-diagnose`.
  Pressure round: `/perform-drill`. Device switch: `/sync-progress`.
- Flow per subtopic: `teach` -> `learn-session` -> `active-revise` -> `perform-drill`
  (`docs/AI-SYSTEM-GUIDE.md`).

## Rules

- **Try first, then reveal.** The user attempts before any explanation.
- **Bound the review ladder.** `session-log` appends about 4-5 error rows a session, one per gap
  pattern, merging near-duplicates; `active-revise` runs at most 8 items and triages the rest
  (fail/shaky first, then oldest-late). A growing backlog means inflow is too high, not that the
  user is behind.
- **Name the gap, not the topic.** A row says the missing piece in a sentence another person
  could test. Example: {{GAP_EXAMPLE}}
- Plain English, short sentences, define jargon once. Depth is shown by trade-offs and failure
  modes, not vocabulary.
- Verify anything version- or date-sensitive with a search. Mark own ideas `[my suggestion]`.
- Do not add topics, folders or systems unprompted.
- A topic unlocks only when all its "Needs" are `passed` or `kept` ({{PLAN_FILE}} §2).

## Layout invariants (scripts depend on these)

- `{{TOPICS_DIR}}/<name>/error-log.md` columns: `Date | Question | My answer | Correct | Cause | Fix drill | Re-test`. Cause = {{CAUSES}} (`English` is this project's name for principles 1.3's `comprehension`).
- `glossary.md` columns: `Term | Simple definition (my words) | Code | Related / not same as | Said aloud?`.
- `patterns.md` columns: `Trigger (when I see...) | Move (...I do) | From row`. Optional file, created on the first pass at the pattern rung.
- One folder per topic directly under `{{TOPICS_DIR}}/`; the folder name is the topic id, and the
  scripts read it with the parent-directory name.
- Scripts take `--project .` and glob recursively. They skip any path segment starting with `_`.
- A `Re-test` cell marks the date it was reviewed on with `✓`, `shaky` or `fail`. An unmarked past
  date makes the row report overdue forever; `validate.py` warns about it.
