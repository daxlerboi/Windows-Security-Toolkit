import pandas as pd
import time

from collector.process_collector import collect_processes
from utils.feature_extractor import extract_features

dataset = []

print("Collecting baseline data...")

for _ in range(25):

    processes = collect_processes()

    for process in processes:

        features = extract_features(process)

        dataset.append(features)

    time.sleep(2)

df = pd.DataFrame(dataset)

df.to_csv(
    "data/baseline/baseline_data.csv",
    index=False
)

print("Baseline collection completed.")