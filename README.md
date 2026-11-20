# learning-kit

The domain-agnostic core of a working learning system: nine Claude Code skills, six scripts and
a markdown knowledge base, driven by one config file per project.

It is the generalized form of the `interview-v2` study system. Nothing in here knows about any
one subject — a project supplies `learning.config.json`, `PLAN.md` and its topics, and gets the
same machinery.

## Quickstart (plugin, recommended)

The repo is both the plugin and its own marketplace. Skills load from the plugin, so a fix
pushed here reaches every learning repo on the next `claude plugin update`; nothing is copied.

One-time per device (private repo: git must already reach GitHub, e.g. `gh auth setup-git`):

```sh
claude plugin marketplace add tungto/learning-kit
```

New learning repo:

```sh
mkdir -p ~/LEARNING/SWE/my-subject && cd ~/LEARNING/SWE/my-subject
python3 ~/LEARNING/SWE/learning-kit/init_project.py . --plugin \
        --title "What I am learning and why" --seed-topics basics,practice --git-init
claude plugin install learning-kit@learning-kit --scope project   # once per clone/device
```

`--plugin` writes the project files and enables the plugin in `.claude/settings.json`
(`enabledPlugins` + `extraKnownMarketplaces`), so it is active only in this repo. Then type
`/coach today` (or `/learning-kit:coach today`).

Updating: push to this repo, then `claude plugin update learning-kit@learning-kit` (or turn on
auto-update for the marketplace in `/plugin`). `plugin.json` has no `version` on purpose: every
commit counts as a new version.

Developing the kit: `claude --plugin-dir ~/LEARNING/SWE/learning-kit` loads the working tree.

## Quickstart (copy mode, legacy)

Used by repos installed before the plugin (`english`, `how-to-think`). Copies skills into
`.claude/skills/` with a hash manifest.


```sh
mkdir -p ~/LEARNING/SWE/my-subject && cd ~/LEARNING/SWE/my-subject
python3 ~/LEARNING/SWE/learning-kit/init_project.py . \
        --title "What I am learning and why" --seed-topics basics,practice --git-init
# fill in learning.config.json, PLAN.md, ABOUT-ME.md
python3 scripts/validate.py --project .
python3 .claude/skills/coach/scripts/brief_context.py today --project .
```

Then open Claude Code in the project and type `/coach today`.

## The skills

| Skill | Role | Stage |
|---|---|---|
| `teach` | guided first exposure: cited lesson + printable reference | 1 knowledge |
| `create-lesson` | authors one HTML lesson, its components and the folder indexes | called by `teach`, or directly |
| `learn-session` | answer-first active session on one topic | 2 skill |
| `active-revise` | spaced re-tests along the ladder, gap hunt, patterns sheet | 3 retention |
| `perform-drill` | timed round under pushback, scripted debrief | 4 perform |
| `session-log` | the Clerk: error rows, glossary, deep-dive, flashcards | closes every session |
| `error-diagnose` | weekly root-cause pass across topics | weekly |
| `coach` | the operator: today / done / weekly review / status / topic | always |
| `sync-progress` | handoff + git save/resume across devices | as needed |

## What it is built on

- **Retrieval over review.** The user answers first, always. Nothing is revealed before an attempt.
- **A ladder, not a streak.** `+2d, +7d, +16d, +35d, +90d`, with a result marker on every date
  reviewed; same-day success is fluency, not learning.
- **Bounded inflow.** Each error row costs five future reviews against a cap of eight a run, so
  `session-log` merges by gap pattern and `validate.py` checks the arithmetic.
- **One writer per file.** `coach` owns state, `session-log` owns the logs, `active-revise` owns
  the ladder, `teach` owns its workspace. Anything else is a bug.
- **Evidence, never assumption.** A level or a state moves only on something the user produced.

The laws behind those choices: [docs/principles.md](docs/principles.md). The human-facing guide
a project installs: [docs/AI-SYSTEM-GUIDE.md](docs/AI-SYSTEM-GUIDE.md).

## Layout

| Path | What |
|---|---|
| `init_project.py` | installs or audits an installation (copy + sha256 manifest) |
| `kit/` | `config.py`, `defaults.json`, `mdtable.py`, `dates.py` — installed to `<project>/.claude/kit/` |
| `skills/` | the nine skills, installed one directory at a time |
| `scripts/validate.py` | layout invariants, ladder hygiene, the state machine, review inflow |
| `templates/` | the project-side files, created once and then owned by the project |
| `docs/` | `CONFIG.md`, `WIRING.md`, `ADAPTING.md`, plus the two docs a project installs |
| `tests/` | `make_fixture.py` + a two-topic fixture with today-relative dates |

## Tests

```sh
sh tests/smoke.sh        # every script, both negatives, installer; runs on a temp copy of the fixture
```
