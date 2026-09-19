from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasoapub import OaHasOaPubAdapter, parse_oahasoapub_payload
from tools.research import get_adapter


def test_oahasoapub_empty_query() -> None:
    assert OaHasOaPubAdapter().search("") == []
    assert OaHasOaPubAdapter().search("   ") == []


def test_get_adapter_oahasoapub_aliases() -> None:
    assert get_adapter("oahasoapub").name == "oahasoapub"
    assert get_adapter("hasoapub-oa").name == "oahasoapub"
    assert get_adapter("works-hasoapub-oa").name == "oahasoapub"


def test_parse_oahasoapub_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 21, "cited_by_count": 44},
            {"key": "false", "key_display_name": "false", "count": 7},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasoapub_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with OA publisher copy",
        "Works without OA publisher copy",
    ]
    assert hits[0].source == "oahasoapub"
    assert "21 works" in hits[0].snippet
    assert "44 cites" in hits[0].snippet
    assert "filter=has_oa_publisher:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "7 works" in hits[1].snippet
    assert "filter=has_oa_publisher:false" in hits[1].url


def test_parse_oahasoapub_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasoapub_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with OA publisher copy"]


def test_parse_oahasoapub_list_shape() -> None:
    payload = {
        "has_oa_publisher": [
            {"has_oa_publisher": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasoapub_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without OA publisher copy"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasoapub"
    assert "filter=has_oa_publisher:false" in hits[0].url
