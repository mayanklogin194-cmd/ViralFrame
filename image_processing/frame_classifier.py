import os
import cv2
import numpy as np
from config import KEYFRAME_FOLDER
from image_processing.super_resolution import super_hd_4x
from image_processing.face_enhancer import enhance_faces
from image_processing.instagram_crop import instagram_crop

FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def sharpness(img):
    return cv2.Laplacian(img, cv2.CV_64F).var()

def brightness(img):
    return np.mean(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

def face_count(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)
    return len(faces)

def classify_frames(frames, output_dir):
    brilliant = []
    metadata = {}
    brilliant_path = os.path.join(output_dir, "brilliant")

    for f in frames:
        path = os.path.join(KEYFRAME_FOLDER, f)
        img = cv2.imread(path)
        if img is None:
            continue

        s = sharpness(img)
        b = brightness(img)
        faces = face_count(img)

        score = s * 0.4 + b * 0.2 + faces * 25

        if score > 120:
            brilliant.append(f)
            img = super_hd_4x(img)
            img = enhance_faces(img)
            img = instagram_crop(img, "portrait")
            cv2.imwrite(os.path.join(brilliant_path, f), img)

        metadata[f] = {
            "final_score": round(score, 2),
            "faces": faces,
            "sharpness": s,
            "brightness": b
        }

    return {"brilliant": brilliant}, metadata
