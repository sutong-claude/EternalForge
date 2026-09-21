from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oapriisoaloc import OaPriIsOaLocAdapter, parse_oapriisoaloc_payload
from tools.research import get_adapter


def test_oapriisoaloc_empty_query() -> None:
    assert OaPriIsOaLocAdapter().search("") == []
    assert OaPriIsOaLocAdapter().search("   ") == []


def test_get_adapter_oapriisoaloc_aliases() -> None:
    assert get_adapter("oapriisoaloc").name == "oapriisoaloc"
    assert get_adapter("priisoaloc-oa").name == "oapriisoaloc"
    assert get_adapter("works-priisoaloc-oa").name == "oapriisoaloc"


def test_parse_oapriisoaloc_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oapriisoaloc_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works whose primary location is OA",
        "Works whose primary location is not OA",
    ]
    assert hits[0].source == "oapriisoaloc"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=primary_location.is_oa:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=primary_location.is_oa:false" in hits[1].url


def test_parse_oapriisoaloc_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oapriisoaloc_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works whose primary location is OA"]


def test_parse_oapriisoaloc_list_shape() -> None:
    payload = {
        "is_oa": [
            {"is_oa": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oapriisoaloc_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works whose primary location is not OA"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oapriisoaloc"
    assert "filter=primary_location.is_oa:false" in hits[0].url
