from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthror import OaAuthRorAdapter, parse_oaauthror_payload
from tools.research import get_adapter


def test_oaauthror_empty_query() -> None:
    assert OaAuthRorAdapter().search("") == []
    assert OaAuthRorAdapter().search("   ") == []


def test_get_adapter_oaauthror_aliases() -> None:
    assert get_adapter("oaauthror").name == "oaauthror"
    assert get_adapter("authror-oa").name == "oaauthror"
    assert get_adapter("works-authror-oa").name == "oaauthror"


def test_parse_oaauthror_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://ror.org/00jmfr291",
                "key_display_name": "University of Michigan",
                "count": 12,
            },
            {
                "key": "00jmfr292",
                "key_display_name": "Harvard University",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://ror.org/00f54p054",
                "display_name": "Stanford University",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaauthror_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Harvard University works",
        "University of Michigan works",
        "Stanford University works",
    ]
    assert hits[0].source == "oaauthror"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=authorships.institutions.ror:00jmfr292" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=authorships.institutions.ror:00jmfr291" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaauthror_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "00aaaaaaa", "key_display_name": "MIT", "count": 1},
            {"key": "00bbbbbbb", "key_display_name": "Oxford", "count": 2},
        ]
    }
    hits = parse_oaauthror_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Oxford works"]


def test_parse_oaauthror_rors_list() -> None:
    payload = {
        "rors": [
            {
                "ror": "https://ror.org/00jmfr291",
                "display_name": "University of Michigan",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaauthror_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "University of Michigan works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaauthror"
    assert "filter=authorships.institutions.ror:00jmfr291" in hits[0].url
