# Core principles for a learning system

Portable core. Use it when **building, auditing or repairing** any system that has to move a
skill from "I read about it" to "I can do it alone, a month later, under pressure": interview
prep, a language, a new stack, a habit.

Nothing here names a company, a week count or an hour budget. Those are the **instance**. This
file is the **rules the instance must obey**. This repo's instance lives in
the project's `PLAN.md` and `learning.config.json`.

> **Every number in this file is a default, not a finding.** "Under 20 minutes", "about three
> outcomes", "~25 minutes", "three weeks", "2 minutes aloud": starting values, chosen to be
> concrete enough to test. Law 0.6 applies to this file too. Replace any of them with your own
> data as soon as you have some.

Each law has four fields on purpose. A law without a named anti-pattern is a slogan. A law
without a test cannot be checked.

```
Law → Why → Anti-pattern it prevents → Test that you followed it
```

## The four pillars

| Pillar | One line |
|---|---|
| 0. Design | Build the smallest system that survives a bad week, and let it learn. |
| 1. Cognition | Knowledge enters by producing, stays by spacing, proves itself cold. |
| 2. Productivity | The calendar does the deciding; energy, not hours, is the scarce input. |
| 3. Behaviour | The system's first job is to still exist in week 20. |
| 4. AI | AI is the examiner and the clerk, never the explainer of first resort. |

## If you keep only seven

1. **Produce before you consume** (1.1). Attempt, then check.
2. **Errors are the curriculum** (1.2). Log the miss, the cause, the re-test date.
3. **One tracker, and the next action is never blank** (0.2, 0.3).
4. **The minimum counts** (2.5, 3.1). Continuity beats content.
5. **Cold and alone, or it is not a level** (mastery ladder).
6. **AI examines; you produce** (4.1, 4.8).
7. **The system reviews itself on a cadence** (0.9). Otherwise it drifts until you quit.

---

## 0. Design laws — how to build the system itself

**0.1 Systems before mindset.**
Why: motivation is an output of visible progress, not an input you can summon.
Anti-pattern: a re-read of a motivation book instead of a fixed block in the calendar.
Test: a stranger could run your week from the written plan without asking how you feel.

**0.2 Exactly one tracker, and it answers three questions.**
Why: what is next, how far I came, what to expect. Two trackers means neither is true.
Anti-pattern: a second dashboard, a parallel Notion board, a spreadsheet nobody updates.
Test: name the one file. Every other file is notes, not state.

**0.3 The next action is never blank.**
Why: a blank next step is where abandonment starts. Deciding costs more will than doing.
Anti-pattern: ending a session with "continue studying X".
Test: open the tracker cold. One concrete line tells you what to do in the next 30 minutes.

**0.4 The map sets the target; the day's task pulls the topic.**
Why: pure just-in-time learning becomes patchwork; a pure curriculum ignores real feedback.
Anti-pattern: studying a topic because it is next in a list nothing depends on.
Test: for today's task, name the capability it serves and where that sits on the map.

**0.5 Cut scope in a written order; never add features under stress.**
Why: under pressure you will improvise, and improvisation under stress means quitting.
Anti-pattern: a bad week answered with a redesign, a new tool or a new tracker.
Test: the order of cuts is written down before the first bad week, and the last cut is
"park a topic", not "stop".

**0.6 Mark design choices as choices.**
Why: inventing precision destroys trust in the whole system when one number fails.
Anti-pattern: "study in 52-minute blocks" presented as science.
Test: every number in the plan is either sourced or labelled a default with a review date.

**0.7 No tooling for a system younger than three weeks.**
Why: tool-building is the most enjoyable form of avoidance.
Anti-pattern: week 2 spent on automation, week 3 spent on nothing.
Test: no tool work on a system that has not survived three weeks, and any later tool names the
specific pain it removes.

**0.8 Measure aliveness separately from skill.**
Why: adherence says the system runs. It says nothing about ability.
Anti-pattern: "I did every block" read as "I am ready".
Test: two different bars exist — one for blocks done, one for cold performance.

**0.9 The system reviews itself on a fixed cadence.**
Why: a plan with no review slot cannot learn from your data, so it drifts until you abandon it.
This is the load-bearing law: most of the others are only enforced because a review asks.
Anti-pattern: a plan edited only in a crisis, or never.
Test: a recurring slot exists whose output is the next period's outcomes, the next action, and
**at most one** change to the system itself.

