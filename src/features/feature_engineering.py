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

# This is the single source of truth for column names/order used by the
# model, scaler, thresholds, dashboard, and streaming detector. If you add
# or rename a feature here, update it everywhere else too.
FEATURE_COLUMNS = [
    "typing_speed_mean",
    "typing_speed_std",
    "keystroke_interval_mean",
    "mouse_speed_mean",
    "actions_per_min_mean",
    "session_duration_mean",
    "ip_change_rate",
]


# -------------------------------
# FEATURE ENGINEERING FUNCTION
# -------------------------------
def generate_behavior_features(df, window_size=5):
    """
    Slide a window over each user's own event history and summarize it into
    session-level behavioral features. Windows are built per user_id so a
    window never mixes events from two different people.
    """
    features = []

    for user_id, user_df in df.groupby("user_id", sort=False):
        user_df = user_df.reset_index(drop=True)

        for i in range(window_size, len(user_df) + 1):
            window = user_df.iloc[i - window_size:i]

            features.append({
                "user_id": user_id,
                "typing_speed_mean": window["typing_speed"].mean(),
                "typing_speed_std": window["typing_speed"].std(ddof=0),
                "keystroke_interval_mean": window["keystroke_interval"].mean(),
                "mouse_speed_mean": window["mouse_speed"].mean(),
                "actions_per_min_mean": window["actions_per_min"].mean(),
                "session_duration_mean": window["session_duration"].mean(),
                "ip_change_rate": window["ip_change"].mean(),
                # Label reflects the most recent event in the window (the
                # one actually being scored "right now"), not whether any
                # event in the window was ever fraudulent. Using max() here
                # would label ~83% of windows as fraud once any one of the
                # 5 events is fraudulent, which defeats the point of
                # anomaly detection.
                "label": window["label"].iloc[-1],
            })

    return pd.DataFrame(features)


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    df = pd.read_csv(RAW_DATA_PATH)
    feature_df = generate_behavior_features(df)

    feature_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Feature dataset created")
    print(f"Saved at: {OUTPUT_PATH}")
    print(f"Total rows: {len(feature_df)}")
    print(f"Fraud-window rate: {feature_df['label'].mean():.3f}")
