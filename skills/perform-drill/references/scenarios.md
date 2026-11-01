# Scenario specs

One scenario per round. Load the one in play; `perform.scenarios` says which ones this project uses, and a project may add its own with a `name` and a `prompt`.

## interview

A hiring round on one topic. Scope from `TOPIC.md`; if the user names a target organisation, use whatever job description or notes the project stores and say what you are inferring.

- Mix: definitions -> trade-offs -> failure cases, in that order of depth.
- Behavioral questions: use STAR but never name it. Push for numbers ("what number changed?"), "I" vs "we", and a stated result.
- Live building (code, spreadsheet, design): let the user work cold, ask them to narrate, then ask for the cost and one edge case.
- System or process design: clarify requirements, estimate, then components and failure modes. Ask for trade-offs, not the "one right design".

## cold application

A real decision from the user's own week, answered with the model under a time limit, no notes.

- The user brings the decision; you supply the clock and the pushback.
- Require the actual numbers or the actual constraint, not a sketch.
- One question: "what will you do, and what would change your mind?" Then push on the second half.
- Fail condition: an answer that could not be acted on tomorrow.

## devil's advocate

The user defends a decision they already made, against hostile pushback.

- Persona starts at neutral and goes hostile at the first vague claim.
- Attack the weakest assumption, not the conclusion. Name it when you find it.
- Two rounds minimum. Stop when the user either holds the position with evidence or concedes the specific point.
- Fail condition: the user defends with authority or volume instead of a reason.

## teach-back

The user explains the idea to a sceptical novice in two minutes.

- You play the novice: ask "why does that matter?" and "what would I see if that were wrong?"
- Interrupt once, early, with a plausible wrong restatement and let the user correct it.
- Grade for: one concrete example, the failure mode named, no jargon left undefined.
- Fail condition: a correct explanation the novice could not use.
