from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import ZenodoAdapter, get_adapter, parse_zenodo_payload


def test_zenodo_empty_query() -> None:
    assert ZenodoAdapter().search("") == []
    assert ZenodoAdapter().search("   ") == []


def test_get_adapter_zenodo_aliases() -> None:
    assert get_adapter("zenodo").name == "zenodo"
    assert get_adapter("zen").name == "zenodo"
    assert get_adapter("records").name == "zenodo"


def test_parse_zenodo_payload() -> None:
    payload = {
        "hits": {
            "hits": [
                {
                    "id": 12345,
                    "doi": "10.5281/zenodo.12345",
                    "links": {"html": "https://zenodo.org/records/12345"},
                    "metadata": {
                        "title": "Attention Is All You Need (dataset)",
                        "publication_date": "2017-06-12",
                        "description": "Weights and scripts for the Transformer.",
                        "creators": [{"name": "Vaswani, Ashish"}, {"name": "Shazeer, Noam"}],
                        "resource_type": {"type": "dataset", "title": "Dataset"},
                    },
                },
                {
                    "id": 99,
                    "metadata": {
                        "title": "GAN training notes",
                        "doi": "10.5281/zenodo.99",
                        "creators": ["Goodfellow, Ian"],
                        "publication_date": "2014-06-01",
                    },
                },
                {"metadata": {"title": ""}, "id": ""},
            ]
        }
    }
    hits = parse_zenodo_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Attention Is All You Need (dataset)"
    assert hits[0].url == "https://zenodo.org/records/12345"
    assert hits[0].source == "zenodo"
    assert "Vaswani" in hits[0].snippet
    assert "2017" in hits[0].snippet
    assert "Dataset" in hits[0].snippet
    assert "Transformer" in hits[0].snippet
    assert hits[1].title == "GAN training notes"
    assert hits[1].url == "https://doi.org/10.5281/zenodo.99"
    assert "Goodfellow" in hits[1].snippet


def test_parse_zenodo_respects_limit() -> None:
    payload = {
        "hits": {
            "hits": [
                {"id": 1, "metadata": {"title": "A"}},
                {"id": 2, "metadata": {"title": "B"}},
            ]
        }
    }
    hits = parse_zenodo_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_zenodo_records_list() -> None:
    payload = {
        "records": [
            {
                "id": "88",
                "title": "Standalone deposit",
                "metadata": {"resource_type": {"title": "Software"}},
            }
        ]
    }
    hits = parse_zenodo_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone deposit"
    assert hits[0].url == "https://zenodo.org/records/88"
    assert "Software" in hits[0].snippet
