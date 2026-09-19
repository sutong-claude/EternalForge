from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasoahybrid import OaHasOaHybridAdapter, parse_oahasoahybrid_payload
from tools.research import get_adapter


def test_oahasoahybrid_empty_query() -> None:
    assert OaHasOaHybridAdapter().search("") == []
    assert OaHasOaHybridAdapter().search("   ") == []


def test_get_adapter_oahasoahybrid_aliases() -> None:
    assert get_adapter("oahasoahybrid").name == "oahasoahybrid"
    assert get_adapter("hasoahybrid-oa").name == "oahasoahybrid"
    assert get_adapter("works-hasoahybrid-oa").name == "oahasoahybrid"


def test_parse_oahasoahybrid_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasoahybrid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with hybrid OA",
        "Works without hybrid OA",
    ]
    assert hits[0].source == "oahasoahybrid"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=has_oa_hybrid:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=has_oa_hybrid:false" in hits[1].url


def test_parse_oahasoahybrid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasoahybrid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with hybrid OA"]


def test_parse_oahasoahybrid_list_shape() -> None:
    payload = {
        "has_oa_hybrid": [
            {"has_oa_hybrid": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasoahybrid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without hybrid OA"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasoahybrid"
    assert "filter=has_oa_hybrid:false" in hits[0].url
