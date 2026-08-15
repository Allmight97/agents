from __future__ import annotations

import pytest
from conftest import TestTokenVerifier, make_settings
from mcp.client import Client

from oura_mcp.server import build_server
from oura_mcp.source import FixtureOuraSource


@pytest.mark.asyncio
async def test_server_exposes_exactly_two_read_only_tools() -> None:
    server = build_server(
        make_settings(), source=FixtureOuraSource(), token_verifier=TestTokenVerifier()
    )

    async with Client(server) as client:
        tools = (await client.list_tools()).tools

    assert [tool.name for tool in tools] == ["oura_catalog", "oura_query"]
    assert all(tool.annotations and tool.annotations.read_only_hint for tool in tools)
    assert all(tool.annotations and not tool.annotations.destructive_hint for tool in tools)


@pytest.mark.asyncio
async def test_query_preserves_native_response_and_cursor_provenance() -> None:
    server = build_server(
        make_settings(), source=FixtureOuraSource(), token_verifier=TestTokenVerifier()
    )

    async with Client(server) as client:
        result = await client.call_tool(
            "oura_query",
            {
                "collection": "daily_sleep",
                "start": "2026-01-01",
                "end": "2026-01-02",
            },
        )

    assert result.is_error is False
    assert result.structured_content is not None
    assert result.structured_content["next_cursor"] == "fixture-page-2"
    assert result.structured_content["oura_response"]["next_token"] == "fixture-page-2"
    assert result.structured_content["provenance"]["endpoint"] == ("/v2/usercollection/daily_sleep")


@pytest.mark.asyncio
async def test_query_returns_model_readable_error_for_unbounded_request() -> None:
    server = build_server(
        make_settings(), source=FixtureOuraSource(), token_verifier=TestTokenVerifier()
    )

    async with Client(server) as client:
        result = await client.call_tool("oura_query", {"collection": "daily_sleep"})

    assert result.is_error is True
    assert "requires both start and end" in result.content[0].text


@pytest.mark.asyncio
async def test_empty_upstream_result_remains_a_successful_native_response() -> None:
    class EmptySource(FixtureOuraSource):
        async def query(self, *args, **kwargs):
            return {"data": []}

    server = build_server(make_settings(), source=EmptySource(), token_verifier=TestTokenVerifier())

    async with Client(server) as client:
        result = await client.call_tool(
            "oura_query",
            {
                "collection": "daily_sleep",
                "start": "2026-01-01",
                "end": "2026-01-02",
            },
        )

    assert result.is_error is False
    assert result.structured_content is not None
    assert result.structured_content["oura_response"] == {"data": []}


@pytest.mark.asyncio
async def test_upstream_failure_is_model_readable() -> None:
    class FailingSource(FixtureOuraSource):
        async def query(self, *args, **kwargs):
            raise RuntimeError("Oura returned HTTP 503 for daily_sleep.")

    server = build_server(
        make_settings(), source=FailingSource(), token_verifier=TestTokenVerifier()
    )

    async with Client(server) as client:
        result = await client.call_tool(
            "oura_query",
            {
                "collection": "daily_sleep",
                "start": "2026-01-01",
                "end": "2026-01-02",
            },
        )

    assert result.is_error is True
    assert "HTTP 503" in result.content[0].text
