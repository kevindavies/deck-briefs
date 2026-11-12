"""Print a .pptx deck's text, slide by slide, as the starting point for a brief.

uv run --with python-pptx python deck_text.py deck.pptx

Each slide prints as "## Slide <n>" (with "(skipped)" where it won't show when
presenting), then its text in reading order, then its speaker notes. Existing
deck-brief appendix slides are listed but not printed.
For Google Slides, read the deck through the Google Drive connector instead, or
download it as .pptx (File > Download > Microsoft PowerPoint) and use this.
"""
import sys

from pptx import Presentation

prs = Presentation(sys.argv[1])
for n, s in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text.strip() for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    skipped = s._element.get("show") == "0"
    if texts and texts[0].startswith("Appendix · Deck brief"):
        print(f"## Slide {n}: existing deck-brief appendix (not printed)\n")
        continue
    print(f"## Slide {n}{' (skipped)' if skipped else ''}")
    for t in texts:
        print(t)
    if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip():
        print("Notes:", s.notes_slide.notes_text_frame.text.strip())
    print()
