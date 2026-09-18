from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OaInstitutionAdapter, get_adapter, parse_oainstitution_payload


def test_oainstitution_empty_query() -> None:
    assert OaInstitutionAdapter().search("") == []
    assert OaInstitutionAdapter().search("   ") == []


def test_get_adapter_oainstitution_aliases() -> None:
    assert get_adapter("oainstitution").name == "oainstitution"
    assert get_adapter("institutions-oa").name == "oainstitution"
    assert get_adapter("cites-institution-oa").name == "oainstitution"


def test_parse_oainstitution_payload() -> None:
    payload = {
        "results": [
            {
                "id": "https://openalex.org/I27837315",
                "display_name": "University of Cambridge",
                "display_name_acronyms": ["Cam"],
                "display_name_alternatives": ["Cambridge University"],
                "country_code": "gb",
                "type": "education",
                "homepage_url": "https://www.cam.ac.uk",
                "works_count": 250000,
                "cited_by_count": 8000000,
                "ids": {"ror": "https://ror.org/013meh722"},
            },
            {
                "id": "empty",
                "display_name": "",
            },
            {
                "id": "I114027177",
                "display_name": "Microsoft Research",
                "country_code": "us",
                "type": "company",
                "associated_institutions": [
                    {"display_name": "Microsoft", "relationship": "parent"}
                ],
                "works_count": 40000,
            },
        ]
    }
    hits = parse_oainstitution_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "University of Cambridge"
    assert hits[0].url == "https://www.cam.ac.uk"
    assert hits[0].source == "oainstitution"
    assert "education" in hits[0].snippet
    assert "GB" in hits[0].snippet
    assert "Cam" in hits[0].snippet
    assert "Cambridge University" in hits[0].snippet
    assert "ror:013meh722" in hits[0].snippet
    assert "250000 works" in hits[0].snippet
    assert "8000000 cites" in hits[0].snippet
    assert hits[1].title == "Microsoft Research"
    assert hits[1].url == "https://openalex.org/I114027177"
    assert "company" in hits[1].snippet
    assert "US" in hits[1].snippet
    assert "parent Microsoft" in hits[1].snippet
    assert "40000 works" in hits[1].snippet


def test_parse_oainstitution_respects_limit() -> None:
    payload = {
        "results": [
            {"id": "a", "display_name": "A"},
            {"id": "b", "display_name": "B"},
        ]
    }
    hits = parse_oainstitution_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_oainstitution_institutions_list() -> None:
    payload = {
        "institutions": [
            {
                "id": "https://openalex.org/I1",
                "display_name": "From institutions list",
            }
        ]
    }
    hits = parse_oainstitution_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "From institutions list"
    assert hits[0].url == "https://openalex.org/I1"
    assert hits[0].source == "oainstitution"
