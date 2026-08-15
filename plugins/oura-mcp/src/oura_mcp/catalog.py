"""Oura collection catalog and query-shape ownership."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Literal


class RangeKind(str, Enum):
    NONE = "none"
    DATE = "date"
    DATETIME = "datetime"


@dataclass(frozen=True, slots=True)
class CollectionSpec:
    name: str
    family: str
    path: str
    range_kind: RangeKind
    documented_oauth_scopes: tuple[str, ...]
    supports_cursor: bool = True
    supports_latest: bool = False
    notes: str | None = None

    def public_dict(self) -> dict[str, object]:
        value = asdict(self)
        value["range_kind"] = self.range_kind.value
        value["query_parameters"] = _query_parameters(self)
        return value


OuraCollectionName = Literal[
    "daily_activity",
    "daily_cardiovascular_age",
    "daily_readiness",
    "daily_resilience",
    "daily_sleep",
    "daily_spo2",
    "daily_stress",
    "enhanced_tag",
    "heartrate",
    "personal_info",
    "rest_mode_period",
    "ring_battery_level",
    "ring_configuration",
    "session",
    "sleep",
    "sleep_time",
    "tag",
    "vo2_max",
    "workout",
]


_DASHBOARD_SCOPE_NOTE = (
    "The Oura developer dashboard grants this family, but the published OAuth schema does not "
    "name its exact scope string."
)

_COLLECTIONS = (
    CollectionSpec("daily_activity", "daily", "daily_activity", RangeKind.DATE, ("daily",)),
    CollectionSpec(
        "daily_cardiovascular_age",
        "heart_health",
        "daily_cardiovascular_age",
        RangeKind.DATE,
        (),
        notes=_DASHBOARD_SCOPE_NOTE,
    ),
    CollectionSpec("daily_readiness", "daily", "daily_readiness", RangeKind.DATE, ("daily",)),
    CollectionSpec(
        "daily_resilience",
        "stress",
        "daily_resilience",
        RangeKind.DATE,
        (),
        notes=_DASHBOARD_SCOPE_NOTE,
    ),
    CollectionSpec("daily_sleep", "daily", "daily_sleep", RangeKind.DATE, ("daily",)),
    CollectionSpec("daily_spo2", "spo2", "daily_spo2", RangeKind.DATE, ("spo2Daily",)),
    CollectionSpec(
        "daily_stress",
        "stress",
        "daily_stress",
        RangeKind.DATE,
        (),
        notes=_DASHBOARD_SCOPE_NOTE,
    ),
    CollectionSpec("enhanced_tag", "tag", "enhanced_tag", RangeKind.DATE, ("tag",)),
    CollectionSpec(
        "heartrate",
        "heartrate",
        "heartrate",
        RangeKind.DATETIME,
        ("heartrate",),
        supports_latest=True,
    ),
    CollectionSpec(
        "personal_info",
        "personal",
        "personal_info",
        RangeKind.NONE,
        ("personal", "email"),
        supports_cursor=False,
    ),
    CollectionSpec("rest_mode_period", "daily", "rest_mode_period", RangeKind.DATE, ("daily",)),
    CollectionSpec(
        "ring_battery_level",
        "ring_configuration",
        "ring_battery_level",
        RangeKind.DATETIME,
        (),
        supports_latest=True,
        notes=_DASHBOARD_SCOPE_NOTE,
    ),
    CollectionSpec(
        "ring_configuration",
        "ring_configuration",
        "ring_configuration",
        RangeKind.NONE,
        (),
        notes=_DASHBOARD_SCOPE_NOTE,
    ),
    CollectionSpec("session", "session", "session", RangeKind.DATE, ("session",)),
    CollectionSpec(
        "sleep",
        "daily",
        "sleep",
        RangeKind.DATE,
        ("daily",),
        notes=(
            "Contains Oura-native sleep periods and signals such as HRV and temperature deviation."
        ),
    ),
    CollectionSpec("sleep_time", "daily", "sleep_time", RangeKind.DATE, ("daily",)),
    CollectionSpec("tag", "tag", "tag", RangeKind.DATE, ("tag",)),
    CollectionSpec(
        "vo2_max",
        "heart_health",
        "vO2_max",
        RangeKind.DATE,
        (),
        notes=_DASHBOARD_SCOPE_NOTE,
    ),
    CollectionSpec("workout", "workout", "workout", RangeKind.DATE, ("workout",)),
)

COLLECTIONS = {collection.name: collection for collection in _COLLECTIONS}


def collection_spec(name: str) -> CollectionSpec:
    try:
        return COLLECTIONS[name]
    except KeyError as error:
        available = ", ".join(COLLECTIONS)
        raise ValueError(
            f"Unknown Oura collection {name!r}. Available collections: {available}."
        ) from error


def catalog_payload(*, backend: str, token_configured: bool) -> dict[str, object]:
    runtime_status = (
        "synthetic_fixture"
        if backend == "fixture"
        else ("configured_not_observed" if token_configured else "authorization_required")
    )
    return {
        "provider": "oura",
        "api_version": "v2",
        "published_schema_revision": "openapi-1.37",
        "backend": backend,
        "runtime_status": runtime_status,
        "collections": [collection.public_dict() for collection in _COLLECTIONS],
        "unresolved": [
            {
                "name": "nighttime_movement_trace",
                "status": "not_documented_as_an_api_v2_collection",
                "detail": (
                    "Oura documents movement-derived data, but its published v2 schema does not "
                    "identify the exact nighttime movement graph as a retrievable collection."
                ),
            }
        ],
    }


def _query_parameters(spec: CollectionSpec) -> list[str]:
    parameters: list[str] = []
    if spec.range_kind is RangeKind.DATE:
        parameters.extend(["start (YYYY-MM-DD)", "end (YYYY-MM-DD)"])
    elif spec.range_kind is RangeKind.DATETIME:
        parameters.extend(["start (ISO 8601 with timezone)", "end (ISO 8601 with timezone)"])
    if spec.supports_cursor:
        parameters.append("cursor")
    if spec.supports_latest:
        parameters.append("latest")
    if spec.name != "personal_info":
        parameters.append("fields")
    return parameters
