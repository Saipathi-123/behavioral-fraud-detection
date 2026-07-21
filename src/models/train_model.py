import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from pathlib import Path

# 🔹 Resolve project root dynamically
ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = ROOT_DIR / "data/raw/simulated_events.csv"
MODEL_PATH = ROOT_DIR / "models/isolation_forest.pkl"
SCALER_PATH = ROOT_DIR / "models/scaler.pkl"

FEATURES = [
    "typing_speed",
    "keystroke_interval",
    "mouse_speed",
    "actions_per_min",
    "session_duration",
    "ip_change"
]

# Load data
df = pd.read_csv(DATA_PATH)

X = df[FEATURES]

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Isolation Forest (balanced sensitivity)
model = IsolationForest(
    n_estimators=300,
    contamination=0.08,
    random_state=42
)
model.fit(X_scaled)

# Save artifacts
(ROOT_DIR / "models").mkdir(exist_ok=True)
joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

print("✅ Model retrained successfully")
print("📁 Saved to:", MODEL_PATH)
