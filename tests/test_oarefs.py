from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oarefs import OaRefsAdapter, parse_oarefs_payload
from tools.research import get_adapter


def test_oarefs_empty_query() -> None:
    assert OaRefsAdapter().search("") == []
    assert OaRefsAdapter().search("   ") == []


def test_get_adapter_oarefs_aliases() -> None:
    assert get_adapter("oarefs").name == "oarefs"
    assert get_adapter("refs-oa").name == "oarefs"
    assert get_adapter("works-refs-oa").name == "oarefs"


def test_parse_oarefs_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/W111",
                "key_display_name": "W111",
                "count": 12,
            },
            {
                "key": "https://openalex.org/W222",
                "key_display_name": "W222",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "W333",
                "display_name": "W333",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oarefs_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "W222 works",
        "W111 works",
        "W333 works",
    ]
    assert hits[0].source == "oarefs"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=referenced_works:W222" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=referenced_works:W111" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oarefs_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "W1", "key_display_name": "W1", "count": 1},
            {"key": "W2", "key_display_name": "W2", "count": 2},
        ]
    }
    hits = parse_oarefs_payload(payload, limit=1)
    assert [h.title for h in hits] == ["W2 works"]


def test_parse_oarefs_referenced_work_ids_list() -> None:
    payload = {
        "referenced_work_ids": [
            {
                "referenced_work": "https://openalex.org/W999",
                "display_name": "W999",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oarefs_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "W999 works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oarefs"
    assert "filter=referenced_works:W999" in hits[0].url
