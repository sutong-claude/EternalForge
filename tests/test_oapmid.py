from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oapmid import OaPmidAdapter, parse_oapmid_payload
from tools.research import get_adapter


def test_oapmid_empty_query() -> None:
    assert OaPmidAdapter().search("") == []
    assert OaPmidAdapter().search("   ") == []


def test_get_adapter_oapmid_aliases() -> None:
    assert get_adapter("oapmid").name == "oapmid"
    assert get_adapter("pmid-oa").name == "oapmid"
    assert get_adapter("works-pmid-oa").name == "oapmid"


def test_parse_oapmid_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "12345678",
                "key_display_name": "12345678",
                "count": 12,
            },
            {
                "key": "87654321",
                "key_display_name": "87654321",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "11223344",
                "display_name": "11223344",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oapmid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "87654321 works",
        "12345678 works",
        "11223344 works",
    ]
    assert hits[0].source == "oapmid"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=ids.pmid:87654321" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=ids.pmid:12345678" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oapmid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "1", "key_display_name": "1", "count": 1},
            {"key": "2", "key_display_name": "2", "count": 2},
        ]
    }
    hits = parse_oapmid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["2 works"]


def test_parse_oapmid_pmids_list() -> None:
    payload = {
        "pmids": [
            {
                "pmid": "12345678",
                "display_name": "12345678",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oapmid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "12345678 works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oapmid"
    assert "filter=ids.pmid:12345678" in hits[0].url
