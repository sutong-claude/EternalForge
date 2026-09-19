from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahaspdf import OaHasPdfAdapter, parse_oahaspdf_payload
from tools.research import get_adapter


def test_oahaspdf_empty_query() -> None:
    assert OaHasPdfAdapter().search("") == []
    assert OaHasPdfAdapter().search("   ") == []


def test_get_adapter_oahaspdf_aliases() -> None:
    assert get_adapter("oahaspdf").name == "oahaspdf"
    assert get_adapter("haspdf-oa").name == "oahaspdf"
    assert get_adapter("works-haspdf-oa").name == "oahaspdf"


def test_parse_oahaspdf_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 40, "cited_by_count": 90},
            {"key": "false", "key_display_name": "false", "count": 7},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahaspdf_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Works with PDF", "Works without PDF"]
    assert hits[0].source == "oahaspdf"
    assert "40 works" in hits[0].snippet
    assert "90 cites" in hits[0].snippet
    assert "filter=has_pdf:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "7 works" in hits[1].snippet
    assert "filter=has_pdf:false" in hits[1].url


def test_parse_oahaspdf_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahaspdf_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with PDF"]


def test_parse_oahaspdf_list_shape() -> None:
    payload = {
        "has_pdf": [
            {"has_pdf": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahaspdf_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without PDF"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahaspdf"
    assert "filter=has_pdf:false" in hits[0].url
