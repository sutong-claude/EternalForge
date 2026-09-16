from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.memory import Journal
from tools.arxiv import parse_arxiv_xml
from tools.research import (
    ArxivAdapter,
    CrossrefAdapter,
    DuckDuckGoAdapter,
    FixtureAdapter,
    HackerNewsAdapter,
    Hit,
    MultiAdapter,
    OpenLibraryAdapter,
    SemanticScholarAdapter,
    WikipediaAdapter,
    format_hits,
    get_adapter,
    merge_hits,
    parse_arxiv_payload,
    parse_crossref_payload,
    parse_duckduckgo_payload,
    parse_hackernews_payload,
    parse_openlibrary_payload,
    parse_semanticscholar_payload,
    parse_wikipedia_payload,
    record_hits,
    search,
    summarize,
)


def test_fixture_adapter_matches_seeded_topic() -> None:
    hits = search("EternalForge vision", adapter=FixtureAdapter())
    assert hits
    assert hits[0].title == "EternalForge"
    assert "github.com" in hits[0].url


def test_empty_query_returns_nothing() -> None:
    assert FixtureAdapter().search("   ") == []
    assert DuckDuckGoAdapter().search("") == []
    assert WikipediaAdapter().search("") == []
    assert OpenLibraryAdapter().search("") == []
    assert HackerNewsAdapter().search("") == []
    assert ArxivAdapter().search("") == []
    assert CrossrefAdapter().search("") == []
    assert SemanticScholarAdapter().search("") == []
    assert MultiAdapter(adapters=[FixtureAdapter()]).search("  ") == []


def test_unknown_topic_returns_placeholder() -> None:
    hits = FixtureAdapter().search("quantum-xyz-unknown")
    assert len(hits) == 1
    assert hits[0].source == "fixture"


def test_max_results_is_respected() -> None:
    catalog = {
        "alpha": [
            Hit("A", "u1", "s1", "fixture"),
            Hit("B", "u2", "s2", "fixture"),
            Hit("C", "u3", "s3", "fixture"),
        ]
    }
    hits = FixtureAdapter(catalog).search("alpha", max_results=2)
    assert [h.title for h in hits] == ["A", "B"]


def test_summarize_truncates() -> None:
    text = "word " * 80
    out = summarize(text, max_length=40)
    assert len(out) == 40
    assert out.endswith("...")


def test_format_hits_empty() -> None:
    assert format_hits([]) == "(no results)"


def test_record_hits_writes_journal(tmp_path: Path) -> None:
    hits = [
        Hit(
            title="EternalForge",
            url="https://github.com/sutong-claude/EternalForge",
            snippet="Personal AI research platform.",
            source="fixture",
        )
    ]
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    entry = record_hits("eternalforge", hits, journal=journal)
    assert entry.kind == "research"
    assert "eternalforge" in entry.summary
    assert "1 hit" in entry.summary
    path = tmp_path / "memory" / "journal.jsonl"
    assert path.exists()
    row = json.loads(path.read_text(encoding="utf-8").splitlines()[-1])
    assert row["kind"] == "research"
    assert "EternalForge" in row["details"]


def test_record_hits_empty_query_still_journals(tmp_path: Path) -> None:
    journal = Journal(tmp_path / "journal.jsonl")
    entry = record_hits("blank", [], journal=journal)
    assert entry.kind == "research"
    assert "0 hit" in entry.summary
    assert "(no results)" in entry.details


