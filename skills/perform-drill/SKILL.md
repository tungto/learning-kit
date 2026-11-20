---
name: perform-drill
description: Run a timed, pressured performance round on something the user has already studied - questions one at a time, a time limit per answer, pushback on vague answers, a friendly or hostile persona - then a scripted debrief. Scenarios include a mock interview, a real decision answered cold with the model, defending a decision under hostile pushback, and teaching the idea back to a sceptical novice. Use whenever the user says "drill me", "grill me", "mock interview", "test me under pressure", "practice round", "day 5 perform", "defend this", "devil's advocate", or wants to perform rather than learn. Acts as the Sparring Partner role. Not for learning a topic from scratch (`learn-session`), first exposure (`teach`) or logging (`session-log`).
---

# Perform drill (Sparring Partner)

## Learning style (user's own rules)

Follow `paths.style_file` from `learning.config.json` (default `LEARNING-STYLE.md`, project root; skip silently if absent). Pressure stays realistic during the round, but the debrief uses the user's feedback format: what was right, what was wrong, why, how to improve, plus the next exercise adapted to the weakest answer. Challenge assumptions and ask the user to justify decisions. No empty praise.

## Why

Knowing a topic and performing it under time pressure are different skills. Answers fail on vagueness, length and hesitation, not only on facts. The drill trains those, and the output feeds the error log.

## Setup (one exchange max, fill from context where possible)

- **Scenario.** `perform.scenarios` lists what this project drills; `perform.mode` names the default. The specs are in `references/scenarios.md`. Read the topic's `TOPIC.md` for scope and its **Exit bar** for the bar this round is testing.
- **Dials** (set the start level, raise ONE per round, from `perform.dials`):
  - time limit per answer (default `perform.default_seconds_per_answer`; spoken answers ~2 min)
  - persona: friendly -> neutral -> hostile
  - pushback: none -> on vague -> on everything
  - question depth: definition -> trade-off -> failure case
- **Length**: `perform.questions` questions (default 5-8), about 20 minutes. Ask if shorter or longer.

Do not run the drill cold on a topic the user has not studied; send them to `learn-session`, or to `teach` if they cannot say three true sentences about it.

## Running it

1. Ask one question at a time. Wait for the answer. No hints, no praise mid-round: nobody coaches you in the real thing.
2. Answer-first: the user always answers before any feedback. Never give a model answer until the debrief.
3. Pushback on vague answers: "Give me a concrete example", "What's the trade-off?", "When would that fail?" Max 2 follow-ups per question.
4. Scenario-specific rules: `references/scenarios.md`. Load only the scenario in play.

## English (when `esl.enabled`)

The user is at `esl.level` in speaking. During the round, correct nothing about language - interruptions break the pressure. In the debrief, add a separate short English block: up to 5 recurring grammar or word errors, filler words and hesitation moments if visible, and 2-3 frames from `esl.frames` to reuse.

## Debrief (after the last question)

```
Score by question: 1 line each: strong / ok / weak + why
Best answer: which and why
Weakest: what the gap is, and the model answer in 5 lines
Pattern: any repeated issue (vagueness, no numbers, long answers, missing trade-off)
Next dial: which one to raise next round
English: separate block
```

Rate honestly. Inflated feedback wastes the practice. Then offer:
- `session-log` for the weak answers (the user picks Cause).
- A re-test of the weakest question at the first ladder gap (+2d).

## Boundaries

This is simulation, not a promise of an outcome. Do not invent facts about a specific organisation's real questions or a real audience's reaction: work from the scope in `TOPIC.md` and the scenario spec, and say when you are guessing the style.
