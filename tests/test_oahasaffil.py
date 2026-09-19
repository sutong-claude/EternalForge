from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasaffil import OaHasAffilAdapter, parse_oahasaffil_payload
from tools.research import get_adapter


def test_oahasaffil_empty_query() -> None:
    assert OaHasAffilAdapter().search("") == []
    assert OaHasAffilAdapter().search("   ") == []


def test_get_adapter_oahasaffil_aliases() -> None:
    assert get_adapter("oahasaffil").name == "oahasaffil"
    assert get_adapter("hasaffil-oa").name == "oahasaffil"
    assert get_adapter("works-hasaffil-oa").name == "oahasaffil"


def test_parse_oahasaffil_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 40, "cited_by_count": 90},
            {"key": "false", "key_display_name": "false", "count": 7},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasaffil_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Works with raw affiliation", "Works without raw affiliation"]
    assert hits[0].source == "oahasaffil"
    assert "40 works" in hits[0].snippet
    assert "90 cites" in hits[0].snippet
    assert "filter=has_raw_affiliation_string:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "7 works" in hits[1].snippet
    assert "filter=has_raw_affiliation_string:false" in hits[1].url


def test_parse_oahasaffil_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasaffil_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with raw affiliation"]


def test_parse_oahasaffil_list_shape() -> None:
    payload = {
        "has_raw_affiliation_string": [
            {"has_raw_affiliation_string": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasaffil_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without raw affiliation"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasaffil"
    assert "filter=has_raw_affiliation_string:false" in hits[0].url
