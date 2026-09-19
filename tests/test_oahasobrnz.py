from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasobrnz import OaHasOaBronzeAdapter, parse_oahasobrnz_payload
from tools.research import get_adapter


def test_oahasobrnz_empty_query() -> None:
    assert OaHasOaBronzeAdapter().search("") == []
    assert OaHasOaBronzeAdapter().search("   ") == []


def test_get_adapter_oahasobrnz_aliases() -> None:
    assert get_adapter("oahasobrnz").name == "oahasobrnz"
    assert get_adapter("hasobrnz-oa").name == "oahasobrnz"
    assert get_adapter("works-hasobrnz-oa").name == "oahasobrnz"


def test_parse_oahasobrnz_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasobrnz_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with bronze OA",
        "Works without bronze OA",
    ]
    assert hits[0].source == "oahasobrnz"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=has_oa_bronze:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=has_oa_bronze:false" in hits[1].url


def test_parse_oahasobrnz_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasobrnz_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with bronze OA"]


def test_parse_oahasobrnz_list_shape() -> None:
    payload = {
        "has_oa_bronze": [
            {"has_oa_bronze": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasobrnz_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without bronze OA"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasobrnz"
    assert "filter=has_oa_bronze:false" in hits[0].url
