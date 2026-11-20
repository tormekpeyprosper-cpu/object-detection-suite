/**
 * VisionDetect Web Client
 * Supabase Authentication + HTML5 Canvas Bounding Box Rendering
 * Strict Zero-Storage In-Memory Pipeline
 */

import { createClient } from "@supabase/supabase-js";

// Supabase Configuration (Vite environment variables with hardcoded fallbacks)
const SUPABASE_URL = 
  (import.meta.env && import.meta.env.VITE_SUPABASE_URL) || 
  "https://hlhkktramvskboiqnnju.supabase.co";

const SUPABASE_ANON_KEY = 
  (import.meta.env && import.meta.env.VITE_SUPABASE_ANON_KEY) || 
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsaGtrdHJhbXZza2JvaXFubmp1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUxMTQxNDUsImV4cCI6MjExMDY5MDE0NX0.ec37e6bMKyLMhOsaIkzQhVZEm1KO5INbWxnt18Rv_9Q";

// Initialize Supabase Client
export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Application State
let currentSession = null;
let authMode = "signin"; // 'signin' or 'signup'
let currentImageBitmap = null;
let currentImageBlob = null;
let currentDetections = [];
let activeWebcamStream = null;
let currentFacingMode = "user"; // 'user' or 'environment'

// DOM Elements: Auth
const authSection = document.getElementById("authSection");
const appSection = document.getElementById("appSection");
const tabSignIn = document.getElementById("tabSignIn");
const tabSignUp = document.getElementById("tabSignUp");
const authForm = document.getElementById("authForm");
const authEmail = document.getElementById("authEmail");
const authPassword = document.getElementById("authPassword");
const btnTogglePwd = document.getElementById("btnTogglePwd");
const btnAuthSubmit = document.getElementById("btnAuthSubmit");
const authSubmitText = document.getElementById("authSubmitText");
const authSpinner = document.getElementById("authSpinner");
const authAlert = document.getElementById("authAlert");

// DOM Elements: Studio Header & Status
const userBadge = document.getElementById("userBadge");
const userEmailText = document.getElementById("userEmailText");
const btnSignOut = document.getElementById("btnSignOut");
const backendStatus = document.getElementById("backendStatus");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");

// DOM Elements: Studio Tabs & Panels
const tabUpload = document.getElementById("tabUpload");
const tabWebcam = document.getElementById("tabWebcam");
const uploadPanel = document.getElementById("uploadPanel");
const webcamPanel = document.getElementById("webcamPanel");

const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");

const webcamVideo = document.getElementById("webcamVideo");
const btnToggleCam = document.getElementById("btnToggleCam");
const btnSwitchCam = document.getElementById("btnSwitchCam");
const btnCaptureFrame = document.getElementById("btnCaptureFrame");

const apiUrlInput = document.getElementById("apiUrlInput");
const confSlider = document.getElementById("confSlider");
const confValue = document.getElementById("confValue");
const iouSlider = document.getElementById("iouSlider");
const iouValue = document.getElementById("iouValue");
const imgszSelect = document.getElementById("imgszSelect");

const btnDetect = document.getElementById("btnDetect");
const btnClear = document.getElementById("btnClear");

const viewportContainer = document.getElementById("viewportContainer");
const canvasWrapper = document.getElementById("canvasWrapper");
const previewCanvas = document.getElementById("previewCanvas");
const placeholderView = document.getElementById("placeholderView");
const loadingOverlay = document.getElementById("loadingOverlay");
const loadingMsg = document.getElementById("loadingMsg");

const resultsCard = document.getElementById("resultsCard");
const resMode = document.getElementById("resMode");
const resLatency = document.getElementById("resLatency");
const resCount = document.getElementById("resCount");
const resDims = document.getElementById("resDims");
const detectionsTableBody = document.getElementById("detectionsTableBody");

