from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasoadomain import OaHasOaDomainAdapter, parse_oahasoadomain_payload
from tools.research import get_adapter


def test_oahasoadomain_empty_query() -> None:
    assert OaHasOaDomainAdapter().search("") == []
    assert OaHasOaDomainAdapter().search("   ") == []


def test_get_adapter_oahasoadomain_aliases() -> None:
    assert get_adapter("oahasoadomain").name == "oahasoadomain"
    assert get_adapter("hasoadomain-oa").name == "oahasoadomain"
    assert get_adapter("works-hasoadomain-oa").name == "oahasoadomain"


def test_parse_oahasoadomain_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 21, "cited_by_count": 44},
            {"key": "false", "key_display_name": "false", "count": 7},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasoadomain_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with OA domain",
        "Works without OA domain",
    ]
    assert hits[0].source == "oahasoadomain"
    assert "21 works" in hits[0].snippet
    assert "44 cites" in hits[0].snippet
    assert "filter=has_oa_domain:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "7 works" in hits[1].snippet
    assert "filter=has_oa_domain:false" in hits[1].url


def test_parse_oahasoadomain_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasoadomain_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with OA domain"]


def test_parse_oahasoadomain_list_shape() -> None:
    payload = {
        "has_oa_domain": [
            {"has_oa_domain": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasoadomain_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without OA domain"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasoadomain"
    assert "filter=has_oa_domain:false" in hits[0].url
