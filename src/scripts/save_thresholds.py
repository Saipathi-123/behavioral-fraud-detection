import pandas as pd
import joblib
import json
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from features.feature_engineering import FEATURE_COLUMNS

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = ROOT_DIR / "data/processed/behavior_features.csv"
MODEL_PATH = ROOT_DIR / "models/isolation_forest.pkl"
SCALER_PATH = ROOT_DIR / "models/scaler.pkl"
THRESHOLD_PATH = ROOT_DIR / "models/thresholds.json"

df = pd.read_csv(DATA_PATH)
X = df[FEATURE_COLUMNS]

scaler = joblib.load(SCALER_PATH)
model = joblib.load(MODEL_PATH)

X_scaled = scaler.transform(X)
scores = model.decision_function(X_scaled)

thresholds = {
    "fraud": float(np.percentile(scores, 5)),
    "suspicious": float(np.percentile(scores, 25))
}

with open(THRESHOLD_PATH, "w") as f:
    json.dump(thresholds, f, indent=4)

print("Thresholds saved successfully")
print("Fraud threshold     :", thresholds["fraud"])
print("Suspicious threshold:", thresholds["suspicious"])
