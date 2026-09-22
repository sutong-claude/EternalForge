from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oalocver import OaLocVerAdapter, parse_oalocver_payload
from tools.research import get_adapter


def test_oalocver_empty_query() -> None:
    assert OaLocVerAdapter().search("") == []
    assert OaLocVerAdapter().search("   ") == []


def test_get_adapter_oalocver_aliases() -> None:
    assert get_adapter("oalocver").name == "oalocver"
    assert get_adapter("locver-oa").name == "oalocver"
    assert get_adapter("works-locver-oa").name == "oalocver"


def test_parse_oalocver_payload() -> None:
    payload = {
        "group_by": [
            {"key": "publishedVersion", "key_display_name": "publishedVersion", "count": 12},
            {"key": "acceptedVersion", "key_display_name": "acceptedVersion", "count": 40, "cited_by_count": 80},
            {"key": "unknown", "count": 3},
            {"key": "submittedVersion", "key_display_name": "submittedVersion", "works_count": 5},
        ]
    }
    hits = parse_oalocver_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["acceptedVersion works", "publishedVersion works", "submittedVersion works"]
    assert hits[0].source == "oalocver"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=locations.version:acceptedversion" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oalocver_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "publishedVersion", "key_display_name": "publishedVersion", "count": 1},
            {"key": "acceptedVersion", "key_display_name": "acceptedVersion", "count": 2},
        ]
    }
    hits = parse_oalocver_payload(payload, limit=1)
    assert [h.title for h in hits] == ["acceptedVersion works"]


def test_parse_oalocver_versions_list() -> None:
    payload = {
        "versions": [
            {"version": "publishedVersion", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oalocver_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "publishedVersion works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oalocver"
    assert "filter=locations.version:publishedversion" in hits[0].url
