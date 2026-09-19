from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahaspmcid import OaHasPmcidAdapter, parse_oahaspmcid_payload
from tools.research import get_adapter


def test_oahaspmcid_empty_query() -> None:
    assert OaHasPmcidAdapter().search("") == []
    assert OaHasPmcidAdapter().search("   ") == []


def test_get_adapter_oahaspmcid_aliases() -> None:
    assert get_adapter("oahaspmcid").name == "oahaspmcid"
    assert get_adapter("haspmcid-oa").name == "oahaspmcid"
    assert get_adapter("works-haspmcid-oa").name == "oahaspmcid"


def test_parse_oahaspmcid_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 40, "cited_by_count": 90},
            {"key": "false", "key_display_name": "false", "count": 7},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahaspmcid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Works with PMCID", "Works without PMCID"]
    assert hits[0].source == "oahaspmcid"
    assert "40 works" in hits[0].snippet
    assert "90 cites" in hits[0].snippet
    assert "filter=has_pmcid:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "7 works" in hits[1].snippet
    assert "filter=has_pmcid:false" in hits[1].url


def test_parse_oahaspmcid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahaspmcid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with PMCID"]


def test_parse_oahaspmcid_list_shape() -> None:
    payload = {
        "has_pmcid": [
            {"has_pmcid": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahaspmcid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without PMCID"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahaspmcid"
    assert "filter=has_pmcid:false" in hits[0].url
