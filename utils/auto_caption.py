import shutil
import os
from config import REEL_FOLDER

def add_captions(video_path):
    output = os.path.join(REEL_FOLDER, "captioned_reel.mp4")
    shutil.copy(video_path, output)
    return output
