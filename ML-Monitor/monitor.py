import time

from collector.process_collector import (
    collect_processes
)

from collector.persistence_collector import (
    collect_persistence
)

from utils.feature_extractor import (
    extract_features
)

from utils.logger import log_alert

from rules.heuristic_engine import (
    calculate_risk,
    persistence_risk
)

from ml.detect import predict_anomaly

print("=== Smart Cybersecurity Monitor ===")

while True:

    processes = collect_processes()

    for process in processes:

        try:

            features = extract_features(
                process
            )

            prediction = predict_anomaly(
                features
            )

            risk = calculate_risk(
                process
            )

            if prediction == -1 or risk >= 5:

                alert = (
                    f"Suspicious Process | "
                    f"{process['name']} | "
                    f"PID={process['pid']} | "
                    f"Risk={risk}"
                )

                print("\n[!] " + alert)

                log_alert(alert)

        except:
            continue

    persistence_entries = (
        collect_persistence()
    )

    for entry in persistence_entries:

        try:

            risk = persistence_risk(
                entry
            )

            if risk >= 5:

                alert = (
                    f"Persistence Detected | "
                    f"{entry['name']} | "
                    f"Risk={risk}"
                )

                print("\n[!] " + alert)

                log_alert(alert)

        except:
            continue

    time.sleep(5)