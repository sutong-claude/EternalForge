from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oapridoaj import OaPriDoajAdapter, parse_oapridoaj_payload
from tools.research import get_adapter


def test_oapridoaj_empty_query() -> None:
    assert OaPriDoajAdapter().search("") == []
    assert OaPriDoajAdapter().search("   ") == []


def test_get_adapter_oapridoaj_aliases() -> None:
    assert get_adapter("oapridoaj").name == "oapridoaj"
    assert get_adapter("pridoaj-oa").name == "oapridoaj"
    assert get_adapter("works-pridoaj-oa").name == "oapridoaj"


def test_parse_oapridoaj_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oapridoaj_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works whose primary source is in DOAJ",
        "Works whose primary source is not in DOAJ",
    ]
    assert hits[0].source == "oapridoaj"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=primary_location.source.is_in_doaj:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=primary_location.source.is_in_doaj:false" in hits[1].url


def test_parse_oapridoaj_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oapridoaj_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works whose primary source is in DOAJ"]


def test_parse_oapridoaj_list_shape() -> None:
    payload = {
        "is_in_doaj": [
            {"is_in_doaj": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oapridoaj_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works whose primary source is not in DOAJ"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oapridoaj"
    assert "filter=primary_location.source.is_in_doaj:false" in hits[0].url
