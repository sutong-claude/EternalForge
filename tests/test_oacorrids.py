from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oacorrids import OaCorrIdsAdapter, parse_oacorrids_payload
from tools.research import get_adapter


def test_oacorrids_empty_query() -> None:
    assert OaCorrIdsAdapter().search("") == []
    assert OaCorrIdsAdapter().search("   ") == []


def test_get_adapter_oacorrids_aliases() -> None:
    assert get_adapter("oacorrids").name == "oacorrids"
    assert get_adapter("corrids-oa").name == "oacorrids"
    assert get_adapter("works-corrids-oa").name == "oacorrids"


def test_parse_oacorrids_payload() -> None:
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
    hits = parse_oacorrids_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Yann LeCun works",
        "Yoshua Bengio works",
        "Geoffrey Hinton works",
    ]
    assert hits[0].source == "oacorrids"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=corresponding_author_ids:A1969205034" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=corresponding_author_ids:A5023888391" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oacorrids_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "A1", "key_display_name": "Alice", "count": 1},
            {"key": "A2", "key_display_name": "Bob", "count": 2},
        ]
    }
    hits = parse_oacorrids_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Bob works"]


def test_parse_oacorrids_author_ids_list() -> None:
    payload = {
        "corresponding_author_ids": [
            {
                "author": "https://openalex.org/A5023888391",
                "display_name": "Yoshua Bengio",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oacorrids_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Yoshua Bengio works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oacorrids"
    assert "filter=corresponding_author_ids:A5023888391" in hits[0].url
