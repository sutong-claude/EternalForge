from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oabestlic import OaBestLicAdapter, parse_oabestlic_payload
from tools.research import get_adapter


def test_oabestlic_empty_query() -> None:
    assert OaBestLicAdapter().search("") == []
    assert OaBestLicAdapter().search("   ") == []


def test_get_adapter_oabestlic_aliases() -> None:
    assert get_adapter("oabestlic").name == "oabestlic"
    assert get_adapter("bestlic-oa").name == "oabestlic"
    assert get_adapter("works-bestlic-oa").name == "oabestlic"


def test_parse_oabestlic_payload() -> None:
    payload = {
        "group_by": [
            {"key": "cc-by", "key_display_name": "cc-by", "count": 12},
            {"key": "cc-by-nc", "key_display_name": "cc-by-nc", "count": 40, "cited_by_count": 80},
            {"key": "unknown", "count": 3},
            {"key": "cc0", "key_display_name": "cc0", "works_count": 5},
        ]
    }
    hits = parse_oabestlic_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["cc-by-nc works", "cc-by works", "cc0 works"]
    assert hits[0].source == "oabestlic"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=best_oa_location.license:cc-by-nc" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oabestlic_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "cc-by", "key_display_name": "cc-by", "count": 1},
            {"key": "cc-by-sa", "key_display_name": "cc-by-sa", "count": 2},
        ]
    }
    hits = parse_oabestlic_payload(payload, limit=1)
    assert [h.title for h in hits] == ["cc-by-sa works"]


def test_parse_oabestlic_licenses_list() -> None:
    payload = {
        "licenses": [
            {"license": "publisher-specific-oa", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oabestlic_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "publisher-specific-oa works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oabestlic"
    assert "filter=best_oa_location.license:publisher-specific-oa" in hits[0].url
