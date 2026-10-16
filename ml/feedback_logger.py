import csv
from datetime import datetime

def log_feedback(image, platform, action):
    with open("ml/user_feedback.csv", "a", newline="") as f:
        csv.writer(f).writerow([image, platform, action, datetime.now()])
