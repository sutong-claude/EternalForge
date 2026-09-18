from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OaFunderAdapter, get_adapter, parse_oafunder_payload


def test_oafunder_empty_query() -> None:
    assert OaFunderAdapter().search("") == []
    assert OaFunderAdapter().search("   ") == []


def test_get_adapter_oafunder_aliases() -> None:
    assert get_adapter("oafunder").name == "oafunder"
    assert get_adapter("funders-oa").name == "oafunder"
    assert get_adapter("cites-funder-oa").name == "oafunder"


def test_parse_oafunder_payload() -> None:
    payload = {
        "results": [
            {
                "id": "https://openalex.org/F4320332161",
                "display_name": "National Institutes of Health",
                "alternate_titles": ["NIH", "US NIH"],
                "country_code": "US",
                "homepage_url": "https://www.nih.gov",
                "works_count": 12000,
                "cited_by_count": 45000,
                "grants_count": 300,
                "description": "US biomedical funder",
            },
            {
                "id": "empty",
                "display_name": "",
                "homepage_url": "",
            },
            {
                "id": "F4320332001",
                "display_name": "National Science Foundation",
                "country_code": "US",
                "works_count": 8000,
            },
        ]
    }
    hits = parse_oafunder_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "National Institutes of Health"
    assert hits[0].url == "https://www.nih.gov"
    assert hits[0].source == "oafunder"
    assert "US" in hits[0].snippet
    assert "NIH" in hits[0].snippet
    assert "12000 works" in hits[0].snippet
    assert "45000 cites" in hits[0].snippet
    assert "300 grants" in hits[0].snippet
    assert "biomedical" in hits[0].snippet
    assert hits[1].title == "National Science Foundation"
    assert hits[1].url == "https://openalex.org/F4320332001"
    assert "8000 works" in hits[1].snippet


def test_parse_oafunder_respects_limit() -> None:
    payload = {
        "results": [
            {"id": "a", "display_name": "A"},
            {"id": "b", "display_name": "B"},
        ]
    }
    hits = parse_oafunder_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_oafunder_funders_list() -> None:
    payload = {
        "funders": [
            {
                "id": "https://openalex.org/F1",
                "display_name": "From funders list",
            }
        ]
    }
    hits = parse_oafunder_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "From funders list"
    assert hits[0].url == "https://openalex.org/F1"
    assert hits[0].source == "oafunder"
