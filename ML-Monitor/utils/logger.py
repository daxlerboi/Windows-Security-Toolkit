from datetime import datetime
import os

LOG_DIR = "data/alerts"
LOG_FILE = "data/alerts/alerts.log"

os.makedirs(
    LOG_DIR,
    exist_ok=True
)

def log_alert(message):
    timestamp = str(
        datetime.now()
    )

    entry = f"[{timestamp}] {message}\n"

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(entry)
