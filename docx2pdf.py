"""Render the generated .docx copy deck to PDF, preserving order,
headings, tables and fill-in shading. Reads the docx so the two
deliverables cannot drift apart."""

import docx
from docx.table import Table as DocxTable
from docx.text.paragraph import Paragraph as DocxParagraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak, KeepTogether,
)
from xml.etree import ElementTree as ET
import re

SRC = "Sezibera-Construction-Content-Request.docx"
OUT = "Sezibera-Construction-Content-Request.pdf"

W, H = A4
MARGIN = 19 * mm
CONTENT_W = W - 2 * MARGIN

INK = colors.HexColor("#151515")
GREY = colors.HexColor("#6E6E6E")
RED = colors.HexColor("#B00020")
LIGHT = colors.HexColor("#F2F2F2")
FILLBG = colors.HexColor("#FBFBEF")
RULE = colors.HexColor("#CCCCCC")

S = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=26, leading=30,
                            textColor=INK, spaceAfter=6),
    "subtitle": ParagraphStyle("subtitle", fontName="Helvetica", fontSize=16, leading=20,
                               textColor=GREY, spaceAfter=14),
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=17, leading=21,
                         textColor=INK, spaceBefore=16, spaceAfter=9),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13, leading=17,
                         textColor=INK, spaceBefore=12, spaceAfter=6),
    "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11, leading=15,
                         textColor=INK, spaceBefore=9, spaceAfter=5),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=13.5,
                           textColor=INK, spaceAfter=6),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=13.5,
                             textColor=INK, leftIndent=12, bulletIndent=2, spaceAfter=3),
    "check": ParagraphStyle("check", fontName="Helvetica", fontSize=9.5, leading=13.5,
                            textColor=INK, leftIndent=14, spaceAfter=3.5),
    "check_label": ParagraphStyle("check_label", fontName="Helvetica", fontSize=9.5,
                                  leading=12.5, textColor=INK),
    "cellh": ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=7.8, leading=10,
                            textColor=colors.white),
    "cellk": ParagraphStyle("cellk", fontName="Helvetica-Bold", fontSize=8.4, leading=11,
                            textColor=INK),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=11,
                           textColor=INK),
    "cellg": ParagraphStyle("cellg", fontName="Helvetica-Oblique", fontSize=8.2, leading=10.6,
                            textColor=GREY),
}

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def checkbox_row(text, width=None):
    """A real hollow tick-box beside the label.

    The base-14 PDF fonts have no empty-box glyph — every candidate in
    ZapfDingbats renders as a filled square — so the box is drawn as a
    bordered table cell instead.
    """
    w = width if width is not None else CONTENT_W
    gutter = 22

    box = Table([[""]], colWidths=[8.5], rowHeights=[8.5])
    box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    t = Table([[box, Paragraph(esc(text), S["check_label"])]],
              colWidths=[gutter, w - gutter])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 13),
        ("RIGHTPADDING", (0, 0), (0, 0), 0),
        ("LEFTPADDING", (1, 0), (1, 0), 7),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (0, 0), (0, 0), 3),
        ("TOPPADDING", (1, 0), (1, 0), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return t


def iter_block_items(parent):
    body = parent.element.body
    for child in body.iterchildren():
        if child.tag == W_NS + "p":
            yield DocxParagraph(child, parent)
        elif child.tag == W_NS + "tbl":
            yield DocxTable(child, parent)


def para_has_pagebreak(p):
    return bool(p._p.findall(f".//{W_NS}br[@{W_NS}type='page']"))


def cell_fill(c):
    shd = c._tc.find(f".//{W_NS}shd")
    if shd is None:
        return None
    v = shd.get(W_NS + "fill")
    if not v or v in ("auto", "FFFFFF"):
        return None
    return colors.HexColor("#" + v)


def para_size(p):
    for r in p.runs:
        if r.font.size:
            return r.font.size.pt
    return None


def para_color(p):
    for r in p.runs:
        try:
            if r.font.color and r.font.color.rgb:
                return "#" + str(r.font.color.rgb)
        except Exception:
            pass
    return None


def build_para(p):
    """Map a docx paragraph to a reportlab flowable."""
    text = p.text.strip()
    style_name = ""
    try:
        if p.style is not None and p.style.name:
            style_name = p.style.name.lower()
    except Exception:
        pass
    # docx-js writes the outline level directly rather than a named style
    if not style_name:
        st_el = p._p.find(f".//{W_NS}pStyle")
        if st_el is not None:
            style_name = (st_el.get(W_NS + "val") or "").lower()

    if not text:
        return Spacer(1, 4)

    size = para_size(p)
    col = para_color(p)
    bold = any(r.bold for r in p.runs if r.bold)

    # Checkbox lines
    if text.startswith("☐"):
        return checkbox_row(text.lstrip("☐").strip())

    # Bullets
    if p._p.find(f".//{W_NS}numPr") is not None:
        return Paragraph(esc(text), S["bullet"], bulletText="•")

    flat = style_name.replace(" ", "")
    if flat.startswith("heading1"):
        return Paragraph(esc(text), S["h1"])
    if flat.startswith("heading2"):
        return Paragraph(esc(text), S["h2"])
    if flat.startswith("heading3"):
        return Paragraph(esc(text), S["h3"])

    # Cover title / subtitle by size
    if size and size >= 21:
        return Paragraph(esc(text), S["title"])
    if size and size >= 14:
        return Paragraph(esc(text), S["subtitle"])
    if size and size >= 11.5:
        st = ParagraphStyle("big", parent=S["body"], fontSize=11.5, leading=15,
                            fontName="Helvetica-Bold" if bold else "Helvetica")
        return Paragraph(esc(text), st)

    st = S["body"]
    if bold or col:
        st = ParagraphStyle(
            "v", parent=S["body"],
            fontName="Helvetica-Bold" if bold else "Helvetica",
            textColor=colors.HexColor(col) if col else INK,
        )
    return Paragraph(esc(text), st)


def build_table(t):
    ncols = len(t.columns)
    grid = t._tbl.find(f"{W_NS}tblGrid")
    widths = [int(g.get(W_NS + "w")) for g in grid.findall(f"{W_NS}gridCol")]
    total = sum(widths) or 1
    col_w = [CONTENT_W * w / total for w in widths]

    data, styles = [], [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
    ]

    for ri, row in enumerate(t.rows):
        cells, seen = [], set()
        for ci, c in enumerate(row.cells):
            if id(c._tc) in seen:
                cells.append("")
                continue
            seen.add(id(c._tc))

            fill = cell_fill(c)
            if fill:
                styles.append(("BACKGROUND", (ci, ri), (ci, ri), fill))

            is_header = fill is not None and str(fill) == str(INK)
            parts = []
            for cp in c.paragraphs:
                txt = cp.text.strip()
                if not txt:
                    continue
                if txt.startswith("☐"):
                    parts.append(checkbox_row(txt.lstrip("☐").strip(),
                                              width=col_w[ci] - 12))
                    continue
                if is_header:
                    st = S["cellh"]
                else:
                    cb = any(r.bold for r in cp.runs if r.bold)
                    ital = any(r.italic for r in cp.runs if r.italic)
                    ccol = para_color(cp)
                    if ccol and ccol.upper() == "#B00020":
                        st = ParagraphStyle("cr", parent=S["cellk"], textColor=RED, fontSize=9)
                    elif ital:
                        st = S["cellg"]
                    elif cb:
                        st = S["cellk"]
                    else:
                        st = S["cell"]
                parts.append(Paragraph(esc(txt), st))
            cells.append(parts if parts else "")
        data.append(cells)

    # Single-cell callouts should not be split across pages
    tbl = Table(data, colWidths=col_w, repeatRows=1 if ncols > 1 else 0)
    tbl.setStyle(TableStyle(styles))
    return tbl


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GREY)
    canvas.drawString(MARGIN, 11 * mm, "Sezibera Construction — Website Copy Deck & Content Request")
    canvas.drawRightString(W - MARGIN, 11 * mm, str(doc.page))
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN, 14.5 * mm, W - MARGIN, 14.5 * mm)
    canvas.restoreState()


def main():
    src = docx.Document(SRC)
    story = []

    for block in iter_block_items(src):
        if isinstance(block, DocxTable):
            story.append(Spacer(1, 3))
            story.append(build_table(block))
            story.append(Spacer(1, 7))
        else:
            if para_has_pagebreak(block):
                story.append(PageBreak())
                continue
            story.append(build_para(block))

    doc = BaseDocTemplate(
        OUT, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=22 * mm,
        title="Sezibera Construction — Website Copy Deck & Content Request",
        author="Sezibera Construction website project",
    )
    frame = Frame(MARGIN, 22 * mm, CONTENT_W, H - MARGIN - 22 * mm, id="body")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=footer)])
    doc.build(story)
    print("PDF written")


if __name__ == "__main__":
    main()
