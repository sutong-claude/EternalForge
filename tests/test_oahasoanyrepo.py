from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oahasoanyrepo import OaHasOaAnyRepoAdapter, parse_oahasoanyrepo_payload
from tools.research import get_adapter


def test_oahasoanyrepo_empty_query() -> None:
    assert OaHasOaAnyRepoAdapter().search("") == []
    assert OaHasOaAnyRepoAdapter().search("   ") == []


def test_get_adapter_oahasoanyrepo_aliases() -> None:
    assert get_adapter("oahasoanyrepo").name == "oahasoanyrepo"
    assert get_adapter("hasoanyrepo-oa").name == "oahasoanyrepo"
    assert get_adapter("works-hasoanyrepo-oa").name == "oahasoanyrepo"


def test_parse_oahasoanyrepo_payload() -> None:
    payload = {
        "group_by": [
            {"key": "true", "key_display_name": "true", "count": 18, "cited_by_count": 41},
            {"key": "false", "key_display_name": "false", "count": 6},
            {"key": "unknown", "count": 3},
        ]
    }
    hits = parse_oahasoanyrepo_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "Works with any OA repository",
        "Works without any OA repository",
    ]
    assert hits[0].source == "oahasoanyrepo"
    assert "18 works" in hits[0].snippet
    assert "41 cites" in hits[0].snippet
    assert "filter=has_oa_any_repository:true" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "6 works" in hits[1].snippet
    assert "filter=has_oa_any_repository:false" in hits[1].url


def test_parse_oahasoanyrepo_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "true", "count": 9},
            {"key": "false", "count": 1},
        ]
    }
    hits = parse_oahasoanyrepo_payload(payload, limit=1)
    assert [h.title for h in hits] == ["Works with any OA repository"]


def test_parse_oahasoanyrepo_list_shape() -> None:
    payload = {
        "has_oa_any_repository": [
            {"has_oa_any_repository": False, "works_count": 2, "cited_by_count": 5},
        ]
    }
    hits = parse_oahasoanyrepo_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Works without any OA repository"
    assert "2 works" in hits[0].snippet
    assert "5 cites" in hits[0].snippet
    assert hits[0].source == "oahasoanyrepo"
    assert "filter=has_oa_any_repository:false" in hits[0].url
