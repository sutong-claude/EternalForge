from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oacorrinst import OaCorrInstAdapter, parse_oacorrinst_payload
from tools.research import get_adapter


def test_oacorrinst_empty_query() -> None:
    assert OaCorrInstAdapter().search("") == []
    assert OaCorrInstAdapter().search("   ") == []


def test_get_adapter_oacorrinst_aliases() -> None:
    assert get_adapter("oacorrinst").name == "oacorrinst"
    assert get_adapter("corrinst-oa").name == "oacorrinst"
    assert get_adapter("works-corrinst-oa").name == "oacorrinst"


def test_parse_oacorrinst_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/I136199984",
                "key_display_name": "University of Toronto",
                "count": 12,
            },
            {
                "key": "I97018004",
                "key_display_name": "MIT",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://openalex.org/I63966007",
                "display_name": "Stanford University",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oacorrinst_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "MIT works",
        "University of Toronto works",
        "Stanford University works",
    ]
    assert hits[0].source == "oacorrinst"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=corresponding_institution_ids:I97018004" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=corresponding_institution_ids:I136199984" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oacorrinst_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "I1", "key_display_name": "Alpha U", "count": 1},
            {"key": "I2", "key_display_name": "Beta U", "count": 2},
        ]
    }
    hits = parse_oacorrinst_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Beta U works"]


def test_parse_oacorrinst_institution_ids_list() -> None:
    payload = {
        "corresponding_institution_ids": [
            {
                "institution": "https://openalex.org/I136199984",
                "display_name": "University of Toronto",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oacorrinst_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "University of Toronto works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oacorrinst"
    assert "filter=corresponding_institution_ids:I136199984" in hits[0].url
