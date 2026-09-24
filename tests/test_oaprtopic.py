from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaprtopic import OaPrTopicAdapter, parse_oaprtopic_payload
from tools.research import get_adapter


def test_oaprtopic_empty_query() -> None:
    assert OaPrTopicAdapter().search("") == []
    assert OaPrTopicAdapter().search("   ") == []


def test_get_adapter_oaprtopic_aliases() -> None:
    assert get_adapter("oaprtopic").name == "oaprtopic"
    assert get_adapter("prtopic-oa").name == "oaprtopic"
    assert get_adapter("works-prtopic-oa").name == "oaprtopic"


def test_parse_oaprtopic_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "https://openalex.org/T11636",
                "key_display_name": "Artificial intelligence",
                "count": 12,
            },
            {
                "key": "topic:T11922",
                "key_display_name": "Machine learning",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "T10180",
                "display_name": "Natural language processing",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oaprtopic_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Machine learning works",
        "Artificial intelligence works",
        "Natural language processing works",
    ]
    assert hits[0].source == "oaprtopic"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=primary_topic.id:T11922" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=primary_topic.id:T11636" in hits[1].url
    assert "5 works" in hits[2].snippet
    assert "filter=primary_topic.id:T10180" in hits[2].url


def test_parse_oaprtopic_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "T1", "key_display_name": "Alpha", "count": 1},
            {"key": "T2", "key_display_name": "Beta", "count": 2},
        ]
    }
    hits = parse_oaprtopic_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Beta works"]


def test_parse_oaprtopic_primary_topics_list() -> None:
    payload = {
        "primary_topics": [
            {
                "id": "https://openalex.org/T10905",
                "display_name": "Computer vision",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oaprtopic_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Computer vision works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaprtopic"
    assert "filter=primary_topic.id:T10905" in hits[0].url
