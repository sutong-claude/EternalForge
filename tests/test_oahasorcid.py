from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasorcid import OaHasOrcidAdapter, parse_oahasorcid_payload
from tools.research import get_adapter


def test_oahasorcid_empty_query() -> None:
    assert OaHasOrcidAdapter().search("") == []
    assert OaHasOrcidAdapter().search("   ") == []


def test_get_adapter_oahasorcid_aliases() -> None:
    assert get_adapter("oahasorcid").name == "oahasorcid"
    assert get_adapter("hasorcid-oa").name == "oahasorcid"
    assert get_adapter("works-hasorcid-oa").name == "oahasorcid"


def test_parse_oahasorcid_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 40, "cited_by_count": 90},
            {"key": "false", "key_display_name": "false", "count": 7},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasorcid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Works with ORCID", "Works without ORCID"]
    assert hits[0].source == "oahasorcid"
    assert "40 works" in hits[0].snippet
    assert "90 cites" in hits[0].snippet
    assert "filter=has_orcid:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "7 works" in hits[1].snippet
    assert "filter=has_orcid:false" in hits[1].url


def test_parse_oahasorcid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasorcid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with ORCID"]


def test_parse_oahasorcid_list_shape() -> None:
    payload = {
        "has_orcid": [
            {"has_orcid": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasorcid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without ORCID"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasorcid"
    assert "filter=has_orcid:false" in hits[0].url
