from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import CoreAdapter, get_adapter, parse_core_payload


def test_core_empty_query() -> None:
    assert CoreAdapter().search("") == []
    assert CoreAdapter().search("   ") == []


def test_get_adapter_core_aliases() -> None:
    assert get_adapter("core").name == "core"
    assert get_adapter("coreac").name == "core"
    assert get_adapter("works-core").name == "core"


def test_parse_core_payload() -> None:
    payload = {
        "results": [
            {
                "id": 123,
                "title": "Attention sharing in infancy",
                "yearPublished": 2023,
                "authors": [{"name": "Doe, Jane"}, {"name": "Roe, Sam"}],
                "abstract": "A study of joint attention.",
                "doi": "10.1234/core.1",
                "downloadUrl": "https://example.org/attention.pdf",
            },
            {
                "id": 456,
                "title": "Repository preprint",
                "year": 2021,
                "authors": [{"fullName": "Lee, Pat"}],
            },
            {"id": "", "title": ""},
        ]
    }
    hits = parse_core_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Attention sharing in infancy"
    assert hits[0].url == "https://example.org/attention.pdf"
    assert hits[0].source == "core"
    assert "Doe" in hits[0].snippet
    assert "2023" in hits[0].snippet
    assert "joint attention" in hits[0].snippet
    assert hits[1].title == "Repository preprint"
    assert hits[1].url == "https://core.ac.uk/works/456"
    assert "2021" in hits[1].snippet


def test_parse_core_respects_limit() -> None:
    payload = {
        "results": [
            {"id": "a", "title": "A"},
            {"id": "b", "title": "B"},
        ]
    }
    hits = parse_core_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_core_data_list() -> None:
    payload = {
        "data": [
            {
                "title": "Standalone CORE hit",
                "doi": "10.9/soft",
                "yearPublished": "2020",
            }
        ]
    }
    hits = parse_core_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone CORE hit"
    assert hits[0].url == "https://doi.org/10.9/soft"
    assert "2020" in hits[0].snippet
