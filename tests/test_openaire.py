from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import OpenaireAdapter, get_adapter, parse_openaire_payload


def test_openaire_empty_query() -> None:
    assert OpenaireAdapter().search("") == []
    assert OpenaireAdapter().search("   ") == []


def test_get_adapter_openaire_aliases() -> None:
    assert get_adapter("openaire").name == "openaire"
    assert get_adapter("oaire").name == "openaire"
    assert get_adapter("graph").name == "openaire"


def test_parse_openaire_payload() -> None:
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
    hits = parse_openaire_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Attention sharing in infancy"
    assert hits[0].url == "https://example.org/attention"
    assert hits[0].source == "openaire"
    assert "Doe" in hits[0].snippet
    assert "2023" in hits[0].snippet
    assert "publication" in hits[0].snippet
    assert "joint attention" in hits[0].snippet
    assert hits[1].title == "keras-attention-mechanism"
    assert hits[1].url == "https://github.com/philipperemy/keras-attention-mechanism"
    assert "software" in hits[1].snippet


def test_parse_openaire_respects_limit() -> None:
    payload = {
        "results": [
            {"id": "a", "mainTitle": "A"},
            {"id": "b", "mainTitle": "B"},
        ]
    }
    hits = parse_openaire_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_openaire_research_products_list() -> None:
    payload = {
        "researchProducts": [
            {
                "title": "Standalone graph hit",
                "pids": [{"scheme": "doi", "value": "10.9/soft"}],
                "publicationDate": "2021",
            }
        ]
    }
    hits = parse_openaire_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone graph hit"
    assert hits[0].url == "https://doi.org/10.9/soft"
    assert "2021" in hits[0].snippet
