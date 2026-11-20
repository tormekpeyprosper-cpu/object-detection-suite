# Cross-Platform Object Detection System

A complete full-stack computer vision application featuring **ONE shared Python FastAPI backend** and **TWO clients** (a responsive HTML5/Canvas Vite web application and an Expo React Native mobile application) secured with **Supabase Authentication**, deployed via **Vercel Serverless**, and backed by an in-memory, zero-disk-storage privacy architecture.

---

## 📁 Repository Structure

```
object-detection-suite/
├── api/                      # Vercel Serverless Python Entrypoint
│   ├── index.py              # Serverless bridge directing /api/* to FastAPI
│   └── requirements.txt      # Python dependencies for Vercel deployment
├── backend/                  # Shared FastAPI Python Backend
│   ├── main.py               # Supabase-authenticated detection & health APIs
│   ├── test_backend.py       # Automated validation test suite
│   ├── requirements.txt      # Python dependencies (FastAPI, Uvicorn, HTTPX, Pillow)
│   ├── .env                  # Live environment variables (Supabase & Mock Mode)
│   └── .env.example          # Environment variable template
├── web-app/                  # Modern Web Client (HTML5 Canvas + Vite)
│   ├── index.html            # Cyberpunk Dark Glassmorphic Login + Detection Studio
│   ├── styles.css            # Option A styling: frosted glass, glows & gradients
│   ├── app.js                # Supabase Auth, canvas overlay & webcam engine
│   ├── package.json          # Vite scripts & @supabase/supabase-js dependency
│   ├── vite.config.js        # Vite local development server config (port 3000)
│   ├── .env                  # Vite client environment (VITE_SUPABASE_*)
│   ├── .env.example          # Client env template
│   └── dist/                 # Production-built bundle for Vercel Edge CDN
├── mobile-app/               # Cross-Platform Mobile Client (React Native + Expo)
│   ├── App.js                # Supabase Auth Screen + Camera/Gallery Vision Studio
│   ├── config.js             # Supabase & backend API endpoints configuration
│   ├── app.json              # Expo application manifest & permissions
│   ├── babel.config.js       # Expo Babel preset
│   ├── package.json          # React Native, Expo, and @supabase/supabase-js
│   └── README.md             # Mobile-specific setup & device connection guide
├── vercel.json               # Vercel deployment routing (FastAPI + Vite static)
├── REPORT.md                 # Complete formal evaluation & deployment report
└── README.md                 # Project documentation & run commands
```

---

## 🔒 Strict Zero-Storage Privacy Policy

Both the backend and clients enforce a strict **In-Memory Zero-Storage Architecture**:
- **Backend:** Uploaded image bytes are read directly into volatile memory (`image_bytes = await file.read()`). Images are **never** saved to disk, temp folders, caches, databases, or Supabase Storage. Bytes are explicitly deallocated and garbage-collected immediately after inference.
- **Supabase Usage:** Supabase is utilized strictly for identity authentication (JWT Bearer tokens) and optional lightweight non-image telemetry (user ID, counts, inference latency). Zero image files or base64 blobs are written to Supabase.
- **Web Client:** Images are loaded into in-memory bitmaps. The "Clear / Reset" button purges the canvas, revokes object URLs, and resets state.
- **Mobile Client:** Captured photos use transient cache references and are **never** saved to the device's camera roll or media library. Clearing or resetting purges all image references.

---

## ⚡ Quick Start Guide

### 1. Backend Service (`backend/`)

#### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- `pip`

#### Setup & Run Locally
```bash
# Navigate to the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
The API will be live at `http://localhost:8000`.  
- Interactive Swagger API Documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/health`

#### Run Backend Verification Tests
```bash
python test_backend.py
```

#### Inference Modes (Mock vs. Ultralytics)
- **Mock Mode (Default):** The backend returns realistic mock bounding boxes adapted to image dimensions. This allows frontend development and testing immediately before the final 1,000-image model is deployed.
- **Live Ultralytics Cloud Mode:** Update `backend/.env` with your real endpoint and API key to stream inferences directly through Ultralytics YOLO Hub:
  ```env
  ULTRALYTICS_ENDPOINT_URL=https://api.ultralytics.com/v1/predict/YOUR_MODEL_ID
  ULTRALYTICS_API_KEY=your_ultralytics_bearer_token
  ```

---

### 2. Web Application (`web-app/`)

#### Prerequisites
- Node.js 18+ and `npm`

#### Setup & Run Locally
```bash
# Navigate to the web-app directory
cd web-app

# Install dependencies (including @supabase/supabase-js)
npm install

# Start the Vite development server
npm run dev
```
Open `http://localhost:3000` in your browser.

