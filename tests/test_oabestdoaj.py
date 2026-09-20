from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oabestdoaj import OaBestDoajAdapter, parse_oabestdoaj_payload
from tools.research import get_adapter


def test_oabestdoaj_empty_query() -> None:
    assert OaBestDoajAdapter().search("") == []
    assert OaBestDoajAdapter().search("   ") == []


def test_get_adapter_oabestdoaj_aliases() -> None:
    assert get_adapter("oabestdoaj").name == "oabestdoaj"
    assert get_adapter("bestdoaj-oa").name == "oabestdoaj"
    assert get_adapter("works-bestdoaj-oa").name == "oabestdoaj"


def test_parse_oabestdoaj_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oabestdoaj_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works whose best OA source is in DOAJ",
        "Works whose best OA source is not in DOAJ",
    ]
    assert hits[0].source == "oabestdoaj"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=best_oa_location.source.is_in_doaj:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=best_oa_location.source.is_in_doaj:false" in hits[1].url


def test_parse_oabestdoaj_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oabestdoaj_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works whose best OA source is in DOAJ"]


def test_parse_oabestdoaj_list_shape() -> None:
    payload = {
        "is_in_doaj": [
            {"is_in_doaj": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oabestdoaj_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works whose best OA source is not in DOAJ"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oabestdoaj"
    assert "filter=best_oa_location.source.is_in_doaj:false" in hits[0].url
