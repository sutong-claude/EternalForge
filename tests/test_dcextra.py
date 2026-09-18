from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import DataCiteExtraAdapter, get_adapter, parse_dcextra_payload


def test_dcextra_empty_query() -> None:
    assert DataCiteExtraAdapter().search("") == []
    assert DataCiteExtraAdapter().search("   ") == []


def test_get_adapter_dcextra_aliases() -> None:
    assert get_adapter("dcextra").name == "dcextra"
    assert get_adapter("dc-extra").name == "dcextra"
    assert get_adapter("cites-dc").name == "dcextra"


def test_parse_dcextra_payload() -> None:
    payload = {
        "data": [
            {
                "id": "10.5281/zenodo.123",
                "attributes": {
                    "titles": [{"title": "Open Climate Dataset"}],
                    "publisher": {"name": "Zenodo"},
                    "subjects": [{"subject": "climate"}, {"subject": "open data"}],
                    "rightsList": [{"rightsIdentifier": "CC-BY-4.0"}],
                    "citationCount": 12,
                    "language": "en",
                    "container": {"title": "Zenodo"},
                    "url": "https://doi.org/10.5281/zenodo.123",
                },
            },
            {
                "id": "10.1234/empty",
                "attributes": {"titles": [{"title": ""}], "url": ""},
            },
            {
                "id": "10.5555/sample",
                "attributes": {
                    "titles": [{"title": "Sample Table"}],
                    "publisher": "Figshare",
                    "citationCount": 3,
                },
            },
        ]
    }
    hits = parse_dcextra_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Open Climate Dataset"
    assert hits[0].url == "https://doi.org/10.5281/zenodo.123"
    assert hits[0].source == "dcextra"
    assert "Zenodo" in hits[0].snippet
    assert "climate" in hits[0].snippet
    assert "CC-BY-4.0" in hits[0].snippet
    assert "12 cites" in hits[0].snippet
    assert "en" in hits[0].snippet
    assert hits[1].title == "Sample Table"
    assert hits[1].url == "https://doi.org/10.5555/sample"
    assert "Figshare" in hits[1].snippet
    assert "3 cites" in hits[1].snippet


def test_parse_dcextra_respects_limit() -> None:
    payload = {
        "data": [
            {"id": "10.1/a", "attributes": {"titles": [{"title": "A"}]}},
            {"id": "10.1/b", "attributes": {"titles": [{"title": "B"}]}},
        ]
    }
    hits = parse_dcextra_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_dcextra_dois_list() -> None:
    payload = {
        "dois": [
            {
                "doi": "10.9999/x",
                "titles": [{"title": "From dois list"}],
            }
        ]
    }
    hits = parse_dcextra_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "From dois list"
    assert hits[0].url == "https://doi.org/10.9999/x"
    assert hits[0].source == "dcextra"
