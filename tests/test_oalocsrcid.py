from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oalocsrcid import OaLocSrcIdAdapter, parse_oalocsrcid_payload
from tools.research import get_adapter


def test_oalocsrcid_empty_query() -> None:
    assert OaLocSrcIdAdapter().search("") == []
    assert OaLocSrcIdAdapter().search("   ") == []


def test_get_adapter_oalocsrcid_aliases() -> None:
    assert get_adapter("oalocsrcid").name == "oalocsrcid"
    assert get_adapter("locsrcid-oa").name == "oalocsrcid"
    assert get_adapter("works-locsrcid-oa").name == "oalocsrcid"


def test_parse_oalocsrcid_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/S137773608",
                "key_display_name": "Nature",
                "count": 12,
            },
            {
                "key": "S2764455111",
                "key_display_name": "arXiv",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://openalex.org/S4306400194",
                "display_name": "bioRxiv",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oalocsrcid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["arXiv works", "Nature works", "bioRxiv works"]
    assert hits[0].source == "oalocsrcid"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=locations.source.id:S2764455111" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=locations.source.id:S137773608" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oalocsrcid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "S1", "key_display_name": "Nature", "count": 1},
            {"key": "S2", "key_display_name": "Science", "count": 2},
        ]
    }
    hits = parse_oalocsrcid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Science works"]


def test_parse_oalocsrcid_source_ids_list() -> None:
    payload = {
        "source_ids": [
            {"source": "https://openalex.org/S137773608", "display_name": "Nature", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oalocsrcid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Nature works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oalocsrcid"
    assert "filter=locations.source.id:S137773608" in hits[0].url
