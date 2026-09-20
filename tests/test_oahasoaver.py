from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasoaver import OaHasOaVerAdapter, parse_oahasoaver_payload
from tools.research import get_adapter


def test_oahasoaver_empty_query() -> None:
    assert OaHasOaVerAdapter().search("") == []
    assert OaHasOaVerAdapter().search("   ") == []


def test_get_adapter_oahasoaver_aliases() -> None:
    assert get_adapter("oahasoaver").name == "oahasoaver"
    assert get_adapter("hasoaver-oa").name == "oahasoaver"
    assert get_adapter("works-hasoaver-oa").name == "oahasoaver"


def test_parse_oahasoaver_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 21, "cited_by_count": 44},
            {"key": "false", "key_display_name": "false", "count": 7},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasoaver_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with OA version",
        "Works without OA version",
    ]
    assert hits[0].source == "oahasoaver"
    assert "21 works" in hits[0].snippet
    assert "44 cites" in hits[0].snippet
    assert "filter=has_oa_version:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "7 works" in hits[1].snippet
    assert "filter=has_oa_version:false" in hits[1].url


def test_parse_oahasoaver_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasoaver_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with OA version"]


def test_parse_oahasoaver_list_shape() -> None:
    payload = {
        "has_oa_version": [
            {"has_oa_version": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasoaver_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without OA version"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasoaver"
    assert "filter=has_oa_version:false" in hits[0].url
