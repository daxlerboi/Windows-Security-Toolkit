import joblib
import pandas as pd
import joblib

model = joblib.load(
    "ml/anomaly_model.pkl"
)

scaler = joblib.load(
    "ml/scaler.pkl"
)

def predict_anomaly(features):
    X = pd.DataFrame([features])
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)
    return prediction[0]
