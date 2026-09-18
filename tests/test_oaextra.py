from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OaExtraAdapter, get_adapter, parse_oaextra_payload


def test_oaextra_empty_query() -> None:
    assert OaExtraAdapter().search("") == []
    assert OaExtraAdapter().search("   ") == []


def test_get_adapter_oaextra_aliases() -> None:
    assert get_adapter("oaextra").name == "oaextra"
    assert get_adapter("oa-extra").name == "oaextra"
    assert get_adapter("cites-oa").name == "oaextra"


def test_parse_oaextra_payload() -> None:
    payload = {
        "results": [
            {
                "display_name": "Attention Is All You Need",
                "id": "https://openalex.org/W2964141474",
                "doi": "https://doi.org/10.5555/3295222.3295349",
                "authorships": [
                    {"author": {"display_name": "Ashish Vaswani"}},
                    {"author": {"display_name": "Noam Shazeer"}},
                ],
                "publication_year": 2017,
                "publication_date": "2017-06-12",
                "primary_location": {"source": {"display_name": "NeurIPS"}},
                "type": "article",
                "cited_by_count": 84210,
                "open_access": {"is_oa": True, "oa_status": "green"},
                "concepts": [
                    {"display_name": "Transformer"},
                    {"display_name": "Attention"},
                ],
                "language": "en",
                "abstract": "We propose the Transformer.",
            },
            {
                "title": "Generative Adversarial Nets",
                "doi": "10.5555/2969033.2969125",
                "authorships": [{"author": {"display_name": "Ian Goodfellow"}}],
                "publication_year": 2014,
                "type": "journal-article",
            },
            {"title": "", "doi": "", "id": ""},
        ]
    }
    hits = parse_oaextra_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Attention Is All You Need"
    assert hits[0].url == "https://doi.org/10.5555/3295222.3295349"
    assert hits[0].source == "oaextra"
    assert "Vaswani" in hits[0].snippet
    assert "2017-06-12" in hits[0].snippet
    assert "NeurIPS" in hits[0].snippet
    assert "84210 cites" in hits[0].snippet
    assert "green" in hits[0].snippet
    assert "Transformer" in hits[0].snippet
    assert hits[1].title == "Generative Adversarial Nets"
    assert hits[1].url == "https://doi.org/10.5555/2969033.2969125"
    assert "Goodfellow" in hits[1].snippet
    assert "2014" in hits[1].snippet


def test_parse_oaextra_respects_limit() -> None:
    payload = {
        "results": [
            {"display_name": "A", "id": "https://openalex.org/WA"},
            {"display_name": "B", "id": "https://openalex.org/WB"},
        ]
    }
    hits = parse_oaextra_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_oaextra_works_list() -> None:
    payload = {
        "works": [
            {
                "display_name": "Standalone extras hit",
                "id": "W123",
                "publication_year": 2020,
                "cited_by_count": 12,
                "open_access": {"is_oa": True},
            }
        ]
    }
    hits = parse_oaextra_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone extras hit"
    assert hits[0].url == "https://openalex.org/W123"
    assert "2020" in hits[0].snippet
    assert "12 cites" in hits[0].snippet
    assert "oa" in hits[0].snippet
