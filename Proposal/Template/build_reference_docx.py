#!/usr/bin/env python3

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt


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


doc = Document()
section = doc.sections[0]
section.page_width = Mm(210)
section.page_height = Mm(297)
section.top_margin = Mm(14)
section.bottom_margin = Mm(17)
section.left_margin = Mm(14)
section.right_margin = Mm(14)
section.header_distance = Mm(8)
section.footer_distance = Mm(8)

normal = doc.styles['Normal']
set_style_font(normal, latin='Times New Roman', east_asia='Malgun Gothic', size=10)
normal.paragraph_format.line_spacing = 1.0
normal.paragraph_format.space_after = Pt(2)

for style_name in ['Body Text', 'First Paragraph', 'Compact']:
    if style_name in doc.styles:
        style = doc.styles[style_name]
        set_style_font(style, latin='Times New Roman', east_asia='Malgun Gothic', size=10)
        style.paragraph_format.line_spacing = 1.0
        style.paragraph_format.space_after = Pt(2)

title = doc.styles['Title']
set_style_font(title, latin='Times New Roman', east_asia='Malgun Gothic', size=16, bold=True)
title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_after = Pt(6)

for style_name in ['Author', 'Date', 'Subtitle']:
    if style_name in doc.styles:
        style = doc.styles[style_name]
        set_style_font(style, latin='Times New Roman', east_asia='Malgun Gothic', size=10)
        style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        style.paragraph_format.space_after = Pt(2)

for style_name in ['Heading 1', 'Heading 2']:
    if style_name in doc.styles:
        style = doc.styles[style_name]
        set_style_font(style, latin='Times New Roman', east_asia='Malgun Gothic', size=10, bold=True)
        style.paragraph_format.space_before = Pt(6)
        style.paragraph_format.space_after = Pt(3)

for style_name in ['Table', 'Table Grid']:
    if style_name in doc.styles:
        set_style_font(doc.styles[style_name], latin='Times New Roman', east_asia='Malgun Gothic', size=9)

doc.add_paragraph('', style='Title')
doc.save('reference.docx')