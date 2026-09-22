from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oalocholinames import OaLocHoLinamesAdapter, parse_oalocholinames_payload
from tools.research import get_adapter


def test_oalocholinames_empty_query() -> None:
    assert OaLocHoLinamesAdapter().search("") == []
    assert OaLocHoLinamesAdapter().search("   ") == []


def test_get_adapter_oalocholinames_aliases() -> None:
    assert get_adapter("oalocholinames").name == "oalocholinames"
    assert get_adapter("locholinames-oa").name == "oalocholinames"
    assert get_adapter("works-locholinames-oa").name == "oalocholinames"


def test_parse_oalocholinames_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "Springer Nature",
                "key_display_name": "Springer Nature",
                "count": 12,
            },
            {
                "key": "Elsevier",
                "key_display_name": "Elsevier",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "Wiley",
                "display_name": "Wiley",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oalocholinames_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Elsevier works", "Springer Nature works", "Wiley works"]
    assert hits[0].source == "oalocholinames"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=locations.source.host_organization_lineage_names:Elsevier" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=locations.source.host_organization_lineage_names:Springer%20Nature" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oalocholinames_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "One", "key_display_name": "One", "count": 1},
            {"key": "Two", "key_display_name": "Two", "count": 2},
        ]
    }
    hits = parse_oalocholinames_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Two works"]


def test_parse_oalocholinames_names_list() -> None:
    payload = {
        "host_organization_lineage_names": [
            {
                "host_organization_lineage_names": "Elsevier",
                "display_name": "Elsevier",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oalocholinames_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Elsevier works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oalocholinames"
    assert "filter=locations.source.host_organization_lineage_names:Elsevier" in hits[0].url
