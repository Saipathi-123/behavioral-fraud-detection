import pandas as pd
import os

# -------------------------------
# PATH HANDLING
# -------------------------------
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "simulated_events.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

OUTPUT_PATH = os.path.join(PROCESSED_DIR, "behavior_features.csv")

# -------------------------------
# FEATURE ENGINEERING FUNCTION
# -------------------------------
def generate_behavior_features(df, window_size=5):
    features = []

    for i in range(window_size, len(df)):
        window = df.iloc[i - window_size:i]

        features.append({
            "typing_speed_mean": window["typing_speed"].mean(),
            "typing_speed_std": window["typing_speed"].std(),
            "keystroke_interval_mean": window["keystroke_interval"].mean(),
            "mouse_speed_mean": window["mouse_speed"].mean(),
            "actions_per_min_mean": window["actions_per_min"].mean(),
            "session_duration_mean": window["session_duration"].mean(),
            "ip_change_rate": window["ip_change"].mean(),
            "label": window["label"].max()
        })

    return pd.DataFrame(features)

# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    df = pd.read_csv(RAW_DATA_PATH)
    feature_df = generate_behavior_features(df)

    feature_df.to_csv(OUTPUT_PATH, index=False)

    print(f"✅ Feature dataset created")
    print(f"📁 Saved at: {OUTPUT_PATH}")
    print(f"📊 Total rows: {len(feature_df)}")
