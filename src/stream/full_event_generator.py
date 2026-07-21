import pandas as pd
import numpy as np
import random
import os
from datetime import datetime

# -------------------------------
# PATH HANDLING (IMPORTANT FIX)
# -------------------------------

# Get project root directory
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(DATA_RAW_DIR, exist_ok=True)

# -------------------------------
# RANDOM SEEDS
# -------------------------------
np.random.seed(42)
random.seed(42)

# -------------------------------
# CONSTANTS
# -------------------------------
USER_TYPES = ["student", "employee", "admin"]
DEVICES = ["mobile", "laptop", "desktop"]
OS_LIST = ["Windows", "Linux", "Android", "iOS"]
FRAUD_TYPES = ["bot", "account_takeover", "script", None]

# -------------------------------
# EVENT GENERATOR
# -------------------------------
def generate_event(user_id, user_type, fraud_type=None):
    now = datetime.now()

    if fraud_type == "bot":
        typing_speed = np.random.uniform(10, 15)
        keystroke = np.random.uniform(0.01, 0.03)
        mouse_speed = np.random.uniform(1000, 1500)
        actions = np.random.randint(120, 200)
        duration = np.random.uniform(20, 80)
        label = 1

    elif fraud_type == "account_takeover":
        typing_speed = np.random.uniform(5, 9)
        keystroke = np.random.uniform(0.04, 0.07)
        mouse_speed = np.random.uniform(600, 900)
        actions = np.random.randint(60, 120)
        duration = np.random.uniform(80, 200)
        label = 1

    elif fraud_type == "script":
        typing_speed = np.random.uniform(15, 20)
        keystroke = np.random.uniform(0.005, 0.02)
        mouse_speed = 0
        actions = np.random.randint(200, 300)
        duration = np.random.uniform(10, 40)
        label = 1

    else:  # normal user
        typing_speed = np.random.uniform(2, 4)
        keystroke = np.random.uniform(0.08, 0.15)
        mouse_speed = np.random.uniform(200, 400)
        actions = np.random.randint(20, 45)
        duration = np.random.uniform(300, 900)
        label = 0

    return {
        "user_id": user_id,
        "user_type": user_type,
        "device_type": random.choice(DEVICES),
        "os": random.choice(OS_LIST),
        "timestamp": now,
        "login_time_hour": now.hour,
        "typing_speed": round(typing_speed, 2),
        "keystroke_interval": round(keystroke, 3),
        "mouse_speed": round(mouse_speed, 1),
        "session_duration": round(duration, 1),
        "actions_per_min": actions,
        "ip_change": random.choice([0, 1]),
        "label": label
    }

# -------------------------------
# DATASET GENERATOR
# -------------------------------
def generate_dataset(n_users=50, events_per_user=25):
    records = []

    for u in range(n_users):
        user_id = f"user_{u:03d}"
        user_type = random.choice(USER_TYPES)

        for _ in range(events_per_user):
            fraud_choice = random.choices(
                FRAUD_TYPES, weights=[0.1, 0.1, 0.1, 0.7]
            )[0]

            records.append(
                generate_event(user_id, user_type, fraud_choice)
            )

    df = pd.DataFrame(records)

    output_path = os.path.join(DATA_RAW_DIR, "simulated_events.csv")
    df.to_csv(output_path, index=False)

    print(f"✅ Generated {len(df)} events")
    print(f"📁 Saved at: {output_path}")

# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    generate_dataset(n_users=50, events_per_user=25)
