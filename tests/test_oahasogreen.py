from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasogreen import OaHasOaGreenAdapter, parse_oahasogreen_payload
from tools.research import get_adapter


def test_oahasogreen_empty_query() -> None:
    assert OaHasOaGreenAdapter().search("") == []
    assert OaHasOaGreenAdapter().search("   ") == []


def test_get_adapter_oahasogreen_aliases() -> None:
    assert get_adapter("oahasogreen").name == "oahasogreen"
    assert get_adapter("hasogreen-oa").name == "oahasogreen"
    assert get_adapter("works-hasogreen-oa").name == "oahasogreen"


def test_parse_oahasogreen_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasogreen_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with green OA",
        "Works without green OA",
    ]
    assert hits[0].source == "oahasogreen"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=has_oa_green:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=has_oa_green:false" in hits[1].url


def test_parse_oahasogreen_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasogreen_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with green OA"]


def test_parse_oahasogreen_list_shape() -> None:
    payload = {
        "has_oa_green": [
            {"has_oa_green": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasogreen_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without green OA"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasogreen"
    assert "filter=has_oa_green:false" in hits[0].url
