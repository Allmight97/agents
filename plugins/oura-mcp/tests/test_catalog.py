from __future__ import annotations

from oura_mcp.catalog import COLLECTIONS, catalog_payload


def test_catalog_covers_every_published_oura_v2_collection() -> None:
    assert set(COLLECTIONS) == {
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
    }


def test_catalog_marks_unproven_nighttime_movement_trace_as_unresolved() -> None:
    catalog = catalog_payload(backend="fixture", token_configured=False)

    assert catalog["runtime_status"] == "synthetic_fixture"
    assert catalog["unresolved"] == [
        {
            "name": "nighttime_movement_trace",
            "status": "not_documented_as_an_api_v2_collection",
            "detail": (
                "Oura documents movement-derived data, but its published v2 schema does not "
                "identify the exact nighttime movement graph as a retrievable collection."
            ),
        }
    ]


def test_catalog_does_not_invent_dashboard_only_oauth_scope_names() -> None:
    catalog = catalog_payload(backend="live", token_configured=True)
    collections = {item["name"]: item for item in catalog["collections"]}

    assert collections["daily_sleep"]["documented_oauth_scopes"] == ("daily",)
    assert collections["daily_stress"]["documented_oauth_scopes"] == ()
    assert "published OAuth schema does not name" in collections["daily_stress"]["notes"]
