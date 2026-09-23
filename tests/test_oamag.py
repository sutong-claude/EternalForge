from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oamag import OaMagAdapter, parse_oamag_payload
from tools.research import get_adapter


def test_oamag_empty_query() -> None:
    assert OaMagAdapter().search("") == []
    assert OaMagAdapter().search("   ") == []


def test_get_adapter_oamag_aliases() -> None:
    assert get_adapter("oamag").name == "oamag"
    assert get_adapter("mag-oa").name == "oamag"
    assert get_adapter("works-mag-oa").name == "oamag"


def test_parse_oamag_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "2152149102",
                "key_display_name": "2152149102",
                "count": 12,
            },
            {
                "key": "2102581879",
                "key_display_name": "2102581879",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "1986993601",
                "display_name": "1986993601",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oamag_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "2102581879 works",
        "2152149102 works",
        "1986993601 works",
    ]
    assert hits[0].source == "oamag"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=ids.mag:2102581879" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=ids.mag:2152149102" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oamag_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "1", "key_display_name": "1", "count": 1},
            {"key": "2", "key_display_name": "2", "count": 2},
        ]
    }
    hits = parse_oamag_payload(payload, limit=1)
    assert [h.title for h in hits] == ["2 works"]


def test_parse_oamag_mags_list() -> None:
    payload = {
        "mags": [
            {
                "mag": "2152149102",
                "display_name": "2152149102",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oamag_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "2152149102 works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oamag"
    assert "filter=ids.mag:2152149102" in hits[0].url
