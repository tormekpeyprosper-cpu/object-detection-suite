# PENTECOST UNIVERSITY
## CUSTOM OBJECT DETECTION AND RECOGNITION OF MYSELF USING ULTRALYTICS YOLO

**Candidate Name:** Tormekpey Ian Prosper  
**Index / Student ID:** PUIS/23210047  
**Programme of Study:** B.Sc. Industrial Software Engineering  
**Course Title:** Artificial Intelligence and Expert Systems  
**Course Lecturer:** Mr. Harry Atieku-Boateng  
**Date of Submission:** 23 November 2026  

---

## TABLE OF CONTENTS

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

---

## Abstract

Standard object detection models look for generic things. If you download a stock YOLO model trained on COCO [3], point a camera at me, and run inference, it gives you a box that says 'person.' That works if you are counting heads at a turnstile. It does not help at all if you need automated roll call in a lecture room at Pentecost University, or access logging for an engineering project lab. For those, the software needs to know it is looking at me: Tormekpey Ian Prosper.

I had to build the entire dataset myself. I walked around campus with my smartphone and took 1,021 photos across dorm rooms, harsh midday sun, dim study corridors, and group pictures with up to eight classmates. Labeling them took hours. In the group pictures, I drew boxes only around myself and left everyone else completely unboxed as Class 0 negatives. That was deliberate: it forced the loss function to penalize the network whenever it confused a friend's face for mine.

I fine-tuned a YOLO26n nano model on cloud compute across 100 epochs. It finished training in 340.6 seconds and hit 91.7% precision, 80.0% recall, 80.4% mAP@50, and 34.9% mAP@50-95, beating my earlier 945-image baseline by 3.2 percentage points on strict localization. The weights file is only 5.54 MB. I put the model inside a Google Cloud Run container in europe-southwest1 and built a serverless FastAPI proxy on Vercel to handle incoming requests. I refused to store user photos on the server. The proxy takes image bytes into RAM, runs inference, and calls garbage collection right away inside a finally block so nothing ever touches disk. I wrapped it with an HTML5 canvas web page and a React Native Android APK. All 1,021 raw photos are in a shared Google Drive folder.

---

## List of Figures

- **Figure 1:** 100-Epoch Training and Validation Metrics Dashboard (`results.png`)
- **Figure 2:** Precision-Recall Curve Reaching mAP50 = 80.4% (`PR_curve.png`)
- **Figure 3:** F1-Confidence Optimization Curve Peaking at 0.857 (`F1_curve.png`)
- **Figure 4:** Confusion Matrix Raw Candidate Detection Counts (`confusion_matrix.png`)
- **Figure 5:** Normalized Confusion Matrix Across Target Classes (`confusion_matrix_normalized.png`)
- **Figure 6:** Authentic Operational Dataset Sample 1 (`docs/graphs/dataset_sample_1.jpg`)
- **Figure 7:** Authentic Operational Dataset Sample 2 (`docs/graphs/dataset_sample_2.jpg`)
- **Figure 8:** Decoupled Zero-Storage Client-Server Architecture

---

## List of Tables

- **Table 0:** List of Abbreviations
- **Table 1:** Two-Stage and One-Stage Object Detectors
- **Table 2:** Tools and Technologies Used Across the System
- **Table 3:** Training Setup and Hyperparameters (exp-2)
- **Table 4:** Quantitative Performance Comparison (Run 1 vs. Run 2)
- **Table 5:** Field Test and Automated Verification Results
- **Table 6:** Project Resources and Live Links

---

## List of Abbreviations

*Table 0: List of Abbreviations*

