# -*- coding: utf-8 -*-
"""
Generate exact REPORT.md matching target_verbatim_text.txt
"""

import os

BASE_DIR = r"C:\Users\torme\.gemini\antigravity\scratch\object-detection-suite"
TARGET_TXT = os.path.join(BASE_DIR, "target_verbatim_text.txt")
REPORT_MD = os.path.join(BASE_DIR, "REPORT.md")

with open(TARGET_TXT, "r", encoding="utf-8") as f:
    raw = f.read()

blocks = raw.split("\n\n")

md_parts = []

# Title & Metadata
md_parts.append("""# PENTECOST UNIVERSITY
## CUSTOM OBJECT DETECTION AND RECOGNITION OF MYSELF USING ULTRALYTICS YOLO

**Candidate Name:** Tormekpey Ian Prosper  
**Student ID:** PUIS/23210047  
**Programme:** B.Sc. Industrial Software Engineering  
**Course:** Artificial Intelligence and Expert Systems  
**Supervisor / Lecturer:** Mr. Harry Atieku-Boateng  
**Submission Date:** 23 November 2026  
""")

# Table of Contents
md_parts.append("""## Table of Contents

- [Abstract](#abstract)
- [List of Figures](#list-of-figures)
- [List of Tables](#list-of-tables)
- [List of Abbreviations](#list-of-abbreviations)
- [1. Introduction](#1-introduction)
  - [1.1 Background and Problem Statement](#11-background-and-problem-statement)
  - [1.2 Aim and Objectives](#12-aim-and-objectives)
  - [1.3 Scope and Limitations](#13-scope-and-limitations)
  - [1.4 Significance of the Study](#14-significance-of-the-study)
  - [1.5 Report Organization](#15-report-organization)
- [2. Theoretical Background](#2-theoretical-background)
  - [2.1 Object Detection and YOLO](#21-object-detection-and-yolo)
  - [2.2 Evaluation Metrics & Mathematical Formulations](#22-evaluation-metrics--mathematical-formulations)
  - [2.3 Bounding Box Coordinate Mathematics and Cross-Platform Rendering](#23-bounding-box-coordinate-mathematics-and-cross-platform-rendering)
  - [2.4 Retrieval-Augmented Generation (RAG) Architecture](#24-retrieval-augmented-generation-rag-architecture)
- [3. Tools and Technologies](#3-tools-and-technologies)
- [4. Methodology](#4-methodology)
  - [4.1 Data Collection](#41-data-collection)
  - [4.2 Annotation](#42-annotation)
  - [4.3 Training Setup and Runs](#43-training-setup-and-runs)
- [5. Results and Analysis](#5-results-and-analysis)
  - [5.1 Quantitative Benchmark](#51-quantitative-benchmark)
  - [5.2 Analysis of the Improvement](#52-analysis-of-the-improvement)
  - [5.3 Diagnostic Curves and Predictions](#53-diagnostic-curves-and-predictions)
- [6. Deployment](#6-deployment)
  - [6.1 Ultralytics Cloud Deployment](#61-ultralytics-cloud-deployment)
  - [6.2 FastAPI Gateway on Vercel](#62-fastapi-gateway-on-vercel)
  - [6.3 Web Application](#63-web-application)
  - [6.4 Mobile Application](#64-mobile-application)
- [7. Testing and Discussion](#7-testing-and-discussion)
- [8. Challenges and Lessons Learned](#8-challenges-and-lessons-learned)
- [9. Conclusion and Recommendations](#9-conclusion-and-recommendations)
  - [9.1 Conclusion](#91-conclusion)
  - [9.2 Recommendations](#92-recommendations)
- [References](#references)
- [Appendices](#appendices)
  - [Appendix A: Dataset and Annotation Screenshots](#appendix-a-dataset-and-annotation-screenshots)
  - [Appendix B: Training Telemetry & Figures](#appendix-b-training-telemetry--figures)
  - [Appendix C: Deployment and Application Architecture](#appendix-c-deployment-and-application-architecture)
  - [Appendix D: Project Resources Table](#appendix-d-project-resources-table)
  - [Appendix E: Declaration of Academic Integrity and Originality](#appendix-e-declaration-of-academic-integrity-and-originality)
""")

# Abstract
abstract_text = "\n\n".join([p.strip() for p in blocks[2].strip().split("\n")[1:] if p.strip()])
md_parts.append(f"""## Abstract\n\n{abstract_text}""")

