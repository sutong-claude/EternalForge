from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasodiamond import OaHasOaDiamondAdapter, parse_oahasodiamond_payload
from tools.research import get_adapter


def test_oahasodiamond_empty_query() -> None:
    assert OaHasOaDiamondAdapter().search("") == []
    assert OaHasOaDiamondAdapter().search("   ") == []


def test_get_adapter_oahasodiamond_aliases() -> None:
    assert get_adapter("oahasodiamond").name == "oahasodiamond"
    assert get_adapter("hasodiamond-oa").name == "oahasodiamond"
    assert get_adapter("works-hasodiamond-oa").name == "oahasodiamond"


def test_parse_oahasodiamond_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasodiamond_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with diamond OA",
        "Works without diamond OA",
    ]
    assert hits[0].source == "oahasodiamond"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=has_oa_diamond:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=has_oa_diamond:false" in hits[1].url


def test_parse_oahasodiamond_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasodiamond_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with diamond OA"]


def test_parse_oahasodiamond_list_shape() -> None:
    payload = {
        "has_oa_diamond": [
            {"has_oa_diamond": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasodiamond_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without diamond OA"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasodiamond"
    assert "filter=has_oa_diamond:false" in hits[0].url
