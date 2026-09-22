from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oalocholineage import OaLocHoLineageAdapter, parse_oalocholineage_payload
from tools.research import get_adapter


def test_oalocholineage_empty_query() -> None:
    assert OaLocHoLineageAdapter().search("") == []
    assert OaLocHoLineageAdapter().search("   ") == []


def test_get_adapter_oalocholineage_aliases() -> None:
    assert get_adapter("oalocholineage").name == "oalocholineage"
    assert get_adapter("locholineage-oa").name == "oalocholineage"
    assert get_adapter("works-locholineage-oa").name == "oalocholineage"


def test_parse_oalocholineage_payload() -> None:
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
    hits = parse_oalocholineage_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["Elsevier works", "Springer Nature works", "Wiley works"]
    assert hits[0].source == "oalocholineage"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=locations.source.host_organization_lineage:https%3A//openalex.org/I4210134890" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oalocholineage_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "https://openalex.org/I1", "key_display_name": "One", "count": 1},
            {"key": "https://openalex.org/I2", "key_display_name": "Two", "count": 2},
        ]
    }
    hits = parse_oalocholineage_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Two works"]


def test_parse_oalocholineage_lineages_list() -> None:
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
    hits = parse_oalocholineage_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Elsevier works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oalocholineage"
    assert "filter=locations.source.host_organization_lineage:https%3A//openalex.org/I4210134890" in hits[0].url
