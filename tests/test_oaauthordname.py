from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaauthordname import OaAuthorDnameAdapter, parse_oaauthordname_payload
from tools.research import get_adapter


def test_oaauthordname_empty_query() -> None:
    assert OaAuthorDnameAdapter().search("") == []
    assert OaAuthorDnameAdapter().search("   ") == []


def test_get_adapter_oaauthordname_aliases() -> None:
    assert get_adapter("oaauthordname").name == "oaauthordname"
    assert get_adapter("authordname-oa").name == "oaauthordname"
    assert get_adapter("works-authordname-oa").name == "oaauthordname"


def test_parse_oaauthordname_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "Josiah Carberry",
                "key_display_name": "Josiah Carberry",
                "count": 12,
            },
            {
                "key": "Yann LeCun",
                "key_display_name": "Yann LeCun",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "Geoffrey Hinton",
                "display_name": "Geoffrey Hinton",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaauthordname_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Yann LeCun works",
        "Josiah Carberry works",
        "Geoffrey Hinton works",
    ]
    assert hits[0].source == "oaauthordname"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=authorships.author.display_name:Yann%20LeCun" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=authorships.author.display_name:Josiah%20Carberry" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oaauthordname_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "Alice", "key_display_name": "Alice", "count": 1},
            {"key": "Bob", "key_display_name": "Bob", "count": 2},
        ]
    }
    hits = parse_oaauthordname_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Bob works"]


def test_parse_oaauthordname_names_list() -> None:
    payload = {
        "display_names": [
            {
                "display_name": "Josiah Carberry",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaauthordname_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Josiah Carberry works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaauthordname"
    assert "filter=authorships.author.display_name:Josiah%20Carberry" in hits[0].url
