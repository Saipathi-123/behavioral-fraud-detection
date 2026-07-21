# AI Behavioral Fraud Detection Platform

An end-to-end, real-time behavioral biometrics system that detects account takeover and suspicious user activity using unsupervised machine learning.

The platform continuously evaluates features such as typing speed, mouse velocity, keystroke intervals, session duration, and IP change frequency to flag anomalies using an Isolation Forest pipeline.

---

## Table of Contents

- [Key Features](#key-features)
- [Machine Learning & Data Pipeline](#machine-learning--data-pipeline)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dashboard Features](#dashboard-features)
- [Future Enhancements](#future-enhancements)
- [Author](#author)

---

## Key Features

| Feature | Description |
|---|---|
| **Unsupervised Anomaly Detection** | Powered by Scikit-Learn's `Isolation Forest` algorithm |
| **Behavioral Biometrics Pipeline** | Feature extraction engine for keystroke dynamics, mouse movement speed, session time, and network signals |
| **Real-Time Streaming Simulation** | Live event generator paired with a streaming detector to flag incoming events instantly |
| **Dynamic Risk Calibration** | Custom score thresholds categorized into Low, Medium, and High threat levels |
| **Interactive Streamlit Dashboard** | Live visualizer displaying real-time security reports, threat classifications, and actionable mitigation steps |

---

## Machine Learning & Data Pipeline

- **Algorithm:** Isolation Forest (`scikit-learn`)
- **Learning Type:** Unsupervised anomaly detection

**Extracted behavioral features:**

- **Typing dynamics** — speed (WPM / characters per second) and keystroke intervals (latency between key presses)
- **Mouse dynamics** — speed, acceleration, and movement vectors
- **Session / network activity** — actions per minute (APM), session duration, and IP change frequency rate

---

## System Architecture

The system operates as a modular machine learning pipeline divided into data processing, model inference, real-time streaming, and interactive visualization layers.

```text
              ┌────────────────────────────────────┐
              │   Simulated Events Logging Engine  │
              │  (data/raw/simulated_events.csv)   │
              └──────────────────┬─────────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────┐
              │     Feature Engineering Pipeline   │
              │(src/features/feature_engineering.py│
              │  - Keystrokes, Mouse, APM, IP      │
              └──────────────────┬─────────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────┐
              │     Model Training & Calibration   │
              │    (src/models/train_model.py)     │
              │  - StandardScaler & IsolationForest│
              └──────────────────┬─────────────────┘
                                 │
                 ┌───────────────┴────────────────┐
                 ▼                                ▼
   ┌─────────────────────────────┐    ┌─────────────────────────────┐
   │  Real-Time Streaming Engine │    │  Streamlit Security Portal  │
   │ (src/stream/realtime_       │    │   (src/dashboard/app.py)    │
   │   fraud_detector.py)        │    │ -Interactive UI & metrics   │
   │ - Live anomaly scoring      │    │ -Threat level classification│
   └─────────────────────────────┘    └─────────────────────────────┘
```

---

## Project Structure

```text
behavioral-fraud-detection/
│
├── data/
│   ├── raw/                          # Simulated event logs
│   └── processed/                    # Engineered behavioral features
│
├── models/
│   ├── isolation_forest.pkl          # Trained Isolation Forest model
│   ├── scaler.pkl                    # Feature scaling parameters
│   ├── score_thresholds.pkl          # Custom anomaly score cutoffs
│   └── thresholds.json               # Exported risk rules
│
├── src/
│   ├── dashboard/
│   │   └── app.py                    # Streamlit dashboard UI
│   ├── features/
│   │   └── feature_engineering.py    # Feature extraction pipeline
│   ├── models/
│   │   └── train_model.py            # Model training script
│   ├── scripts/
│   │   ├── inspect_scores.py         # Score distribution analysis
│   │   └── save_thresholds.py        # Threshold config saver
│   └── stream/
│       ├── full_event_generator.py       # Live event simulator
│       └── realtime_fraud_detector.py    # Real-time detection engine
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/behavioral-fraud-detection.git
cd behavioral-fraud-detection
pip install -r requirements.txt
```

## Usage

### 1. Feature Extraction & Model Training

Run the following steps in order from the project root:

```bash
# 1. Process raw behavioral logs into a feature matrix
python src/features/feature_engineering.py

# 2. Train the Isolation Forest model and save artifacts
python src/models/train_model.py

# 3. Save score thresholds
python src/scripts/save_thresholds.py
```

### 2. Run the Application

```bash
streamlit run src/dashboard/app.py
```

---

## Dashboard Features

- Professional sidebar navigation
- Live system status
- AI-generated analysis report
- Threat level detection
- Security recommendations
- Responsive dashboard layout

---

## Future Enhancements

- [ ] Explainable AI (XAI)
- [ ] Live login monitoring
- [ ] Database integration
- [ ] User authentication
- [ ] Risk score visualization
- [ ] Downloadable security reports
- [ ] Real-time streaming analysis

---

## Author

**Sai Pathi**

AI & Machine Learning Enthusiast
