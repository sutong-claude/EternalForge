from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OaConceptAdapter, get_adapter, parse_oaconcept_payload


def test_oaconcept_empty_query() -> None:
    assert OaConceptAdapter().search("") == []
    assert OaConceptAdapter().search("   ") == []


def test_get_adapter_oaconcept_aliases() -> None:
    assert get_adapter("oaconcept").name == "oaconcept"
    assert get_adapter("concepts-oa").name == "oaconcept"
    assert get_adapter("cites-concept-oa").name == "oaconcept"


def test_parse_oaconcept_payload() -> None:
    payload = {
        "results": [
            {
                "id": "https://openalex.org/C154945302",
                "display_name": "Artificial intelligence",
                "level": 1,
                "ancestors": [{"display_name": "Computer science"}],
                "related_concepts": [{"display_name": "Machine learning"}],
                "works_count": 90000,
                "cited_by_count": 1200000,
                "description": "Systems that learn from data",
            },
            {
                "id": "empty",
                "display_name": "",
            },
            {
                "id": "C12345",
                "display_name": "Natural language processing",
                "works_count": 40000,
            },
        ]
    }
    hits = parse_oaconcept_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Artificial intelligence"
    assert hits[0].url == "https://openalex.org/C154945302"
    assert hits[0].source == "oaconcept"
    assert "L1" in hits[0].snippet
    assert "Computer science" in hits[0].snippet
    assert "Machine learning" in hits[0].snippet
    assert "90000 works" in hits[0].snippet
    assert "1200000 cites" in hits[0].snippet
    assert "learn from data" in hits[0].snippet
    assert hits[1].title == "Natural language processing"
    assert hits[1].url == "https://openalex.org/C12345"
    assert "40000 works" in hits[1].snippet


def test_parse_oaconcept_respects_limit() -> None:
    payload = {
        "results": [
            {"id": "a", "display_name": "A"},
            {"id": "b", "display_name": "B"},
        ]
    }
    hits = parse_oaconcept_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_oaconcept_concepts_list() -> None:
    payload = {
        "concepts": [
            {
                "id": "https://openalex.org/C1",
                "display_name": "From concepts list",
            }
        ]
    }
    hits = parse_oaconcept_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "From concepts list"
    assert hits[0].url == "https://openalex.org/C1"
    assert hits[0].source == "oaconcept"
