# Adapting the kit to a new subject

## 1. Decide the granularity before anything else

One topic per `TOPIC.md`, and the topic is the unit that has a state, an exit bar and an error
log. Too fine (one topic per idea) and the error logs are too thin to diagnose: the whole point
of `error-diagnose` is a pattern across topics. Too coarse (one topic for a whole course) and
`coach` cannot tell you what is next.

Rule of thumb: **4-10 topics, 3-8 subtopics each**, each topic 2-6 estimated hours.

## 2. Write the graph first, the weeks last

`PLAN.md` §2 is the real plan: what needs what. §4 phases are a forecast and will move. Every
`Needs` cell must match the `TOPIC.md` **Needs** field exactly — `validate.py` enforces it,
and the state machine refuses to start a topic whose prerequisites are not `passed` or `kept`.

Mark a prerequisite `(lite)` when the topic only needs a shallow version of it.

## 3. Pick bar categories, not one global bar

A bar is observable and independent. Group topics into 2-4 **bar categories** and write one bar
per category in §3. Examples that work:

| Category | Bar |
|---|---|
| Model / concept | predict ≥8/10 cold on fresh cases, then a 2-minute explain with my own example |
| Numeracy | from blank on a fresh problem, correct to the stated tolerance |
| Technique | ran it in real life for 7 days, with a written result |
| Physical / habit | the change is installed and measured |

"I understand it" is not a bar. If you cannot say what evidence would settle it, the bar is not
written yet.

## 4. Choose the cause vocabulary

`grading.causes` defaults to `concept | careless | English`. Keep `English` if the user is
working in a second language — it is this system's name for principles 1.3's *comprehension*
failure, and it earns a different drill from a concept gap. Drop or rename it only if it would
never apply.

## 5. Write the drop ladder before week 1

`pace.drop_ladder` fires automatically when the pace gate trips, and `coach` is told not to ask
permission. Write it rested: tier 1 is the first thing you would sacrifice, tier 4 the last.
Put the irreducible core in `pace.never_dropped`.

## 6. Source material

Keep one source of truth. If the source is a long document (a transcript, a book, a spec), do
not split it into per-topic copies — they drift as the topics get re-scoped. Keep it whole under
`source/`, build a `source/INDEX.md` mapping sections to topics with line ranges **and** the
verbatim heading text, and cite ranges from each `TOPIC.md` **Sources** section. The heading text
is what recovers the range when line numbers shift.

Third-party material (a paid course, a book) belongs in a private repo. Do not quote it in
anything public.

## 7. Known divergence from interview-v2

`interview-v2` stays on its own copies of these skills and is the reference implementation.
Five fixes exist in the kit and not there:

| Fix | What it was |
|---|---|
| escaped-pipe split in the writer | a row containing `|` could silently duplicate on the dedupe path |
| `patterns.md` dedupe key | keyed on trigger + move, so two phrasings of one move both landed |
| root resolution | `parents[4]` hardcoded skill-dir depth and broke under symlinks |
| `_`-prefix skip | only the first path segment was checked in the three aggregators |
| `parse_plan()` | positional columns: inserting a column made it return `{}` and silently skip the whole unlock check |

Port them if you ever merge the two, and do not "fix" the kit back toward the original.

## 8. Do not build tooling for a system younger than three weeks

`docs/principles.md` 0.7. Run the plain thing first; add scripts when the same manual step has
hurt three times.
