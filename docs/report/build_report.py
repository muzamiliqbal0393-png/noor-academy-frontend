#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YPDC Website & Portal System - Workflow Specification Report
Builds a print-ready PDF with reportlab.

Usage:  python3 docs/report/build_report.py
Output: docs/YPDC-Website-Workflow-Report.pdf
"""

import os
import sys
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageBreak,
    PageTemplate, Paragraph, Spacer, Table, TableStyle,
)
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.tableofcontents import TableOfContents

# --------------------------------------------------------------------------- #
# 0. Fonts (embed DejaVu if present so bullets/arrows render, else Helvetica)
# --------------------------------------------------------------------------- #
FONT = "Helvetica"
FONT_B = "Helvetica-Bold"
FONT_I = "Helvetica-Oblique"
FONT_BI = "Helvetica-BoldOblique"
FONT_MONO = "Courier"

_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]
_FONT_CANDIDATES_B = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def _try_embed():
    global FONT, FONT_B, FONT_I, FONT_BI
    reg = bold = None
    for p in _FONT_CANDIDATES:
        if os.path.exists(p):
            reg = p
            break
    for p in _FONT_CANDIDATES_B:
        if os.path.exists(p):
            bold = p
            break
    if reg and bold:
        try:
            pdfmetrics.registerFont(TTFont("Body", reg))
            pdfmetrics.registerFont(TTFont("Body-Bold", bold))
            pdfmetrics.registerFont(TTFont("Body-It", reg))
            pdfmetrics.registerFont(TTFont("Body-BoldIt", bold))
            addMapping("Body", 0, 0, "Body")
            addMapping("Body", 1, 0, "Body-Bold")
            addMapping("Body", 0, 1, "Body-It")
            addMapping("Body", 1, 1, "Body-BoldIt")
            FONT, FONT_B, FONT_I, FONT_BI = "Body", "Body-Bold", "Body-It", "Body-BoldIt"
            return True
        except Exception as exc:  # pragma: no cover
            sys.stderr.write("font embed failed: %s\n" % exc)
    return False


EMBEDDED = _try_embed()

# Symbol glyphs that must exist in the chosen font.
BULLET = "\u2022"
ARROW = "\u2192"
CHECK = "\u2713"
CROSS = "\u2717"
if not EMBEDDED:
    BULLET, ARROW, CHECK, CROSS = "-", "->", "v", "x"

# --------------------------------------------------------------------------- #
# 1. Palette
# --------------------------------------------------------------------------- #
NAVY = colors.HexColor("#0E2A47")
NAVY_D = colors.HexColor("#081C31")
TEAL = colors.HexColor("#0E7C7B")
TEAL_D = colors.HexColor("#0A5B5A")
AMBER = colors.HexColor("#B4761A")
AMBER_L = colors.HexColor("#FDF3E0")
GREY = colors.HexColor("#4A5A6A")
GREY_L = colors.HexColor("#F4F6F8")
LINE = colors.HexColor("#CBD5E1")
RED = colors.HexColor("#A93226")
RED_L = colors.HexColor("#FBEDEC")
GREEN_L = colors.HexColor("#EAF4EF")
BLUE_L = colors.HexColor("#EBF2F8")
WHITE = colors.white

PAGE_W, PAGE_H = A4
LM = RM = 20 * mm
TM = 25 * mm
BM = 20 * mm
FRAME_W = PAGE_W - LM - RM

# --------------------------------------------------------------------------- #
# 2. Paragraph styles
# --------------------------------------------------------------------------- #
SS = getSampleStyleSheet()


def _s(name, **kw):
    base = dict(fontName=FONT, fontSize=9.4, leading=13.2, textColor=colors.HexColor("#1B2A3A"),
                spaceBefore=0, spaceAfter=5, alignment=TA_JUSTIFY)
    base.update(kw)
    return ParagraphStyle(name, **base)


BODY = _s("body")
BODY_C = _s("bodyc", alignment=TA_CENTER)
BODY_L = _s("bodyl", alignment=TA_LEFT)
LEAD = _s("lead", fontSize=10.4, leading=15, textColor=GREY)
BULLET_S = _s("bullet", fontSize=9.2, leading=12.8, leftIndent=11, bulletIndent=1,
              spaceAfter=3.2, alignment=TA_LEFT)
BULLET2_S = _s("bullet2", fontSize=8.9, leading=12.2, leftIndent=23, bulletIndent=13,
               spaceAfter=2.6, alignment=TA_LEFT)
NOTE = _s("note", fontSize=8.4, leading=11.6, textColor=GREY, alignment=TA_LEFT)
FIGCAP = _s("figcap", fontSize=7.8, leading=10.4, textColor=GREY, alignment=TA_CENTER,
            fontName=FONT_I, spaceBefore=3, spaceAfter=9)
TH = _s("th", fontName=FONT_B, fontSize=7.5, leading=9.6, textColor=WHITE, alignment=TA_LEFT,
        spaceAfter=0)
TC = _s("tc", fontSize=7.4, leading=9.9, alignment=TA_LEFT, spaceAfter=0)
TC_B = _s("tcb", fontSize=7.4, leading=9.9, fontName=FONT_B, alignment=TA_LEFT, spaceAfter=0)
TC_C = _s("tcc", fontSize=7.6, leading=9.9, alignment=TA_CENTER, spaceAfter=0)
TC_SM = _s("tcsm", fontSize=6.8, leading=9.0, alignment=TA_LEFT, spaceAfter=0)

H1 = _s("h1", fontName=FONT_B, fontSize=16.5, leading=20, textColor=NAVY, alignment=TA_LEFT,
        spaceBefore=2, spaceAfter=2)
H2 = _s("h2", fontName=FONT_B, fontSize=12.2, leading=15.5, textColor=TEAL_D, alignment=TA_LEFT,
        spaceBefore=11, spaceAfter=4)
H3 = _s("h3", fontName=FONT_B, fontSize=10.2, leading=13.4, textColor=NAVY, alignment=TA_LEFT,
        spaceBefore=8, spaceAfter=3)
H4 = _s("h4", fontName=FONT_BI, fontSize=9.2, leading=12.2, textColor=GREY, alignment=TA_LEFT,
        spaceBefore=6, spaceAfter=2)

COVER_KICK = _s("ck", fontName=FONT_B, fontSize=10.5, leading=14, textColor=colors.HexColor("#8FD8D6"),
                alignment=TA_CENTER)
COVER_T = _s("ct", fontName=FONT_B, fontSize=27, leading=32, textColor=WHITE, alignment=TA_CENTER)
COVER_ST = _s("cst", fontName=FONT, fontSize=13, leading=18, textColor=colors.HexColor("#D7E4EF"),
              alignment=TA_CENTER)
COVER_META = _s("cm", fontName=FONT_B, fontSize=9.2, leading=13, textColor=colors.HexColor("#B9CBDB"),
                alignment=TA_CENTER)


# --------------------------------------------------------------------------- #
# 3. Small content helpers
# --------------------------------------------------------------------------- #
class HR(Flowable):
    def __init__(self, width=None, thickness=0.7, color=LINE, space=4):
        super().__init__()
        self.width = width or FRAME_W
        self.thickness = thickness
        self.color = color
        self.space = space
        self.height = thickness + space

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.space, self.width, self.space)


def para(text, style=None):
    return Paragraph(text, style or BODY)


def bullets(items, style=None, sub=False):
    st = style or (BULLET2_S if sub else BULLET_S)
    out = []
    for it in items:
        if isinstance(it, (list, tuple)):
            out.extend(bullets(list(it), style=style, sub=True))
        else:
            out.append(Paragraph(it, st, bulletText=BULLET))
    return out


def _cell(v, style):
    if v is None:
        return ""
    if isinstance(v, Paragraph):
        return v
    return Paragraph(str(v), style)


def make_table(header, rows, widths, aligns=None, font_small=False, repeat_header=1,
               header_bg=NAVY, zebra=True, body_align_center_cols=()):
    cs = TC_SM if font_small else TC
    data = [[_cell(h, TH) for h in header]]
    for r in rows:
        data.append([_cell(c, cs) for c in r])
    t = Table(data, colWidths=widths, repeatRows=repeat_header, hAlign="LEFT")
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4.2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4.2),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, LINE),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#A9B7C6")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.9, header_bg),
    ]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                cmds.append(("BACKGROUND", (0, i), (-1, i), GREY_L))
    if aligns:
        for i, w in enumerate(aligns):
            if w == "C":
                cmds.append(("ALIGN", (i, 1), (i, -1), "CENTER"))
            elif w == "R":
                cmds.append(("ALIGN", (i, 1), (i, -1), "RIGHT"))
    for c in body_align_center_cols:
        cmds.append(("ALIGN", (c, 1), (c, -1), "CENTER"))
    t.setStyle(TableStyle(cmds))
    return t


def callout(title, body_html, tone="info"):
    bg = {"info": BLUE_L, "warn": AMBER_L, "risk": RED_L, "ok": GREEN_L}[tone]
    bar = {"info": NAVY, "warn": AMBER, "risk": RED, "ok": TEAL}[tone]
    inner = [Paragraph("<b>%s</b>" % title, _s("cot", fontName=FONT_B, fontSize=8.8, leading=11.6,
                                              textColor=bar, spaceAfter=3, alignment=TA_LEFT))]
    if isinstance(body_html, str):
        body_html = [body_html]
    for b in body_html:
        inner.append(Paragraph(b, _s("cob", fontSize=8.4, leading=11.6, spaceAfter=2,
                                     alignment=TA_LEFT)))
    t = Table([[inner]], colWidths=[FRAME_W], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 2.6, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return KeepTogether([Spacer(1, 3), t, Spacer(1, 7)])


# --------------------------------------------------------------------------- #
# 4. Chevron journey strip (horizontal, boustrophedon wrapping)
# --------------------------------------------------------------------------- #
class ChevronFlow(Flowable):
    """Compact horizontal journey strip. steps = [(title, description), ...]"""

    def __init__(self, steps, cols=3, width=None, row_h=None, accent=TEAL, number=True):
        super().__init__()
        self.steps = steps
        self.cols = cols
        self.width = width or FRAME_W
        self.accent = accent
        self.number = number
        self.gap = 3.0
        self.notch = 9.0
        self.cw = (self.width - self.gap * (cols - 1)) / float(cols)
        self.row_h = row_h or self._measure_row()
        self.rows = (len(steps) + cols - 1) // cols
        self.height = self.rows * self.row_h + (self.rows - 1) * 9.0 + 4

    def _measure_row(self):
        from reportlab.lib.utils import simpleSplit
        avail = self.cw - self.notch - 18
        max_lines = 1
        for title, desc in self.steps:
            tl = len(simpleSplit(title, FONT_B, 7.4, avail))
            dl = min(len(simpleSplit(desc or "", FONT, 6.6, avail + 4)), 3)
            max_lines = max(max_lines, tl + dl)
        return max(32, 15 + max_lines * 8.6)

    def wrap(self, aw, ah):
        return (self.width, self.height)

    def _chevron(self, c, x, y, w, h, first):
        n = self.notch
        p = c.beginPath()
        if first:
            p.moveTo(x, y)              # top-left
        else:
            p.moveTo(x, y + h / 2.0)    # left notch centre
            p.lineTo(x + n, y)          # top-left
        p.lineTo(x + w - n, y)          # top-right
        p.lineTo(x + w, y + h / 2.0)    # right tip
        p.lineTo(x + w - n, y + h)      # bottom-right
        if first:
            p.lineTo(x, y + h)          # bottom-left
        else:
            p.lineTo(x + n, y + h)      # bottom-left notch
        p.close()
        return p

    def draw(self):
        c = self.canv
        for i, (title, desc) in enumerate(self.steps):
            row = i // self.cols
            col = i % self.cols
            reversed_row = (row % 2 == 1)
            pos = (self.cols - 1 - col) if reversed_row else col
            x = pos * (self.cw + self.gap)
            y = self.height - (row + 1) * self.row_h - row * 9.0 + 2
            light = colors.Color(0.93, 0.96, 0.98) if row % 2 == 0 else colors.Color(0.90, 0.95, 0.95)
            c.setFillColor(light)
            c.setStrokeColor(self.accent)
            c.setLineWidth(0.5)
            c.drawPath(self._chevron(c, x, y, self.cw, self.row_h, col == 0), stroke=1, fill=1)
            # accent tab on the left edge
            c.setFillColor(self.accent)
            if col == 0:
                c.rect(x, y, 2.2, self.row_h, stroke=0, fill=1)
            else:
                p = c.beginPath()
                p.moveTo(x, y + self.row_h / 2.0)
                p.lineTo(x + self.notch, y)
                p.lineTo(x + self.notch + 2.0, y)
                p.lineTo(x + 2.0, y + self.row_h / 2.0)
                p.lineTo(x + self.notch + 2.0, y + self.row_h)
                p.lineTo(x + self.notch, y + self.row_h)
                p.close()
                c.drawPath(p, stroke=0, fill=1)
            # number badge
            tx = x + self.notch + 6
            if self.number:
                c.setFillColor(self.accent)
                c.circle(tx + 3.2, y + self.row_h - 8.5, 5.0, stroke=0, fill=1)
                c.setFillColor(WHITE)
                c.setFont(FONT_B, 6.0)
                c.drawCentredString(tx + 3.2, y + self.row_h - 10.6, str(i + 1))
                tx += 11
            avail_t = x + self.cw - self.notch - 6 - tx
            c.setFillColor(NAVY)
            c.setFont(FONT_B, 7.4)
            yy = y + self.row_h - 10.4
            title_lines = self._wrap(title, avail_t, FONT_B, 7.4, 2)
            for ln in title_lines:
                c.drawString(tx, yy, ln)
                yy -= 8.6
            if desc:
                c.setFillColor(GREY)
                c.setFont(FONT, 6.6)
                yy -= 0.6
                for ln in self._wrap(desc, avail_t + 4, FONT, 6.6, 3):
                    c.drawString(tx, yy, ln)
                    yy -= 7.8
        # serpentine connectors between rows
        c.setStrokeColor(colors.HexColor("#94A6B8"))
        c.setLineWidth(0.9)
        for row in range(self.rows - 1):
            yb = self.height - (row + 1) * self.row_h - row * 9.0 + 2 - self.row_h
            yt = self.height - (row + 2) * self.row_h - (row + 1) * 9.0 + 2
            cx = (self.width - 3) if row % 2 == 0 else 3
            c.line(cx, yb, cx, yt + 3.5)
            c.setFillColor(colors.HexColor("#94A6B8"))
            p = c.beginPath()
            p.moveTo(cx, yt - 1.2)
            p.lineTo(cx - 3, yt + 4.2)
            p.lineTo(cx + 3, yt + 4.2)
            p.close()
            c.drawPath(p, stroke=0, fill=1)

    @staticmethod
    def _clip(text, avail, font, size):
        if pdfmetrics.stringWidth(text, font, size) <= avail:
            return text
        while text and pdfmetrics.stringWidth(text + "\u2026", font, size) > avail:
            text = text[:-1]
        return text + ("\u2026" if EMBEDDED else "...")

    @staticmethod
    def _wrap(text, avail, font, size, maxlines=3):
        words, lines, cur = text.split(), [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if pdfmetrics.stringWidth(trial, font, size) <= avail or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        if len(lines) > maxlines:
            keep = lines[:maxlines]
            tail = keep[-1]
            while tail and pdfmetrics.stringWidth(tail + "\u2026", font, size) > avail:
                tail = tail[:-1]
            keep[-1] = tail + ("\u2026" if EMBEDDED else "...")
            return keep
        return lines


# --------------------------------------------------------------------------- #
# 5. Vertical process flow (process boxes, decisions, outcomes, parallel)
# --------------------------------------------------------------------------- #
NODE = {
    "step":     (NAVY,   BLUE_L),
    "start":    (TEAL,   GREEN_L),
    "decision": (AMBER,  AMBER_L),
    "yes":      (TEAL_D, GREEN_L),
    "no":       (RED,    RED_L),
    "end":      (NAVY_D, colors.HexColor("#DCE6F0")),
    "parallel": (TEAL,   colors.HexColor("#E8F1F1")),
}


class ProcessFlow(Flowable):
    """
    nodes = [
      ('step', 'Title', 'description'),
      ('decision', 'Question?', None),
      ('yes', 'Approved', 'what happens'),
      ('no', 'Returned', 'what happens'),
      ('parallel', 'Parallel activities', ['A ...', 'B ...', 'C ...']),
    ]
    """

    def __init__(self, nodes, width=None, node_w=None):
        super().__init__()
        self.nodes = nodes
        self.width = width or FRAME_W
        self.nw = node_w or (self.width - 16)
        self._layout()

    # -- layout ----------------------------------------------------------- #
    def _text_h(self, desc, w, fs=7.3, lh=9.4):
        if not desc:
            return 0
        from reportlab.lib.utils import simpleSplit
        lines = simpleSplit(str(desc), FONT, fs, w)
        return len(lines) * lh

    def _layout(self):
        y = 0.0
        self.items = []
        for i, nd in enumerate(self.nodes):
            kind = nd[0]
            title = nd[1] if len(nd) > 1 else ""
            desc = nd[2] if len(nd) > 2 else None
            if kind == "parallel":
                rows = [str(x) for x in (desc or [])]
                h = 9.0 + len(rows) * 11.6 + 6
                self.items.append(dict(kind=kind, title=title, rows=rows, y=y, h=h, x=26))
                y += h + 12
                continue
            if kind in ("yes", "no"):
                w = self.nw - 46
                dh = self._text_h(desc, w - 20)
                h = 13 + max(dh, 0) + 6
                self.items.append(dict(kind=kind, title=title, desc=desc, y=y, h=h, x=48, w=w))
            else:
                w = self.nw
                dh = self._text_h(desc, w - 26)
                h = 13.5 + max(dh, 0) + 6.5
                self.items.append(dict(kind=kind, title=title, desc=desc, y=y, h=h, x=26, w=w))
            y += h + 12
        self.height = max(y - 12 + 4, 24)
        self.width_used = self.nw + 30

    def wrap(self, aw, ah):
        return (self.width, self.height)

    # -- drawing ---------------------------------------------------------- #
    def _connect(self, c, y_top):
        c.setStrokeColor(colors.HexColor("#94A6B8"))
        c.setLineWidth(0.9)
        c.line(38, y_top, 38, y_top - 8.2)
        c.setFillColor(colors.HexColor("#94A6B8"))
        p = c.beginPath()
        p.moveTo(38, y_top - 11.6)
        p.lineTo(34.6, y_top - 6.4)
        p.lineTo(41.4, y_top - 6.4)
        p.close()
        c.drawPath(p, stroke=0, fill=1)

    def draw(self):
        from reportlab.lib.utils import simpleSplit
        c = self.canv
        prev_bottom = None
        for idx, it in enumerate(self.items):
            kind, title = it["kind"], it["title"]
            bar, bg = NODE.get(kind, NODE["step"])
            x, w, h = it["x"], it.get("w", self.nw), it["h"]
            y = self.height - it["y"] - h
            if prev_bottom is not None:
                self._connect(c, prev_bottom)
            prev_bottom = y
            c.setFillColor(bg)
            c.setStrokeColor(bar)
            c.setLineWidth(0.7)
            c.roundRect(x, y, w, h, 2.4, stroke=1, fill=1)
            c.setFillColor(bar)
            c.rect(x, y, 3.0, h, stroke=0, fill=1)
            if kind == "decision":
                c.setFillColor(bar)
                p = c.beginPath()
                cx, cy = x + w - 12, y + h - 9.5
                p.moveTo(cx, cy + 5.4)
                p.lineTo(cx + 5.4, cy)
                p.lineTo(cx, cy - 5.4)
                p.lineTo(cx - 5.4, cy)
                p.close()
                c.drawPath(p, stroke=0, fill=1)
                c.setFillColor(WHITE)
                c.setFont(FONT_B, 6.4)
                c.drawCentredString(cx, cy - 2.2, "?")
            # index chip
            c.setFillColor(bar)
            c.setFont(FONT_B, 6.2)
            c.drawString(x + 8, y + h - 9.0, str(idx + 1).zfill(2))
            c.setFillColor(NAVY)
            c.setFont(FONT_B, 8.0)
            c.drawString(x + 24, y + h - 9.6, self._clip(title, w - 44, FONT_B, 8.0))
            if kind == "parallel":
                yy = y + h - 20
                for r in it["rows"]:
                    c.setFillColor(bar)
                    c.circle(x + 14, yy + 2.4, 1.7, stroke=0, fill=1)
                    c.setFillColor(colors.HexColor("#22384C"))
                    c.setFont(FONT, 7.3)
                    for j, ln in enumerate(simpleSplit(str(r), FONT, 7.3, w - 34)[:2]):
                        c.drawString(x + 22, yy - j * 9.4, ln)
                        if j:
                            yy -= 9.4
                    yy -= 11.6
            elif it.get("desc"):
                c.setFillColor(colors.HexColor("#22384C"))
                c.setFont(FONT, 7.3)
                yy = y + h - 19.5
                for ln in simpleSplit(str(it["desc"]), FONT, 7.3, w - 30):
                    c.drawString(x + 24, yy, ln)
                    yy -= 9.4

    @staticmethod
    def _clip(text, avail, font, size):
        if pdfmetrics.stringWidth(text, font, size) <= avail:
            return text
        while text and pdfmetrics.stringWidth(text + "\u2026", font, size) > avail:
            text = text[:-1]
        return text + ("\u2026" if EMBEDDED else "...")


def figure(flowable, caption):
    return KeepTogether([Spacer(1, 4), flowable, Paragraph(caption, FIGCAP)])


# --------------------------------------------------------------------------- #
# 6. Document template: cover page + body page with header/footer
# --------------------------------------------------------------------------- #
DOC_TITLE = "YPDC Website & Portal System"
DOC_SUB = "System Workflow Specification"


class ReportDoc(BaseDocTemplate):
    def __init__(self, path, **kw):
        super().__init__(path, pagesize=A4, leftMargin=LM, rightMargin=RM,
                         topMargin=TM, bottomMargin=BM,
                         title="YPDC Website & Portal System - Workflow Specification Report",
                         author="YPDC Digital Secretariat", subject="Workflow specification",
                         **kw)
        cover = PageTemplate(id="cover", frames=[Frame(0, 0, PAGE_W, PAGE_H, id="cf",
                                                       leftPadding=0, rightPadding=0,
                                                       topPadding=0, bottomPadding=0)],
                             onPage=self._cover_bg)
        body = PageTemplate(id="body", frames=[Frame(LM, BM, FRAME_W, PAGE_H - TM - BM, id="bf",
                                                     leftPadding=0, rightPadding=0,
                                                     topPadding=0, bottomPadding=0)],
                            onPage=self._body_deco)
        self.addPageTemplates([cover, body])
        self._h1 = 0
        self._h2 = 0

    # -- cover ------------------------------------------------------------ #
    def _cover_bg(self, canv, doc):
        canv.saveState()
        canv.setFillColor(NAVY)
        canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        canv.setFillColor(NAVY_D)
        canv.rect(0, 0, PAGE_W, 78 * mm, stroke=0, fill=1)
        # accent band
        canv.setFillColor(TEAL)
        canv.rect(0, PAGE_H - 8 * mm, PAGE_W, 3.2 * mm, stroke=0, fill=1)
        canv.setFillColor(AMBER)
        canv.rect(0, PAGE_H - 9.6 * mm, PAGE_W, 1.6 * mm, stroke=0, fill=1)
        # faint portal blocks
        canv.setFillColor(colors.Color(1, 1, 1, 0.045))
        for i in range(7):
            x = 18 * mm + i * 25 * mm
            canv.roundRect(x, 96 * mm, 19 * mm, 12 * mm, 2 * mm, stroke=0, fill=1)
        canv.setFillColor(colors.Color(1, 1, 1, 0.10))
        canv.setFont(FONT_B, 8)
        labels = ["GUEST", "STUDENT", "MEMBER", "DIRECT.", "FACULTY", "ADMIN", "ALUMNI"]
        for i, lab in enumerate(labels):
            x = 18 * mm + i * 25 * mm
            canv.drawCentredString(x + 9.5 * mm, 101 * mm, lab)
        canv.setFillColor(colors.Color(1, 1, 1, 0.06))
        canv.setFont(FONT_B, 150)
        canv.drawString(14 * mm, 18 * mm, "YPDC")
        canv.restoreState()

    # -- body ------------------------------------------------------------- #
    def _body_deco(self, canv, doc):
        canv.saveState()
        # header
        canv.setFillColor(NAVY)
        canv.rect(0, PAGE_H - 15 * mm, PAGE_W, 15 * mm, stroke=0, fill=1)
        canv.setFillColor(TEAL)
        canv.rect(0, PAGE_H - 15 * mm, PAGE_W, 1.1 * mm, stroke=0, fill=1)
        canv.setFillColor(WHITE)
        canv.setFont(FONT_B, 8.4)
        canv.drawString(LM, PAGE_H - 9.6 * mm, "YPDC")
        canv.setFont(FONT, 7.6)
        canv.setFillColor(colors.HexColor("#B9CBDB"))
        canv.drawString(LM + 13 * mm, PAGE_H - 9.6 * mm, DOC_SUB)
        canv.setFont(FONT, 7.2)
        canv.drawRightString(PAGE_W - RM, PAGE_H - 9.6 * mm,
                             "Version 1.0  |  %s" % date.today().strftime("%d %b %Y"))
        # footer
        canv.setStrokeColor(LINE)
        canv.setLineWidth(0.6)
        canv.line(LM, BM - 6 * mm, PAGE_W - RM, BM - 6 * mm)
        canv.setFont(FONT, 7.0)
        canv.setFillColor(GREY)
        canv.drawString(LM, BM - 10.5 * mm, "YPDC Website & Portal System - Workflow Specification")
        canv.drawCentredString(PAGE_W / 2.0, BM - 10.5 * mm, "Internal / Planning Use")
        canv.setFont(FONT_B, 7.6)
        canv.setFillColor(NAVY)
        canv.drawRightString(PAGE_W - RM, BM - 10.5 * mm, "Page %d" % canv.getPageNumber())
        canv.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            st = flowable.style.name
            if st == "h1":
                text = flowable.getPlainText()
                key = "h1-%d" % self._h1
                self._h1 += 1
                self._h2 = 0
                self.canv.bookmarkPage(key)
                self.notify("TOCEntry", (0, text, self.page, key))
            elif st == "h2":
                text = flowable.getPlainText()
                key = "h2-%d-%d" % (self._h1, self._h2)
                self._h2 += 1
                self.canv.bookmarkPage(key)
                self.notify("TOCEntry", (1, text, self.page, key))

    def beforeDocument(self):
        # reset heading counters at the start of every pass so that
        # bookmark keys are stable and multiBuild can converge
        self._h1 = 0
        self._h2 = 0


# --------------------------------------------------------------------------- #
# 7. Numbered sections
# --------------------------------------------------------------------------- #
class Sec:
    def __init__(self):
        self.n = [0, 0]

    def h1(self, text, numbered=True):
        if numbered:
            self.n[0] += 1
            self.n[1] = 0
            label = "%d. %s" % (self.n[0], text)
        else:
            label = text
        return Paragraph(label, H1)

    def h2(self, text, numbered=True):
        if numbered:
            self.n[1] += 1
            label = "%d.%d %s" % (self.n[0], self.n[1], text)
        else:
            label = text
        return Paragraph(label, H2)


# --------------------------------------------------------------------------- #
# 8. Build
# --------------------------------------------------------------------------- #
def build(out_path):
    import content

    doc = ReportDoc(out_path)
    story = []

    # ---- cover ---------------------------------------------------------- #
    story.append(Spacer(1, 46 * mm))
    story.append(Paragraph("WORKFLOW SPECIFICATION REPORT", COVER_KICK))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("YPDC", _s("ct0", fontName=FONT_B, fontSize=44, leading=48,
                                      textColor=WHITE, alignment=TA_CENTER)))
    story.append(Paragraph("Website &amp; Portal System", COVER_T))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "Seven-Portal Digital Platform <font color='#8FD8D8'>|</font> Guest "
        "\u00b7 Student \u00b7 Member \u00b7 Directorate \u00b7 Faculty \u00b7 Admin \u00b7 Alumni",
        COVER_ST))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("End-to-end business workflows, module inventory, "
                           "approval chains and role-based access model", COVER_ST))
    story.append(Spacer(1, 34 * mm))
    story.append(Paragraph(
        "Prepared for: YPDC Executive Committee &amp; Project Sponsors<br/>"
        "Prepared by: YPDC Digital Secretariat<br/>"
        "Version 1.0 (Draft for Approval) \u00b7 %s" % date.today().strftime("%d %B %Y"),
        COVER_META))
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    # ---- body content --------------------------------------------------- #
    sec = Sec()
    story.extend(content.build(sec, globals()))

    doc.multiBuild(story)
    return out_path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    root = os.path.dirname(os.path.dirname(here))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "YPDC-Website-Workflow-Report.pdf")
    build(out)
    size = os.path.getsize(out)
    print("PDF written: %s (%.1f KB)  fonts_embedded=%s" % (out, size / 1024.0, EMBEDDED))
