from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaparatext import OaParatextAdapter, parse_oaparatext_payload
from tools.research import get_adapter


def test_oaparatext_empty_query() -> None:
    assert OaParatextAdapter().search("") == []
    assert OaParatextAdapter().search("   ") == []


def test_get_adapter_oaparatext_aliases() -> None:
    assert get_adapter("oaparatext").name == "oaparatext"
    assert get_adapter("paratext-oa").name == "oaparatext"
    assert get_adapter("works-paratext-oa").name == "oaparatext"


def test_parse_oaparatext_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 4, "cited_by_count": 12},
            {"key": "false", "key_display_name": "false", "count": 80},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oaparatext_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Not paratext works", "Paratext works"]
    assert hits[0].source == "oaparatext"
    assert "80 works" in hits[0].snippet
    assert "filter=is_paratext:false" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "4 works" in hits[1].snippet
    assert "12 cites" in hits[1].snippet
    assert "filter=is_paratext:true" in hits[1].url


def test_parse_oaparatext_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 1},
            {"key": "false", "count": 9},
        ]
    }
    hits = parse_oaparatext_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Not paratext works"]


def test_parse_oaparatext_list_shape() -> None:
    payload = {
        "paratext": [
            {"is_paratext": True, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oaparatext_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Paratext works"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oaparatext"
    assert "filter=is_paratext:true" in hits[0].url
