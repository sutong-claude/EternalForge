from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasoaalicid import OaHasOaLicIdAdapter, parse_oahasoaalicid_payload
from tools.research import get_adapter


def test_oahasoaalicid_empty_query() -> None:
    assert OaHasOaLicIdAdapter().search("") == []
    assert OaHasOaLicIdAdapter().search("   ") == []


def test_get_adapter_oahasoaalicid_aliases() -> None:
    assert get_adapter("oahasoaalicid").name == "oahasoaalicid"
    assert get_adapter("hasoaalicid-oa").name == "oahasoaalicid"
    assert get_adapter("works-hasoaalicid-oa").name == "oahasoaalicid"


def test_parse_oahasoaalicid_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 21, "cited_by_count": 44},
            {"key": "false", "key_display_name": "false", "count": 7},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasoaalicid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with OA license id",
        "Works without OA license id",
    ]
    assert hits[0].source == "oahasoaalicid"
    assert "21 works" in hits[0].snippet
    assert "44 cites" in hits[0].snippet
    assert "filter=has_oa_license_id:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "7 works" in hits[1].snippet
    assert "filter=has_oa_license_id:false" in hits[1].url


def test_parse_oahasoaalicid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasoaalicid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with OA license id"]


def test_parse_oahasoaalicid_list_shape() -> None:
    payload = {
        "has_oa_license_id": [
            {"has_oa_license_id": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasoaalicid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without OA license id"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasoaalicid"
    assert "filter=has_oa_license_id:false" in hits[0].url
