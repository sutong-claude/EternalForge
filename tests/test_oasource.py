from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OaSourceAdapter, get_adapter, parse_oasource_payload


def test_oasource_empty_query() -> None:
    assert OaSourceAdapter().search("") == []
    assert OaSourceAdapter().search("   ") == []


def test_get_adapter_oasource_aliases() -> None:
    assert get_adapter("oasource").name == "oasource"
    assert get_adapter("sources-oa").name == "oasource"
    assert get_adapter("cites-source-oa").name == "oasource"


def test_parse_oasource_payload() -> None:
    payload = {
        "results": [
            {
                "id": "https://openalex.org/S137773608",
                "display_name": "Nature",
                "type": "journal",
                "issn_l": "0028-0836",
                "publisher": "Springer Nature",
                "country_code": "gb",
                "is_oa": False,
                "is_in_doaj": False,
                "works_count": 500000,
                "cited_by_count": 20000000,
                "homepage_url": "https://www.nature.com",
            },
            {
                "id": "empty",
                "display_name": "",
            },
            {
                "id": "S12345",
                "display_name": "PLOS ONE",
                "type": "journal",
                "issn": ["1932-6203"],
                "host_organization_name": "Public Library of Science",
                "is_oa": True,
                "is_in_doaj": True,
                "works_count": 300000,
            },
        ]
    }
    hits = parse_oasource_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Nature"
    assert hits[0].url == "https://www.nature.com"
    assert hits[0].source == "oasource"
    assert "journal" in hits[0].snippet
    assert "Springer Nature" in hits[0].snippet
    assert "0028-0836" in hits[0].snippet
    assert "GB" in hits[0].snippet
    assert "500000 works" in hits[0].snippet
    assert "20000000 cites" in hits[0].snippet
    assert hits[1].title == "PLOS ONE"
    assert hits[1].url == "https://openalex.org/S12345"
    assert "Public Library of Science" in hits[1].snippet
    assert "1932-6203" in hits[1].snippet
    assert "OA" in hits[1].snippet
    assert "DOAJ" in hits[1].snippet
    assert "300000 works" in hits[1].snippet


def test_parse_oasource_respects_limit() -> None:
    payload = {
        "results": [
            {"id": "a", "display_name": "A"},
            {"id": "b", "display_name": "B"},
        ]
    }
    hits = parse_oasource_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_oasource_sources_list() -> None:
    payload = {
        "sources": [
            {
                "id": "https://openalex.org/S1",
                "display_name": "From sources list",
            }
        ]
    }
    hits = parse_oasource_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "From sources list"
    assert hits[0].url == "https://openalex.org/S1"
    assert hits[0].source == "oasource"
