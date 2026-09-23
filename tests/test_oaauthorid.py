from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthorid import OaAuthorIdAdapter, parse_oaauthorid_payload
from tools.research import get_adapter


def test_oaauthorid_empty_query() -> None:
    assert OaAuthorIdAdapter().search("") == []
    assert OaAuthorIdAdapter().search("   ") == []


def test_get_adapter_oaauthorid_aliases() -> None:
    assert get_adapter("oaauthorid").name == "oaauthorid"
    assert get_adapter("authorid-oa").name == "oaauthorid"
    assert get_adapter("works-authorid-oa").name == "oaauthorid"


def test_parse_oaauthorid_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/A5023888391",
                "key_display_name": "Yoshua Bengio",
                "count": 12,
            },
            {
                "key": "A1969205034",
                "key_display_name": "Yann LeCun",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://openalex.org/A2110161625",
                "display_name": "Geoffrey Hinton",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaauthorid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Yann LeCun works",
        "Yoshua Bengio works",
        "Geoffrey Hinton works",
    ]
    assert hits[0].source == "oaauthorid"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=authorships.author.id:A1969205034" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=authorships.author.id:A5023888391" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaauthorid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "A1", "key_display_name": "Alice", "count": 1},
            {"key": "A2", "key_display_name": "Bob", "count": 2},
        ]
    }
    hits = parse_oaauthorid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Bob works"]


def test_parse_oaauthorid_author_ids_list() -> None:
    payload = {
        "author_ids": [
            {
                "author": "https://openalex.org/A5023888391",
                "display_name": "Yoshua Bengio",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaauthorid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Yoshua Bengio works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaauthorid"
    assert "filter=authorships.author.id:A5023888391" in hits[0].url
