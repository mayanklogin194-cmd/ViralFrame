import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

def train_from_feedback(metadata):
    df = pd.read_csv("ml/user_feedback.csv")
    if len(df) < 10:
        return None

    X, y = [], []
    for _, r in df.iterrows():
        if r["image"] in metadata:
            m = metadata[r["image"]]
            X.append([m["final_score"], len(m["suggestions"]), m["faces"]])
            y.append(1 if r["action"] in ["downloaded", "uploaded"] else 0)

    model = RandomForestRegressor(n_estimators=150)
    model.fit(X, y)

    with open("ml/virality_model.pkl", "wb") as f:
        pickle.dump(model, f)
