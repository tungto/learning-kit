---
name: session-log
description: End-of-session logging for any learning session. Turns what happened into rows in the topic's `error-log.md` (date, question, my answer, correct, cause, fix drill, re-test), `glossary.md` (one-line cheat-sheet rows, plain AI-written definitions, no cap) and `deep-dive.md` (long answers), plus a few flashcards and the next review dates. Use whenever the user says "log session", "update glossary", "add to error log", "I got X wrong", "log my mistakes", "make flashcards", "wrap up", "end session", or finishes a learn-session, teach lesson or perform-drill, even if they do not mention files. Acts as the Clerk role: it organizes, it never adds new knowledge the user did not produce.
---

# Session log (Clerk)

Files per topic folder (`topics/<name>/`):
- `error-log.md` (cols: Date | Question | My answer | Correct | Cause | Fix drill | Re-test)
- `glossary.md` (cols: Term | Simple definition (my words) | Code | Related / not same as | Said aloud?) - a cheat sheet: one short line per row
- `deep-dive.md` (prose, `## term` sections) - the long spoken answer for terms that need one

Column sets differ per file and are declared in `layout.tables`, so always run `--check` first and match the header.

## Why

The error log is the raw data for weekly root-cause analysis (`error-diagnose`). A row that is vague, or whose cause is guessed, poisons the pattern search. So rows must be specific and the user, not you, decides cause. The glossary is a quick lookup: definitions are written by the AI in plain English at `esl.level` (user rule, 2026-11-19), so the user can read them fast.

## Steps

1. **Topic folder.** From the conversation, or ask. Resolve to an existing folder under `topics/`, never a new one.
2. **Collect candidates.** From the session: wrong or shaky answers, unknown terms, words that blocked understanding. If the session is not in this conversation, ask the user to paste or list them. Do not invent mistakes.
3. **Errors.** One row per **named gap**, not per question. `active-revise` and `learn-session` run a gap hunt on every wrong answer and every answer below confidence 3; each gap they name gets its own row. A row names the missing piece, never the topic: a sentence another person could test passes, "weak on X" does not - a vague row poisons the weekly pattern search. If a session hands you a vague gap, ask what exactly broke before writing it. An answer that was right on the substance but failed on English is a row too, with the pattern as the Question ("drops `is` in passives"). **Every answer that hit the rewrite gate gets an English row**, even when the idea was right and the row would otherwise be skipped: the language pattern is the gap. Never fold a language fix into a `concept` row - a concept row earns a concept drill, and the slip then gets no language drill and shows up nowhere in the weekly pattern search.

   **Merge before you append, and cap the review load.** Each row costs five future reviews (+2d, +7d, +16d, +35d, +90d) while `active-revise` can only run `review.cap_per_run` items a run. Ten new rows a session means fifty future reviews against a throughput of eight: the review slot eats the whole plan within weeks. So:
   - **Same pattern = one row.** Two misses from the same missing piece (failed in two different cases) are one row, with the second case added to the Fix drill. Grep the existing rows for the pattern before appending; enrich the existing row instead of writing a near-duplicate, and reset its Re-test to today +1d (a repeat miss drops it to the bottom rung).
   - **Cap: `review.rows_per_session` rows a session (default about 4-5), `review.rows_per_long_session` after a long or high-pressure session.** The cap counts *review items*, not misses. Nothing is dropped: surplus gaps fold into the Fix drill of the row that shares their pattern, so the data stays and the ladder stays finite.
   - If more than six genuinely distinct patterns broke in one session, that is the finding. Say it, write the five that matter most (repeat misses first, then confident-but-wrong, then the rest), and park the others as Parking lot bullets for `error-diagnose` to read at the weekly review.
   - **English rows: one row per language pattern**, not per sentence. "drops `is` in passives" is one row however many times it happened.

   For each: one row. Fill Question (short), My answer (what the user really said), Correct (one line), Fix drill (a 10-15 min targeted drill, e.g. "five fresh cases, predict the outcome before checking"), Re-test (today + the first ladder gap, written as `YYYY-MM-DD`; also note the second gap in the cell). Ask the user to pick **Cause** from `grading.causes` (default `concept`, `careless`, `English`; `grading.cause_help` says what each means). Offer your reading as a suggestion only. Wait for their pick.
