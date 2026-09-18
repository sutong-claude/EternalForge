from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OaYearAdapter, get_adapter, parse_oayear_payload


def test_oayear_empty_query() -> None:
    assert OaYearAdapter().search("") == []
    assert OaYearAdapter().search("   ") == []


def test_get_adapter_oayear_aliases() -> None:
    assert get_adapter("oayear").name == "oayear"
    assert get_adapter("years-oa").name == "oayear"
    assert get_adapter("works-year-oa").name == "oayear"


def test_parse_oayear_payload() -> None:
    payload = {
        "group_by": [
            {"key": "2020", "key_display_name": "2020", "count": 10},
            {"key": "2024", "count": 40, "cited_by_count": 900},
            {"key": "unknown", "count": 3},
            {"key": "2019", "works_count": 5},
        ]
    }
    hits = parse_oayear_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["2024 works", "2020 works", "2019 works"]
    assert hits[0].source == "oayear"
    assert "40 works" in hits[0].snippet
    assert "900 cites" in hits[0].snippet
    assert "filter=publication_year:2024" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "10 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oayear_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "2021", "count": 1},
            {"key": "2022", "count": 2},
        ]
    }
    hits = parse_oayear_payload(payload, limit=1)
    assert [h.title for h in hits] == ["2022 works"]


def test_parse_oayear_counts_by_year() -> None:
    payload = {
        "counts_by_year": [
            {"year": 2018, "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oayear_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "2018 works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oayear"
