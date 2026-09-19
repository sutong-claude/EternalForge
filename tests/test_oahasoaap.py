from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasoaap import OaHasOaapAdapter, parse_oahasoaap_payload
from tools.research import get_adapter


def test_oahasoaap_empty_query() -> None:
    assert OaHasOaapAdapter().search("") == []
    assert OaHasOaapAdapter().search("   ") == []


def test_get_adapter_oahasoaap_aliases() -> None:
    assert get_adapter("oahasoaap").name == "oahasoaap"
    assert get_adapter("hasoaap-oa").name == "oahasoaap"
    assert get_adapter("works-hasoaap-oa").name == "oahasoaap"


def test_parse_oahasoaap_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 22, "cited_by_count": 55},
            {"key": "false", "key_display_name": "false", "count": 4},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasoaap_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with accepted or published OA",
        "Works without accepted or published OA",
    ]
    assert hits[0].source == "oahasoaap"
    assert "22 works" in hits[0].snippet
    assert "55 cites" in hits[0].snippet
    assert "filter=has_oa_accepted_or_published:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "4 works" in hits[1].snippet
    assert "filter=has_oa_accepted_or_published:false" in hits[1].url


def test_parse_oahasoaap_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasoaap_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with accepted or published OA"]


def test_parse_oahasoaap_list_shape() -> None:
    payload = {
        "has_oa_accepted_or_published": [
            {"has_oa_accepted_or_published": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasoaap_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without accepted or published OA"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasoaap"
    assert "filter=has_oa_accepted_or_published:false" in hits[0].url
