import time
import random
import joblib
import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR / "src"))

# Reuse the SAME event generator used to build the training data, instead
# of drawing from unrelated uniform ranges. The old version here generated
# noise that didn't resemble any of the trained classes (normal/bot/ATO/
# script), so the model flagged nearly everything as fraud regardless of
# input — this made the "real-time" demo meaningless.
from stream.full_event_generator import generate_event, USER_TYPES, FRAUD_TYPES

# --------------------------------------------------
# Load trained model & scaler
# --------------------------------------------------
MODEL_PATH = ROOT_DIR / "models/isolation_forest.pkl"
SCALER_PATH = ROOT_DIR / "models/scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("Model & Scaler Loaded Successfully\n")


# --------------------------------------------------
# Simulate a short session of raw events for one user, then aggregate
# --------------------------------------------------
def simulate_session_events(n_events):
    user_id = "demo_user"
    user_type = random.choice(USER_TYPES)
    # Weighted like the training data: mostly normal, some fraud types
    fraud_choice = random.choices(FRAUD_TYPES, weights=[0.1, 0.1, 0.1, 0.7])[0]
    return [generate_event(user_id, user_type, fraud_choice) for _ in range(n_events)]


def aggregate_session(events):
    df = pd.DataFrame(events)

    session_duration_mean = df["session_duration"].mean()
    actions_per_min_mean = df["actions_per_min"].mean()

    features = {
        "typing_speed_mean": df["typing_speed"].mean(),
        "typing_speed_std": df["typing_speed"].std(ddof=0),
        "keystroke_interval_mean": df["keystroke_interval"].mean(),
        "mouse_speed_mean": df["mouse_speed"].mean(),
        "actions_per_min_mean": actions_per_min_mean,
        "session_duration_mean": session_duration_mean,
        "ip_change_rate": df["ip_change"].mean(),
    }

    feature_df = pd.DataFrame([features])

    # Force same feature order the scaler was fit on
    feature_df = feature_df[scaler.feature_names_in_]

    return feature_df


# --------------------------------------------------
# Real-time fraud detection loop
# --------------------------------------------------
def realtime_fraud_detection(max_iterations=None):
    print("Real-Time Fraud Detection Started\n")

    i = 0
    while max_iterations is None or i < max_iterations:
        events = simulate_session_events(random.randint(6, 15))

        feature_df = aggregate_session(events)
        scaled = scaler.transform(feature_df)
        prediction = model.predict(scaled)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if prediction[0] == -1:
            print(f"🚨 [{timestamp}] FRAUD DETECTED")
        else:
            print(f"✅ [{timestamp}] Normal Activity")

        time.sleep(2)
        i += 1


# --------------------------------------------------
# Run
# --------------------------------------------------
if __name__ == "__main__":
    realtime_fraud_detection()
