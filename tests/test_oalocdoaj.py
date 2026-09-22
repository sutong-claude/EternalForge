from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oalocdoaj import OaLocDoajAdapter, parse_oalocdoaj_payload
from tools.research import get_adapter


def test_oalocdoaj_empty_query() -> None:
    assert OaLocDoajAdapter().search("") == []
    assert OaLocDoajAdapter().search("   ") == []


def test_get_adapter_oalocdoaj_aliases() -> None:
    assert get_adapter("oalocdoaj").name == "oalocdoaj"
    assert get_adapter("locdoaj-oa").name == "oalocdoaj"
    assert get_adapter("works-locdoaj-oa").name == "oalocdoaj"


def test_parse_oalocdoaj_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oalocdoaj_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with a location source in DOAJ",
        "Works without a location source in DOAJ",
    ]
    assert hits[0].source == "oalocdoaj"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=locations.source.is_in_doaj:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=locations.source.is_in_doaj:false" in hits[1].url


def test_parse_oalocdoaj_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oalocdoaj_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with a location source in DOAJ"]


def test_parse_oalocdoaj_list_shape() -> None:
    payload = {
        "is_in_doaj": [
            {"is_in_doaj": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oalocdoaj_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without a location source in DOAJ"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oalocdoaj"
    assert "filter=locations.source.is_in_doaj:false" in hits[0].url
