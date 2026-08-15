"""Hosted Oura OAuth callback and signed, short-lived state values."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Any
from urllib.parse import urlencode

import httpx

from .token_store import EncryptedTokenStore


class OAuthError(RuntimeError):
    pass


class OAuthStateSigner:
    def __init__(self, secret: str, *, ttl_seconds: int = 600) -> None:
        if len(secret.encode("utf-8")) < 32:
            raise OAuthError("OURA_STATE_SECRET must contain at least 32 bytes.")
        self._secret = secret.encode("utf-8")
        self._ttl_seconds = ttl_seconds

    def issue(self) -> str:
        payload = json.dumps(
            {"issued_at": int(time.time()), "nonce": secrets.token_urlsafe(24)},
            separators=(",", ":"),
        ).encode("utf-8")
        encoded = _urlsafe(payload)
        signature = _urlsafe(hmac.digest(self._secret, encoded.encode("ascii"), hashlib.sha256))
        return f"{encoded}.{signature}"

    def verify(self, value: str) -> None:
        try:
            encoded, supplied_signature = value.split(".", 1)
            expected_signature = _urlsafe(
                hmac.digest(self._secret, encoded.encode("ascii"), hashlib.sha256)
            )
            if not hmac.compare_digest(supplied_signature, expected_signature):
                raise OAuthError("Oura OAuth state validation failed.")
            payload = json.loads(_unurlsafe(encoded))
            issued_at = payload["issued_at"]
        except (ValueError, KeyError, json.JSONDecodeError, UnicodeDecodeError) as error:
            raise OAuthError("Oura OAuth state validation failed.") from error
        if not isinstance(issued_at, int) or not 0 <= time.time() - issued_at <= self._ttl_seconds:
            raise OAuthError("Oura OAuth state expired. Generate a new authorization URL.")


class OuraOAuth:
    def __init__(
        self,
        *,
        authorize_url: str,
        token_url: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: str,
        state_signer: OAuthStateSigner,
        token_store: EncryptedTokenStore,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._authorize_url = authorize_url
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._scopes = scopes
        self._state_signer = state_signer
        self._token_store = token_store
        self._http_client = http_client

    def authorization_url(self) -> str:
        query = urlencode(
            {
                "response_type": "code",
                "client_id": self._client_id,
                "redirect_uri": self._redirect_uri,
                "scope": self._scopes,
                "state": self._state_signer.issue(),
            }
        )
        return f"{self._authorize_url}?{query}"

    async def exchange_callback(self, *, code: str, state: str) -> None:
        self._state_signer.verify(state)
        client = self._http_client or httpx.AsyncClient(timeout=30)
        owns_client = self._http_client is None
        try:
            response = await client.post(
                self._token_url,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "redirect_uri": self._redirect_uri,
                },
            )
            response.raise_for_status()
            token = normalized_token_response(response.json())
            await self._token_store.save(token)
        except (httpx.HTTPError, ValueError, TypeError) as error:
            raise OAuthError("Oura authorization code exchange failed.") from error
        finally:
            if owns_client:
                await client.aclose()


def normalized_token_response(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise OAuthError("Oura returned an unexpected token response.")
    access_token = payload.get("access_token")
    refresh_token = payload.get("refresh_token")
    expires_in = payload.get("expires_in")
    if not isinstance(access_token, str) or not isinstance(refresh_token, str):
        raise OAuthError("Oura did not return access and refresh tokens.")
    if not isinstance(expires_in, int | float):
        raise OAuthError("Oura did not return a numeric token expiry.")
    obtained_at = int(time.time())
    return {**payload, "obtained_at": obtained_at, "expires_at": obtained_at + int(expires_in)}


def _urlsafe(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _unurlsafe(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)
