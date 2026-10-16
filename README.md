# Content Genius — AI Reel & Viral Frame Generator

**Content Genius** is a Flask-based web application that turns raw videos into platform-ready short-form content. Upload a video, and the system automatically:

1. Removes silence / dead air  
2. Extracts keyframes  
3. Scores frames for “virality” (sharpness, brightness, faces)  
4. Enhances the best frames (super-resolution + face enhancement + Instagram-style crop)  
5. Generates a vertical **9:16** reel (first ~20 seconds)  
6. Applies captions (placeholder)  
7. Produces downloadable viral-ready frames with AI-generated captions and virality scores  

Supports **Instagram Reels**, **TikTok**, and **YouTube Shorts**.

---

## Features

| Feature | Description |
|---------|-------------|
| **Silence Removal** | Detects non-silent segments with Librosa and concatenates them with MoviePy |
| **Keyframe Extraction** | Extracts 1 frame per second using OpenCV |
| **Frame Classification** | Scores frames on sharpness (Laplacian), brightness, and face count (Haar cascade) |
| **Super Resolution** | 4× upscaling with ESPCN DNN model (`models/ESPCN_x4.pb`) or Lanczos fallback |
| **Face Enhancement** | Detail enhancement + sharpening on detected faces |
| **Instagram Crop** | Smart center-crop to 4:5 / 1:1 / 1.91:1 ratios |
| **Reel Generator** | Crops & resizes to 9:16 (1080×1920) vertical format |
| **Virality Score** | Weighted score from sharpness, brightness, and face presence |
| **Caption Generation** | Platform-aware short captions for frames |
| **Feedback / ML stubs** | Logging, creator profile, and RandomForest training scaffolding |

---

## Project Structure

```
video_project 15(REEL)/
├── app.py                      # Flask application & routes
├── config.py                   # Paths, folders, FFmpeg location
├── models/
│   └── ESPCN_x4.pb             # OpenCV DNN Super-Resolution model
├── image_processing/
│   ├── frame_classifier.py     # Score & select “brilliant” frames
│   ├── face_enhancer.py        # Face detail enhancement
│   ├── instagram_crop.py       # Aspect-ratio cropping
│   ├── super_resolution.py     # 4× ESPCN upscaling
│   ├── text_safe_zone.py       # Safe-area overlay helper
│   └── virality_predictor.py   # Simple virality heuristic
├── video_processing/
│   ├── silence_removal.py      # Remove silent parts
│   ├── keyframe_extractor.py   # Extract 1 fps keyframes
│   └── reel_generator.py       # Create 9:16 vertical reel
├── utils/
│   ├── auto_caption.py         # Caption overlay (currently copies file)
│   └── caption_generator.py    # Platform-specific caption text
├── ml/
│   ├── creator_profile.py      # Adaptive weights from feedback
│   ├── feedback_logger.py      # Log user actions
│   ├── train_from_feedback.py  # Train RandomForest on feedback
│   └── virality_predictor.py   # Virality scoring
├── templates/
│   ├── index.html              # Upload UI
│   └── result.html             # Results + downloads
├── uploads/                    # Incoming videos
└── processed/
    ├── keyframes/              # Extracted frames
    ├── best_frames/brilliant/  # Enhanced viral frames
    └── reels/                  # Generated vertical videos
```

---

## Requirements

### System

- **Python 3.10+**
- **FFmpeg** (required by MoviePy)  
  - Update the path in `config.py` (`FFMPEG_PATH`) to match your system.
- Optional: CUDA / GPU for faster OpenCV DNN (not required)

### Python packages

```bash
pip install flask werkzeug opencv-python numpy moviepy librosa scikit-learn pandas
```

Recommended versions (approximate):

```
flask>=2.3
opencv-python>=4.8
moviepy>=1.0.3
librosa>=0.10
numpy
scikit-learn
pandas
werkzeug
```

> **Note:** MoviePy may also need `imageio-ffmpeg` or a system FFmpeg binary.

---

## Setup & Run

1. **Clone / extract** the project and enter the directory:

   ```bash
   cd "video_project 15(REEL)"
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install flask werkzeug opencv-python numpy moviepy librosa scikit-learn pandas
   ```

4. **Configure FFmpeg**:

   Edit `config.py` and set `FFMPEG_PATH` to the full path of your `ffmpeg` executable.

5. **Run the app**:

   ```bash
   python app.py
   ```

6. Open your browser at **http://127.0.0.1:5000**

---

## Usage

1. Go to the home page (**Content Genius**).
2. Drag & drop or select a video (MP4 / MOV, up to 500 MB).
3. Choose target platform (Instagram Reels / TikTok / YouTube Shorts).
4. Click **Generate Viral Assets**.
5. On the results page you will see:
   - Silence-removed video
   - Vertical 9:16 captioned reel (downloadable)
   - Grid of “brilliant” frames with virality % and captions (downloadable)

---

## Pipeline Overview

```
Upload Video
    │
    ▼
Silence Removal (Librosa + MoviePy)
    │
    ├──► Keyframe Extraction (1 fps)
    │         │
    │         ▼
    │    Frame Scoring (sharpness + brightness + faces)
    │         │
    │         ▼
    │    Brilliant Frames → Super-Res → Face Enhance → Instagram Crop
    │
    └──► Reel Generator (crop to 9:16, first 20 s)
              │
              ▼
         Caption Placeholder → Final Reel
```

---

## Configuration Notes

- **Max upload size**: 500 MB (`app.config['MAX_CONTENT_LENGTH']`)
- **Reel length**: currently limited to the first 20 seconds (see `reel_generator.py`)
- **Brilliant threshold**: score > 120 (adjustable in `frame_classifier.py`)
- **Super-resolution model**: `models/ESPCN_x4.pb` (falls back to Lanczos if missing)

---

## Known Limitations / TODOs

- Auto-captioning is currently a file copy placeholder (`utils/auto_caption.py`). Integrate Whisper, AssemblyAI, or similar for real captions.
- Virality model is a simple heuristic; the ML training pipeline (`ml/`) is scaffolded but not wired into the main request flow.
- FFmpeg path is hardcoded for a Windows machine — update for your OS.
- No authentication or rate limiting.
- Large videos may be slow because processing is synchronous.

---

## License

This project appears to be a personal / educational prototype. Add a license of your choice (MIT, Apache-2.0, etc.) if you plan to distribute it.

---

## Credits

Built with:

- Flask  
- OpenCV (DNN Super-Resolution, Haar cascades)  
- MoviePy  
- Librosa  
- Tailwind CSS (CDN)  

---

**Happy creating viral content!** 🚀
