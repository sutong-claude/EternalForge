from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OaAuthorAdapter, get_adapter, parse_oaauthor_payload


def test_oaauthor_empty_query() -> None:
    assert OaAuthorAdapter().search("") == []
    assert OaAuthorAdapter().search("   ") == []


def test_get_adapter_oaauthor_aliases() -> None:
    assert get_adapter("oaauthor").name == "oaauthor"
    assert get_adapter("authors-oa").name == "oaauthor"
    assert get_adapter("cites-author-oa").name == "oaauthor"


def test_parse_oaauthor_payload() -> None:
    payload = {
        "results": [
            {
                "id": "https://openalex.org/A5023888391",
                "display_name": "Geoffrey Hinton",
                "display_name_alternatives": ["G. E. Hinton"],
                "orcid": "https://orcid.org/0000-0002-1418-9870",
                "last_known_institutions": [
                    {"display_name": "University of Toronto", "country_code": "ca"}
                ],
                "works_count": 400,
                "cited_by_count": 500000,
                "summary_stats": {"h_index": 160},
            },
            {
                "id": "empty",
                "display_name": "",
            },
            {
                "id": "A123",
                "display_name": "Jane Researcher",
                "affiliations": [
                    {"institution": {"display_name": "MIT", "country_code": "us"}}
                ],
                "works_count": 12,
            },
        ]
    }
    hits = parse_oaauthor_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Geoffrey Hinton"
    assert hits[0].url == "https://openalex.org/A5023888391"
    assert hits[0].source == "oaauthor"
    assert "orcid:0000-0002-1418-9870" in hits[0].snippet
    assert "University of Toronto (CA)" in hits[0].snippet
    assert "G. E. Hinton" in hits[0].snippet
    assert "h=160" in hits[0].snippet
    assert "400 works" in hits[0].snippet
    assert "500000 cites" in hits[0].snippet
    assert hits[1].title == "Jane Researcher"
    assert hits[1].url == "https://openalex.org/A123"
    assert "MIT (US)" in hits[1].snippet
    assert "12 works" in hits[1].snippet


def test_parse_oaauthor_respects_limit() -> None:
    payload = {
        "results": [
            {"id": "a", "display_name": "A"},
            {"id": "b", "display_name": "B"},
        ]
    }
    hits = parse_oaauthor_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_oaauthor_authors_list() -> None:
    payload = {
        "authors": [
            {
                "id": "https://openalex.org/A1",
                "display_name": "From authors list",
            }
        ]
    }
    hits = parse_oaauthor_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "From authors list"
    assert hits[0].url == "https://openalex.org/A1"
    assert hits[0].source == "oaauthor"
