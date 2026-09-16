from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import PubMedAdapter, get_adapter, parse_pubmed_payload


def test_pubmed_empty_query() -> None:
    assert PubMedAdapter().search("") == []
    assert PubMedAdapter().search("   ") == []


def test_get_adapter_pubmed_aliases() -> None:
    assert get_adapter("pubmed").name == "pubmed"
    assert get_adapter("ncbi").name == "pubmed"
    assert get_adapter("medline").name == "pubmed"


def test_parse_pubmed_payload() -> None:
    payload = {
        "result": {
            "uids": ["31978945", "25362348"],
            "31978945": {
                "uid": "31978945",
                "title": "A large-scale binding and functional map of human protein-coding genes.",
                "authors": [{"name": "ENCODE Project Consortium"}],
                "source": "Nature",
                "pubdate": "2020 Jul",
            },
            "25362348": {
                "uid": "25362348",
                "title": "CRISPR-Cas systems for editing, regulating and targeting genomes.",
                "authors": [{"name": "Sander JD"}, {"name": "Joung JK"}],
                "source": "Nat Biotechnol",
                "pubdate": "2014 Apr",
            },
            "empty": {"title": "", "uid": ""},
        }
    }
    hits = parse_pubmed_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "A large-scale binding and functional map of human protein-coding genes"
    assert hits[0].url == "https://pubmed.ncbi.nlm.nih.gov/31978945/"
    assert hits[0].source == "pubmed"
    assert "Nature" in hits[0].snippet
    assert "2020" in hits[0].snippet
    assert hits[1].title.startswith("CRISPR-Cas systems")
    assert "Sander" in hits[1].snippet
    assert hits[1].url == "https://pubmed.ncbi.nlm.nih.gov/25362348/"


def test_parse_pubmed_respects_limit() -> None:
    payload = {
        "result": {
            "uids": ["1", "2"],
            "1": {"title": "A", "uid": "1"},
            "2": {"title": "B", "uid": "2"},
        }
    }
    hits = parse_pubmed_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_pubmed_articles_list() -> None:
    payload = {
        "articles": [
            {"pmid": "99", "title": "Standalone article.", "source": "Lancet"},
        ]
    }
    hits = parse_pubmed_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone article"
    assert hits[0].url == "https://pubmed.ncbi.nlm.nih.gov/99/"
    assert "Lancet" in hits[0].snippet
