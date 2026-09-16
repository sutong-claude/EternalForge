from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import EuropePMCAdapter, get_adapter, parse_europepmc_payload


def test_europepmc_empty_query() -> None:
    assert EuropePMCAdapter().search("") == []
    assert EuropePMCAdapter().search("   ") == []


def test_get_adapter_europepmc_aliases() -> None:
    assert get_adapter("europepmc").name == "europepmc"
    assert get_adapter("epmc").name == "europepmc"
    assert get_adapter("europe").name == "europepmc"


def test_parse_europepmc_payload() -> None:
    payload = {
        "resultList": {
            "result": [
                {
                    "id": "31978945",
                    "source": "MED",
                    "pmid": "31978945",
                    "title": "A large-scale binding and functional map of human protein-coding genes.",
                    "authorString": "ENCODE Project Consortium",
                    "journalTitle": "Nature",
                    "pubYear": "2020",
                    "abstractText": "The Encyclopedia of DNA Elements.",
                },
                {
                    "id": "25362348",
                    "source": "MED",
                    "pmid": "25362348",
                    "title": "CRISPR-Cas systems for editing, regulating and targeting genomes.",
                    "authorString": "Sander JD, Joung JK",
                    "journalTitle": "Nat Biotechnol",
                    "pubYear": "2014",
                },
                {"title": "", "id": ""},
            ]
        }
    }
    hits = parse_europepmc_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "A large-scale binding and functional map of human protein-coding genes"
    assert hits[0].url == "https://europepmc.org/article/MED/31978945"
    assert hits[0].source == "europepmc"
    assert "Nature" in hits[0].snippet
    assert "2020" in hits[0].snippet
    assert "Encyclopedia" in hits[0].snippet
    assert hits[1].title.startswith("CRISPR-Cas systems")
    assert "Sander" in hits[1].snippet
    assert hits[1].url == "https://europepmc.org/article/MED/25362348"


def test_parse_europepmc_respects_limit() -> None:
    payload = {
        "resultList": {
            "result": [
                {"title": "A", "id": "1", "source": "MED"},
                {"title": "B", "id": "2", "source": "MED"},
            ]
        }
    }
    hits = parse_europepmc_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_europepmc_articles_list() -> None:
    payload = {
        "articles": [
            {"pmid": "99", "title": "Standalone article.", "journalTitle": "Lancet"},
        ]
    }
    hits = parse_europepmc_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone article"
    assert hits[0].url == "https://europepmc.org/article/MED/99"
    assert "Lancet" in hits[0].snippet
