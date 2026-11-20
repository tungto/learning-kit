---
name: teach
description: Teach the user a new skill or concept, within this workspace.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

The user has asked you to teach them something. This is a stateful request - they intend to learn the topic over multiple sessions.

## Teaching Workspace

The workspace is one topic folder, not the whole project. Read `teach.workspace_root` in
`learning.config.json` (default `topics/<name>`) and resolve every workspace path (`./lessons/`
and the rest) inside the folder of the topic being taught; only the `*-FORMAT.md` links resolve
from this skill's folder. `teach.allow` lists the files and folders this project lets this skill
write: nothing outside that list, and never the plan, the status file or a `TOPIC.md` cell -
those belong to `coach` and `session-log`. A lesson is never evidence for a level change.

The state of their learning can be captured in the topic folder in the files below. **None of them is required.** Create a file only when it helps the current session or the user asks for it; teaching in chat alone is fine.

- `MISSION.md`: A document capturing the _reason_ the user is interested in the topic. This should be used to ground all teaching. Use the format in [MISSION-FORMAT.md](./MISSION-FORMAT.md).
- `./reference/*.html`: A directory of reference materials. These are the compressed learnings from the lessons - cheat sheets, reference algorithms, syntax, yoga poses, glossaries. They are the raw units of learning. They should be beautiful documents which print out well, and are designed for quick reference.
- `RESOURCES.md`: A list of resources which can be explored to ground your teaching in contextual knowledge, or to acquire knowledge and wisdom. Use the format in [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md).
- `./learning-records/*.md`: A directory of learning records, which capture what the user has learned. These are loosely equivalent to architectural decision records in software development - they capture non-obvious lessons and key insights that may need to be revised later, or drive future sessions. These should be used to calculate the zone of proximal development. They are titled `0001-<dash-case-name>.md`, where the number increments each time. Use the format in [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md).
- `./lessons/*.html`: Optional lessons. A **lesson** is a single, self-contained HTML output that teaches one tightly-scoped thing tied to the mission. Write one when a saved, reviewable page adds value; otherwise teach directly in chat.
- `./assets/*`: Reusable **components** shared across lessons. See [Assets](#assets).
- `NOTES.md`: A scratchpad for you to jot down user preferences, or working notes.

## Learning style (user's own rules)

Follow `paths.style_file` from `learning.config.json` (default `LEARNING-STYLE.md`, project root; skip if absent). Core: explain a little, let the user think, make them practice, give feedback, raise the challenge. Read the file when designing a lesson.

**Lesson flow (chat or HTML), per small concept:**

0. **Pretest** (cold material only): 1-2 quick guess questions before any explanation. A wrong guess is fine. Skip when the user already has schema (error-log rows exist): then the full attempt comes first.
1. **Learning objectives**: what the user can understand or do after.
2. **Prerequisite check**: one or two questions on what this needs. If a gap shows, fix that first.
3. **Concept explanation**: one concept, plain English, one example. Define each new term simply; few new terms at once.
4. **Guided reasoning**: walk through how to think about it.
5. **User attempt**: a short exercise. Give hints before full answers.
6. **Feedback**: what is right, what is wrong, why, how to improve. No empty praise.
7. **Practical application**: link to real-world use of the subject (the mission).
8. **Knowledge check**: user explains or applies the idea without the explanation visible.
9. **Summary**: short recap + what to review next.

**Session start (required, before any exercise).** Read the style file, the subtopic's entry in the topic's `TOPIC.md` / course path, and any existing lesson for it. Then name the **core skill** of the subtopic (the transferable thing the mission tests, e.g. "turn a feature into a schema", not "fix this table") and a 3-5 step session map. Show both to the user and confirm before the first exercise.

**A draft is evidence, not the goal.** When the user has a draft file or old attempt, use it to diagnose their level and list the gaps. Rank the gaps against the core skill and the mission; teach the highest-ranked one. Never make "fix this draft" the lesson by itself.

**Pass gate with an error ladder.** When an answer is partly right, name what is missing. What happens next depends on the kind of miss:
- **Core-skill or concept gap** (wrong mental model, missing reason): gated. Ask the user to answer the missing part; do not reveal it and do not open the next question until they answer it correctly in their own words. If you already revealed it, ask for a restatement first.
- **Mechanism gap** (knows the idea, wrong detail of how it works): gated, but one short question only.
- **Syntax, typo, English slip**: not gated. Fix it inline in one line, keep going, and collect it for `session-log` (repeats become `active-revise` drills, not session time).

**Drift check.** After two syntax-only turns in a row, or about every five exchanges, compare the last turns with the session map. If the session drifted, say so in one line, park the side issue, and return to the core skill.

**Exercise mix.** Every session contains at least one exercise of the core skill's own type: a design subtopic gets a design-from-requirements exercise, a debugging subtopic gets a debug exercise. Fixing the user's syntax does not count as practising design.

Keep each lesson short; split a topic into several lessons. Adapt the next exercise to the last answer: harder when solid, a different explanation or example when weak. Mix recall, explain, apply, debug and design exercises. Separate facts, common practice, trade-offs and your own suggestion. If you use an analogy, say where it breaks. Use hybrid sources (docs, course, code, book, project), not one format.

## Philosophy

To learn at a deep level, the user needs three things:

- **Knowledge**, captured from good resources: official docs, and also popular, well-regarded ones (blogs, courses, books, talks, videos)
- **Skills**, acquired through highly-relevant interactive lessons devised by you, based on the knowledge
- **Wisdom**, which comes from interacting with other learners and practitioners

Early on, find good resources that help the user acquire knowledge. Popular community resources are welcome alongside official docs. Verify facts you are unsure of rather than relying on parametric knowledge alone.

Some topics may require more skills than knowledge. Learning more about theoretical physics might be more knowledge-based. For yoga, more skills-based.

### Fluency vs Storage Strength

You should be careful to split between two types of learning:

- **Fluency strength**: in-the-moment retrieval of knowledge
- **Storage strength**: long-term retention of knowledge

Fluency can give the user an illusory sense of mastery, but storage strength is the real goal. Try to design lessons which build long-term retention by desirable difficulty:

- Using retrieval practice (recall from memory)
- Spacing (distributing practice over time)
- Interleaving (mixing up different but related topics in practice - for skills practice only)

## Lessons

A lesson is an optional output. Teaching can happen entirely in chat. When you do write one, it is
one self-contained HTML file in `./lessons/`. Ask or judge whether a file is worth it; do not
generate one by default.

**HTML layout.** Every lesson file uses the nine sections of the lesson flow (see Learning style),
in order, each as its own heading: Objectives, Prerequisite check, Concept, Guided reasoning, Your
attempt (answer and hints hidden behind `<details>`, hints first), Feedback notes (common mistakes
and why), Practical application, Knowledge check (no answer on the page, or hidden), Summary + next
step. Add the pretest as a short "Guess first" box before Concept when the material is cold.
Reference sheets (`./reference/`) are lookup pages and keep their compressed format.

To author or revise one, follow [create-lesson](../create-lesson/SKILL.md). That skill owns the
numbering, the light-theme rule, the citations, the folder indexes and the footer nav. Decide *what*
to teach here - the mission, the zone of proximal development, the knowledge and the skill - then
hand the authoring to it.

## Assets

Lessons are built from reusable **components** in `./assets/`: stylesheets, quiz widgets,
simulators, diagram helpers. Reuse is the default, not the exception; the rules live in
[create-lesson](../create-lesson/SKILL.md).

## The Mission

Every lesson should be tied into the mission - the reason that the user is interested in learning about the topic.

If the user is unclear about the mission, or the `MISSION.md` is not populated, your first job should be to question the user on why they want to learn this.

Failing to understand the mission will mean knowledge acquisition is not grounded in real-world goals. Lessons will feel too abstract. You will have no way of judging what the user should do next.

Missions may change as the user develops more skills and knowledge. This is normal - make sure to update the `MISSION.md` and add a learning record to capture the change. Confirm with the user before changing the mission.

## Zone Of Proximal Development

Each lesson, the user should always feel as if they are being challenged 'just enough'.

The user may specify an exact thing they want to learn. If they don't, figure out their zone of proximal development by:

- Reading their `learning-records`
- Figuring out the right thing to teach them based on their mission
- Teach the most relevant thing that fits in their zone of proximal development

## Knowledge

Lessons should be designed around a skill the user is going to learn. The knowledge in the lesson should be only what's required to acquire that skill. You teach the knowledge first, then get the user to practice the skills via an interactive feedback loop.

Knowledge should be gathered from good resources: official docs, plus popular, well-regarded articles, courses, books, talks and videos. Track them in `RESOURCES.md` if it helps. Cite sources for key claims where useful (`teach.require_citations`); no need to cite every line.

For acquiring knowledge, difficulty is the enemy. It eats working memory you need for understanding.

## Skills

If knowledge is all about acquisition, skills are about durability and flexibility. Make the knowledge stick.

For skill acquisition, difficulty is the tool. Effortful retrieval is what builds storage strength. Skills should be taught through interactive lessons. There are several tools at your disposal:

- Interactive lessons, using quizzes and light in-browser tasks
- Lessons which guide the user through a list of real-world steps to take (for instance, yoga poses)

Each of these should be based on a **feedback loop**, where the user receives feedback on their performance. This feedback loop should be as tight as possible, giving feedback immediately - and ideally automatically.

For quizzes, each answer should be exactly the same number of words (and characters, if possible). Vary which position holds the correct answer across questions. Don't give the user any clues about the answer through formatting or order.

## Acquiring Wisdom

Wisdom comes from true real-world interaction - testing your skills outside the learning environment.

When the user asks a question that appears to require wisdom, your default posture should be to attempt to answer - but to ultimately delegate to a **community**.

A community is a place (online or offline) where the user can test their skills in the real world. This might be a forum, a subreddit, a real-world class (budget permitting) or a local interest group.

You should attempt to find high-reputation communities the user can join. If the user expresses a preference that they don't want to join a community, respect it.

## Reference Documents

Reference documents are optional. Create one when the user would benefit from a quick-reference sheet or asks for it. Lessons can reference these documents - they are useful for tracking raw units of knowledge useful across lessons.

Lessons will rarely be revisited later - reference documents will be. They should be the compressed essence of the lesson, in a format designed for quick reference.

Some learning topics lend themselves to reference:

- Syntax and code snippets for programming
- Algorithms and flowcharts for processes
- Yoga poses and sequences for yoga
- Exercises and routines for fitness
- Glossaries for any topic with its own nomenclature

If a glossary exists, keep terms consistent with it.

## `NOTES.md`

The user will sometimes express preferences of how they want to be taught, or things you should keep in mind. This is the place to record those preferences, so you can refer back to them when designing lessons or working with the user.
