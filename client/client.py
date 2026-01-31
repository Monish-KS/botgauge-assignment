import random
import time
import requests
from typing import Optional


class APIError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[requests.Response] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class KeyValueClient:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
        timeout: float = 10.0,
        max_retries: int = 5,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.session = requests.Session()

    def _do_request(self, method: str, path: str, json_data: Optional[dict] = None, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        try:
            resp = self.session.request(
                method,
                url,
                json=json_data,
                timeout=self.timeout,
                **kwargs,
            )
        except requests.exceptions.Timeout:
            raise APIError("request timed out")
        except requests.exceptions.ConnectionError as e:
            raise APIError(f"connection failed: {e}")
        return resp

    def _request(self, method: str, path: str, json_data: Optional[dict] = None, **kwargs) -> requests.Response:
        last_resp = None
        last_error = None
        for attempt in range(self.max_retries):
            try:
                resp = self._do_request(method, path, json_data=json_data, **kwargs)
            except APIError as e:
                last_error = e
                if attempt == self.max_retries - 1:
                    raise
                wait = self.base_delay * (2 ** attempt)
                wait = min(wait, self.max_delay)
                jitter = random.uniform(0, wait * 0.2)
                time.sleep(wait + jitter)
                continue
            if resp.status_code == 429:
                last_resp = resp
                if attempt == self.max_retries - 1:
                    raise APIError("rate limit exceeded", status_code=429, response=resp)
                try:
                    wait = float(resp.headers.get("Retry-After", self.base_delay * (2 ** attempt)))
                except (ValueError, TypeError):
                    wait = self.base_delay * (2 ** attempt)
                wait = min(wait, self.max_delay)
                jitter = random.uniform(0, wait * 0.2)
                time.sleep(wait + jitter)
                continue
            if resp.status_code >= 500:
                last_resp = resp
                if attempt == self.max_retries - 1:
                    raise APIError(resp.text or "server error", status_code=resp.status_code, response=resp)
                wait = self.base_delay * (2 ** attempt)
                wait = min(wait, self.max_delay)
                jitter = random.uniform(0, wait * 0.2)
                time.sleep(wait + jitter)
                continue
            return resp
        if last_error is not None:
            raise last_error
        raise APIError("request failed", response=last_resp)

    def create_item(self, key: str, value: str) -> dict:
        resp = self._request("POST", "/items/", json_data={"key": key, "value": value})
        if resp.status_code == 409:
            return self.get_item(key)
        if resp.status_code != 200:
            raise APIError(resp.text or "create failed", status_code=resp.status_code, response=resp)
        return resp.json()

    def get_item(self, key: str) -> dict:
        resp = self._request("GET", f"/items/{key}")
        if resp.status_code == 404:
            raise APIError("item not found", status_code=404, response=resp)
        if resp.status_code != 200:
            raise APIError(resp.text or "get failed", status_code=resp.status_code, response=resp)
        return resp.json()

    def update_item(self, key: str, value: str) -> dict:
        resp = self._request("PUT", f"/items/{key}", json_data={"value": value})
        if resp.status_code == 404:
            raise APIError("item not found", status_code=404, response=resp)
        if resp.status_code != 200:
            raise APIError(resp.text or "update failed", status_code=resp.status_code, response=resp)
        return resp.json()

    def delete_item(self, key: str) -> dict:
        resp = self._request("DELETE", f"/items/{key}")
        if resp.status_code == 404:
            raise APIError("item not found", status_code=404, response=resp)
        if resp.status_code != 200:
            raise APIError(resp.text or "delete failed", status_code=resp.status_code, response=resp)
        return resp.json()

    def list_items(self, page: int = 1, page_size: int = 10) -> dict:
        resp = self._request("GET", f"/items/?page={page}&page_size={page_size}")
        if resp.status_code != 200:
            raise APIError(resp.text or "list failed", status_code=resp.status_code, response=resp)
        return resp.json()