// Color Palette for Distinct Class Bounding Boxes
const BOX_COLORS = [
  { stroke: "#06b6d4", fill: "rgba(6, 182, 212, 0.2)" }, // Cyan
  { stroke: "#10b981", fill: "rgba(16, 185, 129, 0.2)" }, // Emerald
  { stroke: "#f59e0b", fill: "rgba(245, 158, 11, 0.2)" }, // Amber
  { stroke: "#ec4899", fill: "rgba(236, 72, 153, 0.2)" }, // Pink
  { stroke: "#8b5cf6", fill: "rgba(139, 92, 246, 0.2)" }, // Purple
  { stroke: "#3b82f6", fill: "rgba(59, 130, 246, 0.2)" }, // Blue
];

// Initialize on DOM load
document.addEventListener("DOMContentLoaded", async () => {
  if (apiUrlInput) {
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
      apiUrlInput.value = `${window.location.origin}/api/detect`;
    } else if (import.meta.env && import.meta.env.VITE_API_BASE_URL) {
      apiUrlInput.value = `${import.meta.env.VITE_API_BASE_URL}/api/detect`;
    }
  }
  setupAuthListeners();
  setupStudioListeners();
  await checkInitialSession();
  checkBackendHealth();
});

// ==============================================================================
// 1. Supabase Authentication Handlers
// ==============================================================================
function setupAuthListeners() {
  tabSignIn.addEventListener("click", () => setAuthMode("signin"));
  tabSignUp.addEventListener("click", () => setAuthMode("signup"));

  btnTogglePwd.addEventListener("click", () => {
    const isPassword = authPassword.type === "password";
    authPassword.type = isPassword ? "text" : "password";
    btnTogglePwd.textContent = isPassword ? "🔒" : "👁️";
  });

  authForm.addEventListener("submit", handleAuthSubmit);
  btnSignOut.addEventListener("click", handleSignOut);

  // Listen to Supabase auth state changes
  supabase.auth.onAuthStateChange((event, session) => {
    currentSession = session;
    updateUIForSession(session);
  });
}

function setAuthMode(mode) {
  authMode = mode;
  hideAuthAlert();
  if (mode === "signin") {
    tabSignIn.classList.add("active");
    tabSignUp.classList.remove("active");
    authSubmitText.textContent = "Sign In";
  } else {
    tabSignUp.classList.add("active");
    tabSignIn.classList.remove("active");
    authSubmitText.textContent = "Create Account";
  }
}

async function checkInitialSession() {
  try {
    const { data: { session } } = await supabase.auth.getSession();
    currentSession = session;
    updateUIForSession(session);
  } catch (err) {
    console.error("Session check error:", err);
  }
}

function updateUIForSession(session) {
  if (session && session.user) {
    authSection.style.display = "none";
    appSection.style.display = "flex";
    userEmailText.textContent = session.user.email || "Authenticated User";
    checkBackendHealth();
  } else {
    authSection.style.display = "flex";
    appSection.style.display = "none";
    clearAndResetState();
  }
}

async function handleAuthSubmit(e) {
  e.preventDefault();
  const email = authEmail.value.trim();
  const password = authPassword.value;

  if (!email || !password) {
    showAuthAlert("Please enter both email and password.", "error");
    return;
  }

  setAuthLoading(true);
  hideAuthAlert();

  try {
    if (authMode === "signin") {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      if (error) throw error;
      currentSession = data.session;
      showAuthAlert("Signed in successfully!", "success");
    } else {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
      });
      if (error) throw error;
      if (data.session) {
        currentSession = data.session;
        showAuthAlert("Account created successfully!", "success");
      } else {
        showAuthAlert("Registration submitted! Please check your email to confirm your account.", "success");
      }
    }
  } catch (err) {
    showAuthAlert(err.message || "Authentication failed.", "error");
  } finally {
    setAuthLoading(false);
  }
}

async function handleSignOut() {
  try {
    await supabase.auth.signOut();
  } catch (err) {
    console.error("Sign out error:", err);
  } finally {
    currentSession = null;
    updateUIForSession(null);
  }
}

function showAuthAlert(message, type) {
  authAlert.textContent = message;
  authAlert.className = `auth-alert ${type}`;
}

function hideAuthAlert() {
  authAlert.style.display = "none";
}

