from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import EpmcExtraAdapter, get_adapter, parse_epmcextra_payload


def test_epmcextra_empty_query() -> None:
    assert EpmcExtraAdapter().search("") == []
    assert EpmcExtraAdapter().search("   ") == []


def test_get_adapter_epmcextra_aliases() -> None:
    assert get_adapter("epmcextra").name == "epmcextra"
    assert get_adapter("epmc-extra").name == "epmcextra"
    assert get_adapter("cites-epmc").name == "epmcextra"


def test_parse_epmcextra_payload() -> None:
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
                    "pubType": ["research-article", "journal article"],
                    "isOpenAccess": "Y",
                    "citedByCount": 88,
                    "language": "eng",
                    "keywordList": {"keyword": ["ENCODE", "genomics"]},
                    "abstractText": "The Encyclopedia of DNA Elements.",
                },
                {
                    "id": "25362348",
                    "source": "MED",
                    "pmid": "25362348",
                    "title": "CRISPR-Cas systems for editing, regulating and targeting genomes.",
                    "authorString": "Sander JD, Joung JK",
                    "journalTitle": "Nat Biotechnol",
                    "firstPublicationDate": "2014-11-01",
                    "isOpenAccess": "N",
                    "citedByCount": 12,
                },
                {"title": "", "id": ""},
            ]
        }
    }
    hits = parse_epmcextra_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "A large-scale binding and functional map of human protein-coding genes"
    assert hits[0].url == "https://europepmc.org/article/MED/31978945"
    assert hits[0].source == "epmcextra"
    assert "Nature" in hits[0].snippet
    assert "2020" in hits[0].snippet
    assert "research-article" in hits[0].snippet
    assert "OA" in hits[0].snippet
    assert "88 cites" in hits[0].snippet
    assert "ENCODE" in hits[0].snippet
    assert "eng" in hits[0].snippet
    assert "Encyclopedia" in hits[0].snippet
    assert hits[1].title.startswith("CRISPR-Cas systems")
    assert hits[1].url == "https://europepmc.org/article/MED/25362348"
    assert "2014" in hits[1].snippet
    assert "closed" in hits[1].snippet
    assert "12 cites" in hits[1].snippet


def test_parse_epmcextra_respects_limit() -> None:
    payload = {
        "resultList": {
            "result": [
                {"title": "A", "id": "1", "source": "MED"},
                {"title": "B", "id": "2", "source": "MED"},
            ]
        }
    }
    hits = parse_epmcextra_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_epmcextra_articles_list() -> None:
    payload = {
        "articles": [
            {
                "pmid": "99",
                "title": "Standalone extras article.",
                "journalTitle": "Lancet",
                "pmcid": "PMC1",
                "citedByCount": 3,
            }
        ]
    }
    hits = parse_epmcextra_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone extras article"
    assert hits[0].url == "https://europepmc.org/article/MED/99"
    assert "Lancet" in hits[0].snippet
    assert "OA" in hits[0].snippet
    assert "3 cites" in hits[0].snippet