# List of Figures
fig_lines = blocks[3].strip().split("\n")[1:]
fig_md = "\n".join([f"- {l.strip()}" for l in fig_lines if l.strip()])
md_parts.append(f"""## List of Figures\n\n{fig_md}""")

# List of Tables
tbl_lines = blocks[4].strip().split("\n")[1:]
tbl_md = "\n".join([f"- {l.strip()}" for l in tbl_lines if l.strip()])
md_parts.append(f"""## List of Tables\n\n{tbl_md}""")

# List of Abbreviations & Table 0
abbrev_lines = blocks[5].strip().split("\n")
caption_0 = abbrev_lines[1].strip()
t0_header = abbrev_lines[2].strip()
t0_rows = abbrev_lines[3:]
t0_md = f"### {caption_0}\n\n| Term | Meaning |\n| :--- | :--- |\n"
for r in t0_rows:
    parts = [c.strip() for c in r.split("|")]
    t0_md += f"| **{parts[0]}** | {parts[1]} |\n"
md_parts.append(f"""## List of Abbreviations\n\n{t0_md}""")

# 1. Introduction
intro_lines = blocks[6].strip().split("\n")
p_intro = "\n\n".join([p.strip() for p in intro_lines[2:] if p.strip()])
md_parts.append(f"""## 1. Introduction\n\n### 1.1 Background and Problem Statement\n\n{p_intro}""")

# 1.2 Aim and Objectives
aim_lines = blocks[7].strip().split("\n")
p_aim_lead = aim_lines[1].strip()
aim_items = "\n".join([item.strip() for item in aim_lines[2:] if item.strip()])
md_parts.append(f"""### 1.2 Aim and Objectives\n\n{p_aim_lead}\n\n{aim_items}""")

# 1.3 Scope and Limitations
md_parts.append(f"""### 1.3 Scope and Limitations\n\n{blocks[8].strip().split(chr(10))[1].strip()}""")

# 1.4 Significance of the Study
md_parts.append(f"""### 1.4 Significance of the Study\n\n{blocks[9].strip().split(chr(10))[1].strip()}""")

# 2. Theoretical Background
yolo_lines = blocks[10].strip().split("\n")
p_yolo = "\n\n".join([p.strip() for p in yolo_lines[2:] if p.strip()])
md_parts.append(f"""## 2. Theoretical Background\n\n### 2.1 Object Detection and YOLO\n\n{p_yolo}""")

# Table 1
t1_lines = blocks[11].strip().split("\n")
caption_1 = t1_lines[0].strip()
t1_rows = t1_lines[1:]
t1_md = f"### {caption_1}\n\n| Detector Paradigm | Representative Architectures | Inference Methodology | Suitability for this Project |\n| :--- | :--- | :--- | :--- |\n"
for r in t1_rows[1:]:
    parts = [c.strip() for c in r.split("|")]
    t1_md += f"| **{parts[0]}** | {parts[1]} | {parts[2]} | {parts[3]} |\n"
md_parts.append(f"""{t1_md}\n\n{blocks[12].strip()}""")

# 2.2 Evaluation Metrics
metrics_lines = blocks[13].strip().split("\n")
p_met_lead = metrics_lines[1].strip()
met_items = "\n".join([item.strip() for item in metrics_lines[2:] if item.strip()])
md_parts.append(f"""### 2.2 Evaluation Metrics & Mathematical Formulations\n\n{p_met_lead}\n\n{met_items}""")

# 2.3 Bounding Box Mathematics
bbox_lines = blocks[14].strip().split("\n")
p_bbox_1 = bbox_lines[1].strip()
p_bbox_box = f"```\n{bbox_lines[2].strip()}\n```"
p_bbox_2 = bbox_lines[3].strip()
bbox_bullets = "\n".join([b.strip() for b in bbox_lines[4:] if b.strip()])
md_parts.append(f"""### 2.3 Bounding Box Coordinate Mathematics and Cross-Platform Rendering\n\n{p_bbox_1}\n\n{p_bbox_box}\n\n{p_bbox_2}\n\n{bbox_bullets}""")

# 2.4 RAG Architecture
md_parts.append(f"""### 2.4 Retrieval-Augmented Generation (RAG) Architecture\n\n{blocks[15].strip().split(chr(10))[1].strip()}""")

# 3. Tools and Technologies & Table 2
tools_lines = blocks[16].strip().split("\n")
p_tools_lead = tools_lines[1].strip()
t2_lines = blocks[17].strip().split("\n")
caption_2 = t2_lines[0].strip()
t2_rows = t2_lines[1:]
t2_md = f"### {caption_2}\n\n| Tool / Technology | Role in the Project |\n| :--- | :--- |\n"
for r in t2_rows[1:]:
    parts = [c.strip() for c in r.split("|")]
    t2_md += f"| **{parts[0]}** | {parts[1]} |\n"
