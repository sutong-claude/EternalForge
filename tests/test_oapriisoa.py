from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oapriisoa import OaPriIsOaAdapter, parse_oapriisoa_payload
from tools.research import get_adapter


def test_oapriisoa_empty_query() -> None:
    assert OaPriIsOaAdapter().search("") == []
    assert OaPriIsOaAdapter().search("   ") == []


def test_get_adapter_oapriisoa_aliases() -> None:
    assert get_adapter("oapriisoa").name == "oapriisoa"
    assert get_adapter("priisoa-oa").name == "oapriisoa"
    assert get_adapter("works-priisoa-oa").name == "oapriisoa"


def test_parse_oapriisoa_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oapriisoa_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works whose primary source is OA",
        "Works whose primary source is not OA",
    ]
    assert hits[0].source == "oapriisoa"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=primary_location.source.is_oa:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=primary_location.source.is_oa:false" in hits[1].url


def test_parse_oapriisoa_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oapriisoa_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works whose primary source is OA"]


def test_parse_oapriisoa_list_shape() -> None:
    payload = {
        "is_oa": [
            {"is_oa": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oapriisoa_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works whose primary source is not OA"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oapriisoa"
    assert "filter=primary_location.source.is_oa:false" in hits[0].url
