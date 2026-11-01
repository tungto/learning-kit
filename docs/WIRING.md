# Wiring a project to the kit

```sh
python3 /Users/tungtx/LEARNING/SWE/learning-kit/init_project.py <project-dir> \
        --title "What this project is" --seed-topics a,b,c --git-init
```

Then fill `learning.config.json`, `PLAN.md` and `ABOUT-ME.md`, and run the three verification
commands the script prints.

## Copy, not symlink — why

| | symlink into the kit | copy + manifest (default) |
|---|---|---|
| cross-device git | **breaks**: the repo stores the link, so a clone has no skills unless the kit sits at the same path on that machine | works: a clone is complete and runnable |
| kit updates | instant | `--update`, hash-guarded |
| local edit to a skill | leaks into every other project | contained, and `--check` reports it |
| Claude Code discovery | unverified: the skill scanner may skip a symlinked directory | the same plain layout every project already uses |

`sync-progress` is built on "the repo is the only shared state". A symlinked skill tree
contradicts that, so copy is the default. `--link` exists for a single machine; it is **not
recommended until** someone runs this test: `--link` into a scratch project, open Claude Code
there, and confirm `/` lists the kit skills. Record the result here when you do.

## Ownership

| Path | Owner | On install / `--update` |
|---|---|---|
| `.claude/kit/**` | kit | always refreshed |
| `.claude/skills/<kit skill>/**` | kit | replaced only while the file still matches the manifest hash; a locally edited file is kept and the new version lands as `<file>.kit-new` |
| `scripts/validate.py`, `docs/AI-SYSTEM-GUIDE.md`, `docs/principles.md` | kit | same rule |
| `.claude/settings.json` | shared | JSON merge, timestamped `.bak` first, never replaced |
| `learning.config.json`, `CLAUDE.md`, `PLAN.md`, `STATUS.md`, `ABOUT-ME.md`, `.gitignore`, `topics/**` | project | created if absent, then never touched |
| `.claude/skills/<anything else>/` | project | never read, never written |

A project that wants to own one kit skill outright drops a `.kit-ignore` file in its copy; the
installer then skips that directory for good.

## The manifest

`.claude/.kit-manifest.json` records the kit version, the kit path, the kit's git commit, the
mode and a sha256 per installed file. `--check` compares them and reports drift, missing files,
whether the SessionStart hook is present, unknown config keys and whether `python3` resolves
(the hook fails silently if it does not).

## The hook

`init_project.py` adds one `SessionStart` entry, matcher `startup|resume`, `timeout: 10`:

```sh
python3 "$CLAUDE_PROJECT_DIR/.claude/skills/active-revise/scripts/due_reviews.py" \
        --project "$CLAUDE_PROJECT_DIR" --summary
```

It prints one spoiler-free line — counts only, never a question or an answer, because the
summary lands in the session prompt and seeing the answers would spoil the re-test. Project
hooks are additive to the user's own `~/.claude` hooks, and the entry is only appended when no
existing entry already runs `due_reviews.py`.

If `settings.json` is unparseable the installer writes nothing, prints the block and exits 2.

## Updating

```sh
python3 .../init_project.py <project-dir> --update     # re-install kit-owned files
python3 .../init_project.py <project-dir> --check       # audit, exit 1 on drift
```

`--force` overwrites locally modified kit files and names each one. Use it only after reading the
`.kit-new` diff.
