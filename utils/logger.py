import json
import time
import os

LOG_PATH = "outputs/logs/forensic_log.json"

def log_event(data):
    os.makedirs("outputs/logs", exist_ok=True)

    record = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        **data
    }

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(record)

    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)