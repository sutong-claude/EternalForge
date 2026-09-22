from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oalocdname import OaLocDnameAdapter, parse_oalocdname_payload
from tools.research import get_adapter


def test_oalocdname_empty_query() -> None:
    assert OaLocDnameAdapter().search("") == []
    assert OaLocDnameAdapter().search("   ") == []


def test_get_adapter_oalocdname_aliases() -> None:
    assert get_adapter("oalocdname").name == "oalocdname"
    assert get_adapter("locdname-oa").name == "oalocdname"
    assert get_adapter("works-locdname-oa").name == "oalocdname"


def test_parse_oalocdname_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "Nature",
                "key_display_name": "Nature",
                "count": 12,
            },
            {
                "key": "Science",
                "key_display_name": "Science",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "PLOS ONE",
                "display_name": "PLOS ONE",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oalocdname_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Science works", "Nature works", "PLOS ONE works"]
    assert hits[0].source == "oalocdname"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=locations.source.display_name:Science" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=locations.source.display_name:Nature" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oalocdname_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "One", "key_display_name": "One", "count": 1},
            {"key": "Two", "key_display_name": "Two", "count": 2},
        ]
    }
    hits = parse_oalocdname_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Two works"]


def test_parse_oalocdname_names_list() -> None:
    payload = {
        "display_names": [
            {
                "display_name": "Science",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oalocdname_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Science works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oalocdname"
    assert "filter=locations.source.display_name:Science" in hits[0].url
