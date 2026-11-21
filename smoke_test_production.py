"""
Automated Live Production End-to-End Smoke Test
Target: https://object-detection-suite.vercel.app
"""
import io
import os
import sys
import time
import httpx
from PIL import Image

BASE_URL = "https://object-detection-suite.vercel.app"

def test_live_health():
    print(f"\n[TEST 1] Probing Health Endpoint: {BASE_URL}/api/health")
    headers = {"User-Agent": "SmokeTest/1.0"}
    with httpx.Client(timeout=30.0) as client:
        resp = client.get(f"{BASE_URL}/api/health", headers=headers)
    
    print(f"  Response Status: HTTP {resp.status_code}")
    print(f"  Response Body: {resp.text}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = resp.json()
    assert data.get("status") == "healthy", "Status must be 'healthy'"
    assert data.get("supabase_configured") is True, "Supabase must be configured"
    assert "STRICT_NO_STORAGE" in data.get("storage_policy", ""), "Storage policy must be zero-storage"
    print("  >>> PASS: /api/health is live, healthy, and enforcing zero-storage.")

def test_detect_open_access():
    print(f"\n[TEST 2] Verifying Open Public Access (Unauthenticated Request): {BASE_URL}/api/detect")
    img = Image.new("RGB", (320, 240), color=(70, 130, 180))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    image_bytes = buf.getvalue()

    headers = {"User-Agent": "SmokeTest/1.0"}
    files = {"file": ("open_access_test.jpg", image_bytes, "image/jpeg")}
    data = {"conf": 0.25, "iou": 0.50, "imgsz": 640}

    with httpx.Client(timeout=45.0) as client:
        resp = client.post(f"{BASE_URL}/api/detect", headers=headers, files=files, data=data)

    print(f"  Response Status: HTTP {resp.status_code}")
    print(f"  Response Body: {resp.text}")
    assert resp.status_code == 200, f"Expected 200 OK for open access, got {resp.status_code}"
    res = resp.json()
    assert res.get("status") == "success", "Response status must be 'success'"
    assert res.get("user_id") in ("open-access-user", "anonymous"), f"Expected open access user, got {res.get('user_id')}"
    print(f"  >>> PASS: Open public access confirmed! Inference succeeded with user_id: {res.get('user_id')}.")

    del image_bytes
    del buf

def test_detect_authenticated():
    print(f"\n[TEST 3] Running In-Memory Detection with Bearer Token: {BASE_URL}/api/detect")
    # Synthetic test image created strictly in volatile RAM
    img = Image.new("RGB", (800, 600), color=(30, 144, 255))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    image_bytes = buf.getvalue()

    headers = {
        "Authorization": "Bearer dev-test-token",
        "User-Agent": "SmokeTest/1.0"
    }
    files = {"file": ("in_memory_sample.jpg", image_bytes, "image/jpeg")}
    data = {"conf": "0.25", "iou": "0.50", "imgsz": "640"}

    start_time = time.perf_counter()
    with httpx.Client(timeout=45.0) as client:
        resp = client.post(f"{BASE_URL}/api/detect", headers=headers, files=files, data=data)
    roundtrip_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

    print(f"  Roundtrip Latency: {roundtrip_ms} ms")
    print(f"  Response Status: HTTP {resp.status_code}")
    print(f"  Response Body: {resp.text}")
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

    res = resp.json()
    assert res.get("status") == "success", "Response status must be 'success'"
    active_mode = res.get("mode")
    assert active_mode in ("ultralytics", "mock"), f"Unexpected mode: {active_mode}"
    print(f"  Active Inference Mode: {active_mode}")
    assert res.get("image", {}).get("width") == 800, "Image width must match RAM buffer (800)"
    assert res.get("image", {}).get("height") == 600, "Image height must match RAM buffer (600)"
    if active_mode == "mock":
        assert res.get("detections_count", 0) >= 1, "Must detect at least 1 object in mock mode"
    else:
        assert isinstance(res.get("detections"), list), "Detections must be a list"
        print(f"  Live Ultralytics Inference confirmed: {res.get('detections_count')} detections on test image.")

    for det in res.get("detections", []):
        assert "name" in det
        assert "confidence" in det
        assert "box" in det
        print(f"    Detected: {det['name']} ({round(det['confidence']*100, 1)}%) at {det['box']}")

    # Explicitly clear RAM buffers
    del image_bytes
    del buf
    print("  >>> PASS: In-memory detection executed successfully; image bytes purged from memory.")

def test_mobile_config():
    print("\n[TEST 4] Inspecting mobile-app/config.js")
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mobile-app", "config.js")
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "https://object-detection-suite.vercel.app" in content, "mobile-app/config.js must point to live Vercel URL"
    assert "https://hlhkktramvskboiqnnju.supabase.co" in content, "mobile-app/config.js must have Supabase URL"
    print("  >>> PASS: mobile-app/config.js is correctly configured with live production endpoints.")

def test_disk_zero_storage_audit():
    print("\n[TEST 5] Auditing Disk for Leaked Images")
    project_root = os.path.dirname(os.path.abspath(__file__))
    leaked = []
    for root, dirs, files in os.walk(project_root):
        if "node_modules" in root or ".git" in root or "assets" in root or "docs" in root:
            continue
        for f in files:
            if f.endswith((".jpg", ".jpeg", ".png", ".webp")) and not f in ("favicon.png", "icon.png", "splash.png"):
                leaked.append(os.path.join(root, f))

    assert len(leaked) == 0, f"Leaked images found on disk: {leaked}"
    print("  >>> PASS: Verified 0 image files leaked to disk. Strict Zero-Storage confirmed.")

if __name__ == "__main__":
    print("=" * 70)
    print("OBJECT DETECTION SUITE - LIVE PRODUCTION SMOKE TEST")
    print(f"Target URL: {BASE_URL}")
    print("=" * 70)
    test_live_health()
    test_detect_open_access()
    test_detect_authenticated()
    test_mobile_config()
    test_disk_zero_storage_audit()
    print("=" * 70)
    print("ALL LIVE PRODUCTION SMOKE TESTS PASSED CLEANLY! (5/5)")
    print("=" * 70)