4. **Glossary (cheat sheet).** Log **every** word the user did not know this session. No cap. Write the definition yourself (user rule, 2026-11-19: do not ask for their words): plain English at the `esl.level` (default B1), short common words, no jargon inside the definition. Recall practice happens in `active-revise`, not here.

   The glossary is a quick reference the user scans before performing, so **every cell is one line**:
   - **Simple definition (my words)**: ONE sentence, ~20 words max, plain English written by the AI (the column keeps its old name for the scripts). No bold labels, no paragraphs.
     - ESL gloss: when the term is a normal English word used in a special way, add the plain meaning in parens, 8 words max - `lexical (= as written in the text)`. Skip for pure symbols and acronyms.
   - **Code**: one snippet, formula or `input -> output`, one line. For a non-code domain, the smallest concrete instance.
   - **Related / not same as**: `vs X (one-clause difference)` for things the user may confuse, plus `see: [[term]]` for the neighbours worth learning together. These point at other rows in the same glossary.
   - **Said aloud?**: blank until they say it, then `✓`.
   - If the term needs more than that, end the cell with `-> deep-dive.md#term` and write that section (next step).

   **Check for an existing row before appending.** The script's duplicate check ignores case, but near-synonyms slip through: grep the term first and enrich the existing row instead of adding a second one.

4b. **Deep dive (optional, ~3 sections/session).** Only for terms the user must *say out loud* under pressure. Append a section to the topic's `deep-dive.md` by hand (no script), same order as the glossary:

```markdown
## <term>
**Say first:** one or two plain sentences: what it is, what I use it for, the main trap. Depth is shown by use and failure modes, not by vocabulary (`grading.depth_note`). Short clauses - a long impressive B1-B2 sentence breaks in the middle.
**If pushed:** the mechanism and the precise term, for when someone asks *how*. Never the opener; leading with textbook wording reads as memorized.
**Trap:** the trap the user actually hit this session.
```

   Create the file with an `# <TOPIC> deep dive` heading if it does not exist yet.

5. **Write rows** with the script (keeps the table intact, handles `|`, skips duplicates). `deep-dive.md` is prose - append it by hand, not with the script:

```bash
python3 .claude/skills/session-log/scripts/append_row.py topics/<name>/error-log.md --check
python3 .claude/skills/session-log/scripts/append_row.py topics/<name>/error-log.md \
  "<today>" "<question>" "<my answer>" "<correct, one line>" "<cause>" "<fix drill>" "<today+2d>, +7d <today+7d>"
```

   Use today's date from the environment, never a guess.

   The script rejects an error-log row with any empty cell, a `Cause` outside the configured set,
   or a `Re-test` without a `YYYY-MM-DD` date, and writes nothing. Do not invent a value to get
   past it: ask the user for the missing piece, then re-run.
   Then check the rows you just wrote: `python3 scripts/validate.py --project . --topic <name>`. An ERROR
   names a malformed cell (bad `Cause`, a `Re-test` cell with no date, a wrong cell count) - fix
   it now, while the row is still in front of you.

6. **Flashcards.** Produce 2-5 cloze cards, one idea each, from the rows just written, in a short list the user can paste into Anki: `A {{c1::trigger}} means the move is {{c2::the action}}.` Nothing the user did not produce.
7. **Close the loop with `coach`.** The rows are written, but the status file still says the day did not happen: the daily log row, the streak and the week's block count live there and only `coach` writes them. End every run by telling the user to run `/coach done` (or `skipped`), with the one-line note ready for them to paste. Do not write the status file yourself.
8. **Next reviews and next step.** One line: what to recall tomorrow, and the +2d / +7d re-do item (`active-revise` ladder). One line: the next step, so the next block restarts fast.

## Update TOPIC.md

After writing rows, update the topic's `TOPIC.md`: add the session's hours to **Hours spent**, set **Next action** to the one-line next step, and change a subtopic's Level only when the user showed it alone in this session (never on an AI-assisted pass). Do not change **State**; `coach` owns state changes.

## Output

Short summary: rows added (with table path), glossary terms added, deep-dive sections written, cards, next review, next step, and the `/coach done` reminder. If any write printed `skip:` or `error:`, say so plainly.

## Do not

- Write the Cause column without the user's pick.
- Write a row that names a topic instead of the exact gap.
- Append a near-duplicate of an existing row, or blow past the row cap because every miss "feels important". Merge by pattern.
- Add terms or mistakes the user did not meet in the session.
- Write a multi-paragraph glossary cell. Long content belongs in `deep-dive.md`.
- Edit anything except the first table (and Parking lot bullets).
