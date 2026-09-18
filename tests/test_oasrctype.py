from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oasrctype import OaSrcTypeAdapter, parse_oasrctype_payload
from tools.research import get_adapter


def test_oasrctype_empty_query() -> None:
    assert OaSrcTypeAdapter().search("") == []
    assert OaSrcTypeAdapter().search("   ") == []


def test_get_adapter_oasrctype_aliases() -> None:
    assert get_adapter("oasrctype").name == "oasrctype"
    assert get_adapter("source-types-oa").name == "oasrctype"
    assert get_adapter("works-source-type-oa").name == "oasrctype"


def test_parse_oasrctype_payload() -> None:
    payload = {
        "group_by": [
            {"key": "repository", "key_display_name": "repository", "count": 10},
            {"key": "journal", "key_display_name": "journal", "count": 40, "cited_by_count": 900},
            {"key": "unknown", "count": 3},
            {"key": "ebook-platform", "key_display_name": "ebook platform", "works_count": 5},
        ]
    }
    hits = parse_oasrctype_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Journal sources", "Repository sources", "Ebook Platform sources"]
    assert hits[0].source == "oasrctype"
    assert "40 works" in hits[0].snippet
    assert "900 cites" in hits[0].snippet
    assert "filter=primary_location.source.type:journal" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "10 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oasrctype_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "conference", "key_display_name": "conference", "count": 1},
            {"key": "journal", "key_display_name": "journal", "count": 2},
        ]
    }
    hits = parse_oasrctype_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Journal sources"]


def test_parse_oasrctype_source_types_list() -> None:
    payload = {
        "source_types": [
            {"source_type": "book series", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oasrctype_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Book Series sources"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oasrctype"
    assert "filter=primary_location.source.type:book-series" in hits[0].url
