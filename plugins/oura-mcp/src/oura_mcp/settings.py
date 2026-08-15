"""Environment-backed service configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


class ConfigurationError(RuntimeError):
    pass


def _required(name: str, environment: dict[str, str]) -> str:
    value = environment.get(name, "").strip()
    if not value:
        raise ConfigurationError(f"Set {name} before starting the service.")
    return value


def _csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


@dataclass(frozen=True, slots=True)
class Settings:
    public_base_url: str
    auth0_issuer: str
    auth0_audience: str
    auth0_scope: str = "oura:read"
    backend: str = "fixture"
    allowed_hosts: tuple[str, ...] = ()
    allowed_origins: tuple[str, ...] = ("https://chatgpt.com", "https://chat.openai.com")
    host: str = "0.0.0.0"
    port: int = 8000
    max_query_days: int = 90
    oura_api_base_url: str = "https://api.ouraring.com/v2/usercollection"
    oura_authorize_url: str = "https://cloud.ouraring.com/oauth/authorize"
    oura_token_url: str = "https://api.ouraring.com/oauth/token"
    oura_client_id: str | None = None
    oura_client_secret: str | None = None
    oura_redirect_uri: str | None = None
    oura_scopes: str | None = None
    oura_token_path: Path | None = None
    oura_token_encryption_key: str | None = None
    oura_state_secret: str | None = None

    @property
    def mcp_endpoint_url(self) -> str:
        return f"{self.public_base_url.rstrip('/')}/mcp"

    @classmethod
    def from_env(cls, environment: dict[str, str] | None = None) -> Settings:
        env = dict(os.environ if environment is None else environment)
        public_base_url = _required("MCP_PUBLIC_BASE_URL", env).rstrip("/")
        parsed = urlparse(public_base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.path:
            raise ConfigurationError("MCP_PUBLIC_BASE_URL must be an origin without a path.")
        if parsed.scheme != "https" and parsed.hostname not in {"127.0.0.1", "localhost"}:
            raise ConfigurationError(
                "MCP_PUBLIC_BASE_URL must use HTTPS outside loopback development."
            )

        backend = env.get("OURA_BACKEND", "fixture").strip().lower()
        if backend not in {"fixture", "live"}:
            raise ConfigurationError("OURA_BACKEND must be either 'fixture' or 'live'.")

        configured_hosts = _csv(env.get("MCP_ALLOWED_HOSTS", ""))
        allowed_hosts = configured_hosts or (parsed.netloc,)
        configured_origins = _csv(env.get("MCP_ALLOWED_ORIGINS", ""))
        allowed_origins = configured_origins or (
            "https://chatgpt.com",
            "https://chat.openai.com",
        )

        kwargs: dict[str, object] = {
            "public_base_url": public_base_url,
            "auth0_issuer": _required("AUTH0_ISSUER", env).rstrip("/") + "/",
            "auth0_audience": _required("AUTH0_AUDIENCE", env),
            "auth0_scope": env.get("AUTH0_SCOPE", "oura:read").strip() or "oura:read",
            "backend": backend,
            "allowed_hosts": allowed_hosts,
            "allowed_origins": allowed_origins,
            "host": env.get("HOST", "0.0.0.0").strip() or "0.0.0.0",
            "port": int(env.get("PORT", "8000")),
            "max_query_days": int(env.get("OURA_MAX_QUERY_DAYS", "90")),
            "oura_api_base_url": env.get(
                "OURA_API_BASE_URL", "https://api.ouraring.com/v2/usercollection"
            ).rstrip("/"),
            "oura_authorize_url": env.get(
                "OURA_AUTHORIZE_URL", "https://cloud.ouraring.com/oauth/authorize"
            ),
            "oura_token_url": env.get("OURA_TOKEN_URL", "https://api.ouraring.com/oauth/token"),
        }
        if backend == "live":
            kwargs.update(
                oura_client_id=_required("OURA_CLIENT_ID", env),
                oura_client_secret=_required("OURA_CLIENT_SECRET", env),
                oura_redirect_uri=_required("OURA_REDIRECT_URI", env),
                oura_scopes=_required("OURA_SCOPES", env),
                oura_token_path=Path(
                    env.get("OURA_TOKEN_PATH", "/var/lib/oura-mcp/oauth-token.enc")
                ),
                oura_token_encryption_key=_required("OURA_TOKEN_ENCRYPTION_KEY", env),
                oura_state_secret=_required("OURA_STATE_SECRET", env),
            )
        settings = cls(**kwargs)  # type: ignore[arg-type]
        if settings.max_query_days < 1 or settings.max_query_days > 366:
            raise ConfigurationError("OURA_MAX_QUERY_DAYS must be between 1 and 366.")
        return settings