| Term | Meaning |
| :--- | :--- |
| **AI / ML** | Artificial Intelligence / Machine Learning |
| **API** | Application Programming Interface |
| **APK** | Android Package (installable Android distribution bundle) |
| **CNN** | Convolutional Neural Network |
| **COCO** | Common Objects in Context (benchmark computer vision dataset) |
| **EAS** | Expo Application Services (cloud build system for React Native) |
| **IoU** | Intersection over Union (bounding box overlap evaluation metric) |
| **JWT** | JSON Web Token (stateless authentication token format) |
| **mAP** | Mean Average Precision (area under the precision-recall curve) |
| **NMS** | Non-Maximum Suppression (candidate bounding box filtering algorithm) |
| **PR-AUC** | Precision-Recall Area Under Curve |
| **RAG** | Retrieval-Augmented Generation (context-grounded semantic retrieval) |
| **REST** | Representational State Transfer (HTTP stateless architectural style) |
| **ROC-AUC** | Receiver Operating Characteristic - Area Under Curve |
| **SGD** | Stochastic Gradient Descent (iterative neural network optimizer) |
| **TP / FP / FN / TN** | True Positive / False Positive / False Negative / True Negative |
| **VRAM** | Video Random Access Memory (dedicated GPU memory) |
| **YOLO** | You Only Look Once (single-stage unified object detection network) |

---

## 1. Introduction

### 1.1 Background and Problem Statement
Most vision models today treat every human being as identical. Models trained on COCO [3] slap the label 'person' on whoever walks past the lens. That makes sense for pedestrian detection in autonomous driving or counting foot traffic. But it breaks down the second an application needs to know who is actually standing there. Knowing that 'a human is present' does not help take attendance in my department, nor does it unlock a secure lab door. The software needs to recognize the specific individual.

That was the problem I set out to solve for my capstone. I wanted to see if a student with no budget for expensive hardware could train a single-person detector on 1,021 phone pictures and make it work in messy campus settings. Reality made this difficult. Campus lighting is inconsistent. In midday sun, faces get blown out. In hostel rooms, lighting is weak and yellow. Worse, people walk in groups. I had to solve three things: collect enough varied photos so the model would not flag my classmates, keep inference fast on mobile, and ensure uploaded photos never get stored anywhere.

### 1.2 Aim and Objectives
The main goal of this capstone was to train, test, and ship a cross-platform YOLO26n system that reliably detects me in real-world photos. I broke the build down into seven practical steps:
1. **Dataset:** Collect and label 1,021 phone photos covering solo, backlit, cluttered, and group environments with classmates.
2. **Training:** Fine-tune a YOLO26n nano model on cloud GPUs and compare it against my 945-image baseline (Run 1 vs Run 2).
3. **Evaluation:** Track precision, recall, mAP50, mAP50-95, and the F1-confidence curve.
4. **Cloud Setup:** Host the model weights in a Google Cloud Run container via the Ultralytics platform.
5. **Backend Gateway:** Build a serverless FastAPI proxy on Vercel with zero-storage RAM cleanup using Python garbage collection.
6. **Client Frontends:** Build a web canvas interface and an installable React Native Android APK with open access.
7. **Verification:** Run automated smoke tests to check response times, uptime, and verify zero disk leaks.

### 1.3 Scope and Limitations
This report covers the entire pipeline: taking photos, labeling boxes, tuning weights, tracking loss curves, writing backend proxies, and building frontend apps. The model has one job: detecting me. It has real limits. It needs working internet because inference runs on the cloud. Vercel rejects image uploads over 4.5 MB. And because it runs off a single camera lens, it only works in 2D and cannot calculate physical depth.

### 1.4 Significance of the Study
This project shows that a student does not need a ten-thousand-dollar GPU rig to build real computer vision software. With transfer learning and 1,021 targeted photos, an off-the-shelf nano model reaches high precision on cloud compute. Just as important is the privacy side: the serverless gateway proves you can run computer vision without hoarding user images on a hard drive. It processes photos in memory and drops them immediately.

### 1.5 Report Organization
Here is how the rest of this report is laid out: Chapter 2 covers the theory behind YOLO, the formulas used to score it, coordinate math, and RAG ideas. Chapter 3 lists the tools and libraries I built this with. Chapter 4 explains how I took the photos, labeled them, and configured training. Chapter 5 goes through the numbers, training charts, and confusion matrices. Chapter 6 details the Cloud Run deployment, the Vercel gateway, and the client apps. Chapter 7 documents field testing and automated scripts. Chapter 8 covers what broke and what I learned fixing it. Chapter 9 wraps up with final thoughts and next steps. References and appendices sit at the end.

