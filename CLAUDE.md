# learning-kit: rules for editing the kit itself

This repo is **not** a learning project. It is the machinery other projects install. A consumer
project gets its own `CLAUDE.md` from `templates/CLAUDE.md`.

## What must stay true

1. **Nothing here names a subject.** No topic names, no plan sections, no dates, no job
   descriptions. If a skill needs a number, it reads a config key. Check with:
   `grep -rnwiE 'interview|NAB|Inspectorio|PayLedger|MASTER-PLAN' skills/ templates/ docs/`
   (the only legitimate hit is the `interview` scenario in `perform-drill/references/scenarios.md`).
2. **A skill may only read config keys that exist in `kit/defaults.json`,** and every key there is
   documented in `docs/CONFIG.md`. Adding a key means touching both.
3. **No script resolves the project root from `__file__`.** Use `kit/config.py`. `__file__` may
   only be used to find sibling kit modules.
4. **The mechanisms are not up for redesign while editing wiring.** Answer-first, the three
   true sentences, confidence 1-3, the gap hunt wording, the triage order, the row caps, the
   result markers, the state machine, the pace gate, the ETA formula, the single-writer table:
   these came from a system that works. Reword them only to remove a subject, never to soften a
   rule.
5. **One writer per file** stays the architecture. A new skill that writes a file another skill
   owns is wrong, however convenient.
6. **Tests before a commit:** `python3 tests/make_fixture.py && tests/smoke.sh`. The fixture
   must come back 0 errors, 0 warnings, and both negative controls must still fail.

## When changing a script

- Keep it read-only unless it is `append_row.py` (the one writer of the tables) or
  `init_project.py` (the installer).
- Table access goes through `kit/mdtable.py`, by column name, never by index.
- Date and ladder logic goes through `kit/dates.py`. `split_retest()` is load-bearing: a row
  whose last marked date is not respected reports overdue forever.
- A script that cannot do its job says so and exits non-zero. It never guesses a value to keep
  going.

## When changing prose

- Keep the shape that makes a rule enforceable: a bar is observable, a gap is a sentence someone
  could test, a cap is a number.
- Config keys are named inline (`review.cap_per_run`) with the default in parentheses, so the
  file reads correctly even before anyone opens the config.
- Progressive disclosure: `coach` modes and the long references live in separate files, loaded
  only when that mode runs.

## Versioning

`VERSION` is stamped into each project's manifest. Bump it when a consumer would have to run
`--update` to get a fix.
