from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthororcid import OaAuthorOrcidAdapter, parse_oaauthororcid_payload
from tools.research import get_adapter


def test_oaauthororcid_empty_query() -> None:
    assert OaAuthorOrcidAdapter().search("") == []
    assert OaAuthorOrcidAdapter().search("   ") == []


def test_get_adapter_oaauthororcid_aliases() -> None:
    assert get_adapter("oaauthororcid").name == "oaauthororcid"
    assert get_adapter("authororcid-oa").name == "oaauthororcid"
    assert get_adapter("works-authororcid-oa").name == "oaauthororcid"


def test_parse_oaauthororcid_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://orcid.org/0000-0002-1825-0097",
                "key_display_name": "Josiah Carberry",
                "count": 12,
            },
            {
                "key": "0000-0001-5109-3700",
                "key_display_name": "Yann LeCun",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://orcid.org/0000-0002-3545-4444",
                "display_name": "Geoffrey Hinton",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaauthororcid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Yann LeCun works",
        "Josiah Carberry works",
        "Geoffrey Hinton works",
    ]
    assert hits[0].source == "oaauthororcid"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=authorships.author.orcid:0000-0001-5109-3700" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=authorships.author.orcid:0000-0002-1825-0097" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaauthororcid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "0000-0000-0000-0001", "key_display_name": "Alice", "count": 1},
            {"key": "0000-0000-0000-0002", "key_display_name": "Bob", "count": 2},
        ]
    }
    hits = parse_oaauthororcid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Bob works"]


def test_parse_oaauthororcid_orcids_list() -> None:
    payload = {
        "orcids": [
            {
                "orcid": "https://orcid.org/0000-0002-1825-0097",
                "display_name": "Josiah Carberry",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaauthororcid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Josiah Carberry works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaauthororcid"
    assert "filter=authorships.author.orcid:0000-0002-1825-0097" in hits[0].url
