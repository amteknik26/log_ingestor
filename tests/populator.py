import requests
import json
from concurrent.futures import ThreadPoolExecutor

def send_log(log_data):
    response = requests.post("http://127.0.0.1:3000/ingest", json=log_data)
    return response.json()

# Read from file
with open("sample-logs.json", "r") as file:
    logs = json.load(file)

# send logs in parallel
with ThreadPoolExecutor() as executor:
    results = list(executor.map(send_log, logs))

# Print 
for i, result in enumerate(results, 1):
    print(f"Result {i}: {result}")

