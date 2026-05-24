# Windows Security Toolkit

[![Windows](https://img.shields.io/badge/Windows-supported-0078D4?logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Python](https://img.shields.io/badge/Python-used-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Batch](https://img.shields.io/badge/Batch-tools-222222)](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands)
[![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![scikit--learn](https://img.shields.io/badge/scikit--learn-used-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)

Developer: `daxler_boi`

A hybrid Windows security and monitoring toolkit combining:

* Batch-based security utilities
* Python telemetry collection
* Machine learning anomaly detection
* Heuristic risk analysis
* Real-time monitoring dashboard

---

## Overview

Windows Security Toolkit is designed to monitor and analyze Windows systems using both traditional detection logic and machine learning-based behavioral analysis.

The project combines:

* classic Windows inspection tools
* real-time process telemetry
* anomaly detection
* suspicious behavior analysis
* alert logging
* monitoring dashboards

---

## Features

### Batch Security Tools

#### `SecurityTool.bat`

Menu-driven Windows security utility.

Features:

* network inspection
* active connection analysis
* startup entry inspection
* scheduled task inspection
* firewall checks
* process analysis
* system intelligence reporting

---

#### `BasicRATScan.bat`

Focused RAT and suspicious activity scanner.

Features:

* suspicious connection detection
* port analysis
* remote IP inspection
* risk scoring
* suspicious process hunting

---

## Machine Learning Monitor

The `ML-Monitor/` project provides:

* process telemetry collection
* baseline learning
* anomaly detection
* heuristic risk scoring
* persistence inspection
* live monitoring
* alert logging
* Streamlit dashboard

---

## Folder Structure

```text
Windows Security Toolkit/
├── Batch Tools/
│   ├── SecurityTool.bat
│   └── BasicRATScan.bat
│
├── ML-Monitor/
│   ├── collector/
│   │   ├── __init__.py
│   │   ├── process_collector.py
│   │   ├── persistence_collector.py
│   │   ├── network_collector.py
│   │   └── __pycache__/
│   │
│   ├── dashboard/
│   │   ├── __init__.py
│   │   └── live_dashboard.py
│   │
│   ├── data/
│   │   ├── baseline/
│   │   │   └── baseline_data.csv
│   │   │
│   │   └── alerts/
│   │       └── alerts.log
│   │
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── train_model.py
│   │   ├── detect.py
│   │   ├── anomaly_model.pkl
│   │   ├── scaler.pkl
│   │   └── __pycache__/
│   │
│   ├── rules/
│   │   ├── __init__.py
│   │   ├── heuristic_engine.py
│   │   ├── suspicious_paths.py
│   │   └── __pycache__/
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── feature_extractor.py
│   │   ├── hash_utils.py
│   │   ├── logger.py
│   │   └── __pycache__/
│   │
│   ├── collect_baseline.py
│   ├── monitor.py
│   └── requirements.txt
│
├── assets/
│   └── dashboard_screenshot.png
│
├── Batch Tools/
│   └── (batch processing utilities)
│
├── .git/
│
├── .gitignore
├── LICENSE
├── README.md
├── logs/
├── comments-backup/
└── venv/ (Python virtual environment)
```

---

## Requirements

Install dependencies:

```bash
pip install -r ML-Monitor/requirements.txt
```

---

## Python Libraries Used

* psutil
* pandas
* numpy
* scikit-learn
* joblib
* streamlit
* plotly
* rich

---

## Installation

### Clone Repository

```bash
git clone https://github.com/daxlerboi/Windows-Security-Toolkit
```

---

### Enter Project Directory

```bash
cd "Windows Security Toolkit"
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

---

### Activate Virtual Environment

#### CMD

```cmd
venv\Scripts\activate
```

#### PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

---

### Install Dependencies

```bash
pip install -r ML-Monitor/requirements.txt
```

---

## Full Execution Flow

## Step 1 — Enter ML Monitor

```bash
cd ML-Monitor
```

---

## Step 2 — Collect Baseline Data

```bash
python collect_baseline.py
```

This collects normal system behavior data.

The generated dataset is saved to:

```text
data/baseline/baseline_data.csv
```

Recommended during collection:

* web browsing
* coding
* gaming
* multitasking
* normal PC usage

---

## Step 3 — Train Machine Learning Model

```bash
python ml/train_model.py
```

This creates:

```text
ml/anomaly_model.pkl
ml/scaler.pkl
```

The model uses:

* Isolation Forest
* feature scaling
* anomaly detection

---

## Step 4 — Start Live Monitoring

```bash
python monitor.py
```

The monitor performs:

* process inspection
* anomaly prediction
* heuristic risk scoring
* alert generation
* suspicious path detection

Alerts are saved to:

```text
data/alerts/alerts.log
```

---

## Step 5 — Launch Dashboard

Open another terminal:

```bash
cd dashboard
```

Then:

```bash
streamlit run live_dashboard.py
```

Dashboard URL:

```text
http://localhost:8501
```

---

## Main Code Components

## Baseline Collector

File:

```text
collect_baseline.py
```

Main purpose:

* collect process telemetry
* build normal behavior dataset
* generate ML training data

Example:

```python
processes = collect_processes()

for process in processes:

    features = extract_features(process)

    writer.writerow(features)

    time.sleep(2)
```

---

## Feature Extraction

File:

```text
utils/feature_extractor.py
```

Converts raw telemetry into ML features.

Example:

```python
return {
    "cpu": process.get("cpu", 0),
    "memory": process.get("memory", 0),
    "suspicious_path": suspicious_path
}
```

---

## Model Training

File:

```text
ml/train_model.py
```

Example:

```python
df = pd.read_csv(
    "data/baseline/baseline_data.csv"
)

X = df[['cpu', 'memory', 'suspicious_path']]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

model = IsolationForest(
    contamination=0.02,
    random_state=42
)

model.fit(X_scaled)
```

This trains the anomaly detection model.

---

## Live Detection

File:

```text
ml/detect.py
```

Example:

```python
model = joblib.load(
    "ml/anomaly_model.pkl"
)

scaler = joblib.load(
    "ml/scaler.pkl"
)

prediction = model.predict(X_scaled)
```

---

## Heuristic Risk Engine

File:

```text
rules/heuristic_engine.py
```

The heuristic engine adds risk points for:

* suspicious executable paths
* high CPU usage
* abnormal RAM usage
* suspicious process names

Example:

```python
if cpu > 80:
    score += 3

if memory > 30:
    score += 3
```

---

## Live Monitoring Engine

File:

```text
monitor.py
```

Main monitoring loop:

```python
processes = collect_processes()

for process in processes:

    features = extract_features(process)

    prediction = predict_anomaly(features)

    risk = calculate_risk(process)

    if prediction == -1 or risk >= 5:

        alert = (
            f"Suspicious Process | "
            f"{process['name']} | "
            f"PID={process['pid']}"
        )

        log_alert(alert)
```

This combines:

* ML detection
* heuristic analysis
* alert logging

---

## Dashboard

File:

```text
dashboard/live_dashboard.py
```

Built using:

* Streamlit
* Pandas
* Plotly

Dashboard includes:

* live charts
* process metrics
* monitoring status
* activity tables
* alert display

---

## Detection Logic

The toolkit combines two detection systems.

### Machine Learning Detection

Isolation Forest detects unusual process behavior patterns.

Examples:

* abnormal CPU spikes
* strange memory usage
* uncommon executable behavior

---

### Heuristic Detection

Rule-based logic detects:

* suspicious directories
* LOLBins
* persistence indicators
* abnormal resource usage

---

## Future Improvements

Planned features:

* live network telemetry
* Windows Event Log analysis
* registry persistence scanning
* YARA integration
* real-time dashboard metrics
* malware hash lookup
* quarantine engine
* Discord/Telegram alerts
* GPU telemetry monitoring

---

## Notes

* Designed primarily for Windows systems
* Some scans may require administrator privileges
* Uses `psutil` heavily for telemetry collection
* Isolation Forest is an unsupervised ML algorithm
* Dashboard currently uses simulated chart values and can later connect to real telemetry

---

## Contribution

Contributions and improvements are welcome.

Potential improvement areas:

* stronger ML features
* improved telemetry collection
* dashboard enhancements
* detection tuning
* persistence coverage
* SIEM integration

---

## Contact

Developer: `daxler_boi`

Windows security research and machine learning-assisted monitoring toolkit.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
