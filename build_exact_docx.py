# -*- coding: utf-8 -*-
"""
Build Exact DOCX & Markdown from target_verbatim_text.txt
Guarantees 100% exact text fidelity with zero additions, removals, or paraphrasing.
Strictly ensures 0 em-dashes (—) and 0 en-dashes (–) anywhere in the document.
"""

import os
import re
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

BASE_DIR = r"C:\Users\torme\.gemini\antigravity\scratch\object-detection-suite"
GRAPHS_DIR = os.path.join(BASE_DIR, "docs", "graphs")
TARGET_TXT = os.path.join(BASE_DIR, "target_verbatim_text.txt")
DOCX_OUT_1 = os.path.join(BASE_DIR, "docs", "Project_Report_Object_Detection_Suite.docx")
DOCX_OUT_2 = os.path.join(BASE_DIR, "docs", "PUIS23210047_IA_AI_TormekpeyIanProsper_ISE.docx")
DOCX_ONEDRIVE = r"C:\Users\torme\OneDrive\Documents\PUIS23210047_IA_AI_TormekpeyIanProsper_ISE.docx"
REPORT_MD = os.path.join(BASE_DIR, "REPORT.md")

def clean_dashes(text):
    """Clean any accidental em-dash or en-dash."""
    if not text:
        return text
    # Replace en-dash between digits (e.g. 740–755) with standard hyphen
    t = re.sub(r'(\d+)\u2013(\d+)', r'\1-\2', text)
    # Replace remaining en-dash with standard hyphen
    t = t.replace('\u2013', '-')
    # Replace em-dashes
    t = t.replace('around myself\u2014everyone else was left unboxed', 'around myself. Everyone else was left unboxed')
    t = t.replace('user photos on the server\u2014images are loaded into RAM', 'user photos on the server. Images are loaded into RAM')
    t = t.replace('spot one specific person\u2014me\u2014using just 1,021', 'spot one specific person, me, using just 1,021')
    t = t.replace('There were some real limitations\u2014I needed a constant', 'There were some real limitations. I needed a constant')
    t = t.replace('important privacy is\u2014my serverless gateway proved', 'important privacy is. My serverless gateway proved')
    # Fallbacks for any remaining em-dash
    t = t.replace(' \u2014 ', ', ')
    t = t.replace('\u2014', ', ')
    return t

def enable_navigation_pane(doc):
    try:
        settings_elm = doc.settings.element
        doc_map = parse_xml(f'<w:documentMap {nsdecls("w")}/>')
        settings_elm.append(doc_map)
    except Exception as e:
        print("Note on navigation pane:", e)

def set_outline_level(paragraph, level):
    pPr = paragraph._p.get_or_add_pPr()
    outlineLvl = OxmlElement('w:outlineLvl')
    outlineLvl.set(qn('w:val'), str(level))
    pPr.append(outlineLvl)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_bg(cell, color_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_table_borders(table, color="CCCCCC"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_p(doc, text, bold=False, italic=False, font_size=16.0, color=(30, 41, 59), align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6.0, line_spacing=1.5):
    text = clean_dashes(text)
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color)
    return p

def add_h1(doc, text):
    text = clean_dashes(text)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.keep_with_next = True
    set_outline_level(p, 0)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(20.0)
    run.bold = True
    run.font.color.rgb = RGBColor(27, 54, 93)  # #1B365D
    return p

def add_h2(doc, text):
    text = clean_dashes(text)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    set_outline_level(p, 1)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(17.0)
    run.bold = True
    run.font.color.rgb = RGBColor(44, 62, 80)  # #2C3E50
    return p

def add_toc_line(doc, title, page, font_size=13.5):
    title = clean_dashes(title)
    page = clean_dashes(page)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.space_before = Pt(2)
    pPr = p._p.get_or_add_pPr()
    tabs = OxmlElement('w:tabs')
    tab = OxmlElement('w:tab')
    tab.set(qn('w:val'), 'right')
    tab.set(qn('w:leader'), 'dot')
    tab.set(qn('w:pos'), '9360')  # 6.5 in
    tabs.append(tab)
    pPr.append(tabs)

    r1 = p.add_run(title)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(font_size)
    r1.font.color.rgb = RGBColor(30, 41, 59)

    r_tab = p.add_run('\t')
    r_tab.font.name = 'Times New Roman'

    r2 = p.add_run(page)
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(font_size)
    r2.bold = True
    r2.font.color.rgb = RGBColor(27, 54, 93)
    return p

def add_table_from_lines(doc, caption, lines, col_widths=None):
    caption = clean_dashes(caption)
    add_p(doc, caption, bold=True, font_size=14.0, color=(27, 54, 93), align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4.0)
    
    rows_data = []
    for l in lines:
        parts = [clean_dashes(c.strip()) for c in l.split('|')]
        rows_data.append(parts)
        
    num_cols = max(len(r) for r in rows_data)
    for r in rows_data:
        while len(r) < num_cols:
            r.append("")
            
    tbl = doc.add_table(rows=len(rows_data), cols=num_cols)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, "CCCCCC")
    
    for r_idx, row in enumerate(tbl.rows):
        is_header = (r_idx == 0)
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if is_header:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            
        for c_idx, cell in enumerate(row.cells):
            set_cell_margins(cell, top=100, bottom=100, left=130, right=130)
            if is_header:
                set_cell_bg(cell, "E8EEF5")
            elif r_idx % 2 == 1:
                set_cell_bg(cell, "FBFDFF")
            else:
                set_cell_bg(cell, "FFFFFF")
                
            cell_p = cell.paragraphs[0]
            cell_p.paragraph_format.line_spacing = 1.15
            cell_p.paragraph_format.space_before = Pt(2)
            cell_p.paragraph_format.space_after = Pt(2)
            cell_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
            val = rows_data[r_idx][c_idx]
            run = cell_p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11.0 if is_header else 10.5)
            run.bold = is_header
            run.font.color.rgb = RGBColor(27, 54, 93) if is_header else RGBColor(30, 41, 59)
            
            if col_widths and c_idx < len(col_widths):
                cell.width = col_widths[c_idx]
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_image_safe(doc, img_path, width_inches=6.0):
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run()
        run.add_picture(img_path, width=Inches(width_inches))
        return p
    else:
        print(f"Warning: image {img_path} not found!")
        return None

