from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaretracted import OaRetractedAdapter, parse_oaretracted_payload
from tools.research import get_adapter


def test_oaretracted_empty_query() -> None:
    assert OaRetractedAdapter().search("") == []
    assert OaRetractedAdapter().search("   ") == []


def test_get_adapter_oaretracted_aliases() -> None:
    assert get_adapter("oaretracted").name == "oaretracted"
    assert get_adapter("retracted-oa").name == "oaretracted"
    assert get_adapter("works-retracted-oa").name == "oaretracted"


def test_parse_oaretracted_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 4, "cited_by_count": 12},
            {"key": "false", "key_display_name": "false", "count": 80},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oaretracted_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Not retracted works", "Retracted works"]
    assert hits[0].source == "oaretracted"
    assert "80 works" in hits[0].snippet
    assert "filter=is_retracted:false" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "4 works" in hits[1].snippet
    assert "12 cites" in hits[1].snippet
    assert "filter=is_retracted:true" in hits[1].url


def test_parse_oaretracted_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 1},
            {"key": "false", "count": 9},
        ]
    }
    hits = parse_oaretracted_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Not retracted works"]


def test_parse_oaretracted_list_shape() -> None:
    payload = {
        "retracted": [
            {"is_retracted": True, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oaretracted_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Retracted works"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oaretracted"
    assert "filter=is_retracted:true" in hits[0].url
