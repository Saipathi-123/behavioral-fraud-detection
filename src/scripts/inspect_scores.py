import joblib
import pandas as pd
from pathlib import Path
import sys

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

scaled = scaler.transform(X)
scores = model.decision_function(scaled)

print("\nIsolation Forest Score Distribution")
print("------------------------------------")
print("Min  :", scores.min())
print("25%  :", pd.Series(scores).quantile(0.25))
print("50%  :", pd.Series(scores).quantile(0.50))
print("75%  :", pd.Series(scores).quantile(0.75))
print("Max  :", scores.max())
