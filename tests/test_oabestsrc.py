from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oabestsrc import OaBestSrcAdapter, parse_oabestsrc_payload
from tools.research import get_adapter


def test_oabestsrc_empty_query() -> None:
    assert OaBestSrcAdapter().search("") == []
    assert OaBestSrcAdapter().search("   ") == []


def test_get_adapter_oabestsrc_aliases() -> None:
    assert get_adapter("oabestsrc").name == "oabestsrc"
    assert get_adapter("bestsrc-oa").name == "oabestsrc"
    assert get_adapter("works-bestsrc-oa").name == "oabestsrc"


def test_parse_oabestsrc_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/S137773608",
                "key_display_name": "Nature",
                "count": 12,
            },
            {
                "key": "S2764455111",
                "key_display_name": "arXiv",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://openalex.org/S4306400194",
                "display_name": "bioRxiv",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oabestsrc_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["arXiv works", "Nature works", "bioRxiv works"]
    assert hits[0].source == "oabestsrc"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=best_oa_location.source:S2764455111" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=best_oa_location.source:S137773608" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oabestsrc_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "S1", "key_display_name": "Nature", "count": 1},
            {"key": "S2", "key_display_name": "Science", "count": 2},
        ]
    }
    hits = parse_oabestsrc_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Science works"]


def test_parse_oabestsrc_sources_list() -> None:
    payload = {
        "sources": [
            {"source": "https://openalex.org/S137773608", "display_name": "Nature", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oabestsrc_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Nature works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oabestsrc"
    assert "filter=best_oa_location.source:S137773608" in hits[0].url
