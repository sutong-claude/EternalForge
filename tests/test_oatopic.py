from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OaTopicAdapter, get_adapter, parse_oatopic_payload


def test_oatopic_empty_query() -> None:
    assert OaTopicAdapter().search("") == []
    assert OaTopicAdapter().search("   ") == []


def test_get_adapter_oatopic_aliases() -> None:
    assert get_adapter("oatopic").name == "oatopic"
    assert get_adapter("topics-oa").name == "oatopic"
    assert get_adapter("cites-topic-oa").name == "oatopic"


def test_parse_oatopic_payload() -> None:
    payload = {
        "results": [
            {
                "id": "https://openalex.org/T11636",
                "display_name": "Artificial intelligence",
                "keywords": [{"keyword": "machine learning"}, {"keyword": "neural nets"}],
                "domain": {"display_name": "Physical Sciences"},
                "field": {"display_name": "Computer Science"},
                "subfield": {"display_name": "Artificial Intelligence"},
                "works_count": 90000,
                "cited_by_count": 1200000,
                "description": "Systems that learn from data",
            },
            {
                "id": "empty",
                "display_name": "",
            },
            {
                "id": "T12345",
                "display_name": "Natural language processing",
                "works_count": 40000,
            },
        ]
    }
    hits = parse_oatopic_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Artificial intelligence"
    assert hits[0].url == "https://openalex.org/T11636"
    assert hits[0].source == "oatopic"
    assert "Physical Sciences" in hits[0].snippet
    assert "Computer Science" in hits[0].snippet
    assert "machine learning" in hits[0].snippet
    assert "90000 works" in hits[0].snippet
    assert "1200000 cites" in hits[0].snippet
    assert "learn from data" in hits[0].snippet
    assert hits[1].title == "Natural language processing"
    assert hits[1].url == "https://openalex.org/T12345"
    assert "40000 works" in hits[1].snippet


def test_parse_oatopic_respects_limit() -> None:
    payload = {
        "results": [
            {"id": "a", "display_name": "A"},
            {"id": "b", "display_name": "B"},
        ]
    }
    hits = parse_oatopic_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_oatopic_topics_list() -> None:
    payload = {
        "topics": [
            {
                "id": "https://openalex.org/T1",
                "display_name": "From topics list",
            }
        ]
    }
    hits = parse_oatopic_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "From topics list"
    assert hits[0].url == "https://openalex.org/T1"
    assert hits[0].source == "oatopic"
