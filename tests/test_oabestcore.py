from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oabestcore import OaBestCoreAdapter, parse_oabestcore_payload
from tools.research import get_adapter


def test_oabestcore_empty_query() -> None:
    assert OaBestCoreAdapter().search("") == []
    assert OaBestCoreAdapter().search("   ") == []


def test_get_adapter_oabestcore_aliases() -> None:
    assert get_adapter("oabestcore").name == "oabestcore"
    assert get_adapter("bestcore-oa").name == "oabestcore"
    assert get_adapter("works-bestcore-oa").name == "oabestcore"


def test_parse_oabestcore_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oabestcore_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works whose best OA source is core",
        "Works whose best OA source is not core",
    ]
    assert hits[0].source == "oabestcore"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=best_oa_location.source.is_core:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=best_oa_location.source.is_core:false" in hits[1].url


def test_parse_oabestcore_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oabestcore_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works whose best OA source is core"]


def test_parse_oabestcore_list_shape() -> None:
    payload = {
        "is_core": [
            {"is_core": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oabestcore_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works whose best OA source is not core"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oabestcore"
    assert "filter=best_oa_location.source.is_core:false" in hits[0].url
