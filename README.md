# 🛡️ AI Behavioral Fraud Detection Platform

An end-to-end, real-time behavioral biometrics system that detects account takeover and suspicious user activity using **Unsupervised Machine Learning**. 

The platform continuously evaluates features such as typing speed, mouse velocity, keystroke intervals, session duration, and IP change frequency to flag anomalies using an Isolation Forest pipeline.

---

## 🚀 Features

- **Unsupervised Anomaly Detection**: Powered by Scikit-Learn's Isolation Forest algorithm.
- **Behavioral Biometrics Pipeline**: Engine that extracts keystroke dynamics, movement speed, and network/session signals.
- **Real-Time Streaming Engine**: Simulated live event generator feeding events directly to the detection model.
- **Dynamic Risk Thresholding**: Score calibration with custom thresholds stored for low, medium, and high threat levels.
- **Interactive Streamlit Dashboard**: Live security report visualizer, threat level classification, and actionable AI security recommendations.

---

## 🧠 Machine Learning & Data Pipeline

* **Algorithm**: Isolation Forest (`scikit-learn`)
* **Learning Style**: Unsupervised Machine Learning
* **Extracted Features**:
  * Typing Speed (WPM / Characters per second)
  * Keystroke Intervals (Latency between presses)
  * Mouse Velocity & Acceleration
  * Actions Per Minute (APM)
  * Session Duration
  * IP Change Frequency Rate

---

## 📂 Project Structure

```text
behavioral-fraud-detection/
│
├── data/
│   ├── raw/                  # Simulated event logs
│   └── processed/            # Engineered behavioral features
│
├── models/
│   ├── isolation_forest.pkl  # Trained Isolation Forest model
│   ├── scaler.pkl            # Feature scaling parameters
│   ├── score_thresholds.pkl  # Custom anomaly score cutoffs
│   └── thresholds.json       # Exported risk rules
│
├── src/
│   ├── dashboard/
│   │   └── app.py            # Streamlit dashboard UI
│   ├── features/
│   │   └── feature_engineering.py  # Feature extraction pipeline
│   ├── models/
│   │   └── train_model.py    # Model training script
│   ├── scripts/
│   │   ├── inspect_scores.py # Score distribution analysis
│   │   └── save_thresholds.py# Threshold config saver
│   └── stream/
│       ├── full_event_generator.py   # Live event simulator
│       └── realtime_fraud_detector.py # Real-time detection engine
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone [https://github.com/YOUR_USERNAME/behavioral-fraud-detection.git](https://github.com/YOUR_USERNAME/behavioral-fraud-detection.git)
cd behavioral-fraud-detection
pip install -r requirements.txt
```
# Feature Extraction & Model Training
Navigate into the project
```
1. Process raw behavioral logs into feature matrix
python src/features/feature_engineering.py

2. Train the Isolation Forest model and save artifacts
python src/models/train_model.py

3. Save score thresholds
python src/scripts/save_thresholds.py
```
Run the application
```bash
streamlit run src/dashboard/app.py
```
---
# 📊 Dashboard Features

- Professional Sidebar
- System Status
- AI Analysis Report
- Threat Level Detection
- Security Recommendations
- Responsive Dashboard Layout

---

# 🔮 Future Enhancements

- Explainable AI (XAI)
- Live Login Monitoring
- Database Integration
- User Authentication
- Risk Score Visualization
- Downloadable Security Reports
- Real-time Streaming Analysis

---

# 👨‍💻 Author

**Sai Pathi**

AI & Machine Learning Enthusiast

---

# ⭐ If you found this project useful, consider giving it a Star.
