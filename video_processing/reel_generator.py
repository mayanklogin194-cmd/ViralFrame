import os
from moviepy.editor import VideoFileClip
from config import REEL_FOLDER

def generate_reel(video_path):
    video = VideoFileClip(video_path)

    # Take first 20 sec for demo
    clip = video.subclip(0, min(20, video.duration))

    w, h = clip.size
    target_ratio = 9 / 16

    if w / h > target_ratio:
        new_w = int(h * target_ratio)
        x1 = (w - new_w) // 2
        clip = clip.crop(x1=x1, width=new_w)

    clip = clip.resize(height=1920)

    output = os.path.join(REEL_FOLDER, "insta_reel.mp4")
    clip.write_videofile(output, codec="libx264", audio_codec="aac")

    return output
