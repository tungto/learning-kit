---
name: create-lesson
description: Author or revise one self-contained HTML lesson inside a teaching workspace - pick the number, write the file into `./lessons/`, build it from the components in `./assets/`, and keep the folder indexes and footer nav current. Called by `teach` once it has decided what to teach, or directly when the thing to produce is a lesson file.
argument-hint: "Which lesson, and in which topic?"
---

You are writing one lesson: a single, self-contained HTML file that teaches one tightly-scoped
thing tied to the mission. This is the primary unit of teaching in the workspace.

What to teach is not decided here. If it is not already settled, that is a
[teach](../teach/SKILL.md) job: the mission, the zone of proximal development and the choice of
subtopic come from there.

## Workspace

The workspace is one topic folder, not the whole project. Read `teach.workspace_root` in
`learning.config.json` (default `topics/<name>`) and resolve every workspace path (`./lessons/`,
`./assets/` and the rest) inside the folder of the topic being taught. `teach.allow` lists the
files and folders this project lets this skill write: nothing outside that list, and never the
plan, the status file or a `TOPIC.md` cell - those belong to `coach` and `session-log`. A lesson is
never evidence for a level change.

## Before writing

Read, in this order:

1. `MISSION.md` - the reason the user is learning this. Every lesson ties back to it.
2. `NOTES.md` - stated preferences for how they want to be taught.
3. The highest-numbered files in `./learning-records/` - what is already known, so the lesson lands
   in the zone of proximal development instead of re-teaching.
4. `./assets/` - the components that already exist. Reuse is the default, not the exception.
5. `./lessons/` and `./reference/` - the neighbouring material to cross-link, and the highest
   lesson number.

## The file

Save to `./lessons/NNNN-<dash-case-name>.html`, where `NNNN` is the highest existing number plus
one, zero-padded to four digits.

A lesson should be **beautiful**, with clean, readable typography and layout, since the user will
return to these later to review. Think Tufte.

The lesson should be short, and completable very quickly. Learners' working memory is very small,
and we need to stay within it. But each lesson should give the user a single tangible win that they
can build on. It should be directly tied to the mission, and should be in the user's zone of
proximal development.

**Light theme is the default, always** (`teach.lesson_theme`, default `"light"`). Every HTML file
this skill writes - lessons, reference documents, anything in `./assets/` - opens in light mode
regardless of the operating system setting. Write `<html lang="en" data-theme="light">` on the root
element of every page. A stylesheet may still define a dark palette, but it must be opt-in only:
guard it as `:root[data-theme="dark"]`, and if a `@media (prefers-color-scheme: dark)` block
exists, guard it with `:root:not([data-theme="light"])` so the explicit attribute wins. Never ship
a page that turns dark on its own - these documents are made to print and to be read in the
morning.

## Look and structure

Before writing any HTML, read [references/style-guide.md](references/style-guide.md): the two page
shapes (lesson, reference), the order of a page, the writing rules, what each component is for, how
to draw a diagram, and the checklist a page must pass before you call it done.

The kit ships the starting point in this skill's `assets/`:

- `lesson.css` and `lesson.js` - the shared stylesheet and behaviour (rail, scroll-spy, opt-in dark
  toggle, diagram pause/restart). If the topic's `./assets/` has no stylesheet yet, copy both there
  first; that is the workspace's first component. If it already has one, use it and never overwrite
  it - the topic's copy may have grown.
- `skeleton-lesson.html` (one column, short) and `skeleton-reference.html` (rail + parts, for
  reference pages, reports and tutorials). Start from the matching one and replace every `{{...}}`.

## What every lesson carries

- **Citations** (`teach.require_citations`, default `true`). Lessons should be littered with
  citations - links to external resources to back up any claim made. A claim with no link is the
  AI's memory, not knowledge. Draw them from `RESOURCES.md`; when a lesson earns a new trusted
  source, add it there.
- **One primary source** to read or watch: the most high-quality, high-trust resource found on the
  topic.
- **A reminder to ask followup questions to the agent.** The agent is their teacher, and can assist
  with anything that's unclear.
- **Links via HTML anchors** to other lessons and reference documents.
- **A feedback loop**, when the lesson practises a skill rather than delivering knowledge: quizzes
  or light in-browser tasks, feedback immediate and ideally automatic. The design rules for this -
  fluency versus storage strength, retrieval, spacing, interleaving, and how to write quiz answers
  that give nothing away - live in [teach](../teach/SKILL.md) under `## Skills`.

## Keep the indexes current

Every folder of HTML (`./lessons/`, `./reference/`, `./drills/`, ...) holds an `index.html` listing
its files with title, one-line summary and a cross-link to the same subtopic in the sibling
folders. The workspace root holds an `index.html` hub linking those folder indexes and the control
files. After writing or renaming any lesson or reference document, update both, and end every page
with a footer nav (`<p class="crumb" data-nav-footer>`) back to its folder index, the topic hub and
its sibling-folder counterpart.

## Assets

Lessons are built from reusable **components**, stored in `./assets/`: stylesheets, quiz widgets,
simulators, diagram helpers, and anything else a second lesson could reuse.

Reuse is the default, not the exception. Before authoring a lesson, read `./assets/` and build from
the components already there. When a lesson needs something new and reusable, write it as a
component in `./assets/` and link to it; never inline code a future lesson would duplicate.

A shared stylesheet is the first component every workspace earns: every lesson links it, so the
lessons look like one consistent course rather than a pile of one-offs. As the workspace grows, so
should the component library.

## When the lesson is written

Say which file was written and which indexes were updated. Do not write a `TOPIC.md` cell to
register it - that file has one writer, and it is not this skill.

If possible, open the lesson file for the user by running a CLI command.
