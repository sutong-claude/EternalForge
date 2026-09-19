from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasabs import OaHasAbsAdapter, parse_oahasabs_payload
from tools.research import get_adapter


def test_oahasabs_empty_query() -> None:
    assert OaHasAbsAdapter().search("") == []
    assert OaHasAbsAdapter().search("   ") == []


def test_get_adapter_oahasabs_aliases() -> None:
    assert get_adapter("oahasabs").name == "oahasabs"
    assert get_adapter("hasabs-oa").name == "oahasabs"
    assert get_adapter("works-hasabs-oa").name == "oahasabs"


def test_parse_oahasabs_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 40, "cited_by_count": 90},
            {"key": "false", "key_display_name": "false", "count": 7},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasabs_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Works with abstract", "Works without abstract"]
    assert hits[0].source == "oahasabs"
    assert "40 works" in hits[0].snippet
    assert "90 cites" in hits[0].snippet
    assert "filter=has_abstract:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "7 works" in hits[1].snippet
    assert "filter=has_abstract:false" in hits[1].url


def test_parse_oahasabs_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasabs_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with abstract"]


def test_parse_oahasabs_list_shape() -> None:
    payload = {
        "has_abstract": [
            {"has_abstract": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasabs_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without abstract"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasabs"
    assert "filter=has_abstract:false" in hits[0].url
