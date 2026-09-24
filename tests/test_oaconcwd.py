from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaconcwd import OaConcWdAdapter, parse_oaconcwd_payload
from tools.research import get_adapter


def test_oaconcwd_empty_query() -> None:
    assert OaConcWdAdapter().search("") == []
    assert OaConcWdAdapter().search("   ") == []


def test_get_adapter_oaconcwd_aliases() -> None:
    assert get_adapter("oaconcwd").name == "oaconcwd"
    assert get_adapter("concwd-oa").name == "oaconcwd"
    assert get_adapter("works-concwd-oa").name == "oaconcwd"


def test_parse_oaconcwd_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "Q21198",
                "key_display_name": "computer science",
                "count": 12,
            },
            {
                "key": "wikidata:Q2539",
                "key_display_name": "machine learning",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://www.wikidata.org/wiki/Q11190",
                "display_name": "medicine",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaconcwd_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "machine learning works",
        "computer science works",
        "medicine works",
    ]
    assert hits[0].source == "oaconcwd"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=concepts.wikidata:Q2539" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=concepts.wikidata:Q21198" in hits[1].url
    assert "5 works" in hits[2].snippet
    assert "filter=concepts.wikidata:Q11190" in hits[2].url


def test_parse_oaconcwd_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "Q1", "key_display_name": "alpha", "count": 1},
            {"key": "Q2", "key_display_name": "beta", "count": 2},
        ]
    }
    hits = parse_oaconcwd_payload(payload, limit=1)
    assert [h.title for h in hits] == ["beta works"]


def test_parse_oaconcwd_concepts_list() -> None:
    payload = {
        "concepts": [
            {
                "id": "https://www.wikidata.org/entity/Q2539",
                "display_name": "machine learning",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaconcwd_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "machine learning works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaconcwd"
    assert "filter=concepts.wikidata:Q2539" in hits[0].url
