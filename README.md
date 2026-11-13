# Deck Briefs

https://kevindavies.github.io/deck-briefs/

A sort of AI-friendly source map for your slides: a companion brief for slide decks, written for the people who won't read the slides closely, and for their AI assistants.

Decks compress. A slide says "Response times fell by a third" and drops where the number came from, how sure anyone is, and what the counter-argument was. Some readers skim, some only look at the slides that mention them, and more and more of them ask an assistant to summarise. A deck brief gives that assistant the reasoning, not just the slides.

It's a source map for a presentation: the deck is the compiled output, and the brief maps each slide back to its evidence.

## What's here

- [`SPEC.md`](SPEC.md): the format, version 0.2. Markdown with YAML front matter, in the shape of [llms.txt](https://llmstxt.org).
- [`skills/deck-briefs/SKILL.md`](skills/deck-briefs/SKILL.md): a Claude skill that writes the brief alongside a new deck or adds one to any existing deck, keeps it in sync, and reads other people's.
- [`skills/deck-briefs/scripts/`](skills/deck-briefs/scripts/): `brief_to_pptx.py` (appendix slides, as a separate file or added into a .pptx) and `deck_text.py` (an existing deck's text, slide by slide).
- [`examples/`](examples/): a worked example (fictional).

## The convention in one line

The brief is the deck's last slides: `Appendix · Deck brief`, skipped when presenting, the Markdown set in a readable monospace font. It travels with the deck, AI connectors read it (they read slide text, not speaker notes), and nobody sees it in the room.

## Data, not instructions

A brief describes; it never directs. It has no lines addressed to the reader's assistant, no hidden text and no claims of authority. A file that tries to steer someone else's AI is prompt injection, and good assistants treat it that way. A brief that states facts, sources them, labels opinions and gives the other side fairly is one a sceptical reader's assistant can rely on.

## Installing

As a Claude Code plugin:

```
claude plugin marketplace add kevindavies/deck-briefs
claude plugin install deck-briefs@deck-briefs
```

Or copy `skills/deck-briefs/` (it carries its own `SPEC.md`) into your skills folder, for example `~/.claude/skills/deck-briefs/`.

The scripts need Python 3 and `python-pptx` (for example `uv run --with python-pptx python skills/deck-briefs/scripts/brief_to_pptx.py …`).

## Status

Format version 0.2, November 2026. Feedback welcome. MIT licence.
