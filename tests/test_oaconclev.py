from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaconclev import OaConcLevAdapter, parse_oaconclev_payload
from tools.research import get_adapter


def test_oaconclev_empty_query() -> None:
    assert OaConcLevAdapter().search("") == []
    assert OaConcLevAdapter().search("   ") == []


def test_get_adapter_oaconclev_aliases() -> None:
    assert get_adapter("oaconclev").name == "oaconclev"
    assert get_adapter("conclev-oa").name == "oaconclev"
    assert get_adapter("works-conclev-oa").name == "oaconclev"


def test_parse_oaconclev_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "1",
                "key_display_name": "1",
                "count": 12,
            },
            {
                "key": "level:2",
                "key_display_name": "2",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": 0,
                "display_name": "0",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaconclev_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "level 2 works",
        "level 1 works",
        "level 0 works",
    ]
    assert hits[0].source == "oaconclev"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=concepts.level:2" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=concepts.level:1" in hits[1].url
    assert "5 works" in hits[2].snippet
    assert "filter=concepts.level:0" in hits[2].url


def test_parse_oaconclev_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "0", "key_display_name": "0", "count": 1},
            {"key": "3", "key_display_name": "3", "count": 2},
        ]
    }
    hits = parse_oaconclev_payload(payload, limit=1)
    assert [h.title for h in hits] == ["level 3 works"]


def test_parse_oaconclev_levels_list() -> None:
    payload = {
        "levels": [
            {
                "id": "2",
                "display_name": "2",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaconclev_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "level 2 works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaconclev"
    assert "filter=concepts.level:2" in hits[0].url
