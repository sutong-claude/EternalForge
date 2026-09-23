from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthorcorr import OaAuthorCorrAdapter, parse_oaauthorcorr_payload
from tools.research import get_adapter


def test_oaauthorcorr_empty_query() -> None:
    assert OaAuthorCorrAdapter().search("") == []
    assert OaAuthorCorrAdapter().search("   ") == []


def test_get_adapter_oaauthorcorr_aliases() -> None:
    assert get_adapter("oaauthorcorr").name == "oaauthorcorr"
    assert get_adapter("authorcorr-oa").name == "oaauthorcorr"
    assert get_adapter("works-authorcorr-oa").name == "oaauthorcorr"


def test_parse_oaauthorcorr_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oaauthorcorr_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with a corresponding authorship",
        "Works without a corresponding authorship",
    ]
    assert hits[0].source == "oaauthorcorr"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=authorships.is_corresponding:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=authorships.is_corresponding:false" in hits[1].url


def test_parse_oaauthorcorr_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oaauthorcorr_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with a corresponding authorship"]


def test_parse_oaauthorcorr_list_shape() -> None:
    payload = {
        "is_corresponding": [
            {"is_corresponding": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oaauthorcorr_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without a corresponding authorship"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oaauthorcorr"
    assert "filter=authorships.is_corresponding:false" in hits[0].url
