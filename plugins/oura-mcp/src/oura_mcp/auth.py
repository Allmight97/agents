"""Auth0 access-token verification for the MCP resource server."""

from __future__ import annotations

import time
from typing import Any, Protocol

import anyio
import jwt
from jwt import PyJWKClient
from mcp.server.auth.provider import AccessToken


class SigningKeyProvider(Protocol):
    def get_signing_key_from_jwt(self, token: str) -> Any: ...


class Auth0TokenVerifier:
    """Verify Auth0 JWTs without logging or persisting bearer tokens."""

    def __init__(
        self,
        *,
        issuer: str,
        audience: str,
        resource: str,
        signing_keys: SigningKeyProvider | None = None,
    ) -> None:
        self._issuer = issuer
        self._audience = audience
        self._resource = resource
        self._signing_keys = signing_keys or PyJWKClient(f"{issuer}.well-known/jwks.json")

    async def verify_token(self, token: str) -> AccessToken | None:
        return await anyio.to_thread.run_sync(self._verify_sync, token)

    def _verify_sync(self, token: str) -> AccessToken | None:
        try:
            signing_key = self._signing_keys.get_signing_key_from_jwt(token).key
            claims = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                audience=self._audience,
                issuer=self._issuer,
                options={"require": ["exp", "iat", "iss", "sub"]},
            )
        except jwt.PyJWTError:
            return None

        scopes_claim = claims.get("scope", "")
        if isinstance(scopes_claim, str):
            scopes = [scope for scope in scopes_claim.split() if scope]
        elif isinstance(scopes_claim, list) and all(
            isinstance(scope, str) for scope in scopes_claim
        ):
            scopes = scopes_claim
        else:
            return None

        client_id = claims.get("azp") or claims.get("client_id") or claims.get("sub")
        if not isinstance(client_id, str):
            return None
        expires_at = claims.get("exp")
        if not isinstance(expires_at, int) or expires_at <= int(time.time()):
            return None
        return AccessToken(
            token=token,
            client_id=client_id,
            scopes=scopes,
            expires_at=expires_at,
            resource=self._resource,
            subject=claims["sub"],
            claims=claims,
        )
