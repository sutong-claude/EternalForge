from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasoasub import OaHasOaSubAdapter, parse_oahasoasub_payload
from tools.research import get_adapter


def test_oahasoasub_empty_query() -> None:
    assert OaHasOaSubAdapter().search("") == []
    assert OaHasOaSubAdapter().search("   ") == []


def test_get_adapter_oahasoasub_aliases() -> None:
    assert get_adapter("oahasoasub").name == "oahasoasub"
    assert get_adapter("hasoasub-oa").name == "oahasoasub"
    assert get_adapter("works-hasoasub-oa").name == "oahasoasub"


def test_parse_oahasoasub_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasoasub_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with submitted OA",
        "Works without submitted OA",
    ]
    assert hits[0].source == "oahasoasub"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=has_oa_submitted:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=has_oa_submitted:false" in hits[1].url


def test_parse_oahasoasub_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasoasub_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with submitted OA"]


def test_parse_oahasoasub_list_shape() -> None:
    payload = {
        "has_oa_submitted": [
            {"has_oa_submitted": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasoasub_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without submitted OA"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasoasub"
    assert "filter=has_oa_submitted:false" in hits[0].url
