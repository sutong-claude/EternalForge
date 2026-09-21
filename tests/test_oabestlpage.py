from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oabestlpage import OaBestLpageAdapter, parse_oabestlpage_payload
from tools.research import get_adapter


def test_oabestlpage_empty_query() -> None:
    assert OaBestLpageAdapter().search("") == []
    assert OaBestLpageAdapter().search("   ") == []


def test_get_adapter_oabestlpage_aliases() -> None:
    assert get_adapter("oabestlpage").name == "oabestlpage"
    assert get_adapter("bestlpage-oa").name == "oabestlpage"
    assert get_adapter("works-bestlpage-oa").name == "oabestlpage"


def test_parse_oabestlpage_payload() -> None:
    payload = {
        "group_by": [
            {"key": "https://ex.org/a", "key_display_name": "https://ex.org/a", "count": 12},
            {
                "key": "https://ex.org/b",
                "key_display_name": "https://ex.org/b",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {"key": "https://ex.org/c", "key_display_name": "https://ex.org/c", "works_count": 5},
        ]
    }
    hits = parse_oabestlpage_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "https://ex.org/b works",
        "https://ex.org/a works",
        "https://ex.org/c works",
    ]
    assert hits[0].source == "oabestlpage"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=best_oa_location.landing_page_url:https" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oabestlpage_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "https://ex.org/a", "key_display_name": "https://ex.org/a", "count": 1},
            {"key": "https://ex.org/b", "key_display_name": "https://ex.org/b", "count": 2},
        ]
    }
    hits = parse_oabestlpage_payload(payload, limit=1)
    assert [h.title for h in hits] == ["https://ex.org/b works"]


def test_parse_oabestlpage_landing_page_urls_list() -> None:
    payload = {
        "landing_page_urls": [
            {"landing_page_url": "https://ex.org/z", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oabestlpage_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "https://ex.org/z works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oabestlpage"
    assert "filter=best_oa_location.landing_page_url:https" in hits[0].url
