from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oapridname import OaPriDnameAdapter, parse_oapridname_payload
from tools.research import get_adapter


def test_oapridname_empty_query() -> None:
    assert OaPriDnameAdapter().search("") == []
    assert OaPriDnameAdapter().search("   ") == []


def test_get_adapter_oapridname_aliases() -> None:
    assert get_adapter("oapridname").name == "oapridname"
    assert get_adapter("pridname-oa").name == "oapridname"
    assert get_adapter("works-pridname-oa").name == "oapridname"


def test_parse_oapridname_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "Nature",
                "key_display_name": "Nature",
                "count": 12,
            },
            {
                "key": "Nature Communications",
                "key_display_name": "Nature Communications",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "Science",
                "display_name": "Science",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oapridname_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Nature Communications works",
        "Nature works",
        "Science works",
    ]
    assert hits[0].source == "oapridname"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=primary_location.source.display_name:Nature%20Communications" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=primary_location.source.display_name:Nature" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oapridname_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "Nature", "key_display_name": "Nature", "count": 1},
            {"key": "Science", "key_display_name": "Science", "count": 2},
        ]
    }
    hits = parse_oapridname_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Science works"]


def test_parse_oapridname_display_names_list() -> None:
    payload = {
        "display_names": [
            {
                "display_name": "Nature Communications",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oapridname_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Nature Communications works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oapridname"
    assert "filter=primary_location.source.display_name:Nature%20Communications" in hits[0].url
