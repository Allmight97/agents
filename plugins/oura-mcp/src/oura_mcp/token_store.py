"""Encrypted durable storage for the single Oura OAuth credential set."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

import anyio
from cryptography.fernet import Fernet, InvalidToken


class TokenStoreError(RuntimeError):
    pass


class EncryptedTokenStore:
    def __init__(self, path: Path, encryption_key: str) -> None:
        self.path = path
        try:
            self._fernet = Fernet(encryption_key.encode("ascii"))
        except (ValueError, TypeError) as error:
            raise TokenStoreError("OURA_TOKEN_ENCRYPTION_KEY is not a valid Fernet key.") from error

    def exists(self) -> bool:
        return self.path.exists()

    async def load(self) -> dict[str, Any] | None:
        return await anyio.to_thread.run_sync(self._load_sync)

    async def save(self, token: dict[str, Any]) -> None:
        await anyio.to_thread.run_sync(self._save_sync, token)

    def _load_sync(self) -> dict[str, Any] | None:
        if not self.path.exists():
            return None
        try:
            plaintext = self._fernet.decrypt(self.path.read_bytes())
            payload = json.loads(plaintext)
        except (OSError, InvalidToken, json.JSONDecodeError) as error:
            raise TokenStoreError(
                "The stored Oura token could not be read or decrypted."
            ) from error
        if not isinstance(payload, dict):
            raise TokenStoreError("The stored Oura token has an unexpected shape.")
        return payload

    def _save_sync(self, token: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        ciphertext = self._fernet.encrypt(
            json.dumps(token, separators=(",", ":"), sort_keys=True).encode("utf-8")
        )
        descriptor, temporary_name = tempfile.mkstemp(
            dir=self.path.parent, prefix=f".{self.path.name}.", suffix=".tmp"
        )
        temporary_path = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(ciphertext)
            os.chmod(temporary_path, 0o600)
            temporary_path.replace(self.path)
            os.chmod(self.path, 0o600)
        except BaseException:
            temporary_path.unlink(missing_ok=True)
            raise
