from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools.research import S2GraphAdapter, get_adapter, parse_s2graph_payload


def test_s2graph_empty_query() -> None:
    assert S2GraphAdapter().search("") == []
    assert S2GraphAdapter().search("   ") == []


def test_get_adapter_s2graph_aliases() -> None:
    assert get_adapter("s2graph").name == "s2graph"
    assert get_adapter("graph-s2").name == "s2graph"
    assert get_adapter("s2-extra").name == "s2graph"


def test_parse_s2graph_payload() -> None:
    payload = {
        "data": [
            {
                "paperId": "abc123",
                "title": "Attention Is All You Need",
                "year": 2017,
                "venue": "NeurIPS",
                "authors": [{"name": "Ashish Vaswani"}, {"name": "Noam Shazeer"}],
                "abstract": "We propose a new simple network architecture.",
                "tldr": {"text": "Transformers replace recurrence with attention."},
                "citationCount": 120000,
                "influentialCitationCount": 9000,
                "url": "https://www.semanticscholar.org/paper/abc123",
            },
            {
                "paperId": "def456",
                "title": "Graph extras preprint",
                "publicationDate": "2021-03-01",
                "authors": [{"name": "Lee, Pat"}],
                "externalIds": {"DOI": "10.1234/s2.1"},
            },
            {"title": ""},
        ]
    }
    hits = parse_s2graph_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Attention Is All You Need"
    assert hits[0].url.endswith("abc123")
    assert hits[0].source == "s2graph"
    assert "Vaswani" in hits[0].snippet
    assert "2017" in hits[0].snippet
    assert "120000 cites" in hits[0].snippet
    assert "Transformers replace" in hits[0].snippet
    assert hits[1].title == "Graph extras preprint"
    assert hits[1].url == "https://doi.org/10.1234/s2.1"
    assert "2021" in hits[1].snippet


def test_parse_s2graph_respects_limit() -> None:
    payload = {
        "data": [
            {"paperId": "a", "title": "A"},
            {"paperId": "b", "title": "B"},
        ]
    }
    hits = parse_s2graph_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_s2graph_papers_list() -> None:
    payload = {
        "papers": [
            {
                "title": "Standalone graph hit",
                "year": 2020,
                "externalIds": {"ArXiv": "2001.00001"},
            }
        ]
    }
    hits = parse_s2graph_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Standalone graph hit"
    assert hits[0].url == "https://arxiv.org/abs/2001.00001"
    assert "2020" in hits[0].snippet
