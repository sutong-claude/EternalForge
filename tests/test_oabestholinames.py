from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oabestholinames import OaBestHoLinamesAdapter, parse_oabestholinames_payload
from tools.research import get_adapter


def test_oabestholinames_empty_query() -> None:
    assert OaBestHoLinamesAdapter().search("") == []
    assert OaBestHoLinamesAdapter().search("   ") == []


def test_get_adapter_oabestholinames_aliases() -> None:
    assert get_adapter("oabestholinames").name == "oabestholinames"
    assert get_adapter("bestholinames-oa").name == "oabestholinames"
    assert get_adapter("works-bestholinames-oa").name == "oabestholinames"


def test_parse_oabestholinames_payload() -> None:
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
    hits = parse_oabestholinames_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Elsevier works", "Springer Nature works", "Wiley works"]
    assert hits[0].source == "oabestholinames"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=best_oa_location.source.host_organization_lineage_names:Elsevier" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=best_oa_location.source.host_organization_lineage_names:Springer%20Nature" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oabestholinames_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "One", "key_display_name": "One", "count": 1},
            {"key": "Two", "key_display_name": "Two", "count": 2},
        ]
    }
    hits = parse_oabestholinames_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Two works"]


def test_parse_oabestholinames_names_list() -> None:
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
    hits = parse_oabestholinames_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Elsevier works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oabestholinames"
    assert "filter=best_oa_location.source.host_organization_lineage_names:Elsevier" in hits[0].url
