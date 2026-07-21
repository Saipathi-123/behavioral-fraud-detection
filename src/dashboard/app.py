import streamlit as st
import pandas as pd
import joblib

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
st.sidebar.header("📋 Project Details")

st.sidebar.info("""
**Version:** 1.0

**Model:** Isolation Forest

**Detection:** Behavioral Biometrics

**ML Type:** Unsupervised Learning

**Developer:** Sai Pathi
""")

st.sidebar.header("⚙️ System Status")

st.sidebar.success("✅ Model Loaded")
st.sidebar.success("✅ Scaler Loaded")
st.sidebar.success("✅ Dashboard Active")

# --------------------------------------------------
# Load Model
# --------------------------------------------------
model = joblib.load("models/isolation_forest.pkl")
scaler = joblib.load("models/scaler.pkl")

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
st.subheader("📥 User Behavior Input")

col1, col2 = st.columns(2)

with col1:

    typing_speed = st.number_input(
        "⌨️ Typing Speed (chars/sec)",
        min_value=0.0,
        max_value=30.0,
        value=8.0
    )

    keystroke_interval = st.number_input(
        "⌨️ Keystroke Interval (ms)",
        min_value=0.0,
        max_value=1000.0,
        value=120.0
    )

    session_duration = st.number_input(
        "⏱️ Session Duration (sec)",
        min_value=0.0,
        max_value=7200.0,
        value=600.0
    )

with col2:

    mouse_speed = st.number_input(
        "🖱️ Mouse Speed",
        min_value=0.0,
        max_value=2000.0,
        value=500.0
    )

    actions_per_min = st.number_input(
        "⚡ Actions Per Minute",
        min_value=0.0,
        max_value=500.0,
        value=25.0
    )

    ip_change_rate = st.number_input(
        "🌐 IP Change Rate",
        min_value=0.0,
        max_value=10.0,
        value=0.0
    )

# --------------------------------------------------
# Prediction
# --------------------------------------------------
if st.button("🔍 Analyze User Behavior"):

    input_df = pd.DataFrame([{
        "typing_speed": typing_speed,
        "keystroke_interval": keystroke_interval / 1000,
        "mouse_speed": mouse_speed,
        "actions_per_min": actions_per_min,
        "session_duration": session_duration,
        "ip_change": ip_change_rate
    }])

    X_scaled = scaler.transform(input_df)

    score = model.decision_function(X_scaled)[0]

    # ----------------------------------------------
    # Prediction Label
    # ----------------------------------------------
    if score < -0.05:
        prediction = "🚨 HIGH"
    elif score < 0:
        prediction = "🟡 MEDIUM"
    else:
        prediction = "🟢 LOW"

    # ----------------------------------------------
    # AI Analysis
    # ----------------------------------------------
    st.subheader("🧠 AI Analysis Report")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📊 Risk Score",
            f"{score:.4f}"
        )

    with col2:
        st.metric(
            "🎯 Threat Level",
            prediction
        )

    with col3:
        st.metric(
            "🤖 Model",
            "Isolation Forest"
        )

    st.divider()

    # ----------------------------------------------
    # AI Recommendation
    # ----------------------------------------------
    st.subheader("💡 AI Security Recommendation")

    if score < -0.05:

        st.error("""
### 🚨 High Risk Detected

**Recommended Actions**

- Block login immediately
- Enable Multi-Factor Authentication (MFA)
- Notify Security Team
- Review login activity
- Start incident investigation
""")

    elif score < 0:

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