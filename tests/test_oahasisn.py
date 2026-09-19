from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasisn import OaHasIssnAdapter, parse_oahasisn_payload
from tools.research import get_adapter


def test_oahasisn_empty_query() -> None:
    assert OaHasIssnAdapter().search("") == []
    assert OaHasIssnAdapter().search("   ") == []


def test_get_adapter_oahasisn_aliases() -> None:
    assert get_adapter("oahasisn").name == "oahasisn"
    assert get_adapter("hasissn-oa").name == "oahasisn"
    assert get_adapter("works-hasissn-oa").name == "oahasisn"


def test_parse_oahasisn_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 40, "cited_by_count": 90},
            {"key": "false", "key_display_name": "false", "count": 7},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasisn_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Works with ISSN", "Works without ISSN"]
    assert hits[0].source == "oahasisn"
    assert "40 works" in hits[0].snippet
    assert "90 cites" in hits[0].snippet
    assert "filter=has_issn:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "7 works" in hits[1].snippet
    assert "filter=has_issn:false" in hits[1].url


def test_parse_oahasisn_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasisn_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with ISSN"]


def test_parse_oahasisn_list_shape() -> None:
    payload = {
        "has_issn": [
            {"has_issn": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasisn_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without ISSN"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasisn"
    assert "filter=has_issn:false" in hits[0].url
