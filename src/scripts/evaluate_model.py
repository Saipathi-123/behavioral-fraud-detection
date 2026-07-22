"""
Offline evaluation only — NOT used anywhere in training.

The simulated data carries ground-truth fraud labels because it's
synthetic. A real deployment usually won't have these, which is exactly
why this project trains unsupervised (IsolationForest never sees `label`
during fit). This script exists purely so the model's real-world
usefulness isn't just asserted — it's checked, using the labels that
already exist in the data but were previously unused anywhere in the repo.
"""

import joblib
import pandas as pd
from pathlib import Path
import sys
from sklearn.metrics import classification_report, confusion_matrix

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from features.feature_engineering import FEATURE_COLUMNS

ROOT_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = ROOT_DIR / "models/isolation_forest.pkl"
SCALER_PATH = ROOT_DIR / "models/scaler.pkl"
DATA_PATH = ROOT_DIR / "data/processed/behavior_features.csv"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

df = pd.read_csv(DATA_PATH)
X = df[FEATURE_COLUMNS]
y_true = df["label"]

X_scaled = scaler.transform(X)
raw_pred = model.predict(X_scaled)          # -1 = anomaly, 1 = normal
y_pred = (raw_pred == -1).astype(int)        # 1 = flagged as fraud

print("Confusion matrix (rows=actual, cols=predicted) [normal, fraud]:")
print(confusion_matrix(y_true, y_pred))
print()
print(classification_report(y_true, y_pred, target_names=["normal", "fraud"]))
