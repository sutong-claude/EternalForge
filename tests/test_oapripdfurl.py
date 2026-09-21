from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oapripdfurl import OaPriPdfUrlAdapter, parse_oapripdfurl_payload
from tools.research import get_adapter


def test_oapripdfurl_empty_query() -> None:
    assert OaPriPdfUrlAdapter().search("") == []
    assert OaPriPdfUrlAdapter().search("   ") == []


def test_get_adapter_oapripdfurl_aliases() -> None:
    assert get_adapter("oapripdfurl").name == "oapripdfurl"
    assert get_adapter("pripdfurl-oa").name == "oapripdfurl"
    assert get_adapter("works-pripdfurl-oa").name == "oapripdfurl"


def test_parse_oapripdfurl_payload() -> None:
    payload = {
        "group_by": [
            {"key": "https://ex.org/a.pdf", "key_display_name": "https://ex.org/a.pdf", "count": 12},
            {
                "key": "https://ex.org/b.pdf",
                "key_display_name": "https://ex.org/b.pdf",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {"key": "https://ex.org/c.pdf", "key_display_name": "https://ex.org/c.pdf", "works_count": 5},
        ]
    }
    hits = parse_oapripdfurl_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "https://ex.org/b.pdf works",
        "https://ex.org/a.pdf works",
        "https://ex.org/c.pdf works",
    ]
    assert hits[0].source == "oapripdfurl"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=primary_location.pdf_url:https" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oapripdfurl_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "https://ex.org/a.pdf", "key_display_name": "https://ex.org/a.pdf", "count": 1},
            {"key": "https://ex.org/b.pdf", "key_display_name": "https://ex.org/b.pdf", "count": 2},
        ]
    }
    hits = parse_oapripdfurl_payload(payload, limit=1)
    assert [h.title for h in hits] == ["https://ex.org/b.pdf works"]


def test_parse_oapripdfurl_pdf_urls_list() -> None:
    payload = {
        "pdf_urls": [
            {"pdf_url": "https://ex.org/z.pdf", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oapripdfurl_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "https://ex.org/z.pdf works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oapripdfurl"
    assert "filter=primary_location.pdf_url:https" in hits[0].url
