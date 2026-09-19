from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahaspmid import OaHasPmidAdapter, parse_oahaspmid_payload
from tools.research import get_adapter


def test_oahaspmid_empty_query() -> None:
    assert OaHasPmidAdapter().search("") == []
    assert OaHasPmidAdapter().search("   ") == []


def test_get_adapter_oahaspmid_aliases() -> None:
    assert get_adapter("oahaspmid").name == "oahaspmid"
    assert get_adapter("haspmid-oa").name == "oahaspmid"
    assert get_adapter("works-haspmid-oa").name == "oahaspmid"


def test_parse_oahaspmid_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 40, "cited_by_count": 90},
            {"key": "false", "key_display_name": "false", "count": 7},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahaspmid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Works with PMID", "Works without PMID"]
    assert hits[0].source == "oahaspmid"
    assert "40 works" in hits[0].snippet
    assert "90 cites" in hits[0].snippet
    assert "filter=has_pmid:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "7 works" in hits[1].snippet
    assert "filter=has_pmid:false" in hits[1].url


def test_parse_oahaspmid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahaspmid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with PMID"]


def test_parse_oahaspmid_list_shape() -> None:
    payload = {
        "has_pmid": [
            {"has_pmid": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahaspmid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without PMID"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahaspmid"
    assert "filter=has_pmid:false" in hits[0].url
