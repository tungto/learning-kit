# {{PROJECT_TITLE}}

## 1. Goal

<What "done" means, in one paragraph, in observable terms: what I will be able to do, alone,
under what conditions, by when. Not "learn X" - "explain X in two minutes without notes, and
apply it to a real decision".>

Horizon: <{{START_DATE}} + total_weeks, and what happens then>.

## 2. Topic graph

### 2.1 Graph

```
<topic-a> --> <topic-b> --> <topic-d>
         \--> <topic-c>
<topic-e>   (standalone)
```

Critical path: <the chain that decides the end date>.

| # | Topic | Needs | Unlocks | Bar category | Est. h | Source |
|---|---|---|---|---|--:|---|
| 1 | [<topic-a>]({{TOPICS_DIR}}/<topic-a>/TOPIC.md) | - | <topic-b>, <topic-c> | <category> | 3 | <where the material is> |

`Needs` must match each `TOPIC.md`'s **Needs** field exactly; `validate.py` checks it. A
`(lite)` need only requires the configured minimum level on its subtopics.

### 2.2 Parallel rule

Max `graph.max_parallel_new_topics` new-concept topics at once, plus any standalone topic. Never
two dependent or two similar topics in the same week. No second topic in a week with a
checkpoint.

## 3. Levels and bars

L1 recognize · L2 predict · L3 do alone · L4 spot the failure mode · L5 explain aloud (handle
two follow-ups) · L6 applied for 7 days. (Edit to match `levels.names`.)

| Bar category | Pass bar (independent, cold) |
|---|---|
| <category> | <the observable bar: a score, a from-blank build, a 2-minute explain, a result from real use> |

Done = the bar met cold and alone, **plus** a re-test passed at +7d or later ("kept").

## 4. Phases

A forecast, not a schedule. The week numbers move; the order does not.

### Phase 1: W1-4

| Week | Main | Second | Outcome |
|---|---|---|---|
| 1-2 | <topic-a> | - | <topic-a> passed |

### Phase 2: W5-8

| Week | Main | Second | Outcome |
|---|---|---|---|

## 5. Tracks and effort

<How many hours a week, in which slots. Keep it to what has actually happened for two weeks,
not what would be nice.> Total: `plan.weekly_hours` h/week across the slots in `coach.slot_map`.

### 5.1 Effort levels

| Level | Size | Counts for the streak? |
|---|---|---|
| minimum day | `effort_levels.minimum_day_minutes` - one recall item + one error row | yes |
| minimum | `effort_levels.minimum_minutes` | yes |
| target | `effort_levels.target_minutes` | yes |
| stretch | `effort_levels.stretch_minutes` - target + one follow-up on the same topic | offered, never owed |

### 5.2 Pace gate and drop ladder

Gate: `plan.weekly_hours × pace.gate_fraction` per week, measured over the last
`pace.lookback_weeks` weeks. Below it twice running, the next tier fires automatically.

| Tier | Drops | Saves |
|--:|---|--:|
| 1 | <the first thing to go> | <h> |

Never dropped at any tier: <`pace.never_dropped`>.

## 6. Checkpoints

| CP | Week | Bar | Failure branch |
|---|--:|---|---|
| CP1 | <n> | <what must be true, with evidence> | <exactly what changes: which topic keeps the slot, which subtopics are cut, which dates move> |

The failure branch is written in advance and applied verbatim. Never improvised on the day.
