from __future__ import annotations

from mcp.server.auth.provider import AccessToken

from oura_mcp.settings import Settings


class TestTokenVerifier:
    __test__ = False

    async def verify_token(self, token: str) -> AccessToken | None:
        if token not in {"valid-test-token", "wrong-scope-token"}:
            return None
        return AccessToken(
            token=token,
            client_id="test-client",
            scopes=["oura:read"] if token == "valid-test-token" else ["openid"],
            expires_at=4_102_444_800,
            subject="test-user",
        )


def make_settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "public_base_url": "https://mcp.example.test",
        "auth0_issuer": "https://issuer.example.test/",
        "auth0_audience": "https://mcp.example.test",
        "allowed_hosts": ("testserver", "mcp.example.test"),
        "allowed_origins": ("https://chatgpt.com",),
    }
    values.update(overrides)
    return Settings(**values)  # type: ignore[arg-type]
