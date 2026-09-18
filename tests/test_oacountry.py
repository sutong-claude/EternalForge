from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oacountry import OaCountryAdapter, parse_oacountry_payload
from tools.research import get_adapter


def test_oacountry_empty_query() -> None:
    assert OaCountryAdapter().search("") == []
    assert OaCountryAdapter().search("   ") == []


def test_get_adapter_oacountry_aliases() -> None:
    assert get_adapter("oacountry").name == "oacountry"
    assert get_adapter("countries-oa").name == "oacountry"
    assert get_adapter("works-country-oa").name == "oacountry"


def test_parse_oacountry_payload() -> None:
    payload = {
        "group_by": [
            {"key": "GB", "key_display_name": "United Kingdom", "count": 10},
            {"key": "US", "key_display_name": "United States", "count": 40, "cited_by_count": 900},
            {"key": "unknown", "count": 3},
            {"key": "DE", "key_display_name": "Germany", "works_count": 5},
        ]
    }
    hits = parse_oacountry_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["United States works", "United Kingdom works", "Germany works"]
    assert hits[0].source == "oacountry"
    assert "40 works" in hits[0].snippet
    assert "900 cites" in hits[0].snippet
    assert "filter=authorships.countries:US" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "10 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oacountry_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "FR", "key_display_name": "France", "count": 1},
            {"key": "US", "key_display_name": "United States", "count": 2},
        ]
    }
    hits = parse_oacountry_payload(payload, limit=1)
    assert [h.title for h in hits] == ["United States works"]


def test_parse_oacountry_countries_list() -> None:
    payload = {
        "countries": [
            {"country": "Japan", "country_code": "JP", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oacountry_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Japan works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oacountry"
    assert "filter=authorships.countries:JP" in hits[0].url
