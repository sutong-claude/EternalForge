from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oagrants import OaGrantsAdapter, parse_oagrants_payload
from tools.research import get_adapter


def test_oagrants_empty_query() -> None:
    assert OaGrantsAdapter().search("") == []
    assert OaGrantsAdapter().search("   ") == []


def test_get_adapter_oagrants_aliases() -> None:
    assert get_adapter("oagrants").name == "oagrants"
    assert get_adapter("grants-oa").name == "oagrants"
    assert get_adapter("works-grants-oa").name == "oagrants"


def test_parse_oagrants_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/F4320332161",
                "key_display_name": "National Science Foundation",
                "count": 12,
            },
            {
                "key": "https://openalex.org/F4320306076",
                "key_display_name": "National Institutes of Health",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "F4320320001",
                "display_name": "European Research Council",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oagrants_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "National Institutes of Health works",
        "National Science Foundation works",
        "European Research Council works",
    ]
    assert hits[0].source == "oagrants"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=grants.funder:F4320306076" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet
    assert "filter=grants.funder:F4320320001" in hits[2].url


def test_parse_oagrants_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "F1", "key_display_name": "Alpha Fund", "count": 1},
            {"key": "F2", "key_display_name": "Beta Fund", "count": 2},
        ]
    }
    hits = parse_oagrants_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Beta Fund works"]


def test_parse_oagrants_funders_list() -> None:
    payload = {
        "funders": [
            {
                "funder": "https://openalex.org/F4320339999",
                "display_name": "Wellcome Trust",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oagrants_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Wellcome Trust works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oagrants"
    assert "filter=grants.funder:F4320339999" in hits[0].url
