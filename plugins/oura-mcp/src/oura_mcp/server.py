"""MCP tool registration and HTTP application construction."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from mcp.server import MCPServer
from mcp.server.auth.provider import TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations
from pydantic import AnyHttpUrl
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from .auth import Auth0TokenVerifier
from .catalog import OuraCollectionName, catalog_payload, collection_spec
from .oauth import OAuthError, OAuthStateSigner, OuraOAuth
from .oura import OuraClient
from .settings import Settings
from .source import FixtureOuraSource, LiveOuraSource, OuraSource, validate_query
from .token_store import EncryptedTokenStore


def build_server(
    settings: Settings,
    *,
    source: OuraSource | None = None,
    token_verifier: TokenVerifier | None = None,
) -> MCPServer[None]:
    source, oura_oauth = _source_from_settings(settings) if source is None else (source, None)
    verifier = token_verifier or Auth0TokenVerifier(
        issuer=settings.auth0_issuer,
        audience=settings.auth0_audience,
        resource=settings.public_base_url,
    )
    server: MCPServer[None] = MCPServer(
        name="oura-private-data",
        title="Oura Private Data",
        description="Read-only access to Oura API v2 data without server-generated interpretation.",
        version="0.1.0",
        instructions=(
            "Call oura_catalog before the first query when the available Oura collections or "
            "required bounds are unknown. Return Oura-native values faithfully; do not imply "
            "medical diagnosis or invent unavailable measurements."
        ),
        auth=AuthSettings(
            issuer_url=AnyHttpUrl(settings.auth0_issuer),
            resource_server_url=AnyHttpUrl(settings.public_base_url),
            required_scopes=[settings.auth0_scope],
        ),
        token_verifier=verifier,
    )

    @server.tool(
        name="oura_catalog",
        title="List Oura data collections",
        description=(
            "List every Oura API v2 collection this service understands, including query "
            "parameters, source scopes, runtime authorization state, and explicitly "
            "unresolved data."
        ),
        annotations=ToolAnnotations(
            read_only_hint=True,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=False,
        ),
        structured_output=True,
    )
    async def oura_catalog() -> dict[str, Any]:
        return catalog_payload(
            backend=source.backend_name,
            token_configured=source.token_configured(),
        )

    @server.tool(
        name="oura_query",
        title="Query Oura data",
        description=(
            "Retrieve one Oura collection with explicit date or datetime bounds and optional "
            "cursor traversal. Returns the native Oura response plus request and endpoint "
            "provenance."
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
        fields: list[str] | None = None,
        latest: bool = False,
    ) -> dict[str, Any]:
        spec = collection_spec(collection)
        validate_query(
            spec,
            start=start,
            end=end,
            cursor=cursor,
            fields=fields,
            latest=latest,
            max_query_days=settings.max_query_days,
        )
        raw = await source.query(
            spec,
            start=start,
            end=end,
            cursor=cursor,
            fields=fields,
            latest=latest,
        )
        return {
            "collection": spec.name,
            "provenance": {
                "provider": "oura",
                "api_version": "v2",
                "endpoint": f"/v2/usercollection/{spec.path}",
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "backend": source.backend_name,
            },
            "request": {
                "start": start,
                "end": end,
                "cursor": cursor,
                "fields": fields,
                "latest": latest,
            },
            "next_cursor": raw.get("next_token"),
            "oura_response": raw,
        }

    @server.custom_route("/healthz", methods=["GET"], include_in_schema=False)
    async def health_check(request: Request) -> Response:
        return JSONResponse({"status": "ok", "backend": source.backend_name})

    if oura_oauth is not None:

        @server.custom_route("/oauth/oura/callback", methods=["GET"], include_in_schema=False)
        async def oura_callback(request: Request) -> Response:
            error = request.query_params.get("error_description") or request.query_params.get(
                "error"
            )
            if error:
                return HTMLResponse("Oura authorization was declined.", status_code=400)
            code = request.query_params.get("code", "")
            state = request.query_params.get("state", "")
            if not code or not state:
                return HTMLResponse("The Oura callback is missing code or state.", status_code=400)
            try:
                await oura_oauth.exchange_callback(code=code, state=state)
            except OAuthError:
                return HTMLResponse("Oura authorization could not be completed.", status_code=400)
            return HTMLResponse(
                "Oura authorization is complete. You can close this tab.", status_code=200
            )

    return server


def create_http_app(
    settings: Settings,
    *,
    source: OuraSource | None = None,
    token_verifier: TokenVerifier | None = None,
):
    server = build_server(settings, source=source, token_verifier=token_verifier)
    app = server.streamable_http_app(
        streamable_http_path="/mcp",
        stateless_http=True,
        json_response=True,
        host=settings.host,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=list(settings.allowed_hosts),
            allowed_origins=list(settings.allowed_origins),
        ),
    )
    return PostOnlyMCP(app)


class PostOnlyMCP:
    """Exclude the SDK's earlier Streamable HTTP GET compatibility route."""

    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if (
            scope["type"] == "http"
            and scope["path"] == "/mcp"
            and scope["method"] not in {"POST", "OPTIONS"}
        ):
            response = JSONResponse(
                {"error": "method_not_allowed", "detail": "The MCP endpoint accepts POST only."},
                status_code=405,
                headers={"Allow": "POST, OPTIONS"},
            )
            await response(scope, receive, send)
            return
        await self._app(scope, receive, send)


def _source_from_settings(settings: Settings) -> tuple[OuraSource, OuraOAuth | None]:
    if settings.backend == "fixture":
        return FixtureOuraSource(), None
    assert settings.oura_client_id is not None
    assert settings.oura_client_secret is not None
    assert settings.oura_redirect_uri is not None
    assert settings.oura_scopes is not None
    assert settings.oura_token_path is not None
    assert settings.oura_token_encryption_key is not None
    assert settings.oura_state_secret is not None
    store = EncryptedTokenStore(settings.oura_token_path, settings.oura_token_encryption_key)
    oauth = OuraOAuth(
        authorize_url=settings.oura_authorize_url,
        token_url=settings.oura_token_url,
        client_id=settings.oura_client_id,
        client_secret=settings.oura_client_secret,
        redirect_uri=settings.oura_redirect_uri,
        scopes=settings.oura_scopes,
        state_signer=OAuthStateSigner(settings.oura_state_secret),
        token_store=store,
    )
    client = OuraClient(
        api_base_url=settings.oura_api_base_url,
        token_url=settings.oura_token_url,
        client_id=settings.oura_client_id,
        client_secret=settings.oura_client_secret,
        token_store=store,
    )
    return LiveOuraSource(client), oauth
