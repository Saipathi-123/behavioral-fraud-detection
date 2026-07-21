import joblib
import pandas as pd

MODEL_PATH = "models/isolation_forest.pkl"
SCALER_PATH = "models/scaler.pkl"
DATA_PATH = "data/processed/behavior_features.csv"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

df = pd.read_csv(DATA_PATH)
df = df[scaler.feature_names_in_]

scaled = scaler.transform(df)
scores = model.decision_function(scaled)

print("\n📊 Isolation Forest Score Distribution")
print("------------------------------------")
print("Min  :", scores.min())
print("25%  :", pd.Series(scores).quantile(0.25))
print("50%  :", pd.Series(scores).quantile(0.50))
print("75%  :", pd.Series(scores).quantile(0.75))
print("Max  :", scores.max())