#### Features
- **Option A Cyberpunk Glassmorphic Authentication:** Frosted glass card, dark slate background (`#0f172a`), neon cyan & blue accents, and show/hide password toggle.
- **Gated Studio:** Main vision detection tools are locked until authenticated via Supabase.
- **Dual Input Modes:** Drag-and-drop file upload or live webcam frame capture.
- **Canvas Overlay Engine:** High-visibility neon bounding boxes, labels, and confidence percentages.
- **Clear / Reset:** Instantly purges the canvas, stops webcam streams, and de-references memory.

#### Build for Production
```bash
npm run build
```
Generates a static production bundle in `web-app/dist/`.

---

### 3. Mobile Application (`mobile-app/`)

#### Prerequisites
- Node.js 18+ and `npm`
- **Expo Go** app installed on your physical iOS or Android device (or an Android Emulator / iOS Simulator).

#### Configure Backend Connection
Open `mobile-app/config.js` and set `API_BASE_URL`:
- **Expo Web / iOS Simulator:** `http://localhost:8000`
- **Android Emulator:** `http://10.0.2.2:8000`
- **Physical Phone on Local Wi-Fi:** `http://<YOUR_COMPUTER_IP>:8000` (e.g. `http://192.168.1.150:8000`)
- **Vercel Deployment:** `https://object-detection-suite.vercel.app`

*(Note: You can also tap the ⚙️ icon in the app header to edit the URL directly on your device at any time).*

#### Setup & Run
```bash
# Navigate to the mobile-app directory
cd mobile-app

# Install dependencies
npm install

# Start the Expo development server
npx expo start
```
- Press `w` to open in browser (Expo Web)
- Press `a` to run on connected Android emulator
- Press `i` to run on iOS simulator (macOS)
- Scan the printed QR code with **Expo Go** on your physical phone

---

## 🚀 Live Production Deployment

The system is deployed live on Vercel:
- **Production URL:** [https://object-detection-suite.vercel.app](https://object-detection-suite.vercel.app)
- **API Health Endpoint:** [https://object-detection-suite.vercel.app/api/health](https://object-detection-suite.vercel.app/api/health)
- **Vision Detection Endpoint:** `https://object-detection-suite.vercel.app/api/detect`
- **GitHub Repository:** [https://github.com/tormekpeyprosper-cpu/object-detection-suite](https://github.com/tormekpeyprosper-cpu/object-detection-suite)

### Re-deploying via Vercel CLI
```bash
vercel deploy --prod
```

### Environment Variables on Vercel
In your Vercel Project Settings (`Settings` -> `Environment Variables`), configure:
- `SUPABASE_URL`: `https://hlhkktramvskboiqnnju.supabase.co`
- `SUPABASE_ANON_KEY`: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- `ULTRALYTICS_ENDPOINT_URL`: *(Leave empty for mock mode until model is ready)*
- `ULTRALYTICS_API_KEY`: *(Leave empty for mock mode until model is ready)*

Vercel automatically:
1. Builds `web-app/` into static assets via Vite.
2. Deploys `api/index.py` as a serverless Python FastAPI function.
3. Routes all `/api/*` requests to the FastAPI backend and all other requests to the web app.

---

## 📡 API Reference

### `GET /api/health`
Checks service health, Supabase auth status, and active mode.
```json
{
  "status": "healthy",
  "service": "vision-detect-backend",
  "version": "2.0.0",
  "auth_provider": "Supabase Auth",
  "supabase_configured": true,
  "mode": "mock",
  "storage_policy": "STRICT_NO_STORAGE (In-memory only, zero disk/Supabase image storage)"
}
```

### `POST /api/detect`
Performs object detection on an uploaded image.
- **Method:** `POST`
- **Headers:** `Authorization: Bearer <SUPABASE_JWT_TOKEN>`
- **Content-Type:** `multipart/form-data`
- **Form Fields:**
  - `file`: `[binary image data]` (Required)
  - `conf`: `0.25` (Optional float, 0.0 - 1.0)
  - `iou`: `0.50` (Optional float, 0.0 - 1.0)
  - `imgsz`: `640` (Optional int, e.g., 640 or 1280)

---

## 📊 Dataset & Model Metrics Summary

Refer to [`REPORT.md`](./REPORT.md) for detailed documentation:
- **Baseline Dataset:** 949 initial images from `"WhatsApp Unknown 2026 10 21 at 2..."` archive.
- **Current Splits:** 759 Train / 114 Val / 76 Test (945 labeled, 4 pending).
- **Target Expansion:** 1,000 total images (800 Train / 120 Val / 80 Test).
- **Baseline Experiment (`exp`) Performance:**
  - **Precision:** 90.8%
  - **Recall:** 78.6%
  - **mAP@50:** 80.5%
  - **mAP@50-95:** 31.7%