function setAuthLoading(loading) {
  btnAuthSubmit.disabled = loading;
  authSpinner.style.display = loading ? "inline-block" : "none";
  authSubmitText.style.display = loading ? "none" : "inline";
}

// ==============================================================================
// 2. Studio Detection & Controls
// ==============================================================================
function setupStudioListeners() {
  // Tabs
  tabUpload.addEventListener("click", () => switchTab("upload"));
  tabWebcam.addEventListener("click", () => switchTab("webcam"));

  // Dropzone file handling
  dropzone.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", handleFileSelect);

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });
  dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      loadImageFromFile(e.dataTransfer.files[0]);
    }
  });

  // Sliders
  confSlider.addEventListener("input", (e) => {
    confValue.textContent = Number(e.target.value).toFixed(2);
  });
  iouSlider.addEventListener("input", (e) => {
    iouValue.textContent = Number(e.target.value).toFixed(2);
  });

  // Webcam Controls
  btnToggleCam.addEventListener("click", toggleWebcam);
  btnSwitchCam.addEventListener("click", switchCameraDirection);
  btnCaptureFrame.addEventListener("click", captureWebcamFrame);

  // Detect and Reset
  btnDetect.addEventListener("click", performDetection);
  btnClear.addEventListener("click", clearAndResetState);
}

// Check Backend Health
async function checkBackendHealth() {
  const detectUrl = apiUrlInput.value.trim();
  const baseOrigin = detectUrl.replace(/\/api\/detect\/?$/, "");
  const healthUrl = `${baseOrigin}/api/health`;

  try {
    const res = await fetch(healthUrl);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    statusDot.className = "status-dot";
    if (data.mode === "ultralytics") {
      statusDot.classList.add("connected");
      statusText.textContent = "Backend: Ultralytics Cloud Connected";
    } else {
      statusDot.classList.add("mock");
      statusText.textContent = "Backend: Ready (Mock Inference Mode)";
    }
  } catch (err) {
    statusDot.className = "status-dot error";
    statusText.textContent = "Backend Offline (Start Uvicorn on :8000)";
  }
}

// Switch UI Tabs
function switchTab(mode) {
  if (mode === "upload") {
    tabUpload.classList.add("active");
    tabWebcam.classList.remove("active");
    uploadPanel.style.display = "block";
    webcamPanel.classList.remove("active");
  } else {
    tabWebcam.classList.add("active");
    tabUpload.classList.remove("active");
    uploadPanel.style.display = "none";
    webcamPanel.classList.add("active");
  }
}

function handleFileSelect(e) {
  if (e.target.files && e.target.files.length > 0) {
    loadImageFromFile(e.target.files[0]);
  }
}

function loadImageFromFile(file) {
  if (!file.type.startsWith("image/")) {
    alert("Please select a valid image file.");
    return;
  }

  currentImageBlob = file;
  const objectUrl = URL.createObjectURL(file);
  const img = new Image();
  img.onload = () => {
    currentImageBitmap = img;
    currentDetections = [];
    renderCanvas();
    btnDetect.disabled = false;
    URL.revokeObjectURL(objectUrl);
  };
  img.src = objectUrl;
}

