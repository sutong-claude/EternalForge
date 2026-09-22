from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaloclicid import OaLocLicIdAdapter, parse_oaloclicid_payload
from tools.research import get_adapter


def test_oaloclicid_empty_query() -> None:
    assert OaLocLicIdAdapter().search("") == []
    assert OaLocLicIdAdapter().search("   ") == []


def test_get_adapter_oaloclicid_aliases() -> None:
    assert get_adapter("oaloclicid").name == "oaloclicid"
    assert get_adapter("loclicid-oa").name == "oaloclicid"
    assert get_adapter("works-loclicid-oa").name == "oaloclicid"


def test_parse_oaloclicid_payload() -> None:
    payload = {
        "group_by": [
            {"key": "cc-by", "key_display_name": "cc-by", "count": 12},
            {"key": "cc-by-nc", "key_display_name": "cc-by-nc", "count": 40, "cited_by_count": 80},
            {"key": "unknown", "count": 3},
            {"key": "cc0", "key_display_name": "cc0", "works_count": 5},
        ]
    }
    hits = parse_oaloclicid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["cc-by-nc works", "cc-by works", "cc0 works"]
    assert hits[0].source == "oaloclicid"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=locations.license_id:cc-by-nc" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oaloclicid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "cc-by", "key_display_name": "cc-by", "count": 1},
            {"key": "cc-by-nc", "key_display_name": "cc-by-nc", "count": 2},
        ]
    }
    hits = parse_oaloclicid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["cc-by-nc works"]


def test_parse_oaloclicid_license_ids_list() -> None:
    payload = {
        "license_ids": [
            {"license_id": "cc-by", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oaloclicid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "cc-by works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaloclicid"
    assert "filter=locations.license_id:cc-by" in hits[0].url
