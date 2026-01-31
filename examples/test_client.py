import os
import sys
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _root)

from client import KeyValueClient, APIError

def main():
    client = KeyValueClient("http://127.0.0.1:8000")
    key = "test_key"
    client.create_item(key, "first value")
    print("create ok")
    item = client.get_item(key)
    print("get ok:", item["value"])
    client.update_item(key, "second value")
    item = client.get_item(key)
    print("update ok:", item["value"])
    data = client.list_items(page=1, page_size=5)
    print("list ok:", len(data["items"]), "items, total", data["total"])
    client.delete_item(key)
    print("delete ok")
    try:
        client.get_item(key)
    except APIError as e:
        if e.status_code == 404:
            print("404 after delete ok")
        else:
            raise
    print("all ok")

if __name__ == "__main__":
    main()