// Webcam handlers
async function toggleWebcam() {
  if (activeWebcamStream) {
    stopWebcam();
  } else {
    try {
      const constraints = {
        video: {
          facingMode: currentFacingMode,
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
        audio: false,
      };
      activeWebcamStream = await navigator.mediaDevices.getUserMedia(constraints);
      webcamVideo.srcObject = activeWebcamStream;
      btnToggleCam.textContent = "Stop Camera";
      btnCaptureFrame.disabled = false;
    } catch (err) {
      alert(`Could not access webcam: ${err.message}`);
    }
  }
}

function stopWebcam() {
  if (activeWebcamStream) {
    activeWebcamStream.getTracks().forEach((track) => track.stop());
    activeWebcamStream = null;
    webcamVideo.srcObject = null;
    btnToggleCam.textContent = "Start Camera";
    btnCaptureFrame.disabled = true;
  }
}

async function switchCameraDirection() {
  currentFacingMode = currentFacingMode === "user" ? "environment" : "user";
  if (activeWebcamStream) {
    stopWebcam();
    await toggleWebcam();
  }
}

function captureWebcamFrame() {
  if (!activeWebcamStream || !webcamVideo.videoWidth) return;

  const offscreen = document.createElement("canvas");
  offscreen.width = webcamVideo.videoWidth;
  offscreen.height = webcamVideo.videoHeight;
  const ctx = offscreen.getContext("2d");
  ctx.drawImage(webcamVideo, 0, 0);

  offscreen.toBlob(
    (blob) => {
      if (!blob) return;
      currentImageBlob = blob;
      const objectUrl = URL.createObjectURL(blob);
      const img = new Image();
      img.onload = () => {
        currentImageBitmap = img;
        currentDetections = [];
        renderCanvas();
        btnDetect.disabled = false;
        URL.revokeObjectURL(objectUrl);
        performDetection();
      };
      img.src = objectUrl;
    },
    "image/jpeg",
    0.95
  );
}

// Perform Object Detection via Supabase-Authenticated POST
async function performDetection() {
  if (!currentImageBlob) {
    alert("Please upload an image or capture a webcam frame first.");
    return;
  }

  // Ensure user is authenticated
  if (!currentSession || !currentSession.access_token) {
    alert("Authentication required. Please sign in to run object detection.");
    updateUIForSession(null);
    return;
  }

  const endpoint = apiUrlInput.value.trim() || "http://localhost:8000/api/detect";
  const conf = parseFloat(confSlider.value);
  const iou = parseFloat(iouSlider.value);
  const imgsz = parseInt(imgszSelect.value, 10);

  const formData = new FormData();
  formData.append("file", currentImageBlob, "detect_frame.jpg");
  formData.append("conf", conf);
  formData.append("iou", iou);
  formData.append("imgsz", imgsz);

  showLoading(true, "Authenticating & streaming image to detection pipeline...");
  btnDetect.disabled = true;

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      body: formData,
      headers: {
        "Authorization": `Bearer ${currentSession.access_token}`,
      },
    });

    if (response.status === 401) {
      alert("Your session has expired. Please sign in again.");
      await handleSignOut();
      return;
    }

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || `Server returned HTTP ${response.status}`);
    }

    const result = await response.json();
    currentDetections = result.detections || [];
    renderCanvas();
    displayResultsCard(result);
  } catch (err) {
    alert(`Detection failed: ${err.message}`);
    console.error("Detection error:", err);
  } finally {
    showLoading(false);
    btnDetect.disabled = false;
  }
}

