"""Tests for the real HTTP transport wrappers."""

from __future__ import annotations

import builtins
import types
from typing import Any

import pytest
import requests

from mailchannels.exceptions import AsyncClientNotConfigured
from mailchannels.http_client import RequestsClient
from mailchannels.http_client_async import HTTPXClient


class _FakeRequestsResponse:
    """Fake response object returned by the requests transport tests."""

    def __init__(
        self,
        *,
        status_code: int = 200,
        data: Any = None,
        text: str = "{}",
        headers: dict[str, str] | None = None,
        json_error: ValueError | None = None,
    ) -> None:
        """Create a fake requests response."""
        self.status_code = status_code
        self._data = data
        self.text = text
        self.headers = headers or {}
        self._json_error = json_error

    def json(self) -> Any:
        """Return JSON data or raise the configured JSON decode error."""
        if self._json_error is not None:
            raise self._json_error
        return self._data


class _FakeHTTPXResponse:
    """Fake response object returned by the httpx transport tests."""

    def __init__(
        self,
        *,
        status_code: int = 200,
        data: Any = None,
        text: str = "{}",
        headers: dict[str, str] | None = None,
        json_error: ValueError | None = None,
    ) -> None:
        """Create a fake httpx response."""
        self.status_code = status_code
        self._data = data
        self.text = text
        self.headers = headers or {}
        self._json_error = json_error

    def json(self) -> Any:
        """Return JSON data or raise the configured JSON decode error."""
        if self._json_error is not None:
            raise self._json_error
        return self._data


def test_requests_client_passes_request_arguments_and_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It forwards request arguments to requests with the configured timeout."""
    calls: list[dict[str, Any]] = []

    def fake_request(
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json: dict[str, Any] | None,
        params: dict[str, Any] | None,
        timeout: float,
    ) -> _FakeRequestsResponse:
        """Record the request arguments and return a JSON response."""
        calls.append(
            {
                "method": method,
                "url": url,
                "headers": headers,
                "json": json,
                "params": params,
                "timeout": timeout,
            }
        )
        return _FakeRequestsResponse(
            status_code=201,
            data={"ok": True},
            text='{"ok": true}',
            headers={"X-Request-ID": "req_sync"},
        )

    monkeypatch.setattr(requests, "request", fake_request)
    client = RequestsClient(timeout=12.5)

    response = client.request(
        "POST",
        "https://api.example.test/send",
        headers={"X-Api-Key": "test-key"},
        json={"hello": "world"},
        params={"dry-run": "true"},
    )

    assert calls == [
        {
            "method": "POST",
            "url": "https://api.example.test/send",
            "headers": {"X-Api-Key": "test-key"},
            "json": {"hello": "world"},
            "params": {"dry-run": "true"},
            "timeout": 12.5,
        }
    ]
    assert response.status_code == 201
    assert response.data == {"ok": True}
    assert response.text == '{"ok": true}'
    assert response.headers == {"X-Request-ID": "req_sync"}


def test_requests_client_handles_non_json_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It normalizes non-JSON responses with data set to None."""
    monkeypatch.setattr(
        requests,
        "request",
        lambda *args, **kwargs: _FakeRequestsResponse(
            status_code=204,
            text="",
            headers={"X-Request-ID": "req_empty"},
            json_error=requests.JSONDecodeError("bad json", "", 0),
        ),
    )

    response = RequestsClient().request(
        "DELETE",
        "https://api.example.test/webhook",
        headers={},
    )

    assert response.status_code == 204
    assert response.data is None
    assert response.text == ""
    assert response.headers == {"X-Request-ID": "req_empty"}


async def test_httpx_client_passes_request_arguments_and_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It forwards async request arguments through httpx.AsyncClient."""
    calls: list[dict[str, Any]] = []

    class FakeAsyncClient:
        """Minimal async context manager matching httpx.AsyncClient."""

        def __init__(self, *, timeout: float) -> None:
            """Record the configured timeout."""
            self.timeout = timeout

        async def __aenter__(self) -> FakeAsyncClient:
            """Enter the async context manager."""
            return self

        async def __aexit__(self, *args: object) -> None:
            """Exit the async context manager."""

        async def request(
            self,
            method: str,
            url: str,
            *,
            headers: dict[str, str],
            json: dict[str, Any] | None,
            params: dict[str, Any] | None,
        ) -> _FakeHTTPXResponse:
            """Record the request arguments and return a JSON response."""
            calls.append(
                {
                    "method": method,
                    "url": url,
                    "headers": headers,
                    "json": json,
                    "params": params,
                    "timeout": self.timeout,
                }
            )
            return _FakeHTTPXResponse(
                status_code=202,
                data={"queued": True},
                text='{"queued": true}',
                headers={"X-Request-ID": "req_async"},
            )

    monkeypatch.setitem(
        __import__("sys").modules,
        "httpx",
        types.SimpleNamespace(AsyncClient=FakeAsyncClient),
    )
    client = HTTPXClient(timeout=7.5)

    response = await client.request(
        "POST",
        "https://api.example.test/send-async",
        headers={"X-Api-Key": "test-key"},
        json={"hello": "world"},
        params={"dry-run": "true"},
    )

    assert calls == [
        {
            "method": "POST",
            "url": "https://api.example.test/send-async",
            "headers": {"X-Api-Key": "test-key"},
            "json": {"hello": "world"},
            "params": {"dry-run": "true"},
            "timeout": 7.5,
        }
    ]
    assert response.status_code == 202
    assert response.data == {"queued": True}
    assert response.text == '{"queued": true}'
    assert response.headers == {"X-Request-ID": "req_async"}


async def test_httpx_client_handles_non_json_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It normalizes async non-JSON responses with data set to None."""

    class FakeAsyncClient:
        """Minimal async context manager returning a non-JSON response."""

        def __init__(self, *, timeout: float) -> None:
            """Accept the configured timeout."""

        async def __aenter__(self) -> FakeAsyncClient:
            """Enter the async context manager."""
            return self

        async def __aexit__(self, *args: object) -> None:
            """Exit the async context manager."""

        async def request(self, *args: object, **kwargs: object) -> _FakeHTTPXResponse:
            """Return a response whose JSON parser fails."""
            return _FakeHTTPXResponse(
                status_code=204,
                text="",
                headers={"X-Request-ID": "req_async_empty"},
                json_error=ValueError("bad json"),
            )

    monkeypatch.setitem(
        __import__("sys").modules,
        "httpx",
        types.SimpleNamespace(AsyncClient=FakeAsyncClient),
    )

    response = await HTTPXClient().request(
        "DELETE",
        "https://api.example.test/webhook",
        headers={},
    )

    assert response.status_code == 204
    assert response.data is None
    assert response.text == ""
    assert response.headers == {"X-Request-ID": "req_async_empty"}


async def test_httpx_client_missing_httpx_dependency_raises_configuration_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It raises a helpful configuration error when httpx is unavailable."""
    original_import = builtins.__import__

    def fake_import(name: str, *args: object, **kwargs: object) -> Any:
        """Simulate httpx not being installed."""
        if name == "httpx":
            raise ImportError("No module named httpx")
        return original_import(name, *args, **kwargs)

    monkeypatch.delitem(__import__("sys").modules, "httpx", raising=False)
    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(AsyncClientNotConfigured) as error:
        await HTTPXClient().request(
            "GET",
            "https://api.example.test/usage",
            headers={},
        )

    assert error.value.code == "AsyncClientNotConfigured"
    assert error.value.error_type == "AsyncClientNotConfigured"
    assert 'pip install "mailchannels[async]"' in str(error.value)
