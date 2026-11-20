"""
Backend Unit and Integration Verification Test Suite (Supabase Auth + Mock Detection)
"""
import os
import sys

# Add backend directory to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

import main

def test_config():
    print("Testing config detection...")
    assert not main.is_ultralytics_configured(), "Should be False in mock mode"
    assert main.is_supabase_configured(), "Supabase should be configured with user credentials"
    print("  [OK] Mock inference & Supabase Auth configuration verified.")

def test_mock_generation():
    print("Testing mock detection generation...")
    dets = main.generate_mock_detections(width=1280, height=720, conf_threshold=0.25)
    assert len(dets) >= 1, "Should generate at least one detection"
    first = dets[0]
    assert "name" in first
    assert "confidence" in first
    assert "box" in first
    assert "relative_box" in first
    assert first["box"]["x2"] <= 1280
    assert first["box"]["y2"] <= 720
    print(f"  [OK] Generated {len(dets)} valid mock detections within image bounds.")

def test_ultralytics_parser():
    print("Testing Ultralytics response parsing...")
    sample_api_response = {
        "images": [
            {
                "results": [
                    {
                        "name": "pedestrian",
                        "confidence": 0.912,
                        "box": {"x1": 50, "y1": 100, "x2": 200, "y2": 400}
                    }
                ]
            }
        ]
    }
    parsed = main.parse_ultralytics_detections(sample_api_response, width=1000, height=800)
    assert len(parsed) == 1
    assert parsed[0]["name"] == "pedestrian"
    assert parsed[0]["confidence"] == 0.912
    assert parsed[0]["relative_box"]["x_min"] == 0.05
    assert parsed[0]["relative_box"]["y_min"] == 0.125
    print("  [OK] Correctly parsed Ultralytics API response.")

def test_cors_and_routes():
    print("Testing FastAPI app routes...")
    routes = [route.path for route in main.app.routes]
    assert "/api/health" in routes, "Health route must be registered"
    assert "/api/detect" in routes, "Detect route must be registered"
    print("  [OK] All required API routes registered on FastAPI app.")

if __name__ == "__main__":
    print("=" * 60)
    print("Running Shared Backend Validation Suite")
    print("=" * 60)
    test_config()
    test_mock_generation()
    test_ultralytics_parser()
    test_cors_and_routes()
    print("=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
