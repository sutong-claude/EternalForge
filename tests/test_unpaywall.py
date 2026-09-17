from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import UnpaywallAdapter, get_adapter, parse_unpaywall_payload


def test_unpaywall_empty_query() -> None:
    assert UnpaywallAdapter().search("") == []
    assert UnpaywallAdapter().search("   ") == []


def test_get_adapter_unpaywall_aliases() -> None:
    assert get_adapter("unpaywall").name == "unpaywall"
    assert get_adapter("upw").name == "unpaywall"
    assert get_adapter("oa-status").name == "unpaywall"


def test_parse_unpaywall_payload() -> None:
    payload = {
        "results": [
            {
                "score": 12.4,
                "response": {
                    "doi": "10.1038/nature12373",
                    "title": "A paper about nature",
                    "year": 2013,
                    "journal_name": "Nature",
                    "is_oa": True,
                    "oa_status": "gold",
                    "z_authors": [
                        {"given": "John", "family": "Doe"},
                        {"given": "Jane", "family": "Roe"},
                    ],
                    "best_oa_location": {
                        "url_for_pdf": "https://example.org/nature12373.pdf",
                        "version": "publishedVersion",
                        "license": "cc-by",
                    },
                },
            },
            {
                "title": "Closed preprint",
                "doi": "10.1234/closed.1",
                "year": 2021,
                "is_oa": False,
                "publisher": "Example Press",
            },
            {"title": ""},
        ]
    }
    hits = parse_unpaywall_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "A paper about nature"
    assert hits[0].url == "https://example.org/nature12373.pdf"
    assert hits[0].source == "unpaywall"
    assert "John Doe" in hits[0].snippet
    assert "2013" in hits[0].snippet
    assert "Nature" in hits[0].snippet
    assert "OA" in hits[0].snippet
    assert "gold" in hits[0].snippet
    assert hits[1].title == "Closed preprint"
    assert hits[1].url == "https://doi.org/10.1234/closed.1"
    assert "closed" in hits[1].snippet
    assert "2021" in hits[1].snippet


def test_parse_unpaywall_respects_limit() -> None:
    payload = {
        "results": [
            {"title": "A", "doi": "10.1/a"},
            {"title": "B", "doi": "10.1/b"},
        ]
    }
    hits = parse_unpaywall_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_unpaywall_doi_object() -> None:
    payload = {
        "doi": "10.1038/d41586-018-05968-3",
        "title": "Standalone DOI hit",
        "year": 2018,
        "is_oa": True,
        "best_oa_location": {
            "url_for_landing_page": "https://www.nature.com/articles/d41586-018-05968-3",
        },
    }
    hits = parse_unpaywall_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone DOI hit"
    assert "nature.com" in hits[0].url
    assert "2018" in hits[0].snippet
    assert "OA" in hits[0].snippet
