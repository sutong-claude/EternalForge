from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaaward import OaAwardAdapter, parse_oaaward_payload
from tools.research import get_adapter


def test_oaaward_empty_query() -> None:
    assert OaAwardAdapter().search("") == []
    assert OaAwardAdapter().search("   ") == []


def test_get_adapter_oaaward_aliases() -> None:
    assert get_adapter("oaaward").name == "oaaward"
    assert get_adapter("award-oa").name == "oaaward"
    assert get_adapter("works-award-oa").name == "oaaward"


def test_parse_oaaward_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "R01GM123456",
                "key_display_name": "R01GM123456",
                "count": 12,
            },
            {
                "key": "award:EP/T00000X/1",
                "key_display_name": "EP/T00000X/1",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "ANR-21-CE23-0001",
                "display_name": "ANR-21-CE23-0001",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaaward_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "EP/T00000X/1 works",
        "R01GM123456 works",
        "ANR-21-CE23-0001 works",
    ]
    assert hits[0].source == "oaaward"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=grants.award_id:EP/T00000X/1" in hits[0].url or "filter=grants.award_id:EP%2FT00000X%2F1" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet
    assert "filter=grants.award_id:ANR-21-CE23-0001" in hits[2].url


def test_parse_oaaward_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "A1", "key_display_name": "Alpha Award", "count": 1},
            {"key": "A2", "key_display_name": "Beta Award", "count": 2},
        ]
    }
    hits = parse_oaaward_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Beta Award works"]


def test_parse_oaaward_awards_list() -> None:
    payload = {
        "awards": [
            {
                "award_id": "HORIZON-101000001",
                "display_name": "HORIZON-101000001",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaaward_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "HORIZON-101000001 works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaaward"
    assert "filter=grants.award_id:HORIZON-101000001" in hits[0].url