---

## 2. Theoretical Background

### 2.1 Object Detection and YOLO
Before deep learning took over, computer vision relied on manual feature extraction like Haar cascades, HOG, and SIFT. Those methods were fragile. They worked in clean lab rooms with steady lighting, but failed outdoors when sunlight shifted or hands shook. Convolutional neural networks replaced them because they learn features directly from raw image pixels during training.

Modern neural detectors split into two main designs: two-stage and one-stage detectors. Table 1 outlines how they differ.

*Table 1: Two-stage and one-stage object detectors*

| Detector Paradigm | Representative Architectures | Inference Methodology | Suitability for this Project |
| :--- | :--- | :--- | :--- |
| **Two-stage** | R-CNN family, Fast R-CNN, Faster R-CNN [4] | Proposes candidate regions of interest first, then extracts features and classifies each region separately. | Accurate on paper, but too heavy and slow for real-time phone scanning. |
| **One-stage** | SSD, RetinaNet, YOLO family [1], YOLO26n [2] | Frames detection as a single regression pass, predicting bounding boxes and class probabilities all at once. | Fast and lightweight; small enough to run smoothly over mobile connections. |

I picked YOLO26n [2] because the weights file is only 5.54 MB. It boots up instantly on cloud containers, stays well within memory limits, and returns predictions in under 600 milliseconds.

### 2.2 Evaluation Metrics & Mathematical Formulations
I tracked five standard metrics to evaluate the model:

1. **Precision ($P$):**  
   Out of all the bounding boxes where the model said 'that is Prosper,' how many were actually me?
   $$\text{Precision} = \frac{TP}{TP + FP} = 91.7\%$$
   High precision means the model stops bothering friends with false detections.

2. **Recall ($R$):**  
   Out of all the pictures where I am present, how many did the model find?
   $$\text{Recall} = \frac{TP}{TP + FN} = 80.0\%$$
   Good recall keeps the system from dropping detections when lighting is bad.

3. **Classification Accuracy:**  
   Overall correctness across all spatial proposals:
   $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

4. **F1-Score ($F_1$):**  
   Precision and recall trade off against each other. The F1-score combines them into one harmonic balance:
   $$F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} = 2 \cdot \frac{0.917 \cdot 0.800}{0.917 + 0.800} = 0.854 \quad (\text{Peak: } 0.857 \text{ at confidence } 0.61)$$

5. **Mean Average Precision (mAP):**  
   Area under the precision-recall curve. I looked at:
   - **$\text{mAP}@0.50 = 80.4\%$:** Checks if boxes overlap ground truth by at least half.
   - **$\text{mAP}@0.50:0.95 = 34.9\%$:** Averages scores across ten tighter overlap thresholds from 0.50 to 0.95.

6. **Why PR-AUC Matters More Than ROC-AUC in Object Detection:**  
   In basic binary classification, ROC curves plot True Positive Rate against False Positive Rate. But in object detection grids, empty background boxes outnumber objects by tens of thousands to one. That massive true negative count ($TN$) drags the false positive rate down near zero, artificially inflating ROC-AUC scores above 0.98. Precision-Recall curves avoid this because they evaluate actual detections directly without being distorted by empty background space.

### 2.3 Bounding Box Coordinate Mathematics and Cross-Platform Rendering
YOLO spits out bounding boxes as four normalized numbers between 0.0 and 1.0 relative to image width ($W_{\text{img}}$) and height ($H_{\text{img}}$):
$$\text{box} = [x_{\text{center}}, y_{\text{center}}, w, h]$$

Drawing these on web and phone screens requires standard coordinate math:
1. **Absolute Pixel Origins:**
   $$x_{\text{min}} = \left(x_{\text{center}} - \frac{w}{2}\right) \cdot W_{\text{img}}, \quad y_{\text{min}} = \left(y_{\text{center}} - \frac{h}{2}\right) \cdot H_{\text{img}}$$
2. **Absolute Dimensions:**
   $$\text{box\_width} = w \cdot W_{\text{img}}, \quad \text{box\_height} = h \cdot H_{\text{img}}$$
