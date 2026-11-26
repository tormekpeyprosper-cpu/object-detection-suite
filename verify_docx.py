import os
import docx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
doc_path = os.path.join(BASE_DIR, "docs", "Project_Report_Object_Detection_Suite.docx")
target_file = os.path.join(BASE_DIR, "target_verbatim_text.txt")

doc = docx.Document(doc_path)
print(f"Total paragraphs: {len(doc.paragraphs)}")
print(f"Total tables: {len(doc.tables)}")
print(f"Total inline shapes (images): {len(doc.inline_shapes)}")

with open(target_file, "r", encoding="utf-8") as f:
    target_text = f.read()

# Verify key phrases exist in docx
key_phrases = [
    "PENTECOST UNIVERSITY",
    "CUSTOM OBJECT DETECTION AND RECOGNITION OF MYSELF USING ULTRALYTICS YOLO",
    "Candidate Name: Tormekpey Ian Prosper",
    "Student ID: PUIS/23210047",
    "Most object detection models are built to recognize general objects.",
    "91.7% precision, 80.0% recall, 80.4% mAP@50, and 34.9% mAP@50-95",
    "NVIDIA RTX PRO 6000 Blackwell Server Edition (97,252 MiB VRAM)",
    "https://predict-6b01cbfb6aa91a04b3325654-dproatj77a-no.a.run.app",
    "https://object-detection-suite.vercel.app",
    "https://expo.dev/accounts/inkedme/projects/vision-detect-mobile",
    "https://drive.google.com/drive/folders/1ARy1CuAKU0G6YdFLEGivOJGJ0VmC_hNm?usp=sharing",
    "Figure 8: Decoupled Zero-Storage Client-Server Architecture",
    "I hereby declare that this project report entitled 'Custom Object Detection and Recognition of Myself Using Ultralytics YOLO'"
]

docx_full_text = " ".join([p.text for p in doc.paragraphs])
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            docx_full_text += " " + cell.text

for phrase in key_phrases:
    if phrase in docx_full_text:
        print(f"  [PASS] Found: '{phrase[:50]}...'")
    else:
        print(f"  [FAIL] MISSING: '{phrase}'")

# Check table count and headers
print("\nTables check:")
for i, t in enumerate(doc.tables):
    headers = [cell.text.strip() for cell in t.rows[0].cells]
    print(f"  Table {i}: {len(t.rows)} rows, {len(t.columns)} cols -> Header: {headers}")
