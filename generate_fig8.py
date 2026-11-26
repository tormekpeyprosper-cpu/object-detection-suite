import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')

# Background
fig.patch.set_facecolor('#FFFFFF')

# Styles
box_kw = dict(boxstyle="round,pad=0.5", ec="#2C3E50", lw=1.5)
arrow_kw = dict(arrowstyle="->", lw=2, color="#2980B9")

# 1. Client Layer
ax.text(1.5, 4.3, "1. CLIENT LAYER", fontsize=11, fontweight='bold', color='#1A365D', ha='center')
ax.text(1.5, 3.2, "Web Client (HTML5 / Vite)\nhttps://object-detection-suite.vercel.app\n\nMobile App (React Native / Expo)\nAndroid APK (Camera / Gallery)", 
        ha='center', va='center', fontsize=9, bbox=dict(facecolor='#EBF5FB', **box_kw))

# 2. Serverless Gateway Layer
ax.text(5.0, 4.3, "2. EDGE GATEWAY (VERCEL)", fontsize=11, fontweight='bold', color='#1A365D', ha='center')
ax.text(5.0, 3.2, "FastAPI Reverse Proxy (/api/detect)\n• In-Memory Image Validation\n• Max 4.5 MB Payload Guard\n• Strict Zero-Storage RAM Lifecycle\n(del image_bytes & gc.collect())", 
        ha='center', va='center', fontsize=9, bbox=dict(facecolor='#FEF9E7', **box_kw))

# 3. Cloud Run Inference Layer
ax.text(8.5, 4.3, "3. INFERENCE (CLOUD RUN)", fontsize=11, fontweight='bold', color='#1A365D', ha='center')
ax.text(8.5, 3.2, "Google Cloud Run Container\n(europe-southwest1)\n• Ultralytics YOLO26n Engine\n• Weights: exp-2.pt (5.54 MB)\n• Server-side API Key Auth", 
        ha='center', va='center', fontsize=9, bbox=dict(facecolor='#EAFAF1', **box_kw))

# Arrows between main layers
ax.annotate("", xy=(3.3, 3.2), xytext=(2.7, 3.2), arrowprops=arrow_kw)
ax.annotate("", xy=(6.8, 3.2), xytext=(6.7, 3.2), arrowprops=arrow_kw)

# Data Flow Annotations
ax.text(3.0, 3.6, "Multipart Image\nUpload (RAM)", ha='center', fontsize=8, color='#2C3E50')
ax.text(6.75, 3.6, "Authenticated\nForwarding", ha='center', fontsize=8, color='#2C3E50')

# Bottom Flow (Return / Decoupled Knowledge)
ax.text(5.0, 1.2, "4. DECOUPLED ARCHITECTURE & VERIFICATION\n• Zero-Disk Storage: Images discarded immediately after inference (0 byte disk trace)\n• JSON Detection Payload: Normalized bounding boxes [x, y, w, h] + confidence returned\n• Training Archive: 1,021 photos safely preserved in public Google Drive archive",
        ha='center', va='center', fontsize=9, bbox=dict(facecolor='#F4F6F6', **box_kw))

ax.annotate("", xy=(5.0, 2.1), xytext=(5.0, 2.4), arrowprops=dict(arrowstyle="<-", lw=1.5, color="#7F8C8D"))

plt.title("Figure 8: Decoupled Zero-Storage Client-Server Architecture", fontsize=12, fontweight='bold', pad=15, color='#2C3E50')
plt.tight_layout()

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(BASE_DIR, "docs", "graphs", "figure8_architecture.png")
plt.savefig(out_path, dpi=300, bbox_inches='tight')
print(f"Generated Figure 8 diagram at {out_path}")
