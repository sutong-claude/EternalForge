from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthorname import OaAuthorNameAdapter, parse_oaauthorname_payload
from tools.research import get_adapter


def test_oaauthorname_empty_query() -> None:
    assert OaAuthorNameAdapter().search("") == []
    assert OaAuthorNameAdapter().search("   ") == []


def test_get_adapter_oaauthorname_aliases() -> None:
    assert get_adapter("oaauthorname").name == "oaauthorname"
    assert get_adapter("authorname-oa").name == "oaauthorname"
    assert get_adapter("works-authorname-oa").name == "oaauthorname"


def test_parse_oaauthorname_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "Ada Lovelace",
                "key_display_name": "Ada Lovelace",
                "count": 12,
            },
            {
                "key": "Alan Turing",
                "key_display_name": "Alan Turing",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "Grace Hopper",
                "raw_author_name": "Grace Hopper",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaauthorname_payload(payload, limit=5, query="computing")
    assert [h.title for h in hits] == [
        "Alan Turing works",
        "Ada Lovelace works",
        "Grace Hopper works",
    ]
    assert hits[0].source == "oaauthorname"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=authorships.raw_author_name:Alan%20Turing" in hits[0].url
    assert "search=computing" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=authorships.raw_author_name:Ada%20Lovelace" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaauthorname_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "Author A", "key_display_name": "Author A", "count": 1},
            {"key": "Author B", "key_display_name": "Author B", "count": 2},
        ]
    }
    hits = parse_oaauthorname_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Author B works"]


def test_parse_oaauthorname_author_names_list() -> None:
    payload = {
        "raw_author_names": [
            {
                "raw_author_name": "Ada Lovelace",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaauthorname_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Ada Lovelace works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaauthorname"
    assert "filter=authorships.raw_author_name:Ada%20Lovelace" in hits[0].url
