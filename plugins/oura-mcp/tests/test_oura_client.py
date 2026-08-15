from __future__ import annotations

import time

import httpx
import pytest
from cryptography.fernet import Fernet

from oura_mcp.catalog import collection_spec
from oura_mcp.oura import OuraClient
from oura_mcp.token_store import EncryptedTokenStore


@pytest.mark.asyncio
async def test_expired_token_refreshes_then_queries_without_persisting_response(tmp_path) -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/oauth/token":
            return httpx.Response(
                200,
                json={
                    "access_token": "new-access",
                    "refresh_token": "new-refresh",
                    "expires_in": 3600,
                },
            )
        assert request.headers["Authorization"] == "Bearer new-access"
        return httpx.Response(
            200,
            json={"data": [{"id": "oura-native-id"}], "next_token": "next-page"},
        )

    token_path = tmp_path / "token.enc"
    store = EncryptedTokenStore(token_path, Fernet.generate_key().decode("ascii"))
    await store.save(
        {
            "access_token": "expired-access",
            "refresh_token": "old-refresh",
            "expires_at": int(time.time()) - 1,
        }
    )
    client = OuraClient(
        api_base_url="https://api.ouraring.test/v2/usercollection",
        token_url="https://api.ouraring.test/oauth/token",
        client_id="client-id",
        client_secret="client-secret",
        token_store=store,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )

    result = await client.query(
        collection_spec("daily_sleep"),
        start="2026-01-01",
        end="2026-01-02",
        cursor=None,
        fields=None,
        latest=False,
    )

    assert result == {"data": [{"id": "oura-native-id"}], "next_token": "next-page"}
    assert [request.url.path for request in requests] == [
        "/oauth/token",
        "/v2/usercollection/daily_sleep",
    ]
    persisted = await store.load()
    assert persisted is not None
    assert persisted["refresh_token"] == "new-refresh"
    assert b"oura-native-id" not in token_path.read_bytes()
