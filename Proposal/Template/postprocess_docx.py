#!/usr/bin/env python3

import shutil
import sys
import tempfile
import zipfile
from copy import deepcopy

from lxml import etree


NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def qn(tag):
    prefix, name = tag.split(':')
    return f'{{{NS[prefix]}}}{name}'


def make_section_break_paragraph(final_sect_pr):
    paragraph = etree.Element(qn('w:p'))
    p_pr = etree.SubElement(paragraph, qn('w:pPr'))
    sect_pr = etree.SubElement(p_pr, qn('w:sectPr'))

    for child_name in ['w:pgSz', 'w:pgMar', 'w:docGrid']:
        child = final_sect_pr.find(child_name, NS)
        if child is not None:
            sect_pr.append(deepcopy(child))

    cols = etree.SubElement(sect_pr, qn('w:cols'))
    cols.set(qn('w:space'), '510')
    return paragraph


def set_final_two_column_section(final_sect_pr):
    type_el = final_sect_pr.find('w:type', NS)
    if type_el is None:
        type_el = etree.Element(qn('w:type'))
        final_sect_pr.insert(0, type_el)
    type_el.set(qn('w:val'), 'continuous')

    cols = final_sect_pr.find('w:cols', NS)
    if cols is None:
        cols = etree.SubElement(final_sect_pr, qn('w:cols'))
    cols.attrib.clear()
    cols.set(qn('w:num'), '2')
    cols.set(qn('w:space'), '510')


def bold_first_row(tbl):
    first_row = tbl.find('w:tr', NS)
    if first_row is None:
        return
    for run in first_row.findall('.//w:r', NS):
        r_pr = run.find('w:rPr', NS)
        if r_pr is None:
            r_pr = etree.SubElement(run, qn('w:rPr'))
        if r_pr.find('w:b', NS) is None:
            etree.SubElement(r_pr, qn('w:b'))


def style_tables(root):
    for tbl in root.findall('.//w:tbl', NS):
        tbl_pr = tbl.find('w:tblPr', NS)
        if tbl_pr is None:
            tbl_pr = etree.Element(qn('w:tblPr'))
            tbl.insert(0, tbl_pr)

        tbl_style = tbl_pr.find('w:tblStyle', NS)
        if tbl_style is None:
            tbl_style = etree.SubElement(tbl_pr, qn('w:tblStyle'))
        tbl_style.set(qn('w:val'), 'TableGrid')

        tbl_w = tbl_pr.find('w:tblW', NS)
        if tbl_w is None:
            tbl_w = etree.SubElement(tbl_pr, qn('w:tblW'))
        tbl_w.set(qn('w:type'), 'pct')
        tbl_w.set(qn('w:w'), '5000')

        borders = tbl_pr.find('w:tblBorders', NS)
        if borders is not None:
            tbl_pr.remove(borders)
        borders = etree.SubElement(tbl_pr, qn('w:tblBorders'))

        def add_border(name, value, size):
            border = etree.SubElement(borders, qn(f'w:{name}'))
            border.set(qn('w:val'), value)
            border.set(qn('w:sz'), str(size))
            border.set(qn('w:space'), '0')
            border.set(qn('w:color'), '000000')

        add_border('top', 'single', 12)
        add_border('bottom', 'single', 12)
        add_border('insideH', 'single', 6)
        add_border('left', 'nil', 0)
        add_border('right', 'nil', 0)
        add_border('insideV', 'nil', 0)

        bold_first_row(tbl)


def insert_single_to_two_column_transition(root):
    body = root.find('w:body', NS)
    if body is None:
        return

    final_sect_pr = body.find('w:sectPr', NS)
    if final_sect_pr is None:
        return

    first_heading = None
    for paragraph in body.findall('w:p', NS):
        p_style = paragraph.find('./w:pPr/w:pStyle', NS)
        if p_style is not None and p_style.get(qn('w:val')) in {'Heading1', 'Heading2'}:
            first_heading = paragraph
            break

    if first_heading is None:
        return

    section_break = make_section_break_paragraph(final_sect_pr)
    body.insert(body.index(first_heading), section_break)
    set_final_two_column_section(final_sect_pr)


def main(input_path, output_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(input_path) as zin:
            zin.extractall(temp_dir)

        document_xml = f'{temp_dir}/word/document.xml'
        root = etree.parse(document_xml).getroot()
        insert_single_to_two_column_transition(root)
        style_tables(root)

        with open(document_xml, 'wb') as f:
            f.write(etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone='yes'))

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for folder, _, files in os.walk(temp_dir):
                for file in files:
                    full_path = os.path.join(folder, file)
                    rel_path = os.path.relpath(full_path, temp_dir)
                    zout.write(full_path, rel_path)


if __name__ == '__main__':
    import os

    if len(sys.argv) != 3:
        raise SystemExit('usage: postprocess_docx.py INPUT.docx OUTPUT.docx')
    main(sys.argv[1], sys.argv[2])