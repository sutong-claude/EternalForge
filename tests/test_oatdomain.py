from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oatdomain import OaTDomainAdapter, parse_oatdomain_payload
from tools.research import get_adapter


def test_oatdomain_empty_query() -> None:
    assert OaTDomainAdapter().search("") == []
    assert OaTDomainAdapter().search("   ") == []


def test_get_adapter_oatdomain_aliases() -> None:
    assert get_adapter("oatdomain").name == "oatdomain"
    assert get_adapter("domain-oa").name == "oatdomain"
    assert get_adapter("works-domain-oa").name == "oatdomain"


def test_parse_oatdomain_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/domains/4",
                "key_display_name": "Health Sciences",
                "count": 12,
            },
            {
                "key": "domain:3",
                "key_display_name": "Physical Sciences",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "2",
                "display_name": "Social Sciences",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oatdomain_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Physical Sciences works",
        "Health Sciences works",
        "Social Sciences works",
    ]
    assert hits[0].source == "oatdomain"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=topics.domain.id:3" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=topics.domain.id:4" in hits[1].url
    assert "5 works" in hits[2].snippet
    assert "filter=topics.domain.id:2" in hits[2].url


def test_parse_oatdomain_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "4", "key_display_name": "Alpha Domain", "count": 1},
            {"key": "3", "key_display_name": "Beta Domain", "count": 2},
        ]
    }
    hits = parse_oatdomain_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Beta Domain works"]


def test_parse_oatdomain_domains_list() -> None:
    payload = {
        "domains": [
            {
                "id": "https://openalex.org/domains/1",
                "display_name": "Life Sciences",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oatdomain_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Life Sciences works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oatdomain"
    assert "filter=topics.domain.id:1" in hits[0].url
