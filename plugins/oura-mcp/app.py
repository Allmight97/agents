"""Minimal hosted MCP proof for high-fidelity Oura access."""

from __future__ import annotations

import argparse
import asyncio
import os
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Any
from urllib.parse import urlparse

import jwt
import uvicorn
from jwt import PyJWKClient
from mcp.server import MCPServer
from mcp.server.auth.provider import AccessToken
from mcp.server.auth.settings import AuthSettings
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations
from pydantic import AnyHttpUrl
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from catalog import (
    COLLECTIONS,
    OuraCollectionName,
    RangeKind,
    catalog_payload,
    collection_spec,
)


@dataclass(frozen=True, slots=True)
class Settings:
    public_base_url: str
    auth0_issuer: str
    auth0_audience: str
    auth0_scope: str
    host: str
    port: int

    @classmethod
    def from_env(cls) -> Settings:
        public_base_url = _required("MCP_PUBLIC_BASE_URL").rstrip("/")
        parsed = urlparse(public_base_url)
        if parsed.scheme != "https" or not parsed.netloc or parsed.path:
            raise SystemExit(
                "MCP_PUBLIC_BASE_URL must be a public HTTPS origin without a path."
            )
        return cls(
            public_base_url=public_base_url,
            auth0_issuer=_required("AUTH0_ISSUER").rstrip("/") + "/",
            auth0_audience=_required("AUTH0_AUDIENCE"),
            auth0_scope=os.getenv("AUTH0_SCOPE", "oura:read"),
            host="0.0.0.0",
            port=int(os.getenv("PORT", "8000")),
        )


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Set {name} before starting the service.")
    return value


class Auth0TokenVerifier:
    """Reject any bearer token Auth0 cannot fully verify."""

    def __init__(self, settings: Settings) -> None:
        self.issuer = settings.auth0_issuer
        self.audience = settings.auth0_audience
        self.resource = settings.public_base_url
        self.keys = PyJWKClient(f"{self.issuer}.well-known/jwks.json")

    async def verify_token(self, token: str) -> AccessToken | None:
        return await asyncio.to_thread(self._verify, token)

    def _verify(self, token: str) -> AccessToken | None:
        try:
            key = self.keys.get_signing_key_from_jwt(token).key
            claims = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer,
                options={"require": ["exp", "iat", "iss", "sub"]},
            )
            scopes = claims.get("scope", "").split()
            client_id = claims.get("azp") or claims.get("client_id") or claims["sub"]
            expires_at = claims["exp"]
            if not isinstance(client_id, str) or not isinstance(expires_at, int):
                return None
        except Exception:
            return None
        return AccessToken(
            token=token,
            client_id=client_id,
            scopes=scopes,
            expires_at=expires_at,
            resource=self.resource,
            subject=claims["sub"],
            claims=claims,
        )


def build_app(settings: Settings) -> ASGIApp:
    server: MCPServer[None] = MCPServer(
        name="oura-private-data",
        title="Oura Private Data",
        description="Read-only Oura API v2 data without server-generated interpretation.",
        version="0.1.0",
        auth=AuthSettings(
            issuer_url=AnyHttpUrl(settings.auth0_issuer),
            resource_server_url=AnyHttpUrl(settings.public_base_url),
            required_scopes=[settings.auth0_scope],
        ),
        token_verifier=Auth0TokenVerifier(settings),
    )

    @server.tool(
        name="oura_catalog",
        description="List the Oura API v2 collections and their accepted query bounds.",
        annotations=ToolAnnotations(
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=False,
        ),
        structured_output=True,
    )
    async def oura_catalog() -> dict[str, Any]:
        return catalog_payload()

    @server.tool(
        name="oura_query",
        description=(
            "Retrieve one bounded Oura collection. The current proof returns synthetic data "
            "through the same native-response envelope the live source will use."
        ),
        annotations=ToolAnnotations(
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        ),
        structured_output=True,
    )
    async def oura_query(
        collection: OuraCollectionName,
        start: str | None = None,
        end: str | None = None,
        cursor: str | None = None,
        latest: bool = False,
    ) -> dict[str, Any]:
        spec = collection_spec(collection)
        validate_query(
            spec.range_kind,
            spec.supports_cursor,
            spec.supports_latest,
            start,
            end,
            cursor,
            latest,
        )
        page = 2 if cursor == "fixture-page-2" else 1
        response: dict[str, Any] = {
            "data": [
                {
                    "id": f"synthetic-{spec.name}-{page}",
                    "collection": spec.name,
                    "day": start or "2026-01-01",
                    "synthetic": True,
                }
            ]
        }
        if spec.supports_cursor and page == 1:
            response["next_token"] = "fixture-page-2"
        return {
            "collection": spec.name,
            "provenance": {
                "provider": "oura",
                "api_version": "v2",
                "endpoint": f"/v2/usercollection/{spec.path}",
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "backend": "synthetic_fixture",
            },
            "request": {"start": start, "end": end, "cursor": cursor, "latest": latest},
            "next_cursor": response.get("next_token"),
            "oura_response": response,
        }

    app = server.streamable_http_app(
        streamable_http_path="/mcp",
        stateless_http=True,
        json_response=True,
        host=settings.host,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=[urlparse(settings.public_base_url).netloc],
            allowed_origins=["https://chatgpt.com", "https://chat.openai.com"],
        ),
    )
    return PostOnlyMCP(app)


