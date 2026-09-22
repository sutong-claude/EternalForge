from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oalochost import OaLocHostAdapter, parse_oalochost_payload
from tools.research import get_adapter


def test_oalochost_empty_query() -> None:
    assert OaLocHostAdapter().search("") == []
    assert OaLocHostAdapter().search("   ") == []


def test_get_adapter_oalochost_aliases() -> None:
    assert get_adapter("oalochost").name == "oalochost"
    assert get_adapter("lochost-oa").name == "oalochost"
    assert get_adapter("works-lochost-oa").name == "oalochost"


def test_parse_oalochost_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/P4310320990",
                "key_display_name": "Springer Nature",
                "count": 12,
            },
            {
                "key": "https://openalex.org/P4310319965",
                "key_display_name": "Elsevier",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "P4310319900",
                "display_name": "Wiley",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oalochost_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Elsevier works", "Springer Nature works", "Wiley works"]
    assert hits[0].source == "oalochost"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=locations.source.host_organization:P4310319965" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=locations.source.host_organization:P4310320990" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oalochost_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "P1", "key_display_name": "One", "count": 1},
            {"key": "P2", "key_display_name": "Two", "count": 2},
        ]
    }
    hits = parse_oalochost_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Two works"]


def test_parse_oalochost_hosts_list() -> None:
    payload = {
        "host_organizations": [
            {
                "host_organization": "https://openalex.org/P4310319965",
                "display_name": "Elsevier",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oalochost_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Elsevier works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oalochost"
    assert "filter=locations.source.host_organization:P4310319965" in hits[0].url
