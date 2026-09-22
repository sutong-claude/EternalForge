from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oalocissn import OaLocIssnAdapter, parse_oalocissn_payload
from tools.research import get_adapter


def test_oalocissn_empty_query() -> None:
    assert OaLocIssnAdapter().search("") == []
    assert OaLocIssnAdapter().search("   ") == []


def test_get_adapter_oalocissn_aliases() -> None:
    assert get_adapter("oalocissn").name == "oalocissn"
    assert get_adapter("locissn-oa").name == "oalocissn"
    assert get_adapter("works-locissn-oa").name == "oalocissn"


def test_parse_oalocissn_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "0028-0836",
                "key_display_name": "0028-0836",
                "count": 12,
            },
            {
                "key": "2041-1723",
                "key_display_name": "2041-1723",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "1476-4687",
                "display_name": "1476-4687",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oalocissn_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["2041-1723 works", "0028-0836 works", "1476-4687 works"]
    assert hits[0].source == "oalocissn"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=locations.source.issn_l:2041-1723" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=locations.source.issn_l:0028-0836" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oalocissn_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "0028-0836", "key_display_name": "0028-0836", "count": 1},
            {"key": "2041-1723", "key_display_name": "2041-1723", "count": 2},
        ]
    }
    hits = parse_oalocissn_payload(payload, limit=1)
    assert [h.title for h in hits] == ["2041-1723 works"]


def test_parse_oalocissn_issn_ls_list() -> None:
    payload = {
        "issn_ls": [
            {"issn_l": "2041-1723", "display_name": "2041-1723", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oalocissn_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "2041-1723 works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oalocissn"
    assert "filter=locations.source.issn_l:2041-1723" in hits[0].url
