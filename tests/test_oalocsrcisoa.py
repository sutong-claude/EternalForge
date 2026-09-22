from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oalocsrcisoa import OaLocSrcIsOaAdapter, parse_oalocsrcisoa_payload
from tools.research import get_adapter


def test_oalocsrcisoa_empty_query() -> None:
    assert OaLocSrcIsOaAdapter().search("") == []
    assert OaLocSrcIsOaAdapter().search("   ") == []


def test_get_adapter_oalocsrcisoa_aliases() -> None:
    assert get_adapter("oalocsrcisoa").name == "oalocsrcisoa"
    assert get_adapter("locsrcisoa-oa").name == "oalocsrcisoa"
    assert get_adapter("works-locsrcisoa-oa").name == "oalocsrcisoa"


def test_parse_oalocsrcisoa_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oalocsrcisoa_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with an OA location source",
        "Works without an OA location source",
    ]
    assert hits[0].source == "oalocsrcisoa"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=locations.source.is_oa:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=locations.source.is_oa:false" in hits[1].url


def test_parse_oalocsrcisoa_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oalocsrcisoa_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with an OA location source"]


def test_parse_oalocsrcisoa_list_shape() -> None:
    payload = {
        "is_oa": [
            {"is_oa": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oalocsrcisoa_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without an OA location source"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oalocsrcisoa"
    assert "filter=locations.source.is_oa:false" in hits[0].url
