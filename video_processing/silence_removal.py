import os
import librosa
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from config import PROCESSED_FOLDER

SILENCE_THRESHOLD = 0.02  # Slightly higher to be safe


def remove_silence(video_path):
    video = VideoFileClip(video_path)
    audio = video.audio

    # Save temp audio to analyze
    temp_audio = "temp_silence.wav"
    audio.write_audiofile(temp_audio, logger=None)

    y, sr = librosa.load(temp_audio)
    # Get non-silent intervals
    intervals = librosa.effects.split(y, top_db=25)  # top_db 25 is a good default

    clips = []
    for start_i, end_i in intervals:
        start_t = start_i / sr
        end_t = end_i / sr
        clips.append(video.subclip(start_t, end_t))

    if not clips:
        video.close()
        os.remove(temp_audio)
        return video_path

    final = concatenate_videoclips(clips)
    output = os.path.join(PROCESSED_FOLDER, "cleaned.mp4")
    final.write_videofile(output, codec="libx264", audio_codec="aac", logger=None)

    # Cleanup
    video.close()
    final.close()
    if os.path.exists(temp_audio):
        os.remove(temp_audio)

    return output