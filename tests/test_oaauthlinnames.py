from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthlinnames import OaAuthLinNamesAdapter, parse_oaauthlinnames_payload
from tools.research import get_adapter


def test_oaauthlinnames_empty_query() -> None:
    assert OaAuthLinNamesAdapter().search("") == []
    assert OaAuthLinNamesAdapter().search("   ") == []


def test_get_adapter_oaauthlinnames_aliases() -> None:
    assert get_adapter("oaauthlinnames").name == "oaauthlinnames"
    assert get_adapter("authlinnames-oa").name == "oaauthlinnames"
    assert get_adapter("works-authlinnames-oa").name == "oaauthlinnames"


def test_parse_oaauthlinnames_payload() -> None:
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
    hits = parse_oaauthlinnames_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Harvard University works",
        "University of Michigan works",
        "Stanford University works",
    ]
    assert hits[0].source == "oaauthlinnames"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=authorships.institutions.lineage_names:Harvard%20University" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=authorships.institutions.lineage_names:University%20of%20Michigan" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaauthlinnames_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "One", "key_display_name": "One", "count": 1},
            {"key": "Two", "key_display_name": "Two", "count": 2},
        ]
    }
    hits = parse_oaauthlinnames_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Two works"]


def test_parse_oaauthlinnames_lineage_names_list() -> None:
    payload = {
        "lineage_names": [
            {
                "lineage_name": "Harvard University",
                "display_name": "Harvard University",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaauthlinnames_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Harvard University works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaauthlinnames"
    assert "filter=authorships.institutions.lineage_names:Harvard%20University" in hits[0].url
