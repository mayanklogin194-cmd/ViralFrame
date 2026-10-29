import json
import os

PROFILE_PATH = "ml/creator_profile.json"

DEFAULT_PROFILE = {
    "emotion_weight": 1.0,
    "motion_weight": 1.0,
    "clean_weight": 1.0
}

def load_profile():
    if not os.path.exists(PROFILE_PATH):
        return DEFAULT_PROFILE
    with open(PROFILE_PATH, "r") as f:
        return json.load(f)

def update_profile(suggestions):
    profile = load_profile()
    if "🔥 Best for Instagram Post" in suggestions:
        profile["emotion_weight"] += 0.05
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f)