md_parts.append(f"""## 3. Tools and Technologies\n\n{p_tools_lead}\n\n{t2_md}""")

# 4. Methodology
md_parts.append(f"""## 4. Methodology\n\n### 4.1 Data Collection\n\n{blocks[18].strip().split(chr(10))[2].strip()}""")

# 4.2 Annotation
annot_lines = blocks[19].strip().split("\n")
p_annot = "\n\n".join([p.strip() for p in annot_lines[1:] if p.strip()])
md_parts.append(f"""### 4.2 Annotation\n\n{p_annot}""")

# 4.3 Training Setup and Runs & Table 3
p_train_lead = blocks[20].strip().split("\n")[1].strip()
t3_lines = blocks[21].strip().split("\n")
caption_3 = t3_lines[0].strip()
t3_rows = t3_lines[1:]
t3_md = f"### {caption_3}\n\n| Hyperparameter / Setting | Configured Value |\n| :--- | :--- |\n"
for r in t3_rows[1:]:
    parts = [c.strip() for c in r.split("|")]
    t3_md += f"| **{parts[0]}** | {parts[1]} |\n"
p_train_after = blocks[22].strip()
md_parts.append(f"""### 4.3 Training Setup and Runs\n\n{p_train_lead}\n\n{t3_md}\n\n{p_train_after}""")

# 5. Results and Analysis & Table 4
p_res_lead = blocks[23].strip().split("\n")[2].strip()
t4_lines = blocks[24].strip().split("\n")
caption_4 = t4_lines[0].strip()
t4_rows = t4_lines[1:]
t4_md = f"### {caption_4}\n\n| Evaluation Metric | Run 1 (exp, 945 imgs) | Run 2 (exp-2, 1,021 imgs) | Gain (pts) | Relative Gain |\n| :--- | :--- | :--- | :--- | :--- |\n"
for r in t4_rows[1:]:
    parts = [c.strip() for c in r.split("|")]
    t4_md += f"| **{parts[0]}** | {parts[1]} | {parts[2]} | {parts[3]} | {parts[4]} |\n"
md_parts.append(f"""## 5. Results and Analysis\n\n### 5.1 Quantitative Benchmark\n\n{p_res_lead}\n\n{t4_md}""")

# 5.2 Analysis of the Improvement
imp_lines = blocks[25].strip().split("\n")
p_imp = "\n\n".join([p.strip() for p in imp_lines[1:] if p.strip()])
md_parts.append(f"""### 5.2 Analysis of the Improvement\n\n{p_imp}""")

# 5.3 Diagnostic Curves and Predictions
diag_lines = blocks[26].strip().split("\n")
p_diag_1 = diag_lines[1].strip()
caption_fig1 = diag_lines[2].strip()
p_diag_fig1 = diag_lines[3].strip()

f2_lines = blocks[27].strip().split("\n")
caption_fig2 = f2_lines[0].strip()
p_f2 = f2_lines[1].strip()

f3_lines = blocks[28].strip().split("\n")
caption_fig3 = f3_lines[0].strip()
p_f3 = f3_lines[1].strip()

f45_lines = blocks[29].strip().split("\n")
caption_fig45 = f45_lines[0].strip()
p_f45 = f45_lines[1].strip()

md_parts.append(f"""### 5.3 Diagnostic Curves and Predictions\n\n{p_diag_1}\n\n**{caption_fig1}**\n\n![Figure 1: Training and Validation Metrics Dashboard](docs/graphs/results.png)\n\n{p_diag_fig1}\n\n**{caption_fig2}**\n\n![Figure 2: Precision-Recall Curve](docs/graphs/PR_curve.png)\n\n{p_f2}\n\n**{caption_fig3}**\n\n![Figure 3: F1-Confidence Optimization Curve](docs/graphs/F1_curve.png)\n\n{p_f3}\n\n**{caption_fig45}**\n\n<p align="center">\n  <img src="docs/graphs/confusion_matrix.png" width="48%" />\n  <img src="docs/graphs/confusion_matrix_normalized.png" width="48%" />\n</p>\n\n{p_f45}""")

# 6. Deployment
dep_lines = blocks[30].strip().split("\n")
p_dep_1 = dep_lines[2].strip()
p_dep_link = f"[{dep_lines[3].strip()}]({dep_lines[3].strip()})"
p_dep_2 = dep_lines[4].strip()

gw_lines = blocks[31].strip().split("\n")
p_gw_lead = gw_lines[1].strip()
gw_items = "\n".join([item.strip() for item in gw_lines[2:] if item.strip()])

web_lines = blocks[32].strip().split("\n")
p_web = "\n\n".join([p.strip() for p in web_lines[1:] if p.strip()])

mob_lines = blocks[33].strip().split("\n")
p_mob = "\n\n".join([p.strip() for p in mob_lines[1:] if p.strip()])

md_parts.append(f"""## 6. Deployment\n\n### 6.1 Ultralytics Cloud Deployment\n\n{p_dep_1}\n\n{p_dep_link}\n\n{p_dep_2}\n\n### 6.2 FastAPI Gateway on Vercel\n\n{p_gw_lead}\n\n{gw_items}\n\n### 6.3 Web Application\n\n{p_web}\n\n### 6.4 Mobile Application\n\n{p_mob}""")

# 7. Testing and Discussion & Table 5
p_test_lead = blocks[34].strip().split("\n")[1].strip()
t5_lines = blocks[35].strip().split("\n")
caption_5 = t5_lines[0].strip()
t5_rows = t5_lines[1:]
t5_md = f"### {caption_5}\n\n| Test Scenario | Images | Author Detected | False Positives | Qualitative Notes |\n| :--- | :--- | :--- | :--- | :--- |\n"
for r in t5_rows[1:]:
    parts = [c.strip() for c in r.split("|")]
    t5_md += f"| **{parts[0]}** | {parts[1]} | {parts[2]} | {parts[3]} | {parts[4]} |\n"
p_test_after = blocks[36].strip()

md_parts.append(f"""## 7. Testing and Discussion\n\n{p_test_lead}\n\n{t5_md}\n\n{p_test_after}""")

# 8. Challenges and Lessons Learned
chal_lines = blocks[37].strip().split("\n")
chal_items = "\n".join([item.strip() for item in chal_lines[1:] if item.strip()])
md_parts.append(f"""## 8. Challenges and Lessons Learned\n\n{chal_items}""")

# 9. Conclusion and Recommendations
p_concl = blocks[38].strip().split("\n")[2].strip()
rec_lines = blocks[39].strip().split("\n")
rec_items = "\n".join([item.strip() for item in rec_lines[1:] if item.strip()])

md_parts.append(f"""## 9. Conclusion and Recommendations\n\n### 9.1 Conclusion\n\n{p_concl}\n\n### 9.2 Recommendations\n\n{rec_items}""")

# References
ref_lines = blocks[40].strip().split("\n")
ref_md = "\n".join([f"{r.strip()}  " for r in ref_lines[1:] if r.strip()])
md_parts.append(f"""## References\n\n{ref_md}""")

# Appendices
appA_lines = blocks[41].strip().split("\n")
p_appA_1 = appA_lines[2].strip()
caption_fig67 = appA_lines[3].strip()

p_appB = blocks[42].strip().split("\n")[1].strip()

p_appC = blocks[43].strip().split("\n")[1].strip()

t6_lines = blocks[44].strip().split("\n")
caption_6 = t6_lines[1].strip()
t6_rows = t6_lines[2:]
t6_md = f"### {caption_6}\n\n| Resource | Link / Specification |\n| :--- | :--- |\n"
for r in t6_rows[1:]:
    parts = [c.strip() for c in r.split("|")]
    t6_md += f"| **{parts[0]}** | {parts[1]} |\n"

p_appE = blocks[45].strip().split("\n")[1].strip()

md_parts.append(f"""## Appendices

### Appendix A: Dataset and Annotation Screenshots

{p_appA_1}

**{caption_fig67}**

<p align="center">
  <img src="docs/graphs/dataset_sample_1.jpg" width="48%" />
  <img src="docs/graphs/dataset_sample_2.jpg" width="48%" />
</p>

### Appendix B: Training Telemetry & Figures

{p_appB}

### Appendix C: Deployment and Application Architecture

{p_appC}

**Figure 8: Decoupled Zero-Storage Client-Server Architecture**

![Figure 8: Decoupled Zero-Storage Client-Server Architecture](docs/graphs/figure8_architecture.png)

### Appendix D: Project Resources Table

{t6_md}

### Appendix E: Declaration of Academic Integrity and Originality

{p_appE}
""")

full_md = "\n\n---\n\n".join(md_parts)
with open(REPORT_MD, "w", encoding="utf-8") as out:
    out.write(full_md)

print(f"Generated {REPORT_MD} successfully ({len(full_md)} chars)")
