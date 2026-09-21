from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oapriver import OaPriVerAdapter, parse_oapriver_payload
from tools.research import get_adapter


def test_oapriver_empty_query() -> None:
    assert OaPriVerAdapter().search("") == []
    assert OaPriVerAdapter().search("   ") == []


def test_get_adapter_oapriver_aliases() -> None:
    assert get_adapter("oapriver").name == "oapriver"
    assert get_adapter("priver-oa").name == "oapriver"
    assert get_adapter("works-priver-oa").name == "oapriver"


def test_parse_oapriver_payload() -> None:
    payload = {
        "group_by": [
            {"key": "publishedVersion", "key_display_name": "publishedVersion", "count": 12},
            {"key": "acceptedVersion", "key_display_name": "acceptedVersion", "count": 40, "cited_by_count": 80},
            {"key": "unknown", "count": 3},
            {"key": "submittedVersion", "key_display_name": "submittedVersion", "works_count": 5},
        ]
    }
    hits = parse_oapriver_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["acceptedVersion works", "publishedVersion works", "submittedVersion works"]
    assert hits[0].source == "oapriver"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=primary_location.version:acceptedVersion" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oapriver_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "publishedVersion", "key_display_name": "publishedVersion", "count": 1},
            {"key": "acceptedVersion", "key_display_name": "acceptedVersion", "count": 2},
        ]
    }
    hits = parse_oapriver_payload(payload, limit=1)
    assert [h.title for h in hits] == ["acceptedVersion works"]


def test_parse_oapriver_versions_list() -> None:
    payload = {
        "versions": [
            {"version": "publishedVersion", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oapriver_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "publishedVersion works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oapriver"
    assert "filter=primary_location.version:publishedVersion" in hits[0].url
