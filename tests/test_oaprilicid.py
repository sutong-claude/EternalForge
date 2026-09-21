from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oaprilicid import OaPriLicIdAdapter, parse_oaprilicid_payload
from tools.research import get_adapter


def test_oaprilicid_empty_query() -> None:
    assert OaPriLicIdAdapter().search("") == []
    assert OaPriLicIdAdapter().search("   ") == []


def test_get_adapter_oaprilicid_aliases() -> None:
    assert get_adapter("oaprilicid").name == "oaprilicid"
    assert get_adapter("prilicid-oa").name == "oaprilicid"
    assert get_adapter("works-prilicid-oa").name == "oaprilicid"


def test_parse_oaprilicid_payload() -> None:
    payload = {
        "group_by": [
            {"key": "https://creativecommons.org/licenses/by/4.0", "key_display_name": "cc-by-4.0", "count": 12},
            {"key": "https://creativecommons.org/licenses/by-nc/4.0", "key_display_name": "cc-by-nc-4.0", "count": 40, "cited_by_count": 80},
            {"key": "unknown", "count": 3},
            {"key": "https://creativecommons.org/publicdomain/zero/1.0", "key_display_name": "cc0-1.0", "works_count": 5},
        ]
    }
    hits = parse_oaprilicid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == ["cc-by-nc-4.0 works", "cc-by-4.0 works", "cc0-1.0 works"]
    assert hits[0].source == "oaprilicid"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=primary_location.license_id:https://creativecommons.org/licenses/by-nc/4.0" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "5 works" in hits[2].snippet


def test_parse_oaprilicid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "https://creativecommons.org/licenses/by/4.0", "key_display_name": "cc-by-4.0", "count": 1},
            {"key": "https://creativecommons.org/licenses/by-sa/4.0", "key_display_name": "cc-by-sa-4.0", "count": 2},
        ]
    }
    hits = parse_oaprilicid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["cc-by-sa-4.0 works"]


def test_parse_oaprilicid_license_ids_list() -> None:
    payload = {
        "license_ids": [
            {"license_id": "https://creativecommons.org/licenses/by/4.0", "works_count": 7, "cited_by_count": 11},
        ]
    }
    hits = parse_oaprilicid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "https://creativecommons.org/licenses/by/4.0 works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oaprilicid"
    assert "filter=primary_location.license_id:https://creativecommons.org/licenses/by/4.0" in hits[0].url
