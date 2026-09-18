from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OaPublisherAdapter, get_adapter, parse_oapublisher_payload


def test_oapublisher_empty_query() -> None:
    assert OaPublisherAdapter().search("") == []
    assert OaPublisherAdapter().search("   ") == []


def test_get_adapter_oapublisher_aliases() -> None:
    assert get_adapter("oapublisher").name == "oapublisher"
    assert get_adapter("publishers-oa").name == "oapublisher"
    assert get_adapter("cites-publisher-oa").name == "oapublisher"


def test_parse_oapublisher_payload() -> None:
    payload = {
        "results": [
            {
                "id": "https://openalex.org/P4310320990",
                "display_name": "Springer Nature",
                "alternate_titles": ["Springer", "Nature Portfolio"],
                "country_codes": ["de", "gb"],
                "hierarchy_level": 0,
                "homepage_url": "https://www.springernature.com",
                "works_count": 9000000,
                "cited_by_count": 150000000,
                "sources_count": 3000,
            },
            {
                "id": "empty",
                "display_name": "",
            },
            {
                "id": "P4310319965",
                "display_name": "Public Library of Science",
                "country_codes": ["us"],
                "hierarchy_level": 1,
                "parent_publisher": {"display_name": "Springer Nature"},
                "works_count": 300000,
                "sources_count": 8,
            },
        ]
    }
    hits = parse_oapublisher_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Springer Nature"
    assert hits[0].url == "https://www.springernature.com"
    assert hits[0].source == "oapublisher"
    assert "DE" in hits[0].snippet
    assert "GB" in hits[0].snippet
    assert "Springer" in hits[0].snippet
    assert "L0" in hits[0].snippet
    assert "3000 sources" in hits[0].snippet
    assert "9000000 works" in hits[0].snippet
    assert "150000000 cites" in hits[0].snippet
    assert hits[1].title == "Public Library of Science"
    assert hits[1].url == "https://openalex.org/P4310319965"
    assert "US" in hits[1].snippet
    assert "L1" in hits[1].snippet
    assert "parent Springer Nature" in hits[1].snippet
    assert "300000 works" in hits[1].snippet


def test_parse_oapublisher_respects_limit() -> None:
    payload = {
        "results": [
            {"id": "a", "display_name": "A"},
            {"id": "b", "display_name": "B"},
        ]
    }
    hits = parse_oapublisher_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_oapublisher_publishers_list() -> None:
    payload = {
        "publishers": [
            {
                "id": "https://openalex.org/P1",
                "display_name": "From publishers list",
            }
        ]
    }
    hits = parse_oapublisher_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "From publishers list"
    assert hits[0].url == "https://openalex.org/P1"
    assert hits[0].source == "oapublisher"