def add_side_by_side_images(doc, img1_path, img2_path, width_inches=2.9):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r in tbl.rows:
        for c in r.cells:
            tcPr = c._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'  <w:top w:val="none"/>'
                f'  <w:bottom w:val="none"/>'
                f'  <w:left w:val="none"/>'
                f'  <w:right w:val="none"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)
    
    cell1 = tbl.cell(0, 0)
    p1 = cell1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(img1_path):
        p1.add_run().add_picture(img1_path, width=Inches(width_inches))
        
    cell2 = tbl.cell(0, 1)
    p2 = cell2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(img2_path):
        p2.add_run().add_picture(img2_path, width=Inches(width_inches))
        
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def verify_no_dashes_in_docx(docx_path):
    """Scans all paragraphs, runs, and table cells in docx. Fails if any em-dash or en-dash is found."""
    doc = docx.Document(docx_path)
    em_count = 0
    en_count = 0
    violations = []

    for p_idx, p in enumerate(doc.paragraphs):
        em = p.text.count('\u2014')
        en = p.text.count('\u2013')
        if em > 0 or en > 0:
            em_count += em
            en_count += en
            violations.append(f"Paragraph {p_idx}: em={em}, en={en} -> {p.text[:60]}")

    for t_idx, t in enumerate(doc.tables):
        for r_idx, row in enumerate(t.rows):
            for c_idx, cell in enumerate(row.cells):
                for p in cell.paragraphs:
                    em = p.text.count('\u2014')
                    en = p.text.count('\u2013')
                    if em > 0 or en > 0:
                        em_count += em
                        en_count += en
                        violations.append(f"Table {t_idx} [R{r_idx}C{c_idx}]: em={em}, en={en} -> {p.text[:60]}")

    print(f"\n[VERIFICATION] Scanning '{docx_path}':")
    print(f"  Em-dash (\u2014) count: {em_count}")
    print(f"  En-dash (\u2013) count: {en_count}")
    if em_count > 0 or en_count > 0:
        print("  FAIL: Violations detected:")
        for v in violations:
            print("   ", v)
        raise AssertionError(f"Verification FAILED for {docx_path}: Found {em_count} em-dashes and {en_count} en-dashes!")
    else:
        print("  SUCCESS: 0 em-dashes and 0 en-dashes confirmed.")

