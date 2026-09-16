from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OpenAlexAdapter, get_adapter, parse_openalex_payload


def test_openalex_empty_query() -> None:
    assert OpenAlexAdapter().search("") == []
    assert OpenAlexAdapter().search("   ") == []


def test_get_adapter_openalex_aliases() -> None:
    assert get_adapter("openalex").name == "openalex"
    assert get_adapter("oa").name == "openalex"
    assert get_adapter("works-oa").name == "openalex"


def test_parse_openalex_payload() -> None:
    payload = {
        "results": [
            {
                "id": "https://openalex.org/W2741809807",
                "display_name": "Attention Is All You Need",
                "doi": "https://doi.org/10.5555/3295222.3295349",
                "publication_year": 2017,
                "cited_by_count": 90000,
                "authorships": [
                    {"author": {"display_name": "Ashish Vaswani"}},
                    {"author": {"display_name": "Noam Shazeer"}},
                ],
                "primary_location": {
                    "landing_page_url": "https://papers.nips.cc/paper/7181",
                    "source": {"display_name": "NeurIPS"},
                },
                "abstract_inverted_index": {
                    "The": [0],
                    "dominant": [1],
                    "sequence": [2],
                },
            },
            {
                "id": "W123",
                "title": "Generative Adversarial Nets",
                "doi": "10.5555/2969033.2969125",
                "publication_year": 2014,
                "authors": ["Ian Goodfellow"],
            },
            {"display_name": "", "id": ""},
        ]
    }
    hits = parse_openalex_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Attention Is All You Need"
    assert hits[0].url == "https://papers.nips.cc/paper/7181"
    assert hits[0].source == "openalex"
    assert "Vaswani" in hits[0].snippet
    assert "2017" in hits[0].snippet
    assert "NeurIPS" in hits[0].snippet
    assert "dominant" in hits[0].snippet
    assert hits[1].title == "Generative Adversarial Nets"
    assert hits[1].url == "https://doi.org/10.5555/2969033.2969125"
    assert "Goodfellow" in hits[1].snippet


def test_parse_openalex_respects_limit() -> None:
    payload = {
        "results": [
            {"display_name": "A", "id": "https://openalex.org/WA"},
            {"display_name": "B", "id": "https://openalex.org/WB"},
        ]
    }
    hits = parse_openalex_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_openalex_works_list() -> None:
    payload = {
        "works": [
            {
                "id": "W99",
                "display_name": "Standalone work",
                "host_venue": {"display_name": "Nature"},
            }
        ]
    }
    hits = parse_openalex_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone work"
    assert hits[0].url == "https://openalex.org/W99"
    assert "Nature" in hits[0].snippet
