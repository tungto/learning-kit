---
name: sync-progress
description: Save or resume learning work across devices through git. "save" mode writes HANDOFF.md (where we are, what the user produced, open next steps), optionally a condensed SESSION-<date>.md transcript, then commits and pushes. "resume" mode runs git pull and reads HANDOFF.md, the status file and the coach brief so work continues exactly where it stopped. Use whenever the user says "save progress", "sync", "save and push", "switch device", "continue on my laptop", "resume", "pull and continue", "continue the handoff", "I'm leaving", or ends a session mid-topic, even if they do not mention git or files. Does not teach, log errors or update the status file.
---

# Sync progress (save / resume across devices)

The repo is the only shared state. Claude memory and `~/.claude` do not travel between devices. Anything not committed and pushed is lost on the other device.

Call as `/sync-progress save` or `/sync-progress resume`. No argument: ask which one.

File names come from `paths.*` in `learning.config.json`: `handoff_file` (default `HANDOFF.md`), `status_file`, `plan_file`, `sessions_dir`.

## Before anything

- **Not a git repo** (`git rev-parse --show-toplevel` fails): say so, offer `git init -b main`, and wait for a yes. Never init silently. Until then, `save` can still write the handoff file; say plainly that nothing is committed.
- **No remote** (`git remote -v` empty): write the handoff, commit locally, and say the push was skipped and why. Do not add a remote on your own.

## Boundaries

- The status file and the State field in `TOPIC.md` are `coach` only. Never edit them here. If the session finished a day, say "run `/coach done` first" and wait.
- Error rows and glossary are `session-log` only. If the user got things wrong this session and nothing is logged yet, offer `/session-log` first. Do not skip it silently.
- Do not stage files outside this repo's work (`.DS_Store`, secrets, `.env`). Stage by explicit path, not `git add -A`.

## Save

1. `git status --short` and `git remote -v`. Note what changed.
2. **Write the handoff file** (overwrite, it is a snapshot, keep under ~60 lines):
   - Header: date, day label (e.g. `W3 Tue`), skill/role in use.
   - **Where we are:** 3-5 bullets. Topic, phase, what is done.
   - **Learned so far (user produced):** only things the user said or got right. No new knowledge from Claude.
   - **Open, in order:** the exact next question or step, wrong ideas still pending (with the correct idea in one line), and which skill runs next (`session-log`, `/coach done`).
   - **Next scheduled:** from the status file (Now -> Next action) and the plan's phases section.
   - First line after the header: `Resume on another device: git pull, open Claude Code in this repo, run /sync-progress resume.`
3. **Transcript (optional, ask once):** only if the session had real study content, and only when `sync.transcripts` is true. Write or append `<sessions_dir>/SESSION-YYYY-MM-DD.md` (create the folder if missing): user answers verbatim (errors kept, they are the data), Claude feedback condensed, chatter and setup removed. Link it from the handoff. No tool output, no secrets, no personal data.
4. **Commit and push:**
   ```bash
   git add HANDOFF.md sessions/ <other changed work files by path>
   git commit -m "chore: save progress <date> <topic>"
   git push
   ```
   Commit message: normal style, then the attribution lines from the system reminder. If push is rejected, `git pull --rebase` then push again. Never force push. If auth fails, say so and stop.
5. **Report:** files committed, commit hash, push result, and the one-line next step. Remind: on the other device run `git pull` then `/sync-progress resume`.

## Resume

1. `git status --short`. If the tree is dirty, show it and ask before pulling. Then `git pull --rebase`. Report conflicts plainly, do not auto-resolve.
2. Read the handoff file (if missing: say "no handoff", fall back to `/coach today`). Then the status file for week and streak.
3. Show a 5-line brief: where we stopped, what the user already produced, the first open step, which skill runs.
4. Hand off: continue the open step with the right skill (usually `learn-session`). The try-first rule still applies: ask the pending question, do not reveal the answer.
5. When the handoff topic is finished (wrapped, logged, `/coach done` run), offer to delete the handoff file and commit that.

## Do not

- Edit the status file, the plan, `error-log.md` or `glossary.md`.
- Put Claude's own explanations in "Learned so far".
- Force push, `git add -A`, or push without saying what was pushed.
