# Style guide: lessons, reference pages, reports, tutorials

Loaded by `create-lesson` before it writes any HTML. The look is fixed by `assets/lesson.css`; this
file says how to use it so every page reads the same way. A rule here is a bar: it is either met or
not, and the checklist at the end checks each one.

## 1. Pick the shape

| Shape | Use for | Skeleton | Has |
|---|---|---|---|
| **Lesson** | One tight idea, one tangible win, read top to bottom once | `assets/skeleton-lesson.html` | masthead, 3-5 numbered sections, check-yourself, "In short", footer nav |
| **Reference** | Reports, tutorials, architecture notes, anything read out of order or over 6 sections | `assets/skeleton-reference.html` | left rail TOC with scroll-spy, masthead, part bands, numbered sections, footer nav |

A lesson that wants a rail is two lessons. A reference page with fewer than 6 sections is a lesson.

## 2. The page, top to bottom

1. **Masthead.** `.eyebrow` (kind of document · status), `h1` (max 20ch - a name or a claim, never
   "Introduction to"), `.lede` (max 58ch: what this is **and what it is not**), `.meta` row (audience,
   time, prerequisite, conventions such as what a chip means).
2. **Part bands** (reference only). `.part` with `.part-n` ("Part I"), `h2`, and one line saying what
   the part answers. 2-5 parts. A reader who stops after Part I must still have the whole picture.
3. **Numbered sections.** `<section id="sN">` + `h3` with `<span class="n">N</span>`. Numbers run
   1..N across the whole page, not per part, so "see 7" is unambiguous. Rail links mirror them exactly.
4. **Inside a section**: `h4` for a sub-topic, `h5` for a small-caps label above a component
   (`.kv`, a table). Never skip from `h3` to `h5` to get a smaller look.
5. **Close.** Last section is "In short": 3-5 bullets a reader could repeat from memory, then a
   `.note` labelled "Next step" with one link. Then the footer nav `p.crumb[data-nav-footer]`.

## 3. Writing

- **Rule first, evidence second.** First sentence of a section states the claim; the rest supports
  it. Put the claim's key phrase in `<strong>` - one per paragraph at most.
- **Paragraphs max 4 sentences.** Prose blocks sit in `.col` (68ch). Wide things (tables, diagrams,
  code) may run to 1000px; prose never does.
- **Say what is true now.** Mark planned or partial things with a chip, never with hedged prose.
- **Name the misunderstanding.** When an idea is commonly confused, a `.note.crit` labelled with the
  misunderstanding ("Three things easy to get wrong") states wrong belief → correct belief.
- **Concrete over abstract.** Walk one real request, one real example, through every step before
  generalising. Steps are verbs ("sign", "verify", "stream"), not nouns.
- **Comparisons are tables,** not parallel paragraphs. Two or more items compared on two or more
  attributes → table.
- **Principles are a `.kv` grid**: term (short noun phrase) + one testable sentence. 3-6 cells.
- **Citations** (`teach.require_citations`, default `true`): key claims link their source
  inline (not every line). The primary source also sits in the masthead `.meta` and in "Next step".
- **Language**: write in the user's language (from `NOTES.md`); keep technical terms in their
  original form inside `<code>` or with a `.sub` gloss after the heading. Set `<html lang>` and the
  `data-ui-*` button words on `<body>` to match.

## 4. Components - one job each

| Component | Job | Bar |
|---|---|---|
| `.note` / `.warn` / `.crit` / `.ok` | A rule, a caveat, a danger, a confirmed fact | `.note-label` is a claim or a question ("Why a third plane is needed"), never just "Note". Max 1 per section unless the section is about pitfalls. Body max 3 sentences. |
| `.kv` (`dt` + `dd`) | A set of principles or properties | 3-6 cells; each `dd` one sentence. |
| table in `.tw` | Comparison, inventory, ownership split | Headers short; first column is the thing being described (shown in ink). Max ~8 rows - more is an appendix. |
| `.chip.ok/.warn/.crit/.info` | Status tag inside a table or the meta row | One or two words. Meaning stated once in `.meta`. |
| `pre > code` | The smallest real example | Under ~25 lines; comments mark the line that matters. |
| `pre.ascii` | A quick text diagram where SVG would be overkill | Monospace-safe characters only. |
| `.checklist` | Steps a reader will tick off | Each item an action, starting with a verb. |
| `details > summary` | Check-yourself question, optional depth | The summary is the question; the body the answer plus why. |
| `.dia` | A diagram (below) | Always has `.dia-cap`. |

Anything a second page would reuse (a quiz widget, a simulator, a diagram helper) goes in the
topic's `./assets/`, not inline.

## 5. Diagrams

A diagram earns its place when the idea is a mechanism: who calls whom, in what order, who owns
what, what crosses a boundary. Decoration is not a reason.

- **Hand-written inline SVG** with a `viewBox` (900 wide is the house width) and
  `role="img" aria-label="one sentence of what it shows"`.
- **Use the classes**: `.box` (component), `.lbl` (name, uppercase), `.lbl-sm` (detail),
  `.lbl-ch` (group heading), `.wire` (connection, `.wire-dash` for async/optional), `.lane`
  (timeline swim-lane). Colours only through CSS variables, so both themes work.
- **One colour per role**: `--actor-1` .. `--actor-5`, plus `--accent` for the system the page is
  about. Assign roles once (e.g. actor-1 = the user, actor-3 = external services) and keep them in
  every diagram on the page and across the topic. A box outlined in a role colour has its label in
  that colour; other boxes stay neutral.
- **Orthogonal wires** (`H`/`V` path commands), labelled at the midpoint with what crosses.
- **Sequence over time** → horizontal lanes (`.lane`) per actor, one path weaving between them,
  dots + short verb labels at each stop.
- **Caption** (`.dia-cap`) states the takeaway, not the labels.
- **Motion is optional** and only for flow: a `.pkt` group with `<animateMotion><mpath href="#id">`
  along a wire. Any animated SVG gets a `.dia-ctl` with Pause (`data-toggle="svgId"`) and Restart
  (`data-restart="svgId"`). The CSS already hides packets under reduced motion and in print - the
  still picture must make sense alone.

## 6. Look (already in `lesson.css` - do not override per page)

- Light paper, white surfaces raised by a 1px border, no shadows. Light by default
  (`teach.lesson_theme`, default `"light"`); dark only by the reader's toggle.
- One sans system stack; body 16px / 1.65; headings tight negative letter-spacing and
  `text-wrap: balance`; small labels uppercase 10.5-11px with wide tracking.
- Tabular numerals in tables and section numbers.
- A page that needs a new colour, size or component adds it to the topic's `assets/lesson.css`,
  as a token or class, never as an inline `style`.

## 7. Before saying the page is done

- [ ] `<html lang="..." data-theme="light">`; links `../assets/lesson.css` and `lesson.js` (defer).
- [ ] `h1` ≤ 20ch, lede says what the page is not.
- [ ] Section numbers continuous; rail links (reference) match ids and titles.
- [ ] Every section opens with its claim; no paragraph over 4 sentences.
- [ ] Key claims have a link; one recommended source named; lessons follow the nine-section flow.
- [ ] Every `.note-label` is a claim or question.
- [ ] Every SVG has `role="img"`, `aria-label`, a `.dia-cap`; animated ones have Pause/Restart.
- [ ] No inline colours outside SVG `var(--...)` references; no new hex codes in the page.
- [ ] "In short" + "Next step" + footer nav present; the ask-your-agent reminder is there.
- [ ] Narrow window (< 900px): rail collapses, nothing scrolls sideways except `.tw` and `.dia`.
