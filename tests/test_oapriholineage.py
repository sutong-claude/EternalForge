from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oapriholineage import OaPriHoLineageAdapter, parse_oapriholineage_payload
from tools.research import get_adapter


def test_oapriholineage_empty_query() -> None:
    assert OaPriHoLineageAdapter().search("") == []
    assert OaPriHoLineageAdapter().search("   ") == []


def test_get_adapter_oapriholineage_aliases() -> None:
    assert get_adapter("oapriholineage").name == "oapriholineage"
    assert get_adapter("priholineage-oa").name == "oapriholineage"
    assert get_adapter("works-priholineage-oa").name == "oapriholineage"


def test_parse_oapriholineage_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/I4210148051",
                "key_display_name": "Springer Nature",
                "count": 12,
            },
            {
                "key": "https://openalex.org/I4210134890",
                "key_display_name": "Elsevier",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://openalex.org/I4210163894",
                "display_name": "Wiley",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oapriholineage_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Elsevier works", "Springer Nature works", "Wiley works"]
    assert hits[0].source == "oapriholineage"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=primary_location.source.host_organization_lineage:https%3A//openalex.org/I4210134890" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oapriholineage_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "https://openalex.org/I1", "key_display_name": "One", "count": 1},
            {"key": "https://openalex.org/I2", "key_display_name": "Two", "count": 2},
        ]
    }
    hits = parse_oapriholineage_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Two works"]


def test_parse_oapriholineage_lineages_list() -> None:
    payload = {
        "host_organization_lineages": [
            {
                "host_organization_lineage": "https://openalex.org/I4210134890",
                "display_name": "Elsevier",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oapriholineage_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Elsevier works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oapriholineage"
    assert "filter=primary_location.source.host_organization_lineage:https%3A//openalex.org/I4210134890" in hits[0].url