3. **Non-Maximum Suppression (NMS):** Suppress overlapping duplicate boxes using Non-Maximum Suppression (NMS) at $\text{IoU} \ge 0.50$:
   $$\text{IoU}(A, B) = \frac{\text{Area}(A \cap B)}{\text{Area}(A \cup B)}$$
4. **Web HTML5 Canvas:** On the Vite web client, scale coordinates onto an HTML5 canvas using $s_x = W_{\text{canvas}} / W_{\text{img}}$ and $s_y = H_{\text{canvas}} / H_{\text{img}}$.
5. **Mobile Viewport Scaling:** In React Native, scale boxes with an isotropic ratio $s = \min(W_{\text{viewport}} / W_{\text{img}}, H_{\text{viewport}} / H_{\text{img}})$ and letterbox offsets $(dx, dy)$ so boxes do not distort on tall phone screens.

### 2.4 Retrieval-Augmented Generation (RAG) Architecture
This system decouples computer vision from knowledge retrieval. The YOLO model has one job: spot me and return my verified identity token. Once the backend has that token, it can query a vector database like Supabase pgvector to fetch attendance logs, workout plans, or lab permissions. Separating perception from data keeps the model lightweight, speeds up response times, and keeps user photos strictly inside RAM.

---

## 3. Tools and Technologies

I picked practical, lightweight tools across the whole stack, detailed in Table 2.

*Table 2: Tools and technologies used across the system*

| Tool / Technology | Role in the Project |
| :--- | :--- |
| **Ultralytics Platform** | Ran cloud GPU training, hosted annotation, and managed Google Cloud Run inference. |
| **YOLO26n [2]** | Nano vision model fine-tuned on my personal dataset. |
| **Google Drive** | Hosts the 1,021 raw training photos for open public download. |
| **GitHub** | Version control repo (`object-detection-suite`). |
| **VS Code & Python 3.12** | Local development setup for backend routes and test scripts. |
| **FastAPI [5] & Pillow [8]** | Python backend for memory validation and zero-storage cleanup. |
| **Vercel [6]** | Edge platform hosting the serverless API and Vite web app. |
| **React Native & Expo [7]** | Mobile framework for Android camera capture and APK packaging. |
| **OpenCV [10] & MediaPipe [11]** | Reference libraries used to verify bounding box margins during debugging. |
| **Supabase & pgvector** | PostgreSQL cloud database for telemetry and vector lookups. |

---

## 4. Methodology

### 4.1 Data Collection
Supervised learning lives or dies by its data. I could not just download an existing dataset because I was training the model to recognize me. So I took my smartphone and spent days taking 1,021 photos of myself across campus. I took photos in harsh midday sun, dim hostel bedrooms, backlit hallways with bright windows, and blurry handheld shots. I also had classmates stand around me in groups of two to eight.

