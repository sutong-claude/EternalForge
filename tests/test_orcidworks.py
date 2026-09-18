from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OrcidWorksAdapter, get_adapter, parse_orcidworks_payload
from tools.orcidworks import extract_orcid_id


def test_orcidworks_empty_query() -> None:
    assert OrcidWorksAdapter().search("") == []
    assert OrcidWorksAdapter().search("   ") == []


def test_get_adapter_orcidworks_aliases() -> None:
    assert get_adapter("orcidworks").name == "orcidworks"
    assert get_adapter("works-orcid").name == "orcidworks"
    assert get_adapter("orcid-works").name == "orcidworks"


def test_extract_orcid_id() -> None:
    assert extract_orcid_id("0000-0002-1825-0097") == "0000-0002-1825-0097"
    assert extract_orcid_id("https://orcid.org/0000-0002-1825-0097") == "0000-0002-1825-0097"
    assert extract_orcid_id("no id here") == ""


def test_parse_orcidworks_payload() -> None:
    payload = {
        "group": [
            {
                "work-summary": [
                    {
                        "title": {"title": {"value": "Attention Is All You Need"}},
                        "type": "journal-article",
                        "publication-date": {"year": {"value": "2017"}},
                        "journal-title": {"value": "NeurIPS"},
                        "url": {"value": "https://doi.org/10.5555/3295222.3295349"},
                        "external-ids": {
                            "external-id": [
                                {
                                    "external-id-type": "doi",
                                    "external-id-value": "10.5555/3295222.3295349",
                                }
                            ]
                        },
                    }
                ]
            },
            {
                "work-summary": [
                    {
                        "title": {"title": {"value": "Generative Adversarial Nets"}},
                        "type": "conference-paper",
                        "publication-date": {"year": {"value": "2014"}},
                    }
                ]
            },
            {"work-summary": [{"title": {"title": {"value": ""}}, "url": {}}]},
        ]
    }
    hits = parse_orcidworks_payload(payload, limit=5, orcid="0000-0002-1825-0097")
    assert len(hits) == 2
    assert hits[0].title == "Attention Is All You Need"
    assert hits[0].url == "https://doi.org/10.5555/3295222.3295349"
    assert hits[0].source == "orcidworks"
    assert "journal article" in hits[0].snippet
    assert "2017" in hits[0].snippet
    assert "NeurIPS" in hits[0].snippet
    assert "10.5555/3295222.3295349" in hits[0].snippet
    assert hits[1].title == "Generative Adversarial Nets"
    assert hits[1].url == "https://orcid.org/0000-0002-1825-0097"
    assert "2014" in hits[1].snippet


def test_parse_orcidworks_respects_limit() -> None:
    payload = {
        "group": [
            {"work-summary": [{"title": {"title": {"value": "A"}}}]},
            {"work-summary": [{"title": {"title": {"value": "B"}}}]},
        ]
    }
    hits = parse_orcidworks_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_orcidworks_work_summary_list() -> None:
    payload = {
        "work-summary": [
            {
                "title": {"value": "From summary list"},
                "external-ids": {
                    "external-id": [
                        {"external-id-type": "doi", "external-id-value": "10.1/xyz"}
                    ]
                },
            }
        ]
    }
    hits = parse_orcidworks_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "From summary list"
    assert hits[0].url == "https://doi.org/10.1/xyz"
    assert hits[0].source == "orcidworks"
    assert "10.1/xyz" in hits[0].snippet
