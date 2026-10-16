def predict_virality(meta):
    score = (
        meta["sharpness"] * 0.3 +
        meta["brightness"] * 0.1 +
        meta["faces"] * 20
    )
    return min(round(score, 2), 100)
