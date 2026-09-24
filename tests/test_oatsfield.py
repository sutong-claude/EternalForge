from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oatsfield import OaTsFieldAdapter, parse_oatsfield_payload
from tools.research import get_adapter


def test_oatsfield_empty_query() -> None:
    assert OaTsFieldAdapter().search("") == []
    assert OaTsFieldAdapter().search("   ") == []


def test_get_adapter_oatsfield_aliases() -> None:
    assert get_adapter("oatsfield").name == "oatsfield"
    assert get_adapter("subfield-oa").name == "oatsfield"
    assert get_adapter("works-subfield-oa").name == "oatsfield"


def test_parse_oatsfield_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/subfields/1702",
                "key_display_name": "Artificial intelligence",
                "count": 12,
            },
            {
                "key": "subfield:1705",
                "key_display_name": "Information systems",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "1706",
                "display_name": "Computer vision",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oatsfield_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Information systems works",
        "Artificial intelligence works",
        "Computer vision works",
    ]
    assert hits[0].source == "oatsfield"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=topics.subfield.id:1705" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=topics.subfield.id:1702" in hits[1].url
    assert "5 works" in hits[2].snippet
    assert "filter=topics.subfield.id:1706" in hits[2].url


def test_parse_oatsfield_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "1001", "key_display_name": "Alpha Subfield", "count": 1},
            {"key": "1002", "key_display_name": "Beta Subfield", "count": 2},
        ]
    }
    hits = parse_oatsfield_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Beta Subfield works"]


def test_parse_oatsfield_subfields_list() -> None:
    payload = {
        "subfields": [
            {
                "id": "https://openalex.org/subfields/2002",
                "display_name": "Economics",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oatsfield_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Economics works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oatsfield"
    assert "filter=topics.subfield.id:2002" in hits[0].url
