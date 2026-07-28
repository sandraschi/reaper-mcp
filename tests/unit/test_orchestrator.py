"""
Unit tests for reaper_mcp.portmanteau.orchestrator helpers.
"""

from reaper_mcp.portmanteau.orchestrator import (
    _normalize_regions,
    _parse_timestamp_to_seconds,
)


def test_parse_timestamp_to_seconds_formats() -> None:
    assert _parse_timestamp_to_seconds("12") == 12.0
    assert _parse_timestamp_to_seconds("01:05") == 65.0
    assert _parse_timestamp_to_seconds("1:02:03") == 3723.0
    assert _parse_timestamp_to_seconds("-1") is None


def test_normalize_regions_from_text() -> None:
    raw = "[verse] 00:10-00:35 [chorus] 00:35-01:05"
    regions = _normalize_regions(raw)
    assert len(regions) == 2
    assert regions[0]["name"] == "verse"
    assert regions[0]["start_seconds"] == 10.0
    assert regions[1]["name"] == "chorus"
    assert regions[1]["end_seconds"] == 65.0


def test_normalize_regions_from_list() -> None:
    regions = _normalize_regions(
        [
            {"name": "intro", "start": "00:00", "end": "00:08"},
            {"name": "bad", "start": "00:10", "end": "00:05"},
            {"name": "", "start": 0, "end": 3},
        ]
    )
    assert len(regions) == 1
    assert regions[0]["name"] == "intro"
    assert regions[0]["start_seconds"] == 0.0
    assert regions[0]["end_seconds"] == 8.0
