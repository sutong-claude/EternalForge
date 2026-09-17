from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import DataCiteAdapter, get_adapter, parse_datacite_payload


def test_datacite_empty_query() -> None:
    assert DataCiteAdapter().search("") == []
    assert DataCiteAdapter().search("   ") == []


def test_get_adapter_datacite_aliases() -> None:
    assert get_adapter("datacite").name == "datacite"
    assert get_adapter("dc").name == "datacite"
    assert get_adapter("dois").name == "datacite"


def test_parse_datacite_payload() -> None:
    payload = {
        "data": [
            {
                "id": "10.5281/zenodo.12345",
                "attributes": {
                    "doi": "10.5281/zenodo.12345",
                    "url": "https://zenodo.org/records/12345",
                    "titles": [{"title": "Attention Is All You Need (dataset)"}],
                    "creators": [{"name": "Vaswani, Ashish"}, {"name": "Shazeer, Noam"}],
                    "publicationYear": 2017,
                    "types": {"resourceTypeGeneral": "Dataset"},
                    "descriptions": [
                        {"description": "Weights and scripts for the Transformer."}
                    ],
                },
            },
            {
                "id": "10.5281/zenodo.99",
                "attributes": {
                    "titles": [{"title": "GAN training notes"}],
                    "creators": ["Goodfellow, Ian"],
                    "publicationYear": 2014,
                },
            },
            {"id": "", "attributes": {"titles": [{"title": ""}]}},
        ]
    }
    hits = parse_datacite_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Attention Is All You Need (dataset)"
    assert hits[0].url == "https://zenodo.org/records/12345"
    assert hits[0].source == "datacite"
    assert "Vaswani" in hits[0].snippet
    assert "2017" in hits[0].snippet
    assert "Dataset" in hits[0].snippet
    assert "Transformer" in hits[0].snippet
    assert hits[1].title == "GAN training notes"
    assert hits[1].url == "https://doi.org/10.5281/zenodo.99"
    assert "Goodfellow" in hits[1].snippet


def test_parse_datacite_respects_limit() -> None:
    payload = {
        "data": [
            {"id": "10.1/a", "attributes": {"titles": [{"title": "A"}]}},
            {"id": "10.1/b", "attributes": {"titles": [{"title": "B"}]}},
        ]
    }
    hits = parse_datacite_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_datacite_dois_list() -> None:
    payload = {
        "dois": [
            {
                "doi": "10.1234/soft",
                "title": "Standalone deposit",
                "attributes": {"types": {"resourceTypeGeneral": "Software"}},
            }
        ]
    }
    hits = parse_datacite_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone deposit"
    assert hits[0].url == "https://doi.org/10.1234/soft"
    assert "Software" in hits[0].snippet
