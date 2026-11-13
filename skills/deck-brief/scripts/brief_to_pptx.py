"""Turn a deck brief (.brief.md) into appendix slides, skipped when presenting.

Two ways to use it:

  # 1. Make a separate file of appendix slides, to import into Google Slides
  #    (File > Import slides > select all) or Keynote:
  uv run --with python-pptx python brief_to_pptx.py deck.brief.md --out appendix.pptx

  # 2. Add the appendix straight into an existing PowerPoint deck. Any earlier
  #    "Appendix · Deck brief" slides in it are replaced, so it is safe to re-run:
  uv run --with python-pptx python brief_to_pptx.py deck.brief.md --into deck.pptx [--save-as new.pptx]

Options: --font "Roboto Mono" --size 8 --lines 40 --width 84
The slides stay legible: text is split at section boundaries and never overflows.
"""
import argparse
import math

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Emu, Inches, Pt

TITLE = "Appendix · Deck brief"
INK, MUTED = RGBColor(0x22, 0x22, 0x22), RGBColor(0x77, 0x77, 0x77)


def columns(md, lines_per_col, chars_per_line):
    raw = md.rstrip("\n").split("\n")
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
    cost = lambda para: sum(max(1, math.ceil(len(l) / chars_per_line)) for l in para) + 1
    cols, col, used = [], [], 0
    for para in merged:
        c = cost(para)
        if col and used + c > lines_per_col:
            cols.append(col)
            col, used = [], 0
        col.append(para)
        used += c
    if col:
        cols.append(col)
    return cols


def blank_layout(prs):
    """The layout with the fewest placeholders, so appendix slides start empty."""
    return min(prs.slide_layouts, key=lambda l: len(l.placeholders))


def box(slide, x, y, w, h, lines, size, color, font=None, bold_headings=False):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
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


def is_brief_slide(slide):
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip().startswith(TITLE):
            return True
    return False


def remove_slide(prs, slide):
    ids = prs.slides._sldIdLst
    for sld in list(ids):
        if prs.slides.part.related_part(sld.rId) is slide.part:
            prs.part.drop_rel(sld.rId)
            ids.remove(sld)
            return


def add_brief(prs, md, font="Roboto Mono", size=8, lines=40, width=84):
    for s in [s for s in prs.slides if is_brief_slide(s)]:
        remove_slide(prs, s)
    W, H = prs.slide_width, prs.slide_height
    sx, sy = W / Inches(13.333), H / Inches(7.5)  # scale positions to the deck's size
    at = lambda x, y, w, h: (Emu(int(Inches(x) * sx)), Emu(int(Inches(y) * sy)), Emu(int(Inches(w) * sx)), Emu(int(Inches(h) * sy)))
    cols = columns(md, lines, width)
    n = math.ceil(len(cols) / 2)
    layout = blank_layout(prs)
    for i in range(n):
        s = prs.slides.add_slide(layout)
        for ph in list(s.placeholders):
            ph._element.getparent().remove(ph._element)
        s._element.set("show", "0")  # skipped when presenting
        box(s, *at(0.5, 0.3, 12, 0.3), [f"{TITLE} ({i + 1} of {n})"], 11, MUTED)
        box(s, *at(0.5, 0.58, 12.3, 0.3), ["The evidence behind each slide, as Markdown, for readers and their AI assistants. Skipped when presenting."], 10, MUTED)
        for j, colparas in enumerate(cols[2 * i: 2 * i + 2]):
            body = "\n\n".join("\n".join(pp) for pp in colparas).split("\n")
            box(s, *at(0.5 + j * 6.25, 1.0, 6.0, 6.2), body, size, INK, font, bold_headings=True)
    return n


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--out", help="write the appendix slides to a new .pptx")
    g.add_argument("--into", help="add the appendix to this existing .pptx")
    ap.add_argument("--save-as", help="with --into, save to this path instead of overwriting")
    ap.add_argument("--font", default="Roboto Mono")
    ap.add_argument("--size", type=float, default=8)
    ap.add_argument("--lines", type=int, default=40, help="lines per column")
    ap.add_argument("--width", type=int, default=84, help="characters per line")
    a = ap.parse_args()
    md = open(a.brief, encoding="utf-8").read()
    if a.out:
        prs = Presentation()
        prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
        target = a.out
    else:
        prs = Presentation(a.into)
        target = a.save_as or a.into
    n = add_brief(prs, md, a.font, a.size, a.lines, a.width)
    prs.save(target)
    print(f"{target}: {n} appendix slides, {len(prs.slides)} slides in total")