class PostOnlyMCP:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if (
            scope["type"] == "http"
            and scope["path"] == "/mcp"
            and scope["method"] not in {"POST", "OPTIONS"}
        ):
            response = JSONResponse(
                {"error": "method_not_allowed"},
                status_code=405,
                headers={"Allow": "POST, OPTIONS"},
            )
            await response(scope, receive, send)
            return
        await self.app(scope, receive, send)


def validate_query(
    range_kind: RangeKind,
    supports_cursor: bool,
    supports_latest: bool,
    start: str | None,
    end: str | None,
    cursor: str | None,
    latest: bool,
) -> None:
    if cursor and not supports_cursor:
        raise ValueError("This collection does not support cursors.")
    if latest and not supports_latest:
        raise ValueError("This collection does not support latest=true.")
    if latest and (start or end):
        raise ValueError("latest=true cannot be combined with start or end.")
    if range_kind is RangeKind.NONE:
        if start or end or latest:
            raise ValueError("This collection does not accept a date range.")
        return
    if latest:
        return
    if not start or not end:
        raise ValueError("This collection requires both start and end.")
    start_value = _parse_boundary(start, range_kind)
    end_value = _parse_boundary(end, range_kind)
    if start_value > end_value:
        raise ValueError("start must not be after end.")
    if (end_value - start_value).days > 90:
        raise ValueError("The requested range exceeds 90 days.")


def _parse_boundary(value: str, kind: RangeKind) -> datetime:
    try:
        if kind is RangeKind.DATE:
            return datetime.combine(
                date.fromisoformat(value), datetime.min.time(), tzinfo=timezone.utc
            )
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("Invalid date or datetime boundary.") from error
    if parsed.tzinfo is None:
        raise ValueError("Datetime boundaries require a timezone.")
    return parsed.astimezone(timezone.utc)


def self_check() -> None:
    assert len(COLLECTIONS) == 19
    sleep = collection_spec("sleep")
    validate_query(
        sleep.range_kind,
        sleep.supports_cursor,
        sleep.supports_latest,
        "2026-01-01",
        "2026-01-02",
        None,
        False,
    )
    try:
        validate_query(
            sleep.range_kind,
            sleep.supports_cursor,
            sleep.supports_latest,
            "2026-01-02",
            "2026-01-01",
            None,
            False,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Reverse date ranges must be rejected.")

    settings = Settings(
        public_base_url="https://oura-mcp.example.com",
        auth0_issuer="https://example.us.auth0.com/",
        auth0_audience="https://oura-mcp.example.com",
        auth0_scope="oura:read",
        host="0.0.0.0",
        port=8000,
    )
    assert asyncio.run(Auth0TokenVerifier(settings).verify_token("not-a-jwt")) is None
    build_app(settings)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        self_check()
        return
    settings = Settings.from_env()
    uvicorn.run(
        build_app(settings), host=settings.host, port=settings.port, access_log=False
    )


if __name__ == "__main__":
    main()
