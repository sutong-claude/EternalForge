from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OrcidExtraAdapter, get_adapter, parse_orcidextra_payload


def test_orcidextra_empty_query() -> None:
    assert OrcidExtraAdapter().search("") == []
    assert OrcidExtraAdapter().search("   ") == []


def test_get_adapter_orcidextra_aliases() -> None:
    assert get_adapter("orcidextra").name == "orcidextra"
    assert get_adapter("orcid-extra").name == "orcidextra"
    assert get_adapter("ids-orcid").name == "orcidextra"


def test_parse_orcidextra_payload() -> None:
    payload = {
        "num-found": 2,
        "expanded-result": [
            {
                "orcid-id": "0000-0002-1825-0097",
                "given-names": "Josiah",
                "family-names": "Carberry",
                "credit-name": "Josiah Stinkney Carberry",
                "other-name": ["J. Carberry"],
                "institution-name": ["Brown University"],
            },
            {
                "orcid-id": "0000-0001-5109-3700",
                "given-names": "Sofia",
                "family-names": "Garcia",
                "institution-name": ["CERN"],
            },
            {"orcid-id": "", "given-names": "", "family-names": ""},
        ],
    }
    hits = parse_orcidextra_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Josiah Stinkney Carberry"
    assert hits[0].url == "https://orcid.org/0000-0002-1825-0097"
    assert hits[0].source == "orcidextra"
    assert "0000-0002-1825-0097" in hits[0].snippet
    assert "Brown University" in hits[0].snippet
    assert "J. Carberry" in hits[0].snippet
    assert hits[1].title == "Sofia Garcia"
    assert hits[1].url == "https://orcid.org/0000-0001-5109-3700"
    assert "CERN" in hits[1].snippet


def test_parse_orcidextra_respects_limit() -> None:
    payload = {
        "expanded-result": [
            {"orcid-id": "0000-0000-0000-0001", "given-names": "A", "family-names": "One"},
            {"orcid-id": "0000-0000-0000-0002", "given-names": "B", "family-names": "Two"},
        ]
    }
    hits = parse_orcidextra_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A One"]


def test_parse_orcidextra_result_list() -> None:
    payload = {
        "result": [
            {
                "orcid-identifier": {
                    "uri": "https://orcid.org/0000-0002-1825-0097",
                    "path": "0000-0002-1825-0097",
                    "host": "orcid.org",
                }
            }
        ]
    }
    hits = parse_orcidextra_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "0000-0002-1825-0097"
    assert hits[0].url == "https://orcid.org/0000-0002-1825-0097"
    assert "0000-0002-1825-0097" in hits[0].snippet
