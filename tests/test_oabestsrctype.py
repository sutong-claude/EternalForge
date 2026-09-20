from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oabestsrctype import OaBestSrcTypeAdapter, parse_oabestsrctype_payload
from tools.research import get_adapter


def test_oabestsrctype_empty_query() -> None:
    assert OaBestSrcTypeAdapter().search("") == []
    assert OaBestSrcTypeAdapter().search("   ") == []


def test_get_adapter_oabestsrctype_aliases() -> None:
    assert get_adapter("oabestsrctype").name == "oabestsrctype"
    assert get_adapter("bestsrctype-oa").name == "oabestsrctype"
    assert get_adapter("works-bestsrctype-oa").name == "oabestsrctype"


def test_parse_oabestsrctype_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "journal",
                "key_display_name": "journal",
                "count": 12,
            },
            {
                "key": "repository",
                "key_display_name": "repository",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "conference",
                "display_name": "conference",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oabestsrctype_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["repository works", "journal works", "conference works"]
    assert hits[0].source == "oabestsrctype"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=best_oa_location.source.type:repository" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=best_oa_location.source.type:journal" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oabestsrctype_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "journal", "key_display_name": "journal", "count": 1},
            {"key": "repository", "key_display_name": "repository", "count": 2},
        ]
    }
    hits = parse_oabestsrctype_payload(payload, limit=1)
    assert [h.title for h in hits] == ["repository works"]


def test_parse_oabestsrctype_source_types_list() -> None:
    payload = {
        "source_types": [
            {"source_type": "journal", "display_name": "journal", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oabestsrctype_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "journal works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oabestsrctype"
    assert "filter=best_oa_location.source.type:journal" in hits[0].url
