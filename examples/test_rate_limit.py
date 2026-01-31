import os
import sys
import time
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _root)

import requests

BASE = "http://127.0.0.1:8000"

def test_raw_requests():
    print("Sending 65 requests (limit is 60/min)...")
    for i in range(65):
        try:
            r = requests.get(f"{BASE}/items/?page=1&page_size=1", timeout=5)
            if r.status_code == 429:
                retry_after = r.headers.get("Retry-After", "?")
                print(f"  request {i + 1}: 429 (Retry-After: {retry_after}s)")
            else:
                print(f"  request {i + 1}: {r.status_code}")
        except Exception as e:
            print(f"  request {i + 1}: error {e}")
    print("done (raw requests)\n")

def test_client_retries():
    from client import KeyValueClient, APIError
    print("Using client (will retry on 429)...")
    client = KeyValueClient(BASE, max_retries=5)
    start = time.time()
    for i in range(65):
        try:
            client.list_items(page=1, page_size=1)
            print(f"  request {i + 1}: ok")
        except APIError as e:
            print(f"  request {i + 1}: {e.status_code} {e.message}")
            break
    elapsed = time.time() - start
    print(f"done in {elapsed:.1f}s (client with retries)\n")

if __name__ == "__main__":
    print("=== Rate limit test ===\n")
    try:
        requests.get(f"{BASE}/", timeout=2)
    except requests.exceptions.ConnectionError:
        print("API is not running. Start it first:\n  uvicorn api.main:app --reload\n")
        sys.exit(1)
    print("(API is up)\n")
    test_raw_requests()
    print("Waiting 65s so the rate limit window resets...")
    time.sleep(65)
    test_client_retries()
    print("all done")
