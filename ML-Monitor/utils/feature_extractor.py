import os

SUSPICIOUS_PATHS = [
    "temp",
    "appdata",
    "roaming"
]

def extract_features(process):
    path = str(process['exe']).lower()

    suspicious_path = 0

    for bad in SUSPICIOUS_PATHS:
        if bad in path:
            suspicious_path = 1

    features = {
        "cpu": process['cpu'],
        "memory": process['memory'],
        "suspicious_path": suspicious_path
    }

    return features
