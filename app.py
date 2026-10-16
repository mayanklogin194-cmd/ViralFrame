import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

# Import your existing config and modules
from config import (
    UPLOAD_FOLDER,
    PROCESSED_FOLDER,
    BEST_FRAMES_FOLDER,
    REEL_FOLDER,
    KEYFRAME_FOLDER   # ✅ ADD THIS in config.py
)

from video_processing.silence_removal import remove_silence
from video_processing.keyframe_extractor import extract_keyframes
from image_processing.frame_classifier import classify_frames
from video_processing.reel_generator import generate_reel
from utils.auto_caption import add_captions
from ml.virality_predictor import predict_virality
from utils.caption_generator import generate_caption

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    video = request.files["video"]
    platform = request.form.get("platform", "instagram")

    filename = secure_filename(video.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    video.save(input_path)

    # ================= 1️⃣ Silence Removal =================
    clean_video_path = remove_silence(input_path)
    clean_video_name = os.path.basename(clean_video_path)

    # ================= 2️⃣ Keyframe Extraction =================
    frames = extract_keyframes(clean_video_path)

    # Extract just filenames for UI display
    keyframe_files = [
        os.path.basename(frame) for frame in frames
    ]

    # ================= 3️⃣ Frame Classification =================
    results, metadata = classify_frames(frames, BEST_FRAMES_FOLDER)

    # ================= 4️⃣ Reel Generation =================
    raw_reel = generate_reel(clean_video_path)
    captioned_reel_path = add_captions(raw_reel)
    reel_name = os.path.basename(captioned_reel_path)

    # ================= 5️⃣ Viral Frames =================
    brilliant_images = []

    for img in results["brilliant"]:
        meta = metadata[img]

        brilliant_images.append({
            "name": img,
            "score": meta.get("final_score", 0),
            "virality": predict_virality(meta),
            "caption": generate_caption(meta.get("suggestions", []), platform),
            "suggestions": meta.get("suggestions", [])
        })

    return render_template(
        "result.html",
        brilliant_images=brilliant_images,
        clean_video=clean_video_name,
        reel=reel_name,
        keyframes=keyframe_files,   # ✅ PASS KEYFRAMES
        platform=platform
    )


# ================= MEDIA ROUTES =================

@app.route("/video/<filename>")
def serve_video(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)


@app.route("/reel/<filename>")
def serve_reel(filename):
    return send_from_directory(REEL_FOLDER, filename)


@app.route("/keyframe/<filename>")
def serve_keyframe(filename):
    return send_from_directory(KEYFRAME_FOLDER, filename)


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(
        os.path.join(BEST_FRAMES_FOLDER, "brilliant"),
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)
