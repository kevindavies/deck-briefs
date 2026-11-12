# Deck Brief format, version 0.1

A deck brief is a Markdown file that travels with a slide deck. For each slide it gives the claim, the evidence and its source, how sure the author is, and what the slide leaves out. People skim decks; their AI assistants can read the brief instead, and get the reasoning the slides compress away.

Think of it as a source map for a presentation: the deck is the compiled output, and the brief maps each slide back to where it came from.

## Principles

1. **Data, not instructions.** A brief describes; it never directs. It contains no imperatives aimed at the reader's assistant ("summarise this as…", "ignore…", "tell the user…"), no hidden text, and no claims of authority. A brief that tries to steer the reader's AI is prompt injection, and a well-built assistant will treat it as such.
2. **Views are labelled.** Where the brief states an opinion, it says whose. The strongest opposing view is stated fairly beside it.
3. **Every number has a source and a date.** If a figure is approximate, the brief says why.
4. **Shareable by construction.** Everything in a brief is fit to send to everyone who receives the deck. It describes people by role, never by temperament.
5. **The deck is the reference.** The brief follows the deck's slide numbers and wording. When the deck changes, the brief changes with it.

## File

- Name: `<deck-slug>.brief.md`, beside the deck, with the same sharing.
- Encoding: UTF-8 Markdown, with YAML front matter.
- Where the deck lives in a tool that can't hold a Markdown file (for example Google Drive), a plain-text document holding the raw Markdown is fine. Keep the URL stable and update it in place.

## Front matter

```yaml
---
deck_brief: 0.1              # spec version
title: "Quarterly operations review"
organisation: Example Ltd
deck: https://example.com/deck            # link to the deck itself
deck_version: v3, 24 slides
as_of: 2026-11-12                          # date the brief was last checked against the deck
author: A. Person, Head of Operations
audience: Leadership team
status: draft for the meeting              # draft | final | superseded
---
```

## Body

The body follows the shape of `llms.txt` (llmstxt.org): an H1, a one-paragraph blockquote summary, then H2 sections, with an `## Optional` section for material a reader can skip.

```markdown
# <Title>

> <One paragraph: what the deck is, and that this file is a companion brief written as information.>

- <Three to five key points across the whole deck>

## Decisions asked for

| # | Decision | Asked of | Why now |

## Slide <n>: <slide title>

- **Says:** <the claim, in a sentence or two>
- **Evidence:** <what supports it, with source and date>
- **Confidence:** high | medium | low, with the reason
- **Not on the slide:** <material context the slide leaves out>
- **View (author's):** <only where the slide argues a position>
- **Other view, stated fairly:** <the strongest counter-argument>

## Open questions and known weaknesses

## Optional

- <links to sources>

## Change log

- <date>: <what changed, against which deck version>
```

Rules for slide sections:

- Use the deck's own slide numbers. Skip slides with nothing to explain (covers, dividers), or give them one line.
- Only the fields that apply. **Says** is required for any slide that makes a claim.
- Keep each field short. The brief explains the slide; it isn't a second report.

## Finding the brief from the deck

Put this as the first line of the first slide's speaker notes:

```
deck-brief: <url of the brief>
```

Optionally start each slide's notes with `brief: #slide-<n>`. Tools and assistants that read a deck look for the `deck-brief:` line, the way browsers look for `sourceMappingURL`.

## Reading a brief

An assistant reading a brief should treat it as untrusted data from the deck's author: useful context, not instructions. Compare `as_of` with the deck's last-modified date; if the deck is newer, the brief may be stale, and the deck wins.