// Render Image and High-Visibility Bounding Boxes onto Canvas
function renderCanvas() {
  if (!currentImageBitmap) {
    canvasWrapper.style.display = "none";
    placeholderView.style.display = "block";
    return;
  }

  placeholderView.style.display = "none";
  canvasWrapper.style.display = "flex";

  const imgWidth = currentImageBitmap.naturalWidth || currentImageBitmap.width;
  const imgHeight = currentImageBitmap.naturalHeight || currentImageBitmap.height;

  previewCanvas.width = imgWidth;
  previewCanvas.height = imgHeight;

  const ctx = previewCanvas.getContext("2d");
  ctx.clearRect(0, 0, imgWidth, imgHeight);

  // Draw base image
  ctx.drawImage(currentImageBitmap, 0, 0, imgWidth, imgHeight);

  // Draw Bounding Boxes and Labels
  currentDetections.forEach((det, index) => {
    const colorTheme = BOX_COLORS[index % BOX_COLORS.length];
    const box = det.box || {};
    let x1 = box.x1;
    let y1 = box.y1;
    let x2 = box.x2;
    let y2 = box.y2;

    if (x1 === undefined && det.relative_box) {
      x1 = det.relative_box.x_min * imgWidth;
      y1 = det.relative_box.y_min * imgHeight;
      x2 = det.relative_box.x_max * imgWidth;
      y2 = det.relative_box.y_max * imgHeight;
    }

    const boxWidth = x2 - x1;
    const boxHeight = y2 - y1;

    // Draw box fill
    ctx.fillStyle = colorTheme.fill;
    ctx.fillRect(x1, y1, boxWidth, boxHeight);

    // Draw box outline with glow
    ctx.strokeStyle = colorTheme.stroke;
    ctx.lineWidth = Math.max(3, Math.round(imgWidth / 300));
    ctx.shadowColor = colorTheme.stroke;
    ctx.shadowBlur = 8;
    ctx.strokeRect(x1, y1, boxWidth, boxHeight);
    ctx.shadowBlur = 0;

    // Format label text
    const confPct = Math.round(det.confidence * 100);
    const labelText = `${det.name} ${confPct}%`;

    const fontSize = Math.max(14, Math.round(imgWidth / 45));
    ctx.font = `bold ${fontSize}px sans-serif`;

    const textMetrics = ctx.measureText(labelText);
    const textWidth = textMetrics.width;
    const badgeHeight = fontSize + 8;
    const badgeWidth = textWidth + 12;

    let badgeY = y1 - badgeHeight;
    if (badgeY < 0) badgeY = y1;
    let badgeX = x1;
    if (badgeX + badgeWidth > imgWidth) badgeX = imgWidth - badgeWidth;

    ctx.fillStyle = colorTheme.stroke;
    ctx.beginPath();
    ctx.roundRect(badgeX, badgeY, badgeWidth, badgeHeight, 4);
    ctx.fill();

    ctx.fillStyle = "#ffffff";
    ctx.textBaseline = "middle";
    ctx.fillText(labelText, badgeX + 6, badgeY + badgeHeight / 2);
  });
}

function displayResultsCard(result) {
  resultsCard.style.display = "block";
  resMode.textContent = (result.mode || "MOCK").toUpperCase();
  resLatency.textContent = `${result.inference_time_ms} ms`;
  resCount.textContent = result.detections_count || 0;
  resDims.textContent = `${result.image.width} × ${result.image.height} px`;

  detectionsTableBody.innerHTML = "";
  if (!result.detections || result.detections.length === 0) {
    detectionsTableBody.innerHTML = `<tr><td colspan="3" style="text-align:center; color:var(--text-secondary); padding:1rem;">No detections passed the confidence threshold (${confSlider.value}).</td></tr>`;
    return;
  }

  result.detections.forEach((det, idx) => {
    const color = BOX_COLORS[idx % BOX_COLORS.length].stroke;
    const pct = Math.round(det.confidence * 100);
    const box = det.box || {};
    const coords = `[${Math.round(box.x1)}, ${Math.round(box.y1)}, ${Math.round(box.x2)}, ${Math.round(box.y2)}]`;

    const row = document.createElement("tr");
    row.innerHTML = `
      <td><strong style="color:${color};">&#9632;</strong> ${det.name}</td>
      <td>
        <span class="confidence-chip" style="background:${color}22; color:${color}; border:1px solid ${color}66;">
          ${pct}% (${det.confidence.toFixed(3)})
        </span>
      </td>
      <td style="font-family:monospace; font-size:0.8rem; color:var(--text-secondary);">${coords}</td>
    `;
    detectionsTableBody.appendChild(row);
  });
}

function clearAndResetState() {
  currentImageBitmap = null;
  currentImageBlob = null;
  currentDetections = [];
  if (fileInput) fileInput.value = "";

  stopWebcam();

  if (previewCanvas) {
    const ctx = previewCanvas.getContext("2d");
    ctx.clearRect(0, 0, previewCanvas.width, previewCanvas.height);
  }

  if (canvasWrapper) canvasWrapper.style.display = "none";
  if (placeholderView) placeholderView.style.display = "block";
  if (resultsCard) resultsCard.style.display = "none";
  if (btnDetect) btnDetect.disabled = true;

  checkBackendHealth();
}

function showLoading(show, message = "Processing...") {
  if (loadingMsg) loadingMsg.textContent = message;
  if (loadingOverlay) {
    if (show) loadingOverlay.classList.add("active");
    else loadingOverlay.classList.remove("active");
  }
}
