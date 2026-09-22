from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthcc import OaAuthCcAdapter, parse_oaauthcc_payload
from tools.research import get_adapter


def test_oaauthcc_empty_query() -> None:
    assert OaAuthCcAdapter().search("") == []
    assert OaAuthCcAdapter().search("   ") == []


def test_get_adapter_oaauthcc_aliases() -> None:
    assert get_adapter("oaauthcc").name == "oaauthcc"
    assert get_adapter("authcc-oa").name == "oaauthcc"
    assert get_adapter("works-authcc-oa").name == "oaauthcc"


def test_parse_oaauthcc_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "us",
                "key_display_name": "United States",
                "count": 12,
            },
            {
                "key": "gb",
                "key_display_name": "United Kingdom",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "de",
                "display_name": "Germany",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaauthcc_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["United Kingdom works", "United States works", "Germany works"]
    assert hits[0].source == "oaauthcc"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=authorships.institutions.country_code:GB" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=authorships.institutions.country_code:US" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaauthcc_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "fr", "key_display_name": "France", "count": 1},
            {"key": "jp", "key_display_name": "Japan", "count": 2},
        ]
    }
    hits = parse_oaauthcc_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Japan works"]


def test_parse_oaauthcc_codes_list() -> None:
    payload = {
        "country_codes": [
            {
                "country_code": "nl",
                "display_name": "Netherlands",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaauthcc_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Netherlands works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaauthcc"
    assert "filter=authorships.institutions.country_code:NL" in hits[0].url
