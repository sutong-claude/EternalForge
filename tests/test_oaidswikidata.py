from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaidswikidata import OaIdsWikidataAdapter, parse_oaidswikidata_payload
from tools.research import get_adapter


def test_oaidswikidata_empty_query() -> None:
    assert OaIdsWikidataAdapter().search("") == []
    assert OaIdsWikidataAdapter().search("   ") == []


def test_get_adapter_oaidswikidata_aliases() -> None:
    assert get_adapter("oaidswikidata").name == "oaidswikidata"
    assert get_adapter("idswd-oa").name == "oaidswikidata"
    assert get_adapter("works-idswd-oa").name == "oaidswikidata"


def test_parse_oaidswikidata_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://www.wikidata.org/entity/Q111",
                "key_display_name": "Q111",
                "count": 12,
            },
            {
                "key": "https://www.wikidata.org/wiki/Q222",
                "key_display_name": "Q222",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "Q333",
                "display_name": "Q333",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaidswikidata_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Q222 works",
        "Q111 works",
        "Q333 works",
    ]
    assert hits[0].source == "oaidswikidata"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=ids.wikidata:Q222" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=ids.wikidata:Q111" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaidswikidata_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "Q1", "key_display_name": "Q1", "count": 1},
            {"key": "Q2", "key_display_name": "Q2", "count": 2},
        ]
    }
    hits = parse_oaidswikidata_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Q2 works"]


def test_parse_oaidswikidata_wikidata_ids_list() -> None:
    payload = {
        "wikidata_ids": [
            {
                "wikidata": "https://www.wikidata.org/entity/Q999",
                "display_name": "Q999",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaidswikidata_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Q999 works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaidswikidata"
    assert "filter=ids.wikidata:Q999" in hits[0].url
