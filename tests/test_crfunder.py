from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import CrFunderAdapter, get_adapter, parse_crfunder_payload


def test_crfunder_empty_query() -> None:
    assert CrFunderAdapter().search("") == []
    assert CrFunderAdapter().search("   ") == []


def test_get_adapter_crfunder_aliases() -> None:
    assert get_adapter("crfunder").name == "crfunder"
    assert get_adapter("funders-cr").name == "crfunder"
    assert get_adapter("cites-funder").name == "crfunder"


def test_parse_crfunder_payload() -> None:
    payload = {
        "message": {
            "items": [
                {
                    "id": "100000002",
                    "name": "National Institutes of Health",
                    "alt-names": ["NIH", "US NIH"],
                    "location": "United States",
                    "uri": "https://api.crossref.org/funders/100000002",
                    "work-count": 12000,
                    "descendant-work-count": 45000,
                },
                {
                    "id": "empty",
                    "name": "",
                    "uri": "",
                },
                {
                    "id": "100000001",
                    "name": "National Science Foundation",
                    "location": "United States",
                    "work-count": 8000,
                },
            ]
        }
    }
    hits = parse_crfunder_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "National Institutes of Health"
    assert hits[0].url == "https://api.crossref.org/funders/100000002"
    assert hits[0].source == "crfunder"
    assert "United States" in hits[0].snippet
    assert "NIH" in hits[0].snippet
    assert "12000 works" in hits[0].snippet
    assert "45000 descendant works" in hits[0].snippet
    assert hits[1].title == "National Science Foundation"
    assert hits[1].url == "https://api.crossref.org/funders/100000001"
    assert "8000 works" in hits[1].snippet


def test_parse_crfunder_respects_limit() -> None:
    payload = {
        "message": {
            "items": [
                {"id": "a", "name": "A"},
                {"id": "b", "name": "B"},
            ]
        }
    }
    hits = parse_crfunder_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_crfunder_funders_list() -> None:
    payload = {
        "funders": [
            {
                "id": "10.13039/x",
                "name": "From funders list",
            }
        ]
    }
    hits = parse_crfunder_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "From funders list"
    assert hits[0].url == "https://api.crossref.org/funders/10.13039/x"
    assert hits[0].source == "crfunder"