def test_get_adapter_resolves_known_backends() -> None:
    assert get_adapter("wikipedia").name == "wikipedia"
    assert get_adapter("duckduckgo").name == "duckduckgo"
    assert get_adapter("ddg").name == "duckduckgo"
    assert get_adapter("openlibrary").name == "openlibrary"
    assert get_adapter("ol").name == "openlibrary"
    assert get_adapter("books").name == "openlibrary"
    assert get_adapter("hackernews").name == "hackernews"
    assert get_adapter("hn").name == "hackernews"
    assert get_adapter("algolia").name == "hackernews"
    assert get_adapter("arxiv").name == "arxiv"
    assert get_adapter("papers").name == "arxiv"
    assert get_adapter("preprint").name == "arxiv"
    assert get_adapter("crossref").name == "crossref"
    assert get_adapter("doi").name == "crossref"
    assert get_adapter("works").name == "crossref"
    assert get_adapter("semanticscholar").name == "semanticscholar"
    assert get_adapter("s2").name == "semanticscholar"
    assert get_adapter("scholar").name == "semanticscholar"
    assert get_adapter("multi").name == "multi"
    assert get_adapter("all").name == "multi"
    assert get_adapter("fixture").name == "fixture"
    assert get_adapter(None).name == "wikipedia"


def test_get_adapter_rejects_unknown() -> None:
    try:
        get_adapter("bing")
    except ValueError as exc:
        assert "bing" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_parse_wikipedia_payload() -> None:
    payload = ["q", ["Alpha"], ["first article"], ["https://en.wikipedia.org/wiki/Alpha"]]
    hits = parse_wikipedia_payload(payload, limit=5)
    assert hits[0].title == "Alpha"
    assert hits[0].source == "wikipedia"


def test_parse_duckduckgo_payload_abstract_and_related() -> None:
    payload = {
        "Heading": "Python",
        "AbstractText": "A programming language.",
        "AbstractURL": "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "RelatedTopics": [
            {
                "Text": "Guido van Rossum - Creator of Python",
                "FirstURL": "https://duckduckgo.com/Guido_van_Rossum",
            },
            {
                "Name": "See also",
                "Topics": [
                    {
                        "Text": "Monty Python - Comedy group",
                        "FirstURL": "https://duckduckgo.com/Monty_Python",
                    }
                ],
            },
        ],
    }
    hits = parse_duckduckgo_payload(payload, limit=3)
    assert len(hits) == 3
    assert hits[0].title == "Python"
    assert hits[0].source == "duckduckgo"
    assert hits[1].title == "Guido van Rossum"
    assert hits[2].title == "Monty Python"


def test_parse_duckduckgo_respects_limit_and_dedupes() -> None:
    payload = {
        "Heading": "X",
        "AbstractText": "abs",
        "AbstractURL": "https://example.com/x",
        "RelatedTopics": [
            {"Text": "X", "FirstURL": "https://example.com/x"},
            {"Text": "Y", "FirstURL": "https://example.com/y"},
        ],
    }
    hits = parse_duckduckgo_payload(payload, limit=1)
    assert len(hits) == 1
    assert hits[0].title == "X"


def test_parse_openlibrary_payload() -> None:
    payload = {
        "docs": [
            {
                "title": "Godel, Escher, Bach",
                "key": "/works/OL123W",
                "author_name": ["Douglas Hofstadter"],
                "first_publish_year": 1979,
            },
            {
                "title": "I Am a Strange Loop",
                "key": "/works/OL456W",
                "author_name": ["Douglas Hofstadter"],
                "first_publish_year": 2007,
            },
            {"title": "", "key": ""},
        ]
    }
    hits = parse_openlibrary_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Godel, Escher, Bach"
    assert hits[0].url == "https://openlibrary.org/works/OL123W"
    assert "Hofstadter" in hits[0].snippet
    assert "1979" in hits[0].snippet
    assert hits[0].source == "openlibrary"


def test_parse_openlibrary_respects_limit() -> None:
    payload = {
        "docs": [
            {"title": "A", "key": "/works/A"},
            {"title": "B", "key": "/works/B"},
        ]
    }
    hits = parse_openlibrary_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_hackernews_payload() -> None:
    payload = {
        "hits": [
            {
                "title": "Show HN: EternalForge",
                "url": "https://github.com/sutong-claude/EternalForge",
                "author": "alice",
                "points": 42,
                "num_comments": 7,
                "objectID": "111",
            },
            {
                "title": "",
                "story_title": "Ask HN: research tools",
                "url": "",
                "author": "bob",
                "comment_text": "try adapters",
                "objectID": "222",
            },
            {"title": "", "url": "", "objectID": ""},
        ]
    }
    hits = parse_hackernews_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Show HN: EternalForge"
    assert hits[0].url == "https://github.com/sutong-claude/EternalForge"
    assert hits[0].source == "hackernews"
    assert "alice" in hits[0].snippet
    assert "42 pts" in hits[0].snippet
    assert hits[1].title == "Ask HN: research tools"
    assert hits[1].url == "https://news.ycombinator.com/item?id=222"
    assert "try adapters" in hits[1].snippet


