from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oacontinent import OaContinentAdapter, parse_oacontinent_payload
from tools.research import get_adapter


def test_oacontinent_empty_query() -> None:
    assert OaContinentAdapter().search("") == []
    assert OaContinentAdapter().search("   ") == []


def test_get_adapter_oacontinent_aliases() -> None:
    assert get_adapter("oacontinent").name == "oacontinent"
    assert get_adapter("continents-oa").name == "oacontinent"
    assert get_adapter("works-continent-oa").name == "oacontinent"


def test_parse_oacontinent_payload() -> None:
    payload = {
        "group_by": [
            {"key": "europe", "key_display_name": "Europe", "count": 10},
            {"key": "north_america", "key_display_name": "North America", "count": 40, "cited_by_count": 900},
            {"key": "unknown", "count": 3},
            {"key": "asia", "key_display_name": "Asia", "works_count": 5},
        ]
    }
    hits = parse_oacontinent_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["North America works", "Europe works", "Asia works"]
    assert hits[0].source == "oacontinent"
    assert "40 works" in hits[0].snippet
    assert "900 cites" in hits[0].snippet
    assert "filter=authorships.continents:north_america" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "10 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oacontinent_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "africa", "key_display_name": "Africa", "count": 1},
            {"key": "europe", "key_display_name": "Europe", "count": 2},
        ]
    }
    hits = parse_oacontinent_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Europe works"]


def test_parse_oacontinent_continents_list() -> None:
    payload = {
        "continents": [
            {"continent": "Oceania", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oacontinent_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Oceania works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oacontinent"
    assert "filter=authorships.continents:oceania" in hits[0].url
