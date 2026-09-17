from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import WikidataAdapter, get_adapter, parse_wikidata_payload


def test_wikidata_empty_query() -> None:
    assert WikidataAdapter().search("") == []
    assert WikidataAdapter().search("   ") == []


def test_get_adapter_wikidata_aliases() -> None:
    assert get_adapter("wikidata").name == "wikidata"
    assert get_adapter("wd").name == "wikidata"
    assert get_adapter("entities").name == "wikidata"


def test_parse_wikidata_payload() -> None:
    payload = {
        "search": [
            {
                "id": "Q937",
                "label": "Albert Einstein",
                "description": "German-born theoretical physicist",
                "concepturi": "http://www.wikidata.org/entity/Q937",
            },
            {
                "id": "Q42",
                "label": "Douglas Adams",
                "description": "English author",
                "url": "//www.wikidata.org/wiki/Q42",
            },
            {"id": "", "label": ""},
        ]
    }
    hits = parse_wikidata_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Albert Einstein"
    assert hits[0].url == "http://www.wikidata.org/entity/Q937"
    assert hits[0].source == "wikidata"
    assert "Q937" in hits[0].snippet
    assert "physicist" in hits[0].snippet
    assert hits[1].title == "Douglas Adams"
    assert hits[1].url == "https://www.wikidata.org/wiki/Q42"
    assert "Q42" in hits[1].snippet


def test_parse_wikidata_respects_limit() -> None:
    payload = {
        "search": [
            {"id": "Q1", "label": "A"},
            {"id": "Q2", "label": "B"},
        ]
    }
    hits = parse_wikidata_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_wikidata_entities_map() -> None:
    payload = {
        "entities": {
            "Q5": {
                "id": "Q5",
                "label": {"value": "human"},
                "description": {"value": "common name of Homo sapiens"},
            }
        }
    }
    hits = parse_wikidata_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "human"
    assert hits[0].url == "https://www.wikidata.org/wiki/Q5"
    assert "Homo sapiens" in hits[0].snippet
