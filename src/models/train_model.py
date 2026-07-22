import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from features.feature_engineering import FEATURE_COLUMNS

# Resolve project root dynamically
ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = ROOT_DIR / "data/processed/behavior_features.csv"
MODEL_PATH = ROOT_DIR / "models/isolation_forest.pkl"
SCALER_PATH = ROOT_DIR / "models/scaler.pkl"

# Load session-level features (produced by src/features/feature_engineering.py)
df = pd.read_csv(DATA_PATH)

X = df[FEATURE_COLUMNS]

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# The `label` column exists only for evaluation (see
# src/scripts/evaluate_model.py) — the model itself is trained unsupervised,
# but we use the empirical fraud rate to set a sane `contamination` instead
# of guessing. IsolationForest requires contamination in (0, 0.5].
empirical_fraud_rate = df["label"].mean()
contamination = min(max(round(empirical_fraud_rate, 2), 0.01), 0.5)

model = IsolationForest(
    n_estimators=300,
    contamination=contamination,
    random_state=42
)
model.fit(X_scaled)

# Save artifacts
(ROOT_DIR / "models").mkdir(exist_ok=True)
joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

print("Model retrained successfully")
print("Empirical fraud rate in training windows:", round(empirical_fraud_rate, 3))
print("Contamination used:", contamination)
print("Saved to:", MODEL_PATH)
