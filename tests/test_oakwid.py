from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oakwid import OaKwIdAdapter, parse_oakwid_payload
from tools.research import get_adapter


def test_oakwid_empty_query() -> None:
    assert OaKwIdAdapter().search("") == []
    assert OaKwIdAdapter().search("   ") == []


def test_get_adapter_oakwid_aliases() -> None:
    assert get_adapter("oakwid").name == "oakwid"
    assert get_adapter("kwid-oa").name == "oakwid"
    assert get_adapter("works-kwid-oa").name == "oakwid"


def test_parse_oakwid_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "attention",
                "key_display_name": "attention",
                "count": 12,
            },
            {
                "key": "keyword:transformers",
                "key_display_name": "transformers",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://openalex.org/keywords/neural-networks",
                "display_name": "neural networks",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oakwid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "transformers works",
        "attention works",
        "neural networks works",
    ]
    assert hits[0].source == "oakwid"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=keywords.id:transformers" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=keywords.id:attention" in hits[1].url
    assert "5 works" in hits[2].snippet
    assert "filter=keywords.id:neural-networks" in hits[2].url


def test_parse_oakwid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "alpha", "key_display_name": "alpha", "count": 1},
            {"key": "beta", "key_display_name": "beta", "count": 2},
        ]
    }
    hits = parse_oakwid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["beta works"]


def test_parse_oakwid_keywords_list() -> None:
    payload = {
        "keywords": [
            {
                "id": "https://openalex.org/keywords/computer-vision",
                "display_name": "computer vision",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oakwid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "computer vision works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oakwid"
    assert "filter=keywords.id:computer-vision" in hits[0].url
