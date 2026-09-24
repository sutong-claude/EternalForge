from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oatfield import OaTFieldAdapter, parse_oatfield_payload
from tools.research import get_adapter


def test_oatfield_empty_query() -> None:
    assert OaTFieldAdapter().search("") == []
    assert OaTFieldAdapter().search("   ") == []


def test_get_adapter_oatfield_aliases() -> None:
    assert get_adapter("oatfield").name == "oatfield"
    assert get_adapter("field-oa").name == "oatfield"
    assert get_adapter("works-field-oa").name == "oatfield"


def test_parse_oatfield_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/fields/17",
                "key_display_name": "Computer science",
                "count": 12,
            },
            {
                "key": "field:27",
                "key_display_name": "Medicine",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "11",
                "display_name": "Economics",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oatfield_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Medicine works",
        "Computer science works",
        "Economics works",
    ]
    assert hits[0].source == "oatfield"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=topics.field.id:27" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=topics.field.id:17" in hits[1].url
    assert "5 works" in hits[2].snippet
    assert "filter=topics.field.id:11" in hits[2].url


def test_parse_oatfield_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "17", "key_display_name": "Alpha Field", "count": 1},
            {"key": "27", "key_display_name": "Beta Field", "count": 2},
        ]
    }
    hits = parse_oatfield_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Beta Field works"]


def test_parse_oatfield_fields_list() -> None:
    payload = {
        "fields": [
            {
                "id": "https://openalex.org/fields/22",
                "display_name": "Engineering",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oatfield_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Engineering works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oatfield"
    assert "filter=topics.field.id:22" in hits[0].url
