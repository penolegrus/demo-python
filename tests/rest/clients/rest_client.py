import requests
from typing import Optional, Type, TypeVar, List, Any
from pydantic import BaseModel, parse_obj_as
import json

T = TypeVar('T', bound=BaseModel)

class RestClient:
    def __init__(self, base_url: str = "http://localhost:8080", token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _log_request(self, method: str, url: str, headers: dict, payload: Any = None):
        print(f"\n--- REQUEST ---\n{method} {url}\nHeaders: {headers}")
        if payload is not None:
            try:
                print(f"Payload: {json.dumps(payload, ensure_ascii=False, indent=2, default=str)}")
            except Exception:
                print(f"Payload: {payload}")

    def _log_response(self, resp: requests.Response):
        print(f"--- RESPONSE ---\nStatus: {resp.status_code}")
        try:
            body = resp.json()
            print("Body:")
            print(json.dumps(body, ensure_ascii=False, indent=2, default=str))
        except Exception:
            print(f"Body: {resp.text}")
        print()

    def get(self, path: str, model: Type[T]) -> T:
        url = f"{self.base_url}{path}"
        headers = self._headers()
        self._log_request("GET", url, headers)
        resp = requests.get(url, headers=headers)
        self._log_response(resp)
        resp.raise_for_status()
        return model.parse_obj(resp.json())

    def get_list(self, path: str, model: Type[T], paginated: bool = False) -> List[T]:
        url = f"{self.base_url}{path}"
        headers = self._headers()
        self._log_request("GET", url, headers)
        resp = requests.get(url, headers=headers)
        self._log_response(resp)
        resp.raise_for_status()
        data = resp.json()
        if paginated:
            data = data.get("content", [])
        return parse_obj_as(List[model], data)

    def post(self, path: str, body: Any, model: Optional[Type[T]] = None) -> Optional[T]:
        url = f"{self.base_url}{path}"
        headers = self._headers()
        self._log_request("POST", url, headers, body)
        resp = requests.post(url, json=body, headers=headers)
        self._log_response(resp)
        resp.raise_for_status()
        if model:
            return model.parse_obj(resp.json())
        return None

    def put(self, path: str, body: Any, model: Optional[Type[T]] = None) -> Optional[T]:
        url = f"{self.base_url}{path}"
        headers = self._headers()
        self._log_request("PUT", url, headers, body)
        resp = requests.put(url, json=body, headers=headers)
        self._log_response(resp)
        resp.raise_for_status()
        if model:
            return model.parse_obj(resp.json())
        return None

    def delete(self, path: str) -> requests.Response:
        url = f"{self.base_url}{path}"
        headers = self._headers()
        self._log_request("DELETE", url, headers)
        resp = requests.delete(url, headers=headers)
        self._log_response(resp)
        resp.raise_for_status()
        return resp

    def patch(self, path: str, body: Any = None, model: Optional[Type[T]] = None) -> Optional[T]:
        url = f"{self.base_url}{path}"
        headers = self._headers()
        self._log_request("PATCH", url, headers, body)
        resp = requests.patch(url, json=body, headers=headers)
        self._log_response(resp)
        resp.raise_for_status()
        if model:
            return model.parse_obj(resp.json())
        return None 