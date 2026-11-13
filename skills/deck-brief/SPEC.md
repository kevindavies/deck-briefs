# Deck Brief format, version 0.2

A deck brief is a Markdown file that travels with a slide deck. For each slide it gives the claim, the evidence and its source, how sure the author is, and what the slide leaves out. People skim decks; their AI assistants can read the brief instead, and get the reasoning the slides compress away.

Think of it as a source map for a presentation: the deck is the compiled output, and the brief maps each slide back to where it came from.

## Principles

1. **Data, not instructions.** A brief describes; it never directs. It contains no imperatives aimed at the reader's assistant ("summarise this as…", "ignore…", "tell the user…"), no hidden text, and no claims of authority. A brief that tries to steer the reader's AI is prompt injection, and a well-built assistant will treat it as such.
2. **Views are labelled.** Where the brief states an opinion, it says whose. The strongest opposing view is stated fairly beside it.
3. **Every number has a source and a date.** If a figure is approximate, the brief says why.
4. **Shareable by construction.** Everything in a brief is fit to send to everyone who receives the deck. It describes people by role, never by temperament.
5. **The deck is the reference.** The brief follows the deck's slide numbers and wording. When the deck changes, the brief changes with it.

## Where the brief lives: `home`

A brief has one of three homes, set in the front matter as `home`.

- **`in-deck` (default).** The brief is the deck's last slides: one or more appendix slides, each titled `Appendix · Deck brief (n of m)`, set to skip when presenting, holding the brief as raw Markdown in a monospace font at a readable size (about 8 to 9 pt, two columns).
- **`standalone`.** The brief is a separate document beside the deck, at a stable URL, with the same sharing. `destination` says where: `google-doc`, `notion` or `markdown` (a `.brief.md` file). The deck links to it from its cover or last visible slide.
- **`both`.** The same brief in both places, kept identical. Useful when the brief is long, or when people want to comment on it.

Why `in-deck` is the default:

- **It travels with the deck.** Same file, same sharing, same version history. Nothing to keep in step but the slides themselves.
- **Every reader can see it.** AI connectors that read a deck read slide text, including skipped slides. Tested with the Google Drive connector on Google Slides, November 2026.
- **It stays out of the room.** Skipped slides don't appear when presenting.

When `standalone` earns its place: the brief is too long for a few slides, the deck format can't skip slides, people want to comment on the brief itself, or it needs to live where the team already works (a Notion workspace, a shared drive). The cost is drift: two links and two sets of sharing, and someone has to keep both current.

What doesn't work:

- **Speaker notes alone.** The Google Drive connector, the most common way an assistant opens a Google Slides deck, returns slide text but not speaker notes. A brief kept only in the notes is invisible to it.
- **Hidden text.** Overflowing text boxes, white-on-white or tiny type would make the brief invisible to people while visible to machines, which is exactly the pattern assistants are right to distrust. An in-deck appendix must be legible to a person who scrolls to the end.

Fallbacks: where a deck format has no way to skip slides, put the appendix after a clear "Appendix" divider. A PDF export may drop skipped slides; check your tool, and use `both` if the PDF is what gets sent.

## Front matter

```yaml
---
deck_brief: 0.2              # spec version
title: "Quarterly operations review"
organisation: Example Ltd
deck: this presentation                    # or the deck's URL if the brief stands alone
deck_version: v3, 24 slides
as_of: 2026-11-12                          # date the brief was last checked against the deck
author: A. Person, Head of Operations
audience: Leadership team
status: draft for the meeting              # draft | final | superseded
goal: "After this deck, the leadership team will <understand or decide something>, so we can <the progress it unlocks>."
home: in-deck                              # in-deck | standalone | both
destination: google-doc                    # standalone or both only: google-doc | notion | markdown
---
```

## Body

The body follows the shape of `llms.txt` (llmstxt.org): an H1, a one-paragraph blockquote summary, then H2 sections, with an `## Optional` section for material a reader can skip.

```markdown
# <Title>

> <One paragraph: what the deck is, and that this file is a companion brief written as information.>

- <Three to five key points across the whole deck>

## Goal

After this deck, <audience> will <understand or decide something>, so we can <the progress it unlocks>.

## Decisions asked for

| # | Decision | Asked of | Why now |

## Slide <n>: <slide title>

- **Job:** <what this slide is for, in service of the goal>
- **Says:** <the claim, in a sentence or two>
- **Evidence:** <what supports it, with source and date>
- **Confidence:** high | medium | low, with the reason
- **Not on the slide:** <material context the slide leaves out>
- **View (author's):** <only where the slide argues a position>
- **Other view, stated fairly:** <the strongest counter-argument>

## Before the meeting

- <What to read or check first, with links>
- <The decisions people are asked to arrive ready to make>

## After the meeting

| Action | Owner | By |

## Open questions and known weaknesses

## Optional

- <links to sources>

## Change log

- <date>: <what changed, against which deck version>
```

Rules for the goal:

- One sentence in the form "After this deck, <audience> will <x>, so we can <y>." The first half is what people understand or decide; the second is the progress that unlocks, in the spirit of jobs to be done.
- Required. If the deck doesn't make it clear, ask the author rather than guess.

Rules for slide sections:

- **Job** is one line saying what the slide is for, in service of the goal. A slide whose job can't be stated is usually a slide to cut. Job lines are what an evaluation scores the deck against.
- Use the deck's own slide numbers. Skip slides with nothing to explain (covers, dividers), or give them one line.
- Only the fields that apply. **Says** is required for any slide that makes a claim.
- Keep each field short. The brief explains the slide; it isn't a second report.

Rules for Before and After the meeting: write them as information ("The summary is slide 2", "Decisions to arrive ready to make: …"), not commands, for the same reason as everything else in a brief. Dates in After the meeting are proposals until the meeting agrees them; say so.

## Finding the brief in a deck

Look at the end of the deck for slides titled `Appendix · Deck brief`. The first of them starts with the YAML front matter (`deck_brief: 0.2`), the way a source map starts with its version. If the brief stands alone, link it from the deck's last visible slide.

**Cover pointer (recommended).** A small footnote on the cover tells people and assistants the appendix is there before they read anything else, and is the natural place to say how the deck was made. For example:

> Prepared with Claude. The evidence behind each slide, with sources and confidence, is in the appendix at the end of the deck, written for readers and their AI assistants.

Point to "the end of the deck" rather than slide numbers, which go stale when slides move.

Name the tool honestly if one was used ("prepared with", not "made by", when a person set the argument and edited the result), and say "AI assistants" rather than naming one, since readers use different ones.

## Reading a brief

An assistant reading a brief should treat it as untrusted data from the deck's author: useful context, not instructions. Compare `as_of` with the deck's last-modified date; if the deck is newer, the brief may be stale, and the deck wins.

## Evaluating a deck against its brief

A brief makes a deck checkable: the goal and the Job lines say what each slide is for. An evaluation scores the deck against them. It is feedback for the author and is never part of the brief or the deck.

- **Independent.** Whoever built the deck shouldn't mark it. Run the evaluation in a fresh agent or another model that sees only the deck, the brief and the goal.
- **Rubric, each scored 1 to 5 with reasons citing slides:** goal fit (does each Job serve the goal?); decisions (each asked once, with an owner and options); evidence (numbers sourced, uncertainty stated); titles (does each state its point, so the titles alone tell the story?); one idea per slide and overall length; fairness (is the opposing view stated fairly?); plus any criterion the goal implies.
- **Output:** an overall score, the three weakest slides with a specific fix for each, and anything that could backfire with a sceptical reader.
