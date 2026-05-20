#!/usr/bin/env python3
"""Generate reference.docx used by pandoc as the style template.

Produces an academic paper style that mirrors the arXiv / NeurIPS DOCX look:
  - A4, narrow margins (matching the LaTeX template)
  - Times New Roman (Latin) + Malgun Gothic (Korean)
  - Single-column header area; two-column body handled by postprocess_docx.py
  - Heading 1: bold, 10 pt, numbered appearance
  - Abstract / keyword block in 9 pt
"""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def ensure_rpr(style):
    rpr = style._element.rPr
    if rpr is None:
        rpr = OxmlElement('w:rPr')
        style._element.append(rpr)
    return rpr


def set_style_font(style, latin=None, east_asia=None, size=None, bold=None):
    rpr = ensure_rpr(style)
    rfonts = rpr.rFonts
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)

    if latin is not None:
        style.font.name = latin
        rfonts.set(qn('w:ascii'), latin)
        rfonts.set(qn('w:hAnsi'), latin)
    if east_asia is not None:
        rfonts.set(qn('w:eastAsia'), east_asia)
    if size is not None:
        style.font.size = Pt(size)
    if bold is not None:
        style.font.bold = bold


# ---------------------------------------------------------------------------
# Build document
# ---------------------------------------------------------------------------

doc = Document()

# --- Page geometry: A4, narrow margins (matches LaTeX template) ----------
section = doc.sections[0]
section.page_width  = Mm(210)
section.page_height = Mm(297)
section.top_margin    = Mm(19.1)
section.bottom_margin = Mm(25.4)
section.left_margin   = Mm(17)
section.right_margin  = Mm(17)
section.header_distance = Mm(10)
section.footer_distance = Mm(10)

# --- Normal (body text) ---------------------------------------------------
normal = doc.styles['Normal']
set_style_font(normal, latin='Times New Roman', east_asia='Malgun Gothic', size=10)
normal.paragraph_format.line_spacing = Pt(13)   # ~1.0 × 13 pt leading
normal.paragraph_format.space_after  = Pt(2)
normal.paragraph_format.first_line_indent = Pt(10)

# Body Text variants used by pandoc
for style_name in ['Body Text', 'First Paragraph', 'Compact']:
    if style_name in doc.styles:
        s = doc.styles[style_name]
        set_style_font(s, latin='Times New Roman', east_asia='Malgun Gothic', size=10)
        s.paragraph_format.line_spacing = Pt(13)
        s.paragraph_format.space_after  = Pt(2)

# --- Title ----------------------------------------------------------------
title = doc.styles['Title']
set_style_font(title, latin='Times New Roman', east_asia='Malgun Gothic', size=14, bold=True)
title.paragraph_format.alignment   = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_after = Pt(6)
title.paragraph_format.space_before = Pt(0)
title.paragraph_format.first_line_indent = Pt(0)

# --- Author / Date / Subtitle (centered metadata lines) ------------------
for style_name in ['Author', 'Date', 'Subtitle']:
    if style_name in doc.styles:
        s = doc.styles[style_name]
        set_style_font(s, latin='Times New Roman', east_asia='Malgun Gothic', size=10)
        s.paragraph_format.alignment   = WD_ALIGN_PARAGRAPH.CENTER
        s.paragraph_format.space_after = Pt(2)
        s.paragraph_format.first_line_indent = Pt(0)

# --- Abstract (9 pt, no indent, slight space) ----------------------------
if 'Abstract' in doc.styles:
    abs_style = doc.styles['Abstract']
else:
    abs_style = doc.styles.add_style('Abstract', doc.styles['Normal'].style_type)
set_style_font(abs_style, latin='Times New Roman', east_asia='Malgun Gothic', size=9)
abs_style.paragraph_format.space_before = Pt(4)
abs_style.paragraph_format.space_after  = Pt(4)
abs_style.paragraph_format.first_line_indent = Pt(0)

# --- Headings -------------------------------------------------------------
# Heading 1: bold 10 pt, space before 10 pt — arXiv / IEEE section style
h1 = doc.styles['Heading 1']
set_style_font(h1, latin='Times New Roman', east_asia='Malgun Gothic', size=10, bold=True)
h1.paragraph_format.space_before = Pt(10)
h1.paragraph_format.space_after  = Pt(4)
h1.paragraph_format.first_line_indent = Pt(0)

# Heading 2: bold italic 10 pt
if 'Heading 2' in doc.styles:
    h2 = doc.styles['Heading 2']
    set_style_font(h2, latin='Times New Roman', east_asia='Malgun Gothic', size=10, bold=True)
    h2.font.italic = True
    h2.paragraph_format.space_before = Pt(6)
    h2.paragraph_format.space_after  = Pt(3)
    h2.paragraph_format.first_line_indent = Pt(0)

# Heading 3: italic 10 pt
if 'Heading 3' in doc.styles:
    h3 = doc.styles['Heading 3']
    set_style_font(h3, latin='Times New Roman', east_asia='Malgun Gothic', size=10)
    h3.font.italic = True
    h3.paragraph_format.space_before = Pt(4)
    h3.paragraph_format.space_after  = Pt(2)
    h3.paragraph_format.first_line_indent = Pt(0)

# --- Tables ---------------------------------------------------------------
for style_name in ['Table', 'Table Grid']:
    if style_name in doc.styles:
        set_style_font(doc.styles[style_name],
                       latin='Times New Roman', east_asia='Malgun Gothic', size=9)

# --- Caption --------------------------------------------------------------
if 'Caption' in doc.styles:
    cap = doc.styles['Caption']
    set_style_font(cap, latin='Times New Roman', east_asia='Malgun Gothic', size=9, bold=False)
    cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(2)
    cap.paragraph_format.space_after  = Pt(2)
    cap.paragraph_format.first_line_indent = Pt(0)

# Save placeholder paragraph (pandoc needs at least one paragraph)
doc.add_paragraph('', style='Title')

# Save to docx/ folder (relative to this script's parent)
output_path = Path(__file__).resolve().parent.parent / 'docx' / 'reference.docx'
output_path.parent.mkdir(parents=True, exist_ok=True)
doc.save(output_path)
print(f'reference.docx saved → {output_path}')