**0.10 A topic earns its slot on demand, cost and effect.**
Why: breadth you were never asked for is the most expensive way to feel productive.
Anti-pattern: learning the trending tool; adding a subject for the CV; equal time to everything.
Test: before anything enters the plan, name (a) how often the real target asks for it, (b) your
level and the learning cost, (c) whether it changes your chance of *getting* or of *passing*.
Weak on all three: explain-only, or out. Also name the critical fraction of a topic that unlocks
most of it, and spend there first.

---

## 1. Cognition — how knowledge gets in and stays

**1.1 Produce before you consume.**
Why: retrieval is one of the two highest-utility techniques known. Predicting badly beats
reading well.
Anti-pattern: open the docs, open the AI, then "learn".
Test: for each item, you wrote, said or coded an attempt before seeing any answer.

**1.2 Errors are the curriculum.**
Why: a logged miss is the most reliable signal of your real edge.
Anti-pattern: a miss noticed, understood in the moment, and never written down.
Test: every miss is logged the same session, with a cause and a re-test date. Zero rows is
valid **only** if nothing was missed — never a row invented to fill the quota.

**1.3 Classify the cause, not just the error.**
Why: a concept gap, a careless slip and a comprehension gap need three different fixes.
Anti-pattern: drilling more content when the real failure was misreading the question.
Test: each logged miss carries one cause tag — concept, careless, comprehension — and the drill
matches the tag. (This repo's instance names the third tag `English`; same thing.)

**1.4 Chunk the pattern, not the solution.**
Why: experts store "when I see X, the move is Y". Memorised instances do not transfer.
Anti-pattern: 200 solved problems, no written patterns.
Test: after solving, you can state the trigger and the move in one line, without the problem.

**1.5 Work at the edge.**
Why: re-practising what you already own cold buys nothing; the log tells you where the edge is.
Anti-pattern: re-doing passing material because it feels productive.
Test: the items you practised are ones that failed, or were never tested cold — not ones already
passing at a long interval.

**1.5b Calibrate the edge by hit rate, not by feel.**
Why: "it failed before" is not one difficulty. A set you pass 95% of is comfort wearing the
costume of practice; a set you pass 30% of teaches nothing and burns the slot (1.9, 2.8). The
edge is the band where effort is needed and the attempt still usually lands. **Default: aim for
roughly 80-90% correct on a practice set, measured on cold attempts.** Review this number
against your own re-test data (0.6) — it is a starting value, not a finding.
Anti-pattern: a drill set chosen because the items are tagged failed, with no check on how many
you now pass; grinding a set you fail most of and calling it discipline.
Test: for the last practice set you can state the cold hit rate, and what you did about it —
well above the band: raise a constraint (1.13) or move to the next rung; well below: decompose
the task until one piece sits in the band, or scaffold it (4.6) and re-test blank the same day
(4.3).

**1.6 Space on a ladder, and a fail drops back to the first rung.**
Why: spacing is the other of the two highest-utility techniques. A pass you cannot repeat later
is not a pass.
Anti-pattern: reviewing on the day you feel like it; counting a hinted answer as a pass.
Test: each item has a next-review date, moving up on cold passes and back to the first rung on
a fail or a guess.

**1.7 Interleave confusable neighbours only.**
Why: mixing helps where *choosing the method* is the hard part. Mixing unrelated new topics is
just task switching.
Anti-pattern: labelled drills forever, or a block that jumps between three unrelated subjects.
Test: learn a type blocked, then mix it with its siblings once two or more are learned, with
the labels removed.

**1.8 Big picture before detail.**
Why: details with no map are unattachable and decay fast.
Anti-pattern: line-by-line reading from page one.
Test: before the detail, you can draw or say the shape of the whole thing in a few sentences.

**1.9 Escalate when stuck, in this order.**
Why: struggle is where the learning is, but unbounded struggle is just lost time, and a hint
taken too early throws the retrieval away. The order matters more than any single step.
Anti-pattern: three unbroken hours against one blocker; or asking for the answer at minute two.
Sequence: **struggle (~20-25 min) → write down exactly where you are stuck → smallest possible
hint → leave it (walk, sleep: the connections form away from the desk) → redo from blank the
next day.**
Test: for your last blocker, you can name which step you were on and when you moved.

**1.10 Explaining simply is the proof, not the decoration.**
Why: plain-language explanation exposes gaps every other format hides.
Anti-pattern: "I understand it, I just can't put it in words."
Test: 2 minutes, out loud, no notes, plus two follow-up questions survived.

**1.11 Assume illusions of competence by default.**
Why: recognition feels identical to recall from the inside, and is not it.
Anti-pattern: highlighting, re-reading, nodding at a worked solution, solving with notes open.
Test: every claim of knowing traces to a closed-book attempt, not to familiarity.

**1.12 Working memory is small, so externalise.**
Why: load spent holding state is load not spent thinking. Usable estimates sit around four
chunks.
Anti-pattern: tracking a whole design in your head and blaming your intelligence.
Test: diagrams, intermediate steps and state written down during hard work.

**1.13 Transfer by variation.**
Why: an idea only owned in one setting is owned in no setting.
Anti-pattern: the same exercise, same framing, repeated.
Test: you re-did the idea with a changed constraint, language or scale, and it held.

**1.14 Sleep and movement are part of the method.**
Why: consolidation happens in sleep; exercise supports the hardware.
Anti-pattern: cutting sleep to add study hours, then calling the result a motivation problem.
Test: the plan never borrows hours from sleep or exercise.

**1.15 Fix blocking gaps first; demote the rest to drills.**
Why: a gap that the next topic depends on will fail that topic too. A gap that blocks nothing
must not be allowed to stop everything.
Anti-pattern: perfecting one topic while its dependents wait; or moving on over a gap the next
topic needs.
Test: for each open gap, you can say what it blocks. Blocks the next topic → fix now. Blocks
nothing → it becomes a spaced drill and you move on.

---

## 2. Productivity — how the work actually happens

**2.1 Calendar and if-then rules, not willpower.**
Why: a pre-committed cue beats a plain intention by a wide margin.
Anti-pattern: "I'll fit it in when I can."
Test: fixed slots, same time and place, plus one if-then rule per slot ("if coffee poured,
then cards").

**2.2 Hardest work at your energy peak.**
Why: a new concept at a trough costs double and sticks half.
Anti-pattern: new material late at night because the slot was free.
Test: new and hard material sits in the measured peak window; the trough gets review and admin.

**2.3 One subject per block; switch only on a finished unit.**
Why: every switch costs time and errors, and half-units are hard to restart.
Anti-pattern: four subjects in one sitting, none closed.
Test: each block ends with something complete — a test passing, a problem logged, a commit.

**2.4 Always leave a "next step" line.**
Why: restart cost is the real tax on interrupted work.
Anti-pattern: tomorrow's first 20 minutes spent rebuilding yesterday's context.
Test: the last artefact of every block is one line naming the next move.

**2.5 Every task has a minimum, a target and a stretch.**
Why: tasks that only exist at full size get skipped whole.
Anti-pattern: all-or-nothing tasks, and a stretch outcome quietly treated as the target.
Test: before starting, you named the level you booked for the time you actually have.

**2.6 Choose the task from the time you have, not the time you wish for.**
Why: planning against imaginary time produces zeros, not shortfalls.
Anti-pattern: a 2-hour task started in a 30-minute gap, abandoned at the interesting part.
Test: the task's minimum fits inside the real slot.

**2.7 Hours are never owed. Bars are.**
Why: two different debts get confused. Debt in **hours** accumulates into dread and ends
systems, so a skipped target or stretch is simply gone. Debt in **unmet pass bars** is the
curriculum: it does not expire, and it is paid through remediation, not through catch-up hours.
Anti-pattern: a make-up weekend and an owed-hours backlog; or an unmet bar quietly skipped
because "nothing is owed".
Test: no file tracks owed hours. Every unmet bar has a drill and a re-test date.

**2.8 Never learn on empty.**
Why: low-energy study produces the feeling of work and none of the result.
Anti-pattern: pushing a new concept while tired, then logging the failure as weakness.
Test: a named fallback exists for empty days (review, shadowing, rest) and using it counts.

**2.9 Stop a block that has stopped working.**
Why: the same slip twice, or reading without recalling, means the session is over.
Anti-pattern: serving the clock instead of the outcome.
Test: you can point to blocks you ended early, with a next-step line.

**2.10 Protected time is not budget.**
Why: sleep, exercise and at least one free evening are the inputs, not slack.
Anti-pattern: a plan that balances by taking the one free evening.
Test: the protected items are listed, and no version of the plan schedules over them.

**2.11 Free time is not a duty.**
Why: filling every gap is how a sustainable load becomes a burnout load silently.
Anti-pattern: adding an unplanned subject because an hour appeared.
Test: extra time only ever goes to light or already-planned work, and rest is a valid choice.

---

## 3. Behaviour — how you keep going long enough to win

**3.1 Protect continuity before you protect content — two knobs, not one.**
Why: the dominant failure mode of self-directed learning is stopping, not studying wrongly. So
**starting must be trivial and passing must be hard**: one knob cannot serve both. Easy starting
protects the streak; a hard bar protects the learning.
Anti-pattern: a heroic daily minimum (90 minutes or nothing) with soft self-grading inside it.
Test: the minimum day takes minutes, counts for the streak, and the pass bar still needs no
notes and no AI.

**3.2 Make progress visible, weekly.**
Why: visible progress and small wins are what actually restore motivation.
Anti-pattern: progress that only exists as a feeling, or only as a distant goal.
Test: one artefact per week you can point at — a streak, a score, a working thing.

**3.3 Keep agency.**
Why: burnout tracks high expectation combined with low control. The plan must be yours.
Anti-pattern: a fixed curriculum handed down with no weekly choice inside it.
Test: you pick the week's small number of outcomes yourself.

**3.4 Cap the week at a small number of outcomes.**
Why: more open fronts means less finished, and finishing is the fuel.
Anti-pattern: a ten-item week, four done, read as failure.
Test: the week names about three outcomes, and they fit the minimum budget.

**3.5 One primary focus, with planned secondaries.**
Why: parallel tracks keep slow skills alive; an unbounded number guarantees topic hopping.
Anti-pattern: starting a subject because it is interesting today.
Test: the primary is named before the week starts; a secondary runs only if planned, unblocked
and affordable.

**3.6 Two bad weeks means replan, not push harder.**
Why: repeated misses are information about the plan, not about your character.
Anti-pattern: answering a shortfall with more load, then quitting a week later.
Test: a written trigger exists ("two minimum weeks in a row → replan") and it has teeth.

**3.7 Start dreaded tasks small and keep the wins visible.**
Why: the avoided task is usually the highest-value one, and it only unblocks by shrinking.
Anti-pattern: scheduling the dreaded thing at full size, repeatedly, and moving it each week.
Test: each dreaded area has a 10-minute version in the plan, and a record of wins.

**3.8 Expose yourself to the real conditions early and often.**
Why: skill under pressure is a separate skill; anxiety eats working memory.
Anti-pattern: perfect practice in comfort, collapse in the real round.
Test: recurring timed, spoken or observed reps, not only quiet solo work.

**3.9 Train the recovery behaviour, not just the answer.**
Why: in real performance you will be stuck. What you do in that moment is trainable.
Anti-pattern: practising only known material, so "stuck" has no rehearsed response.
Test: you have a first-sentence frame and a rule to keep going instead of stopping.

**3.10 Claim only what you built and tested.**
Why: an invented number collapses under one follow-up question, and takes your credibility.
Anti-pattern: rounded-up impact in a story or a CV.
Test: every claim maps to an artefact you can show.

**3.11 Re-allocate from evidence, not from the calendar.**
Why: 3.6 fires when the system stalls. This one fires when the system runs fine and is still
aimed wrong. Any split of effort is a hypothesis; real performances are the data.
Anti-pattern: keeping the original split after two real rounds exposed the same weakness; or
re-cutting the plan after one bad day.
Test: when two real performances or two checkpoints show the same gap, effort moves between
areas at the next review, and the change plus its end date is written in the tracker.

---

## 4. AI collaboration — how the AI must behave

**4.1 AI is the examiner, not the explainer of first resort.**
Why: offloading reasoning builds dependence that the real test exposes.
Scope: orientation is allowed — a map, the scope, the vocabulary, "what are the five things here"
(see 1.8). What is not allowed is the **answer to the question in front of you**.
Anti-pattern: asking for the explanation, feeling clarity, retaining nothing.
Test: the AI's first move on today's *exercise* is a question to you, not a solution.

**4.2 Try first, then reveal. Always.**
Why: the attempt is where the learning happens; the reveal only corrects it.
Anti-pattern: the AI writing the exercise solution before you attempt it.
Test: nothing that answers today's task appears in the transcript above your attempt.

**4.3 Loop back after any help.**
Why: an understood explanation is not a reproducible skill.
Anti-pattern: "that makes sense" as the end of the session.
Test: same day, from a blank file or blank page, alone, you redid it.

**4.4 Make the AI argue against you.**
Why: agreeable feedback hides the gap a hostile interviewer will find.
Anti-pattern: a confirming AI and a surprising rejection.
Test: once per topic, "argue against my answer; what would a skeptical senior say?".

**4.5 Hold a stated bar, and name it.**
Why: without a bar, "it works" passes.
Anti-pattern: accepting a working answer with no trade-off, failure mode, scale or cost.
Test: the AI pushes on why this, what breaks, what at 10x, what it costs.

**4.6 Hints before answers, in steps.**
Why: the smallest unblocking nudge preserves the retrieval.
Anti-pattern: a full solution in response to "I'm stuck".
Test: help arrives as a hint, then a bigger hint, then the answer.

**4.7 State your constraints in the prompt, every time.**
Why: the AI defaults to its own register, not yours — language level, depth, format, time.
Anti-pattern: a wall of jargon you half-understand and cannot challenge.
Test: a standing modifier in your prompts (plain language, define jargon once, short, and for
a second language: list my language mistakes separately from the technical feedback).

**4.8 The AI writes the record; you produce the knowledge.**
Why: a clerk that invents content corrupts the only honest signal you have.
Anti-pattern: logs and glossaries filled with the AI's words you never produced.
Test: every logged row traces to something you said, wrote or coded.

**4.9 Verify anything versioned, priced or recent.**
Why: model memory ages, and confident wrong facts are worse than gaps.
Anti-pattern: quoting a stale version, price or trend in a real conversation.
Test: such claims are searched, dated, or marked unverified.

**4.10 Review AI output like a teammate's pull request.**
Why: judging an answer is now the skill, and a plausible wrong answer is the common case.
Reviewing it is also free practice at the bar you are trying to reach.
Anti-pattern: running or repeating AI output because it looks right.
Test: per AI-assisted task, you can name where it was wrong — or state that you checked it
against the edge cases and found nothing.

**4.11 Keep one human touchpoint.**
Why: AI cannot simulate a real audience, real impatience or real conversational repair.
Anti-pattern: a year of fluent AI conversation and a frozen first human round.
Test: a recurring slot with a real person exists in the plan.

**4.12 Separate the roles, and name the role per block.**
Why: an AI doing everything at once drifts into explaining.
Anti-pattern: one undifferentiated chat per session.
Test: the block declares the role — examiner, Socratic questioner, checker, listener, clerk,
sparring partner.

---

## Mastery ladder

| Level | You can |
|---|---|
| L1 | recognise it |
| L2 | predict what it does |
| L3 | implement it alone from blank |
| L4 | debug it and name the cause |
| L5 | explain it aloud and handle follow-ups |
| L6 | apply it in a real project or realistic scenario |

Rules that make the ladder mean something:

- **Per subject.** A level in one subject is no evidence for another.
- **Exposure is not a level.** Read, watched, or did it with help = no level yet.
- **Cold and alone, or it does not count.** No notes, no AI, no hints. A guess is a fail.
- **A level is only *kept* when a delayed re-test passes.** A week later or more.
- **Not every topic needs L6.** Each category gets its own bar, written before you study it.
  Some topics are explain-only by design (0.10).
- **Levels are not effort.** Minimum/target/stretch measures what you booked in a sitting.
  Finishing a stretch is not a level. Doing every block proves nothing by itself (0.8).
- **Advance on mastery, not on the calendar.** Dates are a forecast. Bar met and kept →
  continue. Bar met, delayed re-test failed → review. Bar not met → deepen, with a cap on how
  long you stay, and non-blocking gaps demoted to drills (1.15) so small gaps cannot stop
  everything.

---

## Audit checklist

### Before building (design)

- [ ] Exactly one tracker holds the state? (0.2)
- [ ] The next action is one concrete line, never blank? (0.3)
- [ ] The order of scope cuts is written down, ending in "park", not "stop"? (0.5)
- [ ] Every number in the plan is sourced or labelled a default with a review date? (0.6)
- [ ] Zero tooling planned for the first three weeks? (0.7)
- [ ] Adherence and skill are measured by two different bars? (0.8)
- [ ] A recurring review slot exists, and it may change at most one thing? (0.9)
- [ ] Each topic passed the demand / cost / effect filter, with the critical fraction named? (0.10)
- [ ] Each topic has a written pass bar that requires cold, independent performance? (ladder)
- [ ] Sleep, movement and at least one free evening are untouchable? (2.10)
- [ ] Nothing in the system creates owed **hours**, and every unmet **bar** has a drill? (2.7)
- [ ] A bad day has a named minimum, a few minutes long, that counts for the streak? (3.1)
- [ ] The week names about three outcomes, chosen by the learner? (3.3, 3.4)
- [ ] Each dreaded area has a 10-minute version? (3.7)
- [ ] At least one real-conditions rep per week, and one human touchpoint? (3.8, 4.11)
- [ ] Each AI block has a declared role, and "explainer" is not the default? (4.1, 4.12)

### At every review (run)

- [ ] Did the learner attempt before anything revealed an answer? (1.1, 4.2)
- [ ] Is every miss logged with a cause tag and a re-test date — and no invented rows? (1.2, 1.3)
- [ ] Did practice sit on failed or never-tested items, not on passing ones? (1.5)
- [ ] Was the cold hit rate of each practice set inside the band, or adjusted? (1.5b)
- [ ] Does every open item have a next-review date, with fails dropped to the first rung? (1.6)
- [ ] Were siblings mixed with the labels off, once two or more were learned? (1.7)
- [ ] Was a pattern written for each solved problem, not just the solution? (1.4)
- [ ] For each blocker: struggle, write, hint, leave, redo from blank — in that order? (1.9)
- [ ] Was anything explained aloud, 2 minutes, no notes, follow-ups survived? (1.10)
- [ ] Did every AI-assisted task get reviewed, with a named error or a checked "none"? (4.10)
- [ ] Was a loop-back done from blank after every piece of AI help? (4.3)
- [ ] Does every open gap have a "what does it block" answer? (1.15)
- [ ] Do the effort splits still match the evidence from real performances? (3.11)
- [ ] Is every claim in a story or CV backed by an artefact? (3.10)
- [ ] Two bad periods in a row → has the replan actually happened? (3.6)

A "no" is either a fix or a stated, dated exception. Not a silence.

---

## Evidence and limits

| Claim | Strength |
|---|---|
| Retrieval practice (producing before consuming, closed-book testing) | High utility, well replicated |
| Spaced review over several sessions beats one long one | High utility, well replicated. These two rank together; neither is "the best" |
| Feedback after an attempt adds to the attempt | Supported |
| If-then implementation intentions beat plain intentions | Meta-analytic medium-to-large effect across domains |
| Interleaving | Moderate; helps most with confusable categories, results vary |
| An intermediate difficulty beats both easy and overwhelming practice | Supported in direction; the exact optimal hit rate is a design choice, not a finding |
| Task-switch costs are real and only partly reducible | Supported, mostly from fast lab tasks |
| Sleep's role in consolidation | Supported |
| Illusions of competence (familiarity misread as recall; poor self-monitoring) | Supported |
| Pressure and anxiety reduce available working memory | Supported |
| Working memory capacity ≈ 4 chunks | Usable estimate, the exact number is contested |
| "Focused vs diffuse modes" (1.9) | **Useful model, not an established mechanism.** A popularisation. The *sequence* it recommends is still worth following |
| Block lengths, budget splits, number of parallel subjects, review-ladder intervals | **Design choices.** No study tested them |

**Limits.** The research tests techniques, mostly in controlled settings. None of it tests a
weekly curriculum, a track split or a block length. Every schedule-shaped number in any
instance of this system is a hypothesis to be checked against your own data: re-tests, error
log, scored performances. Keep what your results support; drop the rest, including parts of
this file.

**Deliberately left out:** growth-mindset framing. The claim is popular, the replications are
weak, and the belief layer is covered here by mechanism instead — visible progress (3.2),
agency (3.3), a miss read as plan data rather than character (3.6), and a rehearsed response to
being stuck (3.9). If a mindset line helps you, add it to the instance, not here.

---

## Where the instance lives

These are the laws. The instance - this project's schedule, bars, hour budgets and measures -
lives next to them:

| For | Read |
|---|---|
| This project's goal, graph, bars, phases, tracks and checkpoints | `PLAN.md` |
| Every number the skills read (ladder, caps, levels, pace gate) | `learning.config.json`, documented in the kit's `docs/CONFIG.md` |
| Personal constraints, energy, failure modes | `ABOUT-ME.md` |
| Which skill runs when | `CLAUDE.md` and `docs/AI-SYSTEM-GUIDE.md` |

A number in an instance is a hypothesis. A principle here is a constraint. When they disagree,
change the instance.