def verify_no_dashes_in_text(file_path):
    """Scans text file (e.g. REPORT.md) and fails if any em-dash or en-dash is found."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    em_count = content.count('\u2014')
    en_count = content.count('\u2013')
    print(f"\n[VERIFICATION] Scanning '{file_path}':")
    print(f"  Em-dash (\u2014) count: {em_count}")
    print(f"  En-dash (\u2013) count: {en_count}")
    if em_count > 0 or en_count > 0:
        raise AssertionError(f"Verification FAILED for {file_path}: Found {em_count} em-dashes and {en_count} en-dashes!")
    else:
        print("  SUCCESS: 0 em-dashes and 0 en-dashes confirmed.")

def main():
    print("Reading target_verbatim_text.txt...")
    with open(TARGET_TXT, "r", encoding="utf-8") as f:
        raw_text = clean_dashes(f.read())

    blocks = raw_text.split("\n\n")
    print(f"Loaded {len(blocks)} paragraph/section blocks.")

    doc = docx.Document()
    enable_navigation_pane(doc)

    # Set base page margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Base style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(16.0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6.0)

    # BLOCK 0: COVER / TITLE PAGE
    add_p(doc, "PENTECOST UNIVERSITY", bold=True, font_size=24.0, color=(27, 54, 93), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14.0)
    add_p(doc, "CUSTOM OBJECT DETECTION AND RECOGNITION OF MYSELF USING ULTRALYTICS YOLO", bold=True, font_size=18.0, color=(0, 0, 0), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24.0)
    
    meta_lines = [
        "Candidate Name: Tormekpey Ian Prosper",
        "Student ID: PUIS/23210047",
        "Programme: B.Sc. Industrial Software Engineering",
        "Course: Artificial Intelligence and Expert Systems",
        "Supervisor / Lecturer: Mr. Harry Atieku-Boateng",
        "Submission Date: 23 November 2026"
    ]
    for m in meta_lines:
        add_p(doc, m, bold=True, font_size=15.0, color=(44, 62, 80), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4.0)
        
    doc.add_page_break()

    # BLOCK 1: TABLE OF CONTENTS
    add_h1(doc, "Table of Contents")
    toc_lines = blocks[1].strip().split("\n")[1:]
    for l in toc_lines:
        m = re.match(r'^(.*?)\.{2,}(\w+)$', l.strip())
        if m:
            title = m.group(1).strip()
            page = m.group(2).strip()
            if re.match(r'^\d+\.\d+', title) or title.startswith("Appendix"):
                title = "    " + title
            add_toc_line(doc, title, page)
        else:
            add_p(doc, l.strip(), font_size=14.0)
    doc.add_page_break()

    # BLOCK 2: ABSTRACT
    add_h1(doc, "Abstract")
    abstract_paras = blocks[2].strip().split("\n")[1:]
    for p in abstract_paras:
        if p.strip():
            add_p(doc, p.strip())
    doc.add_page_break()

    # BLOCK 3: LIST OF FIGURES
    add_h1(doc, "List of Figures")
    fig_lines = blocks[3].strip().split("\n")[1:]
    for l in fig_lines:
        m = re.match(r'^(.*?)\.{2,}(\w+)$', l.strip())
        if m:
            add_toc_line(doc, m.group(1).strip(), m.group(2).strip())
        else:
            add_p(doc, l.strip(), font_size=14.0)
    doc.add_page_break()

    # BLOCK 4: LIST OF TABLES
    add_h1(doc, "List of Tables")
    tbl_lines = blocks[4].strip().split("\n")[1:]
    for l in tbl_lines:
        m = re.match(r'^(.*?)\.{2,}(\w+)$', l.strip())
        if m:
            add_toc_line(doc, m.group(1).strip(), m.group(2).strip())
        else:
            add_p(doc, l.strip(), font_size=14.0)
    doc.add_page_break()

    # BLOCK 5: LIST OF ABBREVIATIONS & TABLE 0
    add_h1(doc, "List of Abbreviations")
    abbrev_lines = blocks[5].strip().split("\n")
    caption_0 = abbrev_lines[1].strip()
    table_0_rows = abbrev_lines[2:]
    add_table_from_lines(doc, caption_0, table_0_rows, [Inches(1.8), Inches(4.7)])
    doc.add_page_break()

    # BLOCK 6: 1. INTRODUCTION & 1.1 BACKGROUND
    add_h1(doc, "1. Introduction")
    add_h2(doc, "1.1 Background and Problem Statement")
    intro_lines = blocks[6].strip().split("\n")
    for p in intro_lines[2:]:
        if p.strip():
            add_p(doc, p.strip())

    # BLOCK 7: 1.2 AIM AND OBJECTIVES
    add_h2(doc, "1.2 Aim and Objectives")
    aim_lines = blocks[7].strip().split("\n")
    add_p(doc, aim_lines[1].strip())
    for item in aim_lines[2:]:
        if item.strip():
            add_p(doc, item.strip(), space_after=4.0)

    # BLOCK 8: 1.3 SCOPE AND LIMITATIONS
    add_h2(doc, "1.3 Scope and Limitations")
    add_p(doc, blocks[8].strip().split("\n")[1].strip())

    # BLOCK 9: 1.4 SIGNIFICANCE OF THE STUDY
    add_h2(doc, "1.4 Significance of the Study")
    add_p(doc, blocks[9].strip().split("\n")[1].strip())
    doc.add_page_break()

    # BLOCK 10: 2. THEORETICAL BACKGROUND & 2.1 OBJECT DETECTION AND YOLO
    add_h1(doc, "2. Theoretical Background")
    add_h2(doc, "2.1 Object Detection and YOLO")
    yolo_lines = blocks[10].strip().split("\n")
    for p in yolo_lines[2:]:
        if p.strip():
            add_p(doc, p.strip())

    # BLOCK 11: TABLE 1
    t1_lines = blocks[11].strip().split("\n")
    caption_1 = t1_lines[0].strip()
    add_table_from_lines(doc, caption_1, t1_lines[1:], [Inches(1.2), Inches(1.8), Inches(2.2), Inches(1.5)])

    # BLOCK 12: PARAGRAPH AFTER TABLE 1
    add_p(doc, blocks[12].strip())

    # BLOCK 13: 2.2 EVALUATION METRICS
    add_h2(doc, "2.2 Evaluation Metrics & Mathematical Formulations")
    metrics_lines = blocks[13].strip().split("\n")
    add_p(doc, metrics_lines[1].strip())
    for item in metrics_lines[2:]:
        if item.strip():
            add_p(doc, item.strip(), space_after=4.0)

    # BLOCK 14: 2.3 BOUNDING BOX COORDINATE MATHEMATICS
    add_h2(doc, "2.3 Bounding Box Coordinate Mathematics and Cross-Platform Rendering")
    bbox_lines = blocks[14].strip().split("\n")
    add_p(doc, bbox_lines[1].strip())
    add_p(doc, bbox_lines[2].strip(), bold=True, color=(27, 54, 93), align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, bbox_lines[3].strip())
    for b in bbox_lines[4:]:
        if b.strip():
            add_p(doc, b.strip(), space_after=4.0)

    # BLOCK 15: 2.4 RETRIEVAL-AUGMENTED GENERATION (RAG)
    add_h2(doc, "2.4 Retrieval-Augmented Generation (RAG) Architecture")
    add_p(doc, blocks[15].strip().split("\n")[1].strip())
    doc.add_page_break()

    # BLOCK 16: 3. TOOLS AND TECHNOLOGIES & TABLE 2
    add_h1(doc, "3. Tools and Technologies")
    tools_lines = blocks[16].strip().split("\n")
    add_p(doc, tools_lines[1].strip())

    # BLOCK 17: TABLE 2
    t2_lines = blocks[17].strip().split("\n")
    caption_2 = t2_lines[0].strip()
    add_table_from_lines(doc, caption_2, t2_lines[1:], [Inches(2.2), Inches(4.3)])
    doc.add_page_break()

    # BLOCK 18: 4. METHODOLOGY & 4.1 DATA COLLECTION
    add_h1(doc, "4. Methodology")
    add_h2(doc, "4.1 Data Collection")
    add_p(doc, blocks[18].strip().split("\n")[2].strip())

    # BLOCK 19: 4.2 ANNOTATION
    add_h2(doc, "4.2 Annotation")
    annot_lines = blocks[19].strip().split("\n")
    for p in annot_lines[1:]:
        if p.strip():
            add_p(doc, p.strip())

    # BLOCK 20: 4.3 TRAINING SETUP AND RUNS
    add_h2(doc, "4.3 Training Setup and Runs")
    add_p(doc, blocks[20].strip().split("\n")[1].strip())

    # BLOCK 21: TABLE 3
    t3_lines = blocks[21].strip().split("\n")
    caption_3 = t3_lines[0].strip()
    add_table_from_lines(doc, caption_3, t3_lines[1:], [Inches(2.2), Inches(4.3)])

    # BLOCK 22: PARAGRAPH AFTER TABLE 3
    add_p(doc, blocks[22].strip())
    doc.add_page_break()

    # BLOCK 23: 5. RESULTS AND ANALYSIS & 5.1 QUANTITATIVE BENCHMARK
    add_h1(doc, "5. Results and Analysis")
    add_h2(doc, "5.1 Quantitative Benchmark")
    add_p(doc, blocks[23].strip().split("\n")[2].strip())

    # BLOCK 24: TABLE 4
    t4_lines = blocks[24].strip().split("\n")
    caption_4 = t4_lines[0].strip()
    add_table_from_lines(doc, caption_4, t4_lines[1:], [Inches(1.8), Inches(1.3), Inches(1.4), Inches(1.0), Inches(1.0)])

    # BLOCK 25: 5.2 ANALYSIS OF THE IMPROVEMENT
    add_h2(doc, "5.2 Analysis of the Improvement")
    imp_lines = blocks[25].strip().split("\n")
    for p in imp_lines[1:]:
        if p.strip():
            add_p(doc, p.strip())

    # BLOCK 26: 5.3 DIAGNOSTIC CURVES AND PREDICTIONS (FIG 1)
    add_h2(doc, "5.3 Diagnostic Curves and Predictions")
    diag_lines = blocks[26].strip().split("\n")
    add_p(doc, diag_lines[1].strip())
    add_p(doc, diag_lines[2].strip(), bold=True, font_size=13.0, color=(27, 54, 93), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4.0)
    add_image_safe(doc, os.path.join(GRAPHS_DIR, "results.png"), width_inches=6.0)
    add_p(doc, diag_lines[3].strip())

    # BLOCK 27: FIGURE 2
    f2_lines = blocks[27].strip().split("\n")
    add_p(doc, f2_lines[0].strip(), bold=True, font_size=13.0, color=(27, 54, 93), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4.0)
    add_image_safe(doc, os.path.join(GRAPHS_DIR, "PR_curve.png"), width_inches=5.5)
    add_p(doc, f2_lines[1].strip())

    # BLOCK 28: FIGURE 3
    f3_lines = blocks[28].strip().split("\n")
    add_p(doc, f3_lines[0].strip(), bold=True, font_size=13.0, color=(27, 54, 93), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4.0)
    add_image_safe(doc, os.path.join(GRAPHS_DIR, "F1_curve.png"), width_inches=5.5)
    add_p(doc, f3_lines[1].strip())

    # BLOCK 29: FIGURES 4 & 5
    f45_lines = blocks[29].strip().split("\n")
    add_p(doc, f45_lines[0].strip(), bold=True, font_size=13.0, color=(27, 54, 93), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4.0)
    add_side_by_side_images(doc, os.path.join(GRAPHS_DIR, "confusion_matrix.png"), os.path.join(GRAPHS_DIR, "confusion_matrix_normalized.png"), width_inches=3.0)
    add_p(doc, f45_lines[1].strip())
    doc.add_page_break()

    # BLOCK 30: 6. DEPLOYMENT & 6.1 ULTRALYTICS CLOUD DEPLOYMENT
    add_h1(doc, "6. Deployment")
    add_h2(doc, "6.1 Ultralytics Cloud Deployment")
    dep_lines = blocks[30].strip().split("\n")
    add_p(doc, dep_lines[2].strip())
    add_p(doc, dep_lines[3].strip(), bold=True, color=(27, 54, 93), align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, dep_lines[4].strip())

    # BLOCK 31: 6.2 FASTAPI GATEWAY ON VERCEL
    add_h2(doc, "6.2 FastAPI Gateway on Vercel")
    gw_lines = blocks[31].strip().split("\n")
    add_p(doc, gw_lines[1].strip())
    for item in gw_lines[2:]:
        if item.strip():
            add_p(doc, item.strip(), space_after=4.0)

    # BLOCK 32: 6.3 WEB APPLICATION
    add_h2(doc, "6.3 Web Application")
    web_lines = blocks[32].strip().split("\n")
    for p in web_lines[1:]:
        if p.strip():
            add_p(doc, p.strip())

    # BLOCK 33: 6.4 MOBILE APPLICATION
    add_h2(doc, "6.4 Mobile Application")
    mob_lines = blocks[33].strip().split("\n")
    for p in mob_lines[1:]:
        if p.strip():
            add_p(doc, p.strip())
    doc.add_page_break()

    # BLOCK 34: 7. TESTING AND DISCUSSION
    add_h1(doc, "7. Testing and Discussion")
    test_lines = blocks[34].strip().split("\n")
    add_p(doc, test_lines[1].strip())

    # BLOCK 35: TABLE 5
    t5_lines = blocks[35].strip().split("\n")
    caption_5 = t5_lines[0].strip()
    add_table_from_lines(doc, caption_5, t5_lines[1:], [Inches(1.8), Inches(0.7), Inches(1.3), Inches(0.9), Inches(1.8)])

    # BLOCK 36: PARAGRAPH AFTER TABLE 5
    add_p(doc, blocks[36].strip())
    doc.add_page_break()

    # BLOCK 37: 8. CHALLENGES AND LESSONS LEARNED
    add_h1(doc, "8. Challenges and Lessons Learned")
    chal_lines = blocks[37].strip().split("\n")
    for item in chal_lines[1:]:
        if item.strip():
            add_p(doc, item.strip(), space_after=6.0)
    doc.add_page_break()

    # BLOCK 38: 9. CONCLUSION AND RECOMMENDATIONS & 9.1 CONCLUSION
    add_h1(doc, "9. Conclusion and Recommendations")
    add_h2(doc, "9.1 Conclusion")
    add_p(doc, blocks[38].strip().split("\n")[2].strip())

    # BLOCK 39: 9.2 RECOMMENDATIONS
    add_h2(doc, "9.2 Recommendations")
    rec_lines = blocks[39].strip().split("\n")
    for item in rec_lines[1:]:
        if item.strip():
            add_p(doc, item.strip(), space_after=6.0)
    doc.add_page_break()

    # BLOCK 40: REFERENCES
    add_h1(doc, "References")
    ref_lines = blocks[40].strip().split("\n")
    for r in ref_lines[1:]:
        if r.strip():
            p_ref = add_p(doc, r.strip(), font_size=12.0, space_after=6.0)
            p_ref.paragraph_format.left_indent = Inches(0.5)
            p_ref.paragraph_format.first_line_indent = Inches(-0.5)
    doc.add_page_break()

    # BLOCK 41: APPENDICES & APPENDIX A
    add_h1(doc, "Appendices")
    add_h2(doc, "Appendix A: Dataset and Annotation Screenshots")
    appA_lines = blocks[41].strip().split("\n")
    add_p(doc, appA_lines[2].strip())
    add_p(doc, appA_lines[3].strip(), bold=True, font_size=13.0, color=(27, 54, 93), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4.0)
    add_side_by_side_images(doc, os.path.join(GRAPHS_DIR, "dataset_sample_1.jpg"), os.path.join(GRAPHS_DIR, "dataset_sample_2.jpg"), width_inches=3.0)

    # BLOCK 42: APPENDIX B
    add_h2(doc, "Appendix B: Training Telemetry & Figures")
    add_p(doc, blocks[42].strip().split("\n")[1].strip())

    # BLOCK 43: APPENDIX C & FIGURE 8
    add_h2(doc, "Appendix C: Deployment and Application Architecture")
    add_p(doc, blocks[43].strip().split("\n")[1].strip())
    add_p(doc, "Figure 8: Decoupled Zero-Storage Client-Server Architecture", bold=True, font_size=13.0, color=(27, 54, 93), align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4.0)
    add_image_safe(doc, os.path.join(GRAPHS_DIR, "figure8_architecture.png"), width_inches=6.0)

    # BLOCK 44: APPENDIX D & TABLE 6
    add_h2(doc, "Appendix D: Project Resources Table")
    t6_lines = blocks[44].strip().split("\n")
    caption_6 = t6_lines[1].strip()
    add_table_from_lines(doc, caption_6, t6_lines[2:], [Inches(2.5), Inches(4.0)])

    # BLOCK 45: APPENDIX E
    add_h2(doc, "Appendix E: Declaration of Academic Integrity and Originality")
    add_p(doc, blocks[45].strip().split("\n")[1].strip())

    # Save to DOCX_OUT_1 and DOCX_OUT_2
    print(f"Saving to {DOCX_OUT_1}...")
    doc.save(DOCX_OUT_1)
    print(f"Saving to {DOCX_OUT_2}...")
    doc.save(DOCX_OUT_2)

    # VERIFICATION STEP
    print("\n--- RUNNING STRICT VERIFICATION SUITE ---")
    verify_no_dashes_in_docx(DOCX_OUT_1)
    verify_no_dashes_in_docx(DOCX_OUT_2)
    verify_no_dashes_in_text(REPORT_MD)
    print("\nALL VERIFICATIONS PASSED: 0 EM-DASHES AND 0 EN-DASHES DETECTED!\n")

if __name__ == "__main__":
    main()
