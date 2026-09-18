from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OaTypeAdapter, get_adapter, parse_oatype_payload


def test_oatype_empty_query() -> None:
    assert OaTypeAdapter().search("") == []
    assert OaTypeAdapter().search("   ") == []


def test_get_adapter_oatype_aliases() -> None:
    assert get_adapter("oatype").name == "oatype"
    assert get_adapter("types-oa").name == "oatype"
    assert get_adapter("works-type-oa").name == "oatype"


def test_parse_oatype_payload() -> None:
    payload = {
        "group_by": [
            {"key": "book", "key_display_name": "book", "count": 10},
            {"key": "article", "count": 40, "cited_by_count": 900},
            {"key": "unknown", "count": 3},
            {"key": "dataset", "works_count": 5},
        ]
    }
    hits = parse_oatype_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["article works", "book works", "dataset works"]
    assert hits[0].source == "oatype"
    assert "40 works" in hits[0].snippet
    assert "900 cites" in hits[0].snippet
    assert "filter=type:article" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "10 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oatype_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "book", "count": 1},
            {"key": "article", "count": 2},
        ]
    }
    hits = parse_oatype_payload(payload, limit=1)
    assert [h.title for h in hits] == ["article works"]


def test_parse_oatype_types_list() -> None:
    payload = {
        "types": [
            {"type": "preprint", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oatype_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "preprint works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oatype"
    assert "filter=type:preprint" in hits[0].url
