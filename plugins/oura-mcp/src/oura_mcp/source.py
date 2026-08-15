"""Data-source adapters behind the two-tool MCP surface."""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any, Protocol

from .catalog import CollectionSpec, RangeKind
from .oura import OuraClient


class OuraSource(Protocol):
    backend_name: str

    def token_configured(self) -> bool: ...

    async def query(
        self,
        spec: CollectionSpec,
        *,
        start: str | None,
        end: str | None,
        cursor: str | None,
        fields: list[str] | None,
        latest: bool,
    ) -> dict[str, Any]: ...


class FixtureOuraSource:
    backend_name = "fixture"

    def token_configured(self) -> bool:
        return False

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
        page = 2 if cursor == "fixture-page-2" else 1
        identity: dict[str, Any] = {
            "id": f"synthetic-{spec.name}-{page}",
            "day": start or "2026-01-01",
            "timestamp": start or "2026-01-01T00:00:00+00:00",
            "synthetic": True,
            "collection": spec.name,
        }
        if fields:
            identity["requested_fields"] = list(fields)
        response: dict[str, Any] = {"data": [identity]}
        if spec.supports_cursor and page == 1:
            response["next_token"] = "fixture-page-2"
        return response


class LiveOuraSource:
    backend_name = "live"

    def __init__(self, client: OuraClient) -> None:
        self._client = client

    def token_configured(self) -> bool:
        return self._client.token_configured()

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
        return await self._client.query(
            spec,
            start=start,
            end=end,
            cursor=cursor,
            fields=fields,
            latest=latest,
        )


def validate_query(
    spec: CollectionSpec,
    *,
    start: str | None,
    end: str | None,
    cursor: str | None,
    fields: list[str] | None,
    latest: bool,
    max_query_days: int,
) -> None:
    if cursor and not spec.supports_cursor:
        raise ValueError(f"{spec.name} does not support cursors.")
    if latest and not spec.supports_latest:
        raise ValueError(f"{spec.name} does not support latest=true.")
    if latest and (start or end):
        raise ValueError("latest=true cannot be combined with start or end.")
    if spec.range_kind is RangeKind.NONE:
        if start or end or latest:
            raise ValueError(f"{spec.name} does not accept a date range.")
    elif not latest:
        if not start or not end:
            raise ValueError(f"{spec.name} requires both start and end for a bounded query.")
        start_value = _parse_boundary(start, spec.range_kind)
        end_value = _parse_boundary(end, spec.range_kind)
        if start_value > end_value:
            raise ValueError("start must not be after end.")
        if (end_value - start_value).days > max_query_days:
            raise ValueError(f"The requested range exceeds the {max_query_days}-day limit.")
    if fields:
        if spec.name == "personal_info":
            raise ValueError("personal_info does not accept a fields selection.")
        if len(fields) > 64 or any(not _valid_field(field) for field in fields):
            raise ValueError("fields must contain at most 64 simple Oura field names.")


def _parse_boundary(value: str, kind: RangeKind) -> datetime:
    try:
        if kind is RangeKind.DATE:
            parsed_date = date.fromisoformat(value)
            return datetime.combine(parsed_date, datetime.min.time(), tzinfo=timezone.utc)
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        expected = "YYYY-MM-DD" if kind is RangeKind.DATE else "ISO 8601 with a timezone"
        raise ValueError(f"Invalid range boundary {value!r}; expected {expected}.") from error
    if parsed.tzinfo is None:
        raise ValueError("Datetime boundaries must include a timezone offset.")
    return parsed.astimezone(timezone.utc)


def _valid_field(value: str) -> bool:
    return (
        bool(value)
        and len(value) <= 100
        and all(character.isalnum() or character in {"_", ".", "-"} for character in value)
    )
