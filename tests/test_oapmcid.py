from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.oapmcid import OaPmcidAdapter, parse_oapmcid_payload
from tools.research import get_adapter


def test_oapmcid_empty_query() -> None:
    assert OaPmcidAdapter().search("") == []
    assert OaPmcidAdapter().search("   ") == []


def test_get_adapter_oapmcid_aliases() -> None:
    assert get_adapter("oapmcid").name == "oapmcid"
    assert get_adapter("pmcid-oa").name == "oapmcid"
    assert get_adapter("works-pmcid-oa").name == "oapmcid"


def test_parse_oapmcid_payload() -> None:
    payload = {
        "group_by": [
            {
                "key": "PMC1234567",
                "key_display_name": "PMC1234567",
                "count": 12,
            },
            {
                "key": "PMC7654321",
                "key_display_name": "PMC7654321",
                "count": 40,
                "cited_by_count": 80,
            },
            {"key": "unknown", "count": 3},
            {
                "key": "PMC1122334",
                "display_name": "PMC1122334",
                "works_count": 5,
            },
        ]
    }
    hits = parse_oapmcid_payload(payload, limit=5, query="attention")
    assert [h.title for h in hits] == [
        "PMC7654321 works",
        "PMC1234567 works",
        "PMC1122334 works",
    ]
    assert hits[0].source == "oapmcid"
    assert "40 works" in hits[0].snippet
    assert "80 cites" in hits[0].snippet
    assert "filter=ids.pmcid:PMC7654321" in hits[0].url
    assert "search=attention" in hits[0].url
    assert "12 works" in hits[1].snippet
    assert "filter=ids.pmcid:PMC1234567" in hits[1].url
    assert "5 works" in hits[2].snippet


def test_parse_oapmcid_respects_limit() -> None:
    payload = {
        "group_by": [
            {"key": "PMC1", "key_display_name": "PMC1", "count": 1},
            {"key": "PMC2", "key_display_name": "PMC2", "count": 2},
        ]
    }
    hits = parse_oapmcid_payload(payload, limit=1)
    assert [h.title for h in hits] == ["PMC2 works"]


def test_parse_oapmcid_pmcids_list() -> None:
    payload = {
        "pmcids": [
            {
                "pmcid": "PMC1234567",
                "display_name": "PMC1234567",
                "works_count": 7,
                "cited_by_count": 11,
            },
        ]
    }
    hits = parse_oapmcid_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "PMC1234567 works"
    assert "7 works" in hits[0].snippet
    assert "11 cites" in hits[0].snippet
    assert hits[0].source == "oapmcid"
    assert "filter=ids.pmcid:PMC1234567" in hits[0].url
