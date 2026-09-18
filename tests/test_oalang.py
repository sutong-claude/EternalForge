from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OaLangAdapter, get_adapter, parse_oalang_payload


def test_oalang_empty_query() -> None:
    assert OaLangAdapter().search("") == []
    assert OaLangAdapter().search("   ") == []


def test_get_adapter_oalang_aliases() -> None:
    assert get_adapter("oalang").name == "oalang"
    assert get_adapter("languages-oa").name == "oalang"
    assert get_adapter("works-lang-oa").name == "oalang"


def test_parse_oalang_payload() -> None:
    payload = {
        "group_by": [
            {"key": "zh", "key_display_name": "Chinese", "count": 10},
            {"key": "en", "key_display_name": "English", "count": 40, "cited_by_count": 900},
            {"key": "unknown", "count": 3},
            {"key": "es", "key_display_name": "Spanish", "works_count": 5},
        ]
    }
    hits = parse_oalang_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["English works", "Chinese works", "Spanish works"]
    assert hits[0].source == "oalang"
    assert "40 works" in hits[0].snippet
    assert "900 cites" in hits[0].snippet
    assert "filter=language:en" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "10 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oalang_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "fr", "key_display_name": "French", "count": 1},
            {"key": "en", "key_display_name": "English", "count": 2},
        ]
    }
    hits = parse_oalang_payload(payload, limit=1)
    assert [h.title for h in hits] == ["English works"]


def test_parse_oalang_languages_list() -> None:
    payload = {
        "languages": [
            {"language": "de", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oalang_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "de works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oalang"
    assert "filter=language:de" in hits[0].url
