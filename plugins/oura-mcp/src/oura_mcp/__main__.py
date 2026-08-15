"""Service and authorization CLI."""

from __future__ import annotations

import argparse
import logging

import uvicorn

from .oauth import OAuthStateSigner, OuraOAuth
from .server import create_http_app
from .settings import ConfigurationError, Settings
from .token_store import EncryptedTokenStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Run and authorize the private Oura MCP service.")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("serve", help="Run the Streamable HTTP service.")
    subparsers.add_parser(
        "authorization-url",
        help="Print a short-lived Oura authorization URL using the deployed callback.",
    )
    arguments = parser.parse_args()
    command = arguments.command or "serve"
    try:
        settings = Settings.from_env()
        if command == "authorization-url":
            print(_authorization_url(settings))
            return
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)
        uvicorn.run(
            create_http_app(settings),
            host=settings.host,
            port=settings.port,
            log_level="info",
            access_log=False,
        )
    except ConfigurationError as error:
        parser.error(str(error))


def _authorization_url(settings: Settings) -> str:
    if settings.backend != "live":
        raise ConfigurationError("Set OURA_BACKEND=live before generating an authorization URL.")
    assert settings.oura_client_id is not None
    assert settings.oura_client_secret is not None
    assert settings.oura_redirect_uri is not None
    assert settings.oura_scopes is not None
    assert settings.oura_token_path is not None
    assert settings.oura_token_encryption_key is not None
    assert settings.oura_state_secret is not None
    oauth = OuraOAuth(
        authorize_url=settings.oura_authorize_url,
        token_url=settings.oura_token_url,
        client_id=settings.oura_client_id,
        client_secret=settings.oura_client_secret,
        redirect_uri=settings.oura_redirect_uri,
        scopes=settings.oura_scopes,
        state_signer=OAuthStateSigner(settings.oura_state_secret),
        token_store=EncryptedTokenStore(
            settings.oura_token_path, settings.oura_token_encryption_key
        ),
    )
    return oauth.authorization_url()


if __name__ == "__main__":
    main()
