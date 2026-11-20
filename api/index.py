"""
Vercel Serverless Function Entrypoint for FastAPI
Directs all /api/* routes through the shared VisionDetect FastAPI backend.
"""
import os
import sys

# Ensure both api/ and backend/ directories are in Python module search path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from main import app