All 1,021 photos (103.37 MB) are in a public Google Drive folder for anyone to inspect:
- **Google Drive Dataset Repository (1,021 Images):**  
  [https://drive.google.com/drive/folders/1ARy1CuAKU0G6YdFLEGivOJGJ0VmC_hNm?usp=sharing](https://drive.google.com/drive/folders/1ARy1CuAKU0G6YdFLEGivOJGJ0VmC_hNm?usp=sharing)
- **Local Download Archive:** Stored locally in `C:\Users\torme\Downloads\exp2_dataset_photos`.

### 4.2 Annotation
I labeled every image following the standard YOLO format: `class_id x_center y_center width height`, normalized from 0.0 to 1.0.

I assigned Class 0 only to myself ('Prosper'). When classmates appeared in group shots, I intentionally left them completely unboxed. That felt counterintuitive at first, but it was the most important decision I made. Leaving my peers unannotated forced the loss function to penalize the network whenever it guessed that another human was me. Over 100 epochs, that taught the model that human outlines belong to the background unless they match my specific features. I audited every bounding box by hand to keep borders tight.

### 4.3 Training Setup and Runs
I ran two training experiments. Run 1 was my initial baseline ('exp') using 945 images on YOLOv8n. Run 2 was the final model ('exp-2') with 1,021 images on YOLO26n. I ran Run 2 on cloud hardware with an NVIDIA RTX PRO 6000 GPU (97,252 MiB VRAM) and an AMD EPYC 9655 processor. Table 3 lists the hyperparameters.

*Table 3: Training setup and hyperparameters (exp-2)*

| Hyperparameter / Setting | Configured Value |
| :--- | :--- |
| **Cloud Platform** | Ultralytics Platform Cloud Training |
| **Hardware Accelerator** | NVIDIA RTX PRO 6000 Blackwell Server Edition (97,252 MiB VRAM) |
| **Host Compute** | AMD EPYC 9655 96-Core Processor (384 threads, 1.5 TB Host RAM) |
| **Base Model & Version** | YOLO26 Nano (yolo26n.pt pre-trained weights) [2] |
| **Task & Target Classes** | Single-Class Object Detection: Class 0 ('Prosper') |
| **Image Resolution** | 992 x 992 pixels (configured for high spatial fidelity) |
| **Dataset Partition** | 1,021 Images (817 Train [80%], 122 Val [12%], 82 Test [8%]) |
| **Epochs & Batch Size** | 100 Epochs, Dynamic Automated Batching (-1) |
| **Optimizer & Learning Rate** | SGD (lr0 = 0.01, lrf = 0.01, momentum = 0.937, weight_decay = 0.0005) |
| **Data Augmentations** | Mosaic (p=1.0, closed final 10 epochs), Flip (p=0.5), Random Erasing (p=0.4) |
| **Total Training Duration** | 340.6 seconds (~5.67 minutes across all 100 epochs) |

The model trained for 100 epochs using Stochastic Gradient Descent. I turned on mosaic augmentation, random horizontal flips, and random erasing so the model would learn to spot me even when parts of my body were cut off. Training wrapped up in 340.6 seconds.

---

## 5. Results and Analysis

### 5.1 Quantitative Benchmark
Comparing Run 1 and Run 2 shows solid progress. Table 4 lists the validation numbers.

*Table 4: Quantitative performance comparison (Run 1 vs. Run 2)*

| Evaluation Metric | Run 1 (exp, 945 imgs) | Run 2 (exp-2, 1,021 imgs) | Gain (pts) | Relative Gain |
| :--- | :---: | :---: | :---: | :---: |
| **Precision (P)** | **90.8%** | **91.7%** | **+0.9%** | **+1.0%** |
| **Recall (R)** | **78.6%** | **80.0%** | **+1.4%** | **+1.8%** |
| **mAP@0.50** | **80.5%** | **80.4%** | **-0.1%** | **-0.1%** |
| **mAP@0.50:0.95** | **31.7%** | **34.9%** | **+3.2%** | **+10.1%** |

### 5.2 Analysis of the Improvement
Precision improved to 91.7%, so over nine out of ten detections are accurate hits. Recall reached 80.0%, meaning the model catches me in four out of five difficult shots. While mAP@0.50 stayed essentially flat at 80.4%, the strict mAP@0.50:0.95 metric jumped from 31.7% to 34.9%—a 10.1% relative gain. That jump matters: it shows YOLO26n fits boxes around my head and torso much tighter than the baseline.

Run 1 often drew loose boxes that wobbled when camera angles changed. In Run 2, the higher resolution (992x992) and improved architecture produced clean, tight boundaries. The negative sampling also worked: false alarms on classmates dropped to zero during validation.

### 5.3 Diagnostic Curves and Predictions

#### Figure 1: Training and Validation Metrics Dashboard (`results.png`)
![Training Results](docs/graphs/results.png)
*Figure 1: 100-Epoch Training and Validation Metrics Dashboard (results.png)*

In Figure 1, bounding box loss dropped from 1.750 down to 0.806. Classification loss plummeted from 38.52 down to 0.233 as the network learned to tell me apart from background clutter. Validation curves stayed flat, proving the augmentations kept the model from simply memorizing training images. Best validation fitness happened at epoch 34, saved as `exp-2.pt` (5.54 MB).

#### Figure 2: Precision-Recall Curve (`PR_curve.png`)
![Precision-Recall Curve](docs/graphs/PR_curve.png)
*Figure 2: Precision-Recall Curve Reaching mAP50 = 80.4% (PR_curve.png)*

Figure 2 shows the Precision-Recall curve. The model holds 1.00 precision from recall 0.0 up through 0.60. When the model is confident, it makes almost zero mistakes. Area under the curve reached mAP@0.50 = 80.4%.

#### Figure 3: F1-Confidence Optimization Curve (`F1_curve.png`)
![F1-Confidence Curve](docs/graphs/F1_curve.png)
*Figure 3: F1-Confidence Optimization Curve Peaking at 0.857 (F1_curve.png)*

Figure 3 plots F1-score against confidence thresholds. It peaks at 0.857 at confidence 0.61. In the live web and mobile apps, I defaulted the threshold to 0.25 so quick snapshots don't lose recall, while batch jobs can use the peak 0.61 cutoff.

#### Figures 4 & 5: Confusion Matrices (`confusion_matrix.png` & `confusion_matrix_normalized.png`)
| Raw Detection Counts | Normalized Matrix |
| :---: | :---: |
| ![Confusion Matrix](docs/graphs/confusion_matrix.png) | ![Normalized Confusion Matrix](docs/graphs/confusion_matrix_normalized.png) |

*Figures 4 & 5: Raw Detection Counts and Normalized Confusion Matrices*

Figures 4 and 5 display the confusion matrices. In Figure 4, 13 test targets were located cleanly, while 72 candidate proposals were suppressed before NMS. In Figure 5, row-wise normalization shows 87% of target instances were captured cleanly, validating our 0.50 IoU cutoff.

---

## 6. Deployment

### 6.1 Ultralytics Cloud Deployment
I deployed the 5.54 MB weights file (`exp-2.pt`) as a container service on Google Cloud Run in europe-southwest1:
- **Inference Endpoint URL:** `https://predict-6b01cbfb6aa91a04b3325654-dproatj77a-no.a.run.app`

The container requires an Ultralytics API key. I keep this key strictly in server-side environment variables (`ULTRALYTICS_API_KEY`) on Vercel. It is never exposed in client JavaScript or mobile code.

### 6.2 FastAPI Gateway on Vercel
A serverless FastAPI proxy on Vercel bridges clients to the model, exposing `/api/health` and `/api/detect` with three strict rules:
1. **Open Access:** Anyone can test the system without filling out forms or creating passwords.
2. **Zero-Storage Memory Lifecycle:** Uploaded images stay strictly in volatile RAM. Inside a guaranteed `finally` block, the server runs `del image_bytes` and `gc.collect()` right after inference finishes. Zero bytes touch server hard drives or databases.
3. **Payload Limit:** Payloads over 4.5 MB get rejected with HTTP 413, preventing edge timeouts.

### 6.3 Web Application
The web app is an HTML5 Canvas studio built with Vite and hosted on Vercel:
- **Live Web Studio:** [https://object-detection-suite.vercel.app](https://object-detection-suite.vercel.app)

Users can drop photos or turn on their webcam. Bounding boxes draw live onto the canvas, and a Clear button dumps image bitmaps from browser memory.

### 6.4 Mobile Application
I built the mobile app with React Native and Expo under account `inkedme`:
- **Expo Project URL:** [https://expo.dev/accounts/inkedme/projects/vision-detect-mobile](https://expo.dev/accounts/inkedme/projects/vision-detect-mobile)

Users can snap pictures or pick from their gallery. The viewport calculates isotropic scaling with letterbox offsets so boxes do not drift on tall phone screens. I generated an installable Android APK using EAS (`eas.json`).

---

## 7. Testing and Discussion

I tested the live system manually across five real scenarios, shown in Table 5.

*Table 5: Field test and automated verification results*

| Test Scenario | Images | Author Detected | False Positives | Qualitative Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Solo photo, optimal daylight** | 5 | 5 (100%) | 0 | Clean detection; bounding box margin tightly localized. |
| **Solo photo, dim indoor / backlit** | 4 | 4 (100%) | 0 | Detected reliably despite harsh backlighting and shadows. |
| **Group photo (2 to 4 people)** | 4 | 4 (100%) | 0 | Author successfully isolated; peers correctly ignored. |
| **Group photo (5 to 8 people)** | 3 | 3 (100%) | 0 | Author detected in crowded scene; zero false alerts on others. |
| **Partial facial occlusion (glasses/hand)** | 2 | 2 (100%) | 0 | Reliable recognition despite partial visual occlusion. |

Automated smoke tests against the live API passed 5 out of 5 checks: health endpoint uptime, open access, token passthrough, mobile sync, and zero disk leaks. Roundtrip latency averaged **~575 milliseconds**.

---

## 8. Challenges and Lessons Learned

1. **Phone Photos are Massive:** Phone cameras shoot 10 MB to 15 MB files. Vercel rejects anything over 4.5 MB with HTTP 413. I fixed this by adding canvas downsampling on the web frontend and Pillow thumbnailing in FastAPI before sending bytes to Cloud Run.
2. **Memory Leaks in Zero-Storage Backends:** Python reference cycles can leave image bytes sitting in RAM. Wrapping the pipeline in an explicit `try-finally` block running `del image_bytes` and `gc.collect()` stopped memory leaks and kept disk storage at zero.
3. **Box Drift on Mobile Viewports:** Different phones have weird aspect ratios. Calculating isotropic scaling factors with letterbox offsets stopped boxes from stretching away from my face.
4. **API Key Leaks:** Putting API keys in mobile code is an easy way to get them stolen. Routing calls through the Vercel gateway with environment variables kept cloud credentials safe.
5. **The Big Takeaway:** Dataset quality matters far more than playing with model hyperparameters. Negative sampling on group photos did more for accuracy than any code change.

---

## 9. Conclusion and Recommendations

### 9.1 Conclusion
This capstone showed that an engineering student can train and ship a practical object detection system with consumer phone pictures and cloud compute. Fine-tuned on 1,021 photos on an NVIDIA RTX PRO 6000 GPU, the YOLO26n model achieved 91.7% precision, 80.0% recall, 80.4% mAP@50, and 34.9% mAP@50-95. Deployed to Google Cloud Run and fronted by a serverless FastAPI gateway on Vercel, the system maintains strict zero-storage privacy and returns detections in under 600 milliseconds.

### 9.2 Recommendations
1. **Edge Quantization:** Convert weights into INT8 ONNX, TFLite, or CoreML so mobile phones can run inference completely offline without internet.
2. **Multi-Student Tracking:** Expand the dataset to recognize other classmates for automated attendance tracking across campus.
3. **3D Pose and Depth:** Add dual-camera stereoscopic depth estimation to track physical body mechanics for sports and fitness.

---

## References

- [1] J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, "You Only Look Once: Unified, Real-Time Object Detection," in *Proc. IEEE Conf. Computer Vision and Pattern Recognition (CVPR)*, 2016, pp. 779–788.  
- [2] Ultralytics Inc., "Ultralytics YOLO26 Architecture and Deployment Documentation," 2026. [Online]. Available: https://docs.ultralytics.com  
- [3] T.-Y. Lin et al., "Microsoft COCO: Common Objects in Context," in *Proc. European Conf. Computer Vision (ECCV)*, 2014, pp. 740–755.  
- [4] S. Ren, K. He, R. Girshick, and J. Sun, "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks," *IEEE Trans. Pattern Analysis and Machine Intelligence*, vol. 39, no. 6, pp. 1137–1149, 2017.  
- [5] S. Ramírez, "FastAPI: High performance, easy to learn, fast to code, ready for production," 2024. [Online]. Available: https://fastapi.tiangolo.com  
- [6] Vercel Inc., "Vercel Serverless Functions and Edge Network Architecture," 2024. [Online]. Available: https://vercel.com/docs  
- [7] Meta Platforms Inc. and Expo Project, "React Native and Expo Application Services Documentation," 2024. [Online]. Available: https://reactnative.dev and https://docs.expo.dev  
- [8] A. Clark and contributors, "Pillow (PIL Fork) Documentation," 2024. [Online]. Available: https://python-pillow.org  
- [9] D. Apaak, "Factors influencing sports talent development in senior high schools in the Upper East Region of Ghana," *African Journal of Teacher Education*, vol. 13, no. 2, 2024.  
- [10] G. Bradski, "The OpenCV Library," *Dr. Dobb's Journal of Software Tools*, 2000.  
- [11] C. Lugaresi et al., "MediaPipe: A framework for building perception pipelines," *arXiv preprint arXiv:1906.08172*, 2019.  
- [12] Z. Cao et al., "OpenPose: Realtime multi-person 2D pose estimation using part affinity fields," *IEEE Trans. Pattern Anal. Mach. Intell.*, vol. 43, no. 1, pp. 172–186, 2021.  

---

## Appendices

### Appendix A: Dataset and Annotation Screenshots
Sample operational photographs from the authentic 1,021-image dataset stored in Google Drive:
- Figure 6 & Figure 7: Sample photographs from `docs/graphs/dataset_sample_1.jpg` and `docs/graphs/dataset_sample_2.jpg`.

### Appendix B: Training Telemetry & Figures
The trained weights checkpoint (`exp-2.pt`, 5.54 MB) and raw 101-epoch telemetry metrics (`results.csv`) are located in `docs/graphs/`.

### Appendix C: Deployment and Application Architecture
Decoupled serverless deployment topology connecting client applications, the Vercel FastAPI gateway, and the dedicated Ultralytics Cloud Run inference container under strict zero-storage RAM enforcement.

### Appendix D: Project Resources Table

*Table 6: Project resources*

| Resource | Link / Specification |
| :--- | :--- |
| **Source Code (GitHub Repository)** | [https://github.com/tormekpeyprosper-cpu/object-detection-suite](https://github.com/tormekpeyprosper-cpu/object-detection-suite) |
| **Production Web Application (Vercel)** | [https://object-detection-suite.vercel.app](https://object-detection-suite.vercel.app) |
| **Live API Health Endpoint** | [https://object-detection-suite.vercel.app/api/health](https://object-detection-suite.vercel.app/api/health) |
| **Live Detection API Endpoint** | `https://object-detection-suite.vercel.app/api/detect` |
| **Ultralytics Cloud Run Inference Host** | `https://predict-6b01cbfb6aa91a04b3325654-dproatj77a-no.a.run.app` |
| **Mobile Application (Expo / EAS Project)** | [https://expo.dev/accounts/inkedme/projects/vision-detect-mobile](https://expo.dev/accounts/inkedme/projects/vision-detect-mobile) |
| **Image Dataset (Google Drive - 1,021 Photos)** | [https://drive.google.com/drive/folders/1ARy1CuAKU0G6YdFLEGivOJGJ0VmC_hNm?usp=sharing](https://drive.google.com/drive/folders/1ARy1CuAKU0G6YdFLEGivOJGJ0VmC_hNm?usp=sharing) |
| **Local Dataset Archive Folder** | `C:\\Users\\torme\\Downloads\\exp2_dataset_photos` (1,021 JPEGs, 103.37 MB) |
| **Presentation Slide Deck (16:9 PPTX)** | [`docs/Object_Detection_Suite_Presentation.pptx`](docs/Object_Detection_Suite_Presentation.pptx) |
| **API Authentication Configuration** | Server-side environment variable `ULTRALYTICS_API_KEY` stored in Vercel |

### Appendix E: Declaration of Academic Integrity and Originality
I hereby declare that this project report entitled "Custom Object Detection and Recognition of Myself Using Ultralytics YOLO" is the outcome of my own investigative engineering work, conducted under the supervision of Mr. Harry Atieku-Boateng in the Department of Industrial Software Engineering at Pentecost University. All experimental metrics, model weights, dataset annotations, and client applications were authored, verified, and documented by the candidate. All literature, academic papers, and third-party software libraries referenced throughout this study have been fully acknowledged and cited in the References section in compliance with institutional guidelines.
