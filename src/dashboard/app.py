import streamlit as st
import pandas as pd
import joblib
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

# --------------------------------------------------
# Configure Page
# --------------------------------------------------
st.set_page_config(
    page_title="Behavioral Fraud Detection Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.header("Project Details")

st.sidebar.info("""
**Version:** 1.1

**Model:** Isolation Forest

**Detection:** Behavioral Biometrics (session-level)

**ML Type:** Unsupervised Learning

**Developer:** Sai Pathi
""")

st.sidebar.header("System Status")

# --------------------------------------------------
# Load Model, Scaler, Thresholds
# --------------------------------------------------
try:
    model = joblib.load(ROOT_DIR / "models/isolation_forest.pkl")
    scaler = joblib.load(ROOT_DIR / "models/scaler.pkl")
    st.sidebar.success("Model Loaded")
    st.sidebar.success("Scaler Loaded")
except FileNotFoundError:
    st.sidebar.error("Model/scaler not found — run train_model.py first")
    st.stop()

thresholds_path = ROOT_DIR / "models/thresholds.json"
if thresholds_path.exists():
    with open(thresholds_path) as f:
        thresholds = json.load(f)
    st.sidebar.success("Thresholds Loaded")
else:
    # Fallback only if save_thresholds.py hasn't been run yet
    thresholds = {"fraud": -0.05, "suspicious": 0.0}
    st.sidebar.warning("thresholds.json not found — using fallback cutoffs")

st.sidebar.success("Dashboard Active")

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("🛡️ AI Behavioral Fraud Detection Platform")

st.caption(
    "AI-powered behavioral biometrics analysis using Isolation Forest"
)

# --------------------------------------------------
# User Inputs
# --------------------------------------------------
st.subheader("📥 Session Behavior Input")
st.caption(
    "These are session-level summary stats (mean/std over a short window "
    "of recent activity), matching what the model was trained on — not a "
    "single instantaneous reading."
)

col1, col2 = st.columns(2)

with col1:
    typing_speed_mean = st.number_input(
        "⌨️ Typing Speed — mean (chars/sec)",
        min_value=0.0, max_value=30.0, value=3.0
    )
    typing_speed_std = st.number_input(
        "⌨️ Typing Speed — std dev",
        min_value=0.0, max_value=15.0, value=0.5,
        help="Bots tend to have very low variance; humans vary more."
    )
    keystroke_interval_ms = st.number_input(
        "⌨️ Keystroke Interval — mean (ms)",
        min_value=0.0, max_value=1000.0, value=110.0
    )
    session_duration_mean = st.number_input(
        "⏱️ Session Duration — mean (sec)",
        min_value=0.0, max_value=7200.0, value=600.0
    )

with col2:
    mouse_speed_mean = st.number_input(
        "🖱️ Mouse Speed — mean",
        min_value=0.0, max_value=2000.0, value=300.0
    )
    actions_per_min_mean = st.number_input(
        "⚡ Actions Per Minute — mean",
        min_value=0.0, max_value=500.0, value=30.0
    )
    ip_change_rate = st.number_input(
        "🌐 IP Change Rate (fraction of window with a change)",
        min_value=0.0, max_value=1.0, value=0.0
    )

# --------------------------------------------------
# Prediction
# --------------------------------------------------
if st.button("🔍 Analyze User Behavior"):

    input_df = pd.DataFrame([{
        "typing_speed_mean": typing_speed_mean,
        "typing_speed_std": typing_speed_std,
        "keystroke_interval_mean": keystroke_interval_ms / 1000,
        "mouse_speed_mean": mouse_speed_mean,
        "actions_per_min_mean": actions_per_min_mean,
        "session_duration_mean": session_duration_mean,
        "ip_change_rate": ip_change_rate,
    }])

    # Match the exact column order the scaler was fit on
    input_df = input_df[scaler.feature_names_in_]

    X_scaled = scaler.transform(input_df)
    score = model.decision_function(X_scaled)[0]

    # ----------------------------------------------
    # Prediction Label — driven by thresholds.json, not hardcoded cutoffs
    # ----------------------------------------------
    if score < thresholds["fraud"]:
        prediction = "🚨 HIGH"
    elif score < thresholds["suspicious"]:
        prediction = "🟡 MEDIUM"
    else:
        prediction = "🟢 LOW"

    st.subheader("🧠 AI Analysis Report")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📊 Risk Score", f"{score:.4f}")
    with col2:
        st.metric("🎯 Threat Level", prediction)
    with col3:
        st.metric("🤖 Model", "Isolation Forest")

    st.divider()

    st.subheader("💡 AI Security Recommendation")

    if score < thresholds["fraud"]:
        st.error("""
### 🚨 High Risk Detected

**Recommended Actions**

- Block login immediately
- Enable Multi-Factor Authentication (MFA)
- Notify Security Team
- Review login activity
- Start incident investigation
""")
    elif score < thresholds["suspicious"]:
        st.warning("""
### ⚠️ Suspicious Activity

**Recommended Actions**

- Monitor current session
- Ask for OTP verification
- Record user activity
- Continue behavioral monitoring
""")
    else:
        st.success("""
### ✅ Normal Behavior

**Recommended Actions**

- User behavior appears normal
- Continue monitoring
- No immediate action required
""")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🛡️ Behavioral Fraud Detection")
with col2:
    st.caption("🤖 Isolation Forest Model")
with col3:
    st.caption("👨‍💻 Developed by Sai Pathi")

st.caption(
    "© 2026 | AI-Powered Behavioral Biometrics Fraud Detection System"
)
