from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oasdgs import OaSdgsAdapter, parse_oasdgs_payload
from tools.research import get_adapter


def test_oasdgs_empty_query() -> None:
    assert OaSdgsAdapter().search("") == []
    assert OaSdgsAdapter().search("   ") == []


def test_get_adapter_oasdgs_aliases() -> None:
    assert get_adapter("oasdgs").name == "oasdgs"
    assert get_adapter("sdgs-oa").name == "oasdgs"
    assert get_adapter("works-sdgs-oa").name == "oasdgs"


def test_parse_oasdgs_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://metadata.un.org/sdg/3",
                "key_display_name": "Good health and well-being",
                "count": 12,
            },
            {
                "key": "https://metadata.un.org/sdg/13",
                "key_display_name": "Climate action",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://metadata.un.org/sdg/7",
                "display_name": "Affordable and clean energy",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oasdgs_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Climate action works",
        "Good health and well-being works",
        "Affordable and clean energy works",
    ]
    assert hits[0].source == "oasdgs"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=sustainable_development_goals.id:https" in hits[0].url
    assert "sdg/13" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oasdgs_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "https://metadata.un.org/sdg/1", "key_display_name": "No poverty", "count": 1},
            {"key": "https://metadata.un.org/sdg/2", "key_display_name": "Zero hunger", "count": 2},
        ]
    }
    hits = parse_oasdgs_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Zero hunger works"]


def test_parse_oasdgs_sdgs_list() -> None:
    payload = {
        "sdgs": [
            {
                "sdg": "https://metadata.un.org/sdg/4",
                "display_name": "Quality education",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oasdgs_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Quality education works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oasdgs"
    assert "sdg/4" in hits[0].url
    assert "filter=sustainable_development_goals.id:" in hits[0].url
