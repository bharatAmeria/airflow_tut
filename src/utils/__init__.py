import json
from datetime import datetime

def log_to_file(event: str, status: str, file_path="tracking_log.json"):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "status": status
    }
    with open(file_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


# # logger_utils.py

# import sqlite3
# import json
# from datetime import datetime

# DB_FILE = "airflow_tracking.db"
# LOG_FILE = "tracking_log.json"

# def log_to_db(event: str, status: str, metadata: dict = None):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
#                         timestamp TEXT,
#                         event TEXT,
#                         status TEXT,
#                         metadata TEXT
#                     )''')
#     cursor.execute(
#         "INSERT INTO logs (timestamp, event, status, metadata) VALUES (?, ?, ?, ?)",
#         (datetime.now().isoformat(), event, status, json.dumps(metadata or {}))
#     )
#     conn.commit()
#     conn.close()

# def log_to_file(event: str, status: str, metadata: dict = None):
#     entry = {
#         "timestamp": datetime.now().isoformat(),
#         "event": event,
#         "status": status,
#         "metadata": metadata or {}
#     }
#     with open(LOG_FILE, "a") as f:
#         f.write(json.dumps(entry) + "\n")

