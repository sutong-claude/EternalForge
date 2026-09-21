from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oabestisoaloc import OaBestIsOaLocAdapter, parse_oabestisoaloc_payload
from tools.research import get_adapter


def test_oabestisoaloc_empty_query() -> None:
    assert OaBestIsOaLocAdapter().search("") == []
    assert OaBestIsOaLocAdapter().search("   ") == []


def test_get_adapter_oabestisoaloc_aliases() -> None:
    assert get_adapter("oabestisoaloc").name == "oabestisoaloc"
    assert get_adapter("bestisoaloc-oa").name == "oabestisoaloc"
    assert get_adapter("works-bestisoaloc-oa").name == "oabestisoaloc"


def test_parse_oabestisoaloc_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oabestisoaloc_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works whose best OA location is OA",
        "Works whose best OA location is not OA",
    ]
    assert hits[0].source == "oabestisoaloc"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=best_oa_location.is_oa:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=best_oa_location.is_oa:false" in hits[1].url


def test_parse_oabestisoaloc_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oabestisoaloc_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works whose best OA location is OA"]


def test_parse_oabestisoaloc_list_shape() -> None:
    payload = {
        "is_oa": [
            {"is_oa": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oabestisoaloc_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works whose best OA location is not OA"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oabestisoaloc"
    assert "filter=best_oa_location.is_oa:false" in hits[0].url
