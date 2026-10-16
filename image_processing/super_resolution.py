import cv2
import os
from config import BASE_DIR

MODEL_PATH = os.path.join(BASE_DIR, "models", "ESPCN_x4.pb")


def super_hd_4x(image):
    if not os.path.exists(MODEL_PATH):
        # Fallback to Lanczos interpolation if model is missing
        return cv2.resize(image, None, fx=4, fy=4, interpolation=cv2.INTER_LANCZOS4)

    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(MODEL_PATH)
    sr.setModel("espcn", 4)

    return sr.upsample(image)