import requests
import time

BASE_URL = "http://localhost:8000"
ENDPOINTS = [
    "/ping",
    "/submit",
    "/error",
    "/status",
    "/version",
    "/dataattempt"
]

DELAY = 2  # seconds between each full round of requests

def call_endpoints_forever():
    while True:
        for endpoint in ENDPOINTS:
            url = f"{BASE_URL}{endpoint}"
            try:
                response = requests.get(url)
                print(f"[{response.status_code}] GET {endpoint}")
                print(response.text)
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Failed to call {endpoint}: {e}")
            print("-" * 50)
        time.sleep(DELAY)

if __name__ == "__main__":
    try:
        call_endpoints_forever()
    except KeyboardInterrupt:
        print("\nStopped by user.")