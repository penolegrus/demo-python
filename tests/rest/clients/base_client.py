from __future__ import annotations

import json
from typing import Any, List, Type, TypeVar, Union

import requests
from pydantic import BaseModel, TypeAdapter

T = TypeVar("T", bound=BaseModel)


class HttpClient(requests.Session):
    """
    Универсальный HTTP-клиент с Pydantic-сериализацией и красивым логом.
    """

    def __init__(self,base_url: str = "http://localhost:8080", *, token: Union[str, None] = None) -> None:
        super().__init__()
        self._base = base_url.rstrip("/")
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        self.headers["Content-Type"] = "application/json"

    # ---------- helpers ----------
    def _request(self, method: str, path: str, *, json_body: Any = None, **kwargs) -> requests.Response:
        url = f"{self._base}{path}"

        # костыль-защита: всегда превращаем Pydantic-модель в dict
        if isinstance(json_body, BaseModel):
            json_body = json_body.model_dump(exclude_unset=True)
        elif isinstance(json_body, dict):
            json_body = {k: v for k, v in json_body.items() if v is not None}

        resp = super().request(method, url, json=json_body, **kwargs)

        # -------------- логирование --------------
        print(f"\n--- {method} {url}")
        if json_body is not None:
            body = json_body.model_dump() if isinstance(json_body, BaseModel) else json_body
            print("REQUEST\n" + json.dumps(body, ensure_ascii=False, indent=2, default=str))
        print(f"RESPONSE {resp.status_code}")
        try:
            print(json.dumps(resp.json(), ensure_ascii=False, indent=2, default=str))
        except ValueError:
            print(resp.text)
        # -----------------------------------------
        resp.raise_for_status()
        return resp

    # ---------- удобные методы без конфликта ----------
    def get_(self, path: str, *, model: Type[T] | None = None) -> T | requests.Response:
        resp = self._request("GET", path)
        return model.model_validate(resp.json()) if model else resp

    def post_(
            self,
            path: str,
            *,
            body: BaseModel | dict | None = None,
            model: Type[T] | None = None,
    ) -> Union[T] | requests.Response:
        resp = self._request("POST", path, json_body=body)
        return model.model_validate(resp.json()) if model else resp

    def put_(
            self,
            path: str,
            *,
            body: BaseModel | dict,
            model: Type[T] | None = None,
    ) -> Union[T] | requests.Response:
        resp = self._request("PUT", path, json_body=body)
        return model.model_validate(resp.json()) if model else resp

    def patch_(
            self,
            path: str,
            *,
            body: BaseModel | dict | None = None,
            model: Type[T] | None = None,
    ) -> Union[T] | requests.Response:
        resp = self._request("PATCH", path, json_body=body)
        return model.model_validate(resp.json()) if model else resp

    def delete_(self, path: str) -> requests.Response:
        return self._request("DELETE", path)

    def get_list_(self, path: str, model: Type[T]) -> List[T]:
        resp = self._request("GET", path)
        data = resp.json()
        items = data.get("content") if isinstance(data, dict) else data
        return TypeAdapter(List[model]).validate_python(items)

    # ---------- контекст-менеджер ----------
    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()