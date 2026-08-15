from __future__ import annotations

from conftest import TestTokenVerifier, make_settings
from starlette.testclient import TestClient

from oura_mcp.server import create_http_app
from oura_mcp.source import FixtureOuraSource


def _tools_list_request() -> tuple[dict[str, object], dict[str, str]]:
    body: dict[str, object] = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {
            "_meta": {
                "io.modelcontextprotocol/protocolVersion": "2026-07-28",
                "io.modelcontextprotocol/clientInfo": {"name": "test", "version": "1"},
                "io.modelcontextprotocol/clientCapabilities": {},
            }
        },
    }
    headers = {
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
        "MCP-Protocol-Version": "2026-07-28",
        "Mcp-Method": "tools/list",
    }
    return body, headers


def test_http_transport_requires_auth_and_publishes_discovery_metadata() -> None:
    app = create_http_app(
        make_settings(), source=FixtureOuraSource(), token_verifier=TestTokenVerifier()
    )
    body, headers = _tools_list_request()

    with TestClient(app) as client:
        metadata = client.get("/.well-known/oauth-protected-resource")
        unauthorized = client.post("/mcp", json=body, headers=headers)
        authorized = client.post(
            "/mcp",
            json=body,
            headers={**headers, "Authorization": "Bearer valid-test-token"},
        )
        wrong_scope = client.post(
            "/mcp",
            json=body,
            headers={**headers, "Authorization": "Bearer wrong-scope-token"},
        )

    assert metadata.status_code == 200
    assert metadata.json() == {
        "resource": "https://mcp.example.test/",
        "authorization_servers": ["https://issuer.example.test/"],
        "scopes_supported": ["oura:read"],
        "bearer_methods_supported": ["header"],
    }
    assert unauthorized.status_code == 401
    assert "resource_metadata=" in unauthorized.headers["WWW-Authenticate"]
    assert wrong_scope.status_code == 403
    assert authorized.status_code == 200
    assert [tool["name"] for tool in authorized.json()["result"]["tools"]] == [
        "oura_catalog",
        "oura_query",
    ]


def test_transport_rejects_unapproved_origin() -> None:
    app = create_http_app(
        make_settings(), source=FixtureOuraSource(), token_verifier=TestTokenVerifier()
    )
    body, headers = _tools_list_request()

    with TestClient(app) as client:
        response = client.post(
            "/mcp",
            json=body,
            headers={
                **headers,
                "Authorization": "Bearer valid-test-token",
                "Origin": "https://attacker.example",
            },
        )

    assert response.status_code == 403


def test_transport_has_no_legacy_get_stream() -> None:
    app = create_http_app(
        make_settings(), source=FixtureOuraSource(), token_verifier=TestTokenVerifier()
    )

    with TestClient(app) as client:
        response = client.get("/mcp")

    assert response.status_code == 405
    assert response.headers["Allow"] == "POST, OPTIONS"
