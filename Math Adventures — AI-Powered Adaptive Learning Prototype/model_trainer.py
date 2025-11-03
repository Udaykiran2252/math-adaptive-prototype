# model_trainer.py
import random
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from joblib import dump

DIFF = ["Easy","Medium","Hard"]

def synth_trajectory():
    """
    Create one synthetic transition: given (current_idx, last_acc, last_time) -> next_idx
    We encode plausible rules with some noise to simulate students.
    """
    current_idx = random.choice([0,1,2])
    last_acc = random.random()
    last_time = random.uniform(1.0, 15.0)
    # simple policy with noise
    if last_acc >= 0.8 and last_time <= 6.0 and current_idx < 2:
        next_idx = current_idx + 1
    elif last_acc <= 0.45 and current_idx > 0:
        next_idx = current_idx - 1
    else:
        # maybe keep same but sometimes move up/down
        r = random.random()
        if r < 0.1 and current_idx < 2:
            next_idx = current_idx + 1
        elif r > 0.9 and current_idx > 0:
            next_idx = current_idx - 1
        else:
            next_idx = current_idx
    # add some noise
    if random.random() < 0.05:
        next_idx = random.choice([0,1,2])
    return [current_idx, last_acc, last_time, next_idx]

def generate_dataset(n=5000):
    rows = [synth_trajectory() for _ in range(n)]
    df = pd.DataFrame(rows, columns=["current_idx","last_acc","last_time","next_idx"])
    return df

def train_and_save(path="model.pkl"):
    df = generate_dataset(8000)
    X = df[["current_idx","last_acc","last_time"]].values
    y = df["next_idx"].values
    clf = DecisionTreeClassifier(max_depth=6, random_state=42)
    clf.fit(X,y)
    dump(clf, path)
    print("Saved model to", path)

if __name__ == "__main__":
    train_and_save()
