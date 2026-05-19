import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

df = pd.read_csv(
    "data/baseline/baseline_data.csv"
)

X = df[[
    'cpu',
    'memory',
    'suspicious_path'
]]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

model = IsolationForest(
    contamination=0.02,
    random_state=42
)

model.fit(X_scaled)

joblib.dump(
    model,
    "ml/anomaly_model.pkl"
)

joblib.dump(
    scaler,
    "ml/scaler.pkl"
)

print("Model trained successfully.")
