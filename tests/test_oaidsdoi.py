from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaidsdoi import OaIdsDoiAdapter, parse_oaidsdoi_payload
from tools.research import get_adapter


def test_oaidsdoi_empty_query() -> None:
    assert OaIdsDoiAdapter().search("") == []
    assert OaIdsDoiAdapter().search("   ") == []


def test_get_adapter_oaidsdoi_aliases() -> None:
    assert get_adapter("oaidsdoi").name == "oaidsdoi"
    assert get_adapter("idsdoi-oa").name == "oaidsdoi"
    assert get_adapter("works-idsdoi-oa").name == "oaidsdoi"


def test_parse_oaidsdoi_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://doi.org/10.1000/aaa",
                "key_display_name": "10.1000/aaa",
                "count": 12,
            },
            {
                "key": "https://doi.org/10.1000/bbb",
                "key_display_name": "10.1000/bbb",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "10.1000/ccc",
                "display_name": "10.1000/ccc",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaidsdoi_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "10.1000/bbb works",
        "10.1000/aaa works",
        "10.1000/ccc works",
    ]
    assert hits[0].source == "oaidsdoi"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=ids.doi:10.1000/bbb" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=ids.doi:10.1000/aaa" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaidsdoi_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "10.1/a", "key_display_name": "10.1/a", "count": 1},
            {"key": "10.1/b", "key_display_name": "10.1/b", "count": 2},
        ]
    }
    hits = parse_oaidsdoi_payload(payload, limit=1)
    assert [h.title for h in hits] == ["10.1/b works"]


def test_parse_oaidsdoi_dois_list() -> None:
    payload = {
        "dois": [
            {
                "doi": "https://doi.org/10.1000/xyz",
                "display_name": "10.1000/xyz",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaidsdoi_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "10.1000/xyz works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaidsdoi"
    assert "filter=ids.doi:10.1000/xyz" in hits[0].url
