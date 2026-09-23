from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthoraffils import OaAuthorAffilsAdapter, parse_oaauthoraffils_payload
from tools.research import get_adapter


def test_oaauthoraffils_empty_query() -> None:
    assert OaAuthorAffilsAdapter().search("") == []
    assert OaAuthorAffilsAdapter().search("   ") == []


def test_get_adapter_oaauthoraffils_aliases() -> None:
    assert get_adapter("oaauthoraffils").name == "oaauthoraffils"
    assert get_adapter("authoraffils-oa").name == "oaauthoraffils"
    assert get_adapter("works-authoraffils-oa").name == "oaauthoraffils"


def test_parse_oaauthoraffils_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "Brown University",
                "key_display_name": "Brown University",
                "count": 12,
            },
            {
                "key": "New York University",
                "key_display_name": "New York University",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "University of Toronto",
                "raw_affiliation_strings": "University of Toronto",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaauthoraffils_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "New York University works",
        "Brown University works",
        "University of Toronto works",
    ]
    assert hits[0].source == "oaauthoraffils"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=authorships.raw_affiliation_strings:New%20York%20University" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=authorships.raw_affiliation_strings:Brown%20University" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaauthoraffils_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "Lab A", "key_display_name": "Lab A", "count": 1},
            {"key": "Lab B", "key_display_name": "Lab B", "count": 2},
        ]
    }
    hits = parse_oaauthoraffils_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Lab B works"]


def test_parse_oaauthoraffils_affiliations_list() -> None:
    payload = {
        "raw_affiliation_strings": [
            {
                "raw_affiliation_strings": "Brown University",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaauthoraffils_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Brown University works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaauthoraffils"
    assert "filter=authorships.raw_affiliation_strings:Brown%20University" in hits[0].url
