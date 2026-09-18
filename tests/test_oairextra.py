from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OaireExtraAdapter, get_adapter, parse_oairextra_payload


def test_oairextra_empty_query() -> None:
    assert OaireExtraAdapter().search("") == []
    assert OaireExtraAdapter().search("   ") == []


def test_get_adapter_oairextra_aliases() -> None:
    assert get_adapter("oairextra").name == "oairextra"
    assert get_adapter("oaire-extra").name == "oairextra"
    assert get_adapter("cites-oaire").name == "oairextra"


def test_parse_oairextra_payload() -> None:
    payload = {
        "results": [
            {
                "id": "dedup::abc",
                "mainTitle": "Attention sharing in infancy",
                "type": "publication",
                "publicationDate": "2023-04-01",
                "authors": [{"fullName": "Doe, Jane"}, {"fullName": "Roe, Sam"}],
                "descriptions": ["A study of joint attention."],
                "pids": [{"scheme": "doi", "value": "10.1234/oa.1"}],
                "instances": [{"urls": ["https://example.org/attention"]}],
                "bestAccessRight": {"label": "OPEN"},
                "subjects": [{"subject": {"label": "Psychology"}}, {"label": "Development"}],
                "language": {"code": "en", "label": "English"},
                "publishers": ["Example Press"],
                "indicators": {"citationImpact": {"citationCount": 42}},
            },
            {
                "id": "soft::1",
                "mainTitle": "keras-attention-mechanism",
                "type": "software",
                "authors": [{"name": "Remy, Philippe"}],
                "codeRepositoryUrl": "https://github.com/philipperemy/keras-attention-mechanism",
            },
            {"id": "", "mainTitle": ""},
        ]
    }
    hits = parse_oairextra_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Attention sharing in infancy"
    assert hits[0].url == "https://example.org/attention"
    assert hits[0].source == "oairextra"
    assert "Doe" in hits[0].snippet
    assert "2023" in hits[0].snippet
    assert "publication" in hits[0].snippet
    assert "OPEN" in hits[0].snippet
    assert "Psychology" in hits[0].snippet
    assert "42 cites" in hits[0].snippet
    assert "Example Press" in hits[0].snippet
    assert "English" in hits[0].snippet
    assert "joint attention" in hits[0].snippet
    assert hits[1].title == "keras-attention-mechanism"
    assert hits[1].url == "https://github.com/philipperemy/keras-attention-mechanism"
    assert "software" in hits[1].snippet


def test_parse_oairextra_respects_limit() -> None:
    payload = {
        "results": [
            {"id": "a", "mainTitle": "A"},
            {"id": "b", "mainTitle": "B"},
        ]
    }
    hits = parse_oairextra_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_oairextra_research_products_list() -> None:
    payload = {
        "researchProducts": [
            {
                "title": "Standalone extras hit",
                "pids": [{"scheme": "doi", "value": "10.9/soft"}],
                "publicationDate": "2021",
                "bestAccessRight": {"label": "embargo"},
                "indicators": {"citationImpact": {"citationCount": 3}},
            }
        ]
    }
    hits = parse_oairextra_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone extras hit"
    assert hits[0].url == "https://doi.org/10.9/soft"
    assert "2021" in hits[0].snippet
    assert "embargo" in hits[0].snippet
    assert "3 cites" in hits[0].snippet
