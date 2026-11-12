"""Turn a deck brief (.brief.md) into appendix slides, skipped when presenting.

uv run --with python-pptx python brief_to_pptx.py deck.brief.md appendix.pptx [--font "Roboto Mono"] [--size 8]

Import the result at the end of your deck (Google Slides: File > Import slides,
select all). The slides stay legible: text is split at section boundaries and
never overflows a slide.
"""
import argparse
import math

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

ap = argparse.ArgumentParser()
ap.add_argument("brief")
ap.add_argument("out")
ap.add_argument("--font", default="Roboto Mono")
ap.add_argument("--size", type=float, default=8)
ap.add_argument("--lines", type=int, default=40, help="lines per column")
ap.add_argument("--width", type=int, default=84, help="characters per line")
a = ap.parse_args()

INK, MUTED = RGBColor(0x22, 0x22, 0x22), RGBColor(0x77, 0x77, 0x77)
raw = open(a.brief, encoding="utf-8").read().rstrip("\n").split("\n")

paras, cur = [], []
for ln in raw:
    if ln.strip():
        cur.append(ln)
    elif cur:
        paras.append(cur)
        cur = []
if cur:
    paras.append(cur)
merged = []  # keep a lone heading with the paragraph after it
for para in paras:
    if merged and len(merged[-1]) == 1 and merged[-1][0].startswith("#"):
        merged[-1] += para
    else:
        merged.append(para)

cost = lambda para: sum(max(1, math.ceil(len(l) / a.width)) for l in para) + 1
cols, col, used = [], [], 0
for para in merged:
    c = cost(para)
    if col and used + c > a.lines:
        cols.append(col)
        col, used = [], 0
    col.append(para)
    used += c
if col:
    cols.append(col)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
n = math.ceil(len(cols) / 2)


def box(slide, x, y, w, h, lines, size, color, bold_headings=True, font=None):
    tf = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for k, ln in enumerate(lines):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        r = p.add_run()
        r.text = ln
        r.font.size, r.font.color.rgb = Pt(size), color
        if font:
            r.font.name = font
        r.font.bold = bold_headings and ln.startswith("#")


for i in range(n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s._element.set("show", "0")  # skipped when presenting
    box(s, 0.5, 0.3, 12, 0.3, [f"Appendix · Deck brief ({i + 1} of {n})"], 11, MUTED, False)
    box(s, 0.5, 0.58, 12.3, 0.3, ["The evidence behind each slide, as Markdown, for readers and their AI assistants. Skipped when presenting."], 10, MUTED, False)
    for j, colparas in enumerate(cols[2 * i: 2 * i + 2]):
        lines = "\n\n".join("\n".join(pp) for pp in colparas).split("\n")
        box(s, 0.5 + j * 6.25, 1.0, 6.0, 6.2, lines, a.size, INK, font=a.font)

prs.save(a.out)
print(f"{a.out}: {n} appendix slides")
