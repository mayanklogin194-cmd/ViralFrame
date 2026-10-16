import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed")
KEYFRAME_FOLDER = os.path.join(PROCESSED_FOLDER, "keyframes")
BEST_FRAMES_FOLDER = os.path.join(PROCESSED_FOLDER, "best_frames")
REEL_FOLDER = os.path.join(PROCESSED_FOLDER, "reels")   # ✅ ADD THIS

FFMPEG_PATH = r"C:\Users\Asus\Downloads\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

# Create folders automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(KEYFRAME_FOLDER, exist_ok=True)
os.makedirs(BEST_FRAMES_FOLDER, exist_ok=True)
os.makedirs(os.path.join(BEST_FRAMES_FOLDER, "brilliant"), exist_ok=True)
os.makedirs(REEL_FOLDER, exist_ok=True)  # ✅ ADD THIS

if not os.path.exists(FFMPEG_PATH):
    print(f"⚠️ Warning: FFmpeg not found at {FFMPEG_PATH}")
