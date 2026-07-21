import time
import random
import joblib
import pandas as pd
from datetime import datetime

# --------------------------------------------------
# Load trained model & scaler
# --------------------------------------------------
MODEL_PATH = "models/isolation_forest.pkl"
SCALER_PATH = "models/scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("✅ Model & Scaler Loaded Successfully\n")

# --------------------------------------------------
# Generate raw behavioral event
# --------------------------------------------------
def generate_raw_event():
    return {
        "typing_speed": random.uniform(2, 12),          # chars/sec
        "mouse_speed": random.uniform(100, 1200),       # px/sec
        "keystroke_interval": random.uniform(0.05, 0.5),
        "session_duration": random.uniform(30, 1800),   # seconds
        "ip_change": random.choice([0, 1])
    }

# --------------------------------------------------
# Aggregate events → EXACT training features
# --------------------------------------------------
def aggregate_session(events):
    df = pd.DataFrame(events)

    session_duration_mean = df["session_duration"].mean()
    actions_per_min = len(df) / max(session_duration_mean / 60, 1)

    features = {
        "typing_speed_mean": df["typing_speed"].mean(),
        "typing_speed_std": df["typing_speed"].std(ddof=0),
        "mouse_speed_mean": df["mouse_speed"].mean(),
        "keystroke_interval_mean": df["keystroke_interval"].mean(),
        "session_duration_mean": session_duration_mean,
        "ip_change_rate": df["ip_change"].mean(),
        "actions_per_min_mean": actions_per_min
    }

    feature_df = pd.DataFrame([features])

    # 🔐 FORCE SAME FEATURE ORDER AS TRAINING
    feature_df = feature_df[scaler.feature_names_in_]

    return feature_df

# --------------------------------------------------
# Real-time fraud detection loop
# --------------------------------------------------
def realtime_fraud_detection():
    print("🚀 Real-Time Fraud Detection Started\n")

    while True:
        # simulate a short user session
        events = [generate_raw_event() for _ in range(random.randint(6, 15))]

        feature_df = aggregate_session(events)
        scaled = scaler.transform(feature_df)
        prediction = model.predict(scaled)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if prediction[0] == -1:
            print(f"🚨 [{timestamp}] FRAUD DETECTED")
        else:
            print(f"✅ [{timestamp}] Normal Activity")

        time.sleep(2)

# --------------------------------------------------
# Run
# --------------------------------------------------
if __name__ == "__main__":
    realtime_fraud_detection()
