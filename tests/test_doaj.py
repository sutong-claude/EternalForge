from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import DoajAdapter, get_adapter, parse_doaj_payload


def test_doaj_empty_query() -> None:
    assert DoajAdapter().search("") == []
    assert DoajAdapter().search("   ") == []


def test_get_adapter_doaj_aliases() -> None:
    assert get_adapter("doaj").name == "doaj"
    assert get_adapter("oa-journals").name == "doaj"
    assert get_adapter("journals").name == "doaj"


def test_parse_doaj_payload() -> None:
    payload = {
        "results": [
            {
                "id": "abc123",
                "bibjson": {
                    "title": "Open transformers in the wild",
                    "year": "2023",
                    "abstract": "A survey of open-access transformer papers.",
                    "author": [{"name": "Doe, Jane"}, {"name": "Roe, Sam"}],
                    "journal": {"title": "OA Computing"},
                    "identifier": [{"type": "doi", "id": "10.1234/oa.1"}],
                    "link": [{"url": "https://example.org/oa-transformers", "type": "fulltext"}],
                },
            },
            {
                "id": "def456",
                "bibjson": {
                    "title": "Journal-only note",
                    "year": 2021,
                    "author": ["Lee, Pat"],
                    "identifier": [{"type": "doi", "id": "10.1234/oa.2"}],
                },
            },
            {"id": "", "bibjson": {"title": ""}},
        ]
    }
    hits = parse_doaj_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Open transformers in the wild"
    assert hits[0].url == "https://example.org/oa-transformers"
    assert hits[0].source == "doaj"
    assert "Doe" in hits[0].snippet
    assert "2023" in hits[0].snippet
    assert "OA Computing" in hits[0].snippet
    assert "survey" in hits[0].snippet
    assert hits[1].title == "Journal-only note"
    assert hits[1].url == "https://doi.org/10.1234/oa.2"
    assert "Lee" in hits[1].snippet


def test_parse_doaj_respects_limit() -> None:
    payload = {
        "results": [
            {"id": "a", "bibjson": {"title": "A"}},
            {"id": "b", "bibjson": {"title": "B"}},
        ]
    }
    hits = parse_doaj_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_doaj_articles_list() -> None:
    payload = {
        "articles": [
            {
                "title": "Standalone OA piece",
                "bibjson": {
                    "identifier": [{"type": "doi", "id": "10.9/soft"}],
                    "journal": {"title": "Soft Letters"},
                },
            }
        ]
    }
    hits = parse_doaj_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone OA piece"
    assert hits[0].url == "https://doi.org/10.9/soft"
    assert "Soft Letters" in hits[0].snippet
