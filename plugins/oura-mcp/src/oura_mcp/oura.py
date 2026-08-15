"""Live Oura API v2 client."""

from __future__ import annotations

import time
from typing import Any

import anyio
import httpx

from .catalog import CollectionSpec, RangeKind
from .oauth import OAuthError, normalized_token_response
from .token_store import EncryptedTokenStore


class OuraAPIError(RuntimeError):
    pass


class OuraClient:
    def __init__(
        self,
        *,
        api_base_url: str,
        token_url: str,
        client_id: str,
        client_secret: str,
        token_store: EncryptedTokenStore,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._api_base_url = api_base_url
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._token_store = token_store
        self._http_client = http_client
        self._refresh_lock = anyio.Lock()

    def token_configured(self) -> bool:
        return self._token_store.exists()

    async def query(
        self,
        spec: CollectionSpec,
        *,
        start: str | None,
        end: str | None,
        cursor: str | None,
        fields: list[str] | None,
        latest: bool,
    ) -> dict[str, Any]:
        access_token = await self._access_token()
        parameters: dict[str, str] = {}
        if spec.range_kind is RangeKind.DATE:
            parameters.update(start_date=start or "", end_date=end or "")
        elif spec.range_kind is RangeKind.DATETIME and not latest:
            parameters.update(start_datetime=start or "", end_datetime=end or "")
        if cursor:
            parameters["next_token"] = cursor
        if fields:
            parameters["fields"] = ",".join(fields)
        if latest:
            parameters["latest"] = "true"

        client = self._http_client or httpx.AsyncClient(timeout=30)
        owns_client = self._http_client is None
        try:
            response = await client.get(
                f"{self._api_base_url}/{spec.path}",
                params=parameters or None,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if response.status_code == 401:
                access_token = await self._access_token(force_refresh=True)
                response = await client.get(
                    f"{self._api_base_url}/{spec.path}",
                    params=parameters or None,
                    headers={"Authorization": f"Bearer {access_token}"},
                )
            response.raise_for_status()
            payload = response.json()
        except httpx.HTTPStatusError as error:
            status = error.response.status_code
            if status == 429:
                raise OuraAPIError(
                    "Oura rate-limited this request. Retry after a short delay."
                ) from error
            if status in {401, 403}:
                raise OuraAPIError(
                    f"Oura rejected access to {spec.name}. Reauthorize or check the granted scope."
                ) from error
            raise OuraAPIError(f"Oura returned HTTP {status} for {spec.name}.") from error
        except (httpx.HTTPError, ValueError) as error:
            raise OuraAPIError(f"Oura could not return {spec.name} data.") from error
        finally:
            if owns_client:
                await client.aclose()
        if not isinstance(payload, dict):
            raise OuraAPIError(f"Oura returned an unexpected response shape for {spec.name}.")
        return payload

    async def _access_token(self, *, force_refresh: bool = False) -> str:
        async with self._refresh_lock:
            token = await self._token_store.load()
            if token is None:
                raise OuraAPIError("Oura authorization is not configured yet.")
            expires_at = token.get("expires_at", 0)
            expired = not isinstance(expires_at, int | float) or expires_at <= time.time() + 60
            if force_refresh or expired:
                token = await self._refresh(token)
            access_token = token.get("access_token")
            if not isinstance(access_token, str):
                raise OuraAPIError("The stored Oura credential has no access token.")
            return access_token

    async def _refresh(self, token: dict[str, Any]) -> dict[str, Any]:
        refresh_token = token.get("refresh_token")
        if not isinstance(refresh_token, str):
            raise OuraAPIError("The stored Oura credential has no refresh token. Reauthorize.")
        client = self._http_client or httpx.AsyncClient(timeout=30)
        owns_client = self._http_client is None
        try:
            response = await client.post(
                self._token_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                },
            )
            response.raise_for_status()
            refreshed = normalized_token_response(response.json())
            await self._token_store.save(refreshed)
            return refreshed
        except (httpx.HTTPError, OAuthError, ValueError) as error:
            raise OuraAPIError("Oura token refresh failed. Reauthorize the account.") from error
        finally:
            if owns_client:
                await client.aclose()
