import pandas as pd
import joblib
import json
import numpy as np
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = ROOT_DIR / "data/raw/simulated_events.csv"
MODEL_PATH = ROOT_DIR / "models/isolation_forest.pkl"
SCALER_PATH = ROOT_DIR / "models/scaler.pkl"
THRESHOLD_PATH = ROOT_DIR / "models/thresholds.json"

FEATURES = [
    "typing_speed",
    "keystroke_interval",
    "mouse_speed",
    "actions_per_min",
    "session_duration",
    "ip_change"
]

df = pd.read_csv(DATA_PATH)
X = df[FEATURES]

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

print("✅ Thresholds saved successfully")
print("Fraud threshold     :", thresholds["fraud"])
print("Suspicious threshold:", thresholds["suspicious"])
