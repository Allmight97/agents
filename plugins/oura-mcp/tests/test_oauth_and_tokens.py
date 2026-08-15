from __future__ import annotations

import json

import httpx
import pytest
from cryptography.fernet import Fernet

from oura_mcp.oauth import OAuthError, OAuthStateSigner, OuraOAuth
from oura_mcp.token_store import EncryptedTokenStore


def test_signed_oauth_state_rejects_tampering() -> None:
    signer = OAuthStateSigner("state-secret-longer-than-thirty-two-bytes")
    state = signer.issue()

    signer.verify(state)
    with pytest.raises(OAuthError, match="state validation failed"):
        signer.verify(f"{state}changed")


@pytest.mark.asyncio
async def test_token_store_encrypts_and_survives_reopen(tmp_path) -> None:
    path = tmp_path / "oauth-token.enc"
    key = Fernet.generate_key().decode("ascii")
    token = {
        "access_token": "private-access-token",
        "refresh_token": "private-refresh-token",
        "expires_at": 4_102_444_800,
    }

    await EncryptedTokenStore(path, key).save(token)

    assert b"private-access-token" not in path.read_bytes()
    assert await EncryptedTokenStore(path, key).load() == token
    assert path.stat().st_mode & 0o777 == 0o600
    with pytest.raises((UnicodeDecodeError, json.JSONDecodeError)):
        json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.asyncio
async def test_oauth_callback_exchanges_code_and_persists_rotating_credential(tmp_path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "https://api.ouraring.test/oauth/token"
        assert b"code=authorization-code" in request.content
        return httpx.Response(
            200,
            json={
                "access_token": "access",
                "refresh_token": "refresh",
                "expires_in": 3600,
            },
        )

    signer = OAuthStateSigner("state-secret-longer-than-thirty-two-bytes")
    store = EncryptedTokenStore(tmp_path / "oauth-token.enc", Fernet.generate_key().decode("ascii"))
    oauth = OuraOAuth(
        authorize_url="https://cloud.ouraring.test/oauth/authorize",
        token_url="https://api.ouraring.test/oauth/token",
        client_id="client-id",
        client_secret="client-secret",
        redirect_uri="https://mcp.example.test/oauth/oura/callback",
        scopes="daily personal",
        state_signer=signer,
        token_store=store,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )
    state = signer.issue()

    await oauth.exchange_callback(code="authorization-code", state=state)

    persisted = await store.load()
    assert persisted is not None
    assert persisted["access_token"] == "access"
    assert persisted["refresh_token"] == "refresh"
