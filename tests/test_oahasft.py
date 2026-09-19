from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasft import OaHasFtAdapter, parse_oahasft_payload
from tools.research import get_adapter


def test_oahasft_empty_query() -> None:
    assert OaHasFtAdapter().search("") == []
    assert OaHasFtAdapter().search("   ") == []


def test_get_adapter_oahasft_aliases() -> None:
    assert get_adapter("oahasft").name == "oahasft"
    assert get_adapter("hasft-oa").name == "oahasft"
    assert get_adapter("works-hasft-oa").name == "oahasft"


def test_parse_oahasft_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 40, "cited_by_count": 90},
            {"key": "false", "key_display_name": "false", "count": 7},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasft_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Works with fulltext", "Works without fulltext"]
    assert hits[0].source == "oahasft"
    assert "40 works" in hits[0].snippet
    assert "90 cites" in hits[0].snippet
    assert "filter=has_fulltext:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "7 works" in hits[1].snippet
    assert "filter=has_fulltext:false" in hits[1].url


def test_parse_oahasft_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasft_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with fulltext"]


def test_parse_oahasft_list_shape() -> None:
    payload = {
        "has_fulltext": [
            {"has_fulltext": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasft_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without fulltext"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasft"
    assert "filter=has_fulltext:false" in hits[0].url
