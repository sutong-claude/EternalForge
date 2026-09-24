from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaconcid import OaConcIdAdapter, parse_oaconcid_payload
from tools.research import get_adapter


def test_oaconcid_empty_query() -> None:
    assert OaConcIdAdapter().search("") == []
    assert OaConcIdAdapter().search("   ") == []


def test_get_adapter_oaconcid_aliases() -> None:
    assert get_adapter("oaconcid").name == "oaconcid"
    assert get_adapter("concid-oa").name == "oaconcid"
    assert get_adapter("works-concid-oa").name == "oaconcid"


def test_parse_oaconcid_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "C41008148",
                "key_display_name": "Computer science",
                "count": 12,
            },
            {
                "key": "concept:C154945302",
                "key_display_name": "Artificial intelligence",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "https://openalex.org/C71924100",
                "display_name": "Medicine",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaconcid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Artificial intelligence works",
        "Computer science works",
        "Medicine works",
    ]
    assert hits[0].source == "oaconcid"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=concepts.id:C154945302" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=concepts.id:C41008148" in hits[1].url
    assert "5 works" in hits[2].snippet
    assert "filter=concepts.id:C71924100" in hits[2].url


def test_parse_oaconcid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "C1", "key_display_name": "alpha", "count": 1},
            {"key": "C2", "key_display_name": "beta", "count": 2},
        ]
    }
    hits = parse_oaconcid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["beta works"]


def test_parse_oaconcid_concepts_list() -> None:
    payload = {
        "concepts": [
            {
                "id": "https://openalex.org/C2778407486",
                "display_name": "Deep learning",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaconcid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Deep learning works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaconcid"
    assert "filter=concepts.id:C2778407486" in hits[0].url