def test_parse_hackernews_respects_limit() -> None:
    payload = {
        "hits": [
            {"title": "A", "url": "https://a.example", "objectID": "1"},
            {"title": "B", "url": "https://b.example", "objectID": "2"},
        ]
    }
    hits = parse_hackernews_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_arxiv_payload() -> None:
    payload = {
        "entries": [
            {
                "id": "http://arxiv.org/abs/1706.03762v7",
                "title": "Attention Is All You Need",
                "url": "http://arxiv.org/abs/1706.03762v7",
                "authors": ["Ashish Vaswani", "Noam Shazeer"],
                "published": "2017-06-12",
                "summary": "The dominant sequence transduction models.",
            },
            {
                "id": "http://arxiv.org/abs/1406.2661",
                "title": "Generative Adversarial Nets",
                "url": "http://arxiv.org/abs/1406.2661",
                "authors": ["Ian Goodfellow"],
                "published": "2014-06-10",
                "summary": "",
            },
            {"title": "", "url": "", "id": ""},
        ]
    }
    hits = parse_arxiv_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Attention Is All You Need"
    assert hits[0].url == "http://arxiv.org/abs/1706.03762v7"
    assert hits[0].source == "arxiv"
    assert "Vaswani" in hits[0].snippet
    assert "2017-06-12" in hits[0].snippet
    assert "transduction" in hits[0].snippet
    assert hits[1].title == "Generative Adversarial Nets"
    assert "Goodfellow" in hits[1].snippet


