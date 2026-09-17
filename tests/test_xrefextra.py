from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import XrefExtraAdapter, get_adapter, parse_xrefextra_payload


def test_xrefextra_empty_query() -> None:
    assert XrefExtraAdapter().search("") == []
    assert XrefExtraAdapter().search("   ") == []


def test_get_adapter_xrefextra_aliases() -> None:
    assert get_adapter("xrefextra").name == "xrefextra"
    assert get_adapter("cr-extra").name == "xrefextra"
    assert get_adapter("cites-xr").name == "xrefextra"


def test_parse_xrefextra_payload() -> None:
    payload = {
        "message": {
            "items": [
                {
                    "title": ["Attention Is All You Need"],
                    "DOI": "10.5555/3295222.3295349",
                    "URL": "https://doi.org/10.5555/3295222.3295349",
                    "author": [
                        {"given": "Ashish", "family": "Vaswani"},
                        {"given": "Noam", "family": "Shazeer"},
                    ],
                    "issued": {"date-parts": [[2017, 6, 12]]},
                    "container-title": ["NeurIPS"],
                    "type": "proceedings-article",
                    "is-referenced-by-count": 84210,
                    "license": [{"URL": "https://creativecommons.org/licenses/by/4.0"}],
                    "subject": ["Machine learning", "NLP"],
                    "abstract": "<jats:p>We propose the Transformer.</jats:p>",
                },
                {
                    "title": ["Generative Adversarial Nets"],
                    "DOI": "10.5555/2969033.2969125",
                    "author": [{"given": "Ian", "family": "Goodfellow"}],
                    "issued": {"date-parts": [[2014]]},
                    "type": "journal-article",
                },
                {"title": [], "DOI": "", "URL": ""},
            ]
        }
    }
    hits = parse_xrefextra_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Attention Is All You Need"
    assert hits[0].url == "https://doi.org/10.5555/3295222.3295349"
    assert hits[0].source == "xrefextra"
    assert "Vaswani" in hits[0].snippet
    assert "2017" in hits[0].snippet
    assert "NeurIPS" in hits[0].snippet
    assert "84210 cites" in hits[0].snippet
    assert "by" in hits[0].snippet
    assert "Transformer" in hits[0].snippet
    assert hits[1].title == "Generative Adversarial Nets"
    assert hits[1].url == "https://doi.org/10.5555/2969033.2969125"
    assert "Goodfellow" in hits[1].snippet
    assert "2014" in hits[1].snippet


def test_parse_xrefextra_respects_limit() -> None:
    payload = {
        "message": {
            "items": [
                {"title": ["A"], "URL": "https://doi.org/a"},
                {"title": ["B"], "URL": "https://doi.org/b"},
            ]
        }
    }
    hits = parse_xrefextra_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_xrefextra_works_list() -> None:
    payload = {
        "works": [
            {
                "title": ["Standalone extras hit"],
                "DOI": "10.1234/xr.1",
                "issued": {"date-parts": [[2020]]},
                "is-referenced-by-count": 12,
            }
        ]
    }
    hits = parse_xrefextra_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone extras hit"
    assert hits[0].url == "https://doi.org/10.1234/xr.1"
    assert "2020" in hits[0].snippet
    assert "12 cites" in hits[0].snippet
