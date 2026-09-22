from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthlin import OaAuthLinAdapter, parse_oaauthlin_payload
from tools.research import get_adapter


def test_oaauthlin_empty_query() -> None:
    assert OaAuthLinAdapter().search("") == []
    assert OaAuthLinAdapter().search("   ") == []


def test_get_adapter_oaauthlin_aliases() -> None:
    assert get_adapter("oaauthlin").name == "oaauthlin"
    assert get_adapter("authlin-oa").name == "oaauthlin"
    assert get_adapter("works-authlin-oa").name == "oaauthlin"


def test_parse_oaauthlin_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/I27037357",
                "key_display_name": "University of Michigan",
                "count": 12,
            },
            {
                "key": "https://openalex.org/I136199984",
                "key_display_name": "Harvard University",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://openalex.org/I97018004",
                "display_name": "Stanford University",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaauthlin_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Harvard University works",
        "University of Michigan works",
        "Stanford University works",
    ]
    assert hits[0].source == "oaauthlin"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=authorships.institutions.lineage:https%3A//openalex.org/I136199984" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=authorships.institutions.lineage:https%3A//openalex.org/I27037357" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaauthlin_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "https://openalex.org/I1", "key_display_name": "One", "count": 1},
            {"key": "https://openalex.org/I2", "key_display_name": "Two", "count": 2},
        ]
    }
    hits = parse_oaauthlin_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Two works"]


def test_parse_oaauthlin_lineages_list() -> None:
    payload = {
        "lineages": [
            {
                "lineage": "https://openalex.org/I136199984",
                "display_name": "Harvard University",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaauthlin_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Harvard University works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaauthlin"
    assert "filter=authorships.institutions.lineage:https%3A//openalex.org/I136199984" in hits[0].url
