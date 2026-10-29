import cv2
import os
from config import KEYFRAME_FOLDER

def extract_keyframes(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    count = 0
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % fps == 0:
            name = f"frame_{count}.jpg"
            path = os.path.join(KEYFRAME_FOLDER, name)
            cv2.imwrite(path, frame)
            frames.append(name)

        count += 1

    cap.release()
    return frames
