"""The Oura API collections exposed by the two-tool MCP surface."""

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
    "Granted by the Oura dashboard; exact public OAuth scope name unresolved."
)

_COLLECTIONS = (
    CollectionSpec(
        "daily_activity", "daily", "daily_activity", RangeKind.DATE, ("daily",)
    ),
    CollectionSpec(
        "daily_cardiovascular_age",
        "heart_health",
        "daily_cardiovascular_age",
        RangeKind.DATE,
        (),
        notes=_DASHBOARD_SCOPE_NOTE,
    ),
    CollectionSpec(
        "daily_readiness", "daily", "daily_readiness", RangeKind.DATE, ("daily",)
    ),
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
    CollectionSpec(
        "rest_mode_period", "daily", "rest_mode_period", RangeKind.DATE, ("daily",)
    ),
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
    CollectionSpec("sleep", "daily", "sleep", RangeKind.DATE, ("daily",)),
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
        raise ValueError(f"Unknown Oura collection: {name}") from error


def catalog_payload() -> dict[str, object]:
    return {
        "provider": "oura",
        "api_version": "v2",
        "backend": "synthetic_fixture",
        "collections": [collection.public_dict() for collection in _COLLECTIONS],
        "unresolved": ["nighttime_movement_trace"],
    }
