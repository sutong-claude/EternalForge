from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthtype import OaAuthTypeAdapter, parse_oaauthtype_payload
from tools.research import get_adapter


def test_oaauthtype_empty_query() -> None:
    assert OaAuthTypeAdapter().search("") == []
    assert OaAuthTypeAdapter().search("   ") == []


def test_get_adapter_oaauthtype_aliases() -> None:
    assert get_adapter("oaauthtype").name == "oaauthtype"
    assert get_adapter("authtype-oa").name == "oaauthtype"
    assert get_adapter("works-authtype-oa").name == "oaauthtype"


def test_parse_oaauthtype_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "company",
                "key_display_name": "company",
                "count": 12,
            },
            {
                "key": "education",
                "key_display_name": "education",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "government",
                "display_name": "government",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaauthtype_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["education works", "company works", "government works"]
    assert hits[0].source == "oaauthtype"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=authorships.institutions.type:education" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=authorships.institutions.type:company" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaauthtype_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "nonprofit", "key_display_name": "nonprofit", "count": 1},
            {"key": "facility", "key_display_name": "facility", "count": 2},
        ]
    }
    hits = parse_oaauthtype_payload(payload, limit=1)
    assert [h.title for h in hits] == ["facility works"]


def test_parse_oaauthtype_types_list() -> None:
    payload = {
        "types": [
            {
                "type": "healthcare",
                "display_name": "healthcare",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaauthtype_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "healthcare works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaauthtype"
    assert "filter=authorships.institutions.type:healthcare" in hits[0].url