def test_parse_arxiv_respects_limit() -> None:
    payload = {
        "entries": [
            {"title": "A", "url": "http://arxiv.org/abs/a"},
            {"title": "B", "url": "http://arxiv.org/abs/b"},
        ]
    }
    hits = parse_arxiv_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_arxiv_xml_atom() -> None:
    raw = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
    <feed xmlns=\"http://www.w3.org/2005/Atom\">
      <entry>
        <id>http://arxiv.org/abs/1706.03762v7</id>
        <title>Attention Is All You Need</title>
        <published>2017-06-12T17:57:34Z</published>
        <summary>The dominant sequence transduction models.</summary>
        <author><name>Ashish Vaswani</name></author>
        <link href=\"http://arxiv.org/abs/1706.03762v7\" rel=\"alternate\" type=\"text/html\"/>
      </entry>
    </feed>
    """
    payload = parse_arxiv_xml(raw)
    hits = parse_arxiv_payload(payload, limit=5)
    assert len(hits) == 1
    assert hits[0].title == "Attention Is All You Need"
    assert hits[0].source == "arxiv"
    assert "Vaswani" in hits[0].snippet


def test_parse_crossref_payload() -> None:
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
                },
                {
                    "title": ["Generative Adversarial Nets"],
                    "DOI": "10.5555/2969033.2969125",
                    "author": [{"given": "Ian", "family": "Goodfellow"}],
                    "issued": {"date-parts": [[2014]]},
                },
                {"title": [], "DOI": "", "URL": ""},
            ]
        }
    }
    hits = parse_crossref_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Attention Is All You Need"
    assert hits[0].url == "https://doi.org/10.5555/3295222.3295349"
    assert hits[0].source == "crossref"
    assert "Vaswani" in hits[0].snippet
    assert "2017" in hits[0].snippet
    assert "NeurIPS" in hits[0].snippet
    assert hits[1].title == "Generative Adversarial Nets"
    assert hits[1].url == "https://doi.org/10.5555/2969033.2969125"
    assert "Goodfellow" in hits[1].snippet


def test_parse_crossref_respects_limit() -> None:
    payload = {
        "message": {
            "items": [
                {"title": ["A"], "URL": "https://doi.org/a"},
                {"title": ["B"], "URL": "https://doi.org/b"},
            ]
        }
    }
    hits = parse_crossref_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_parse_semanticscholar_payload() -> None:
    payload = {
        "data": [
            {
                "paperId": "abc123",
                "title": "Attention Is All You Need",
                "url": "https://www.semanticscholar.org/paper/abc123",
                "abstract": "The dominant sequence transduction models.",
                "year": 2017,
                "venue": "NeurIPS",
                "authors": [{"name": "Ashish Vaswani"}, {"name": "Noam Shazeer"}],
            },
            {
                "paperId": "def456",
                "title": "Generative Adversarial Nets",
                "authors": [{"name": "Ian Goodfellow"}],
                "year": 2014,
                "externalIds": {"DOI": "10.5555/2969033.2969125"},
            },
            {"title": "", "url": "", "paperId": ""},
        ]
    }
    hits = parse_semanticscholar_payload(payload, limit=5)
    assert len(hits) == 2
    assert hits[0].title == "Attention Is All You Need"
    assert hits[0].url == "https://www.semanticscholar.org/paper/abc123"
    assert hits[0].source == "semanticscholar"
    assert "Vaswani" in hits[0].snippet
    assert "2017" in hits[0].snippet
    assert "NeurIPS" in hits[0].snippet
    assert "transduction" in hits[0].snippet
    assert hits[1].title == "Generative Adversarial Nets"
    assert hits[1].url == "https://www.semanticscholar.org/paper/def456"
    assert "Goodfellow" in hits[1].snippet


def test_parse_semanticscholar_respects_limit() -> None:
    payload = {
        "data": [
            {"title": "A", "url": "https://www.semanticscholar.org/paper/a"},
            {"title": "B", "url": "https://www.semanticscholar.org/paper/b"},
        ]
    }
    hits = parse_semanticscholar_payload(payload, limit=1)
    assert [h.title for h in hits] == ["A"]


def test_merge_hits_round_robin_and_dedupe() -> None:
    wiki = [
        Hit("Python", "https://en.wikipedia.org/wiki/Python", "lang", "wikipedia"),
        Hit("Monty", "https://en.wikipedia.org/wiki/Monty_Python", "tv", "wikipedia"),
    ]
    books = [
        Hit("Python", "https://en.wikipedia.org/wiki/Python", "dup url", "openlibrary"),
        Hit("Fluent Python", "https://openlibrary.org/works/OL1W", "book", "openlibrary"),
    ]
    merged = merge_hits(wiki, books, limit=3)
    assert [h.title for h in merged] == ["Python", "Fluent Python", "Monty"]
    assert merged[0].source == "wikipedia"


def test_merge_hits_drops_unavailable_when_real_exist() -> None:
    dead = [Hit("wikipedia unavailable for: q", "", "err", "wikipedia")]
    live = [Hit("Book", "https://openlibrary.org/works/OL1W", "ok", "openlibrary")]
    merged = merge_hits(dead, live, limit=5)
    assert [h.source for h in merged] == ["openlibrary"]


def test_merge_hits_keeps_unavailable_if_all_fail() -> None:
    dead = [Hit("wikipedia unavailable for: q", "", "err", "wikipedia")]
    merged = merge_hits(dead, [], limit=5)
    assert merged[0].source == "wikipedia"


def test_multi_adapter_uses_injected_backends() -> None:
    a = FixtureAdapter({"q": [Hit("FromA", "https://a.example/1", "a", "fixture-a")]})
    b = FixtureAdapter({"q": [Hit("FromB", "https://b.example/1", "b", "fixture-b")]})
    hits = MultiAdapter(adapters=[a, b]).search("q", max_results=2)
    assert [h.title for h in hits] == ["FromA", "FromB"]
