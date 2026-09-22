from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthdname import OaAuthDnameAdapter, parse_oaauthdname_payload
from tools.research import get_adapter


def test_oaauthdname_empty_query() -> None:
    assert OaAuthDnameAdapter().search("") == []
    assert OaAuthDnameAdapter().search("   ") == []


def test_get_adapter_oaauthdname_aliases() -> None:
    assert get_adapter("oaauthdname").name == "oaauthdname"
    assert get_adapter("authdname-oa").name == "oaauthdname"
    assert get_adapter("works-authdname-oa").name == "oaauthdname"


def test_parse_oaauthdname_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "University of Michigan",
                "key_display_name": "University of Michigan",
                "count": 12,
            },
            {
                "key": "Harvard University",
                "key_display_name": "Harvard University",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "Stanford University",
                "display_name": "Stanford University",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaauthdname_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Harvard University works",
        "University of Michigan works",
        "Stanford University works",
    ]
    assert hits[0].source == "oaauthdname"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=authorships.institutions.display_name:Harvard%20University" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=authorships.institutions.display_name:University%20of%20Michigan" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaauthdname_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "MIT", "key_display_name": "MIT", "count": 1},
            {"key": "Oxford", "key_display_name": "Oxford", "count": 2},
        ]
    }
    hits = parse_oaauthdname_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Oxford works"]


def test_parse_oaauthdname_names_list() -> None:
    payload = {
        "display_names": [
            {
                "display_name": "University of Michigan",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaauthdname_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "University of Michigan works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaauthdname"
    assert "filter=authorships.institutions.display_name:University%20of%20Michigan" in hits[0].url
