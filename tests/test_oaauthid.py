from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthid import OaAuthIdAdapter, parse_oaauthid_payload
from tools.research import get_adapter


def test_oaauthid_empty_query() -> None:
    assert OaAuthIdAdapter().search("") == []
    assert OaAuthIdAdapter().search("   ") == []


def test_get_adapter_oaauthid_aliases() -> None:
    assert get_adapter("oaauthid").name == "oaauthid"
    assert get_adapter("authid-oa").name == "oaauthid"
    assert get_adapter("works-authid-oa").name == "oaauthid"


def test_parse_oaauthid_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/I27837315",
                "key_display_name": "University of Michigan",
                "count": 12,
            },
            {
                "key": "I136199984",
                "key_display_name": "Harvard University",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://openalex.org/I1299303238",
                "display_name": "Stanford University",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaauthid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Harvard University works",
        "University of Michigan works",
        "Stanford University works",
    ]
    assert hits[0].source == "oaauthid"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=authorships.institutions.id:I136199984" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=authorships.institutions.id:I27837315" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaauthid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "I1", "key_display_name": "MIT", "count": 1},
            {"key": "I2", "key_display_name": "Oxford", "count": 2},
        ]
    }
    hits = parse_oaauthid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Oxford works"]


def test_parse_oaauthid_institution_ids_list() -> None:
    payload = {
        "institution_ids": [
            {
                "institution": "https://openalex.org/I27837315",
                "display_name": "University of Michigan",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaauthid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "University of Michigan works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaauthid"
    assert "filter=authorships.institutions.id:I27837315" in hits[0].url
