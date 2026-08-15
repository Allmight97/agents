from __future__ import annotations

import time
from types import SimpleNamespace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from oura_mcp.auth import Auth0TokenVerifier


class StaticSigningKeys:
    def __init__(self, public_key: object) -> None:
        self._public_key = public_key

    def get_signing_key_from_jwt(self, token: str) -> SimpleNamespace:
        return SimpleNamespace(key=self._public_key)


@pytest.mark.asyncio
async def test_auth0_verifier_accepts_expected_issuer_audience_and_scopes() -> None:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    now = int(time.time())
    encoded = jwt.encode(
        {
            "iss": "https://issuer.example.test/",
            "aud": "https://mcp.example.test",
            "sub": "owner",
            "azp": "chatgpt",
            "scope": "openid oura:read",
            "iat": now,
            "exp": now + 300,
        },
        private_key,
        algorithm="RS256",
    )
    verifier = Auth0TokenVerifier(
        issuer="https://issuer.example.test/",
        audience="https://mcp.example.test",
        resource="https://mcp.example.test",
        signing_keys=StaticSigningKeys(private_key.public_key()),
    )

    access = await verifier.verify_token(encoded)

    assert access is not None
    assert access.client_id == "chatgpt"
    assert access.scopes == ["openid", "oura:read"]
    assert access.subject == "owner"


@pytest.mark.asyncio
async def test_auth0_verifier_rejects_wrong_audience() -> None:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    now = int(time.time())
    encoded = jwt.encode(
        {
            "iss": "https://issuer.example.test/",
            "aud": "https://some-other-resource.example",
            "sub": "owner",
            "iat": now,
            "exp": now + 300,
        },
        private_key,
        algorithm="RS256",
    )
    verifier = Auth0TokenVerifier(
        issuer="https://issuer.example.test/",
        audience="https://mcp.example.test",
        resource="https://mcp.example.test",
        signing_keys=StaticSigningKeys(private_key.public_key()),
    )

    assert await verifier.verify_token(encoded) is None
