"""Adapter registry and get_adapter dispatch."""

from __future__ import annotations

from tools.research_models import FixtureAdapter, SearchAdapter
from tools.research_wiki import DuckDuckGoAdapter, WikipediaAdapter

ADAPTERS: dict[str, type] = {
    "wikipedia": WikipediaAdapter,
    "duckduckgo": DuckDuckGoAdapter,
    "ddg": DuckDuckGoAdapter,
    "fixture": FixtureAdapter,
}

LIVE_EXTRA = {
    "openlibrary",
    "ol",
    "books",
    "hackernews",
    "hn",
    "algolia",
    "arxiv",
    "papers",
    "preprint",
    "crossref",
    "doi",
    "works",
    "semanticscholar",
    "s2",
    "scholar",
    "pubmed",
    "ncbi",
    "medline",
    "europepmc",
    "epmc",
    "europe",
    "openalex",
    "oa",
    "works-oa",
    "zenodo",
    "zen",
    "records",
    "datacite",
    "dc",
    "dois",
    "doaj",
    "oa-journals",
    "journals",
    "wikidata",
    "wd",
    "entities",
    "multi",
    "all",
}


def get_adapter(name: str | None = None) -> SearchAdapter:
    key = (name or "wikipedia").strip().lower()
    if key in LIVE_EXTRA:
        from tools import arxiv as axmod
        from tools import crossref as xrmod
        from tools import datacite as dcmod
        from tools import doaj as doajmod
        from tools import europepmc as epmcmod
        from tools import hackernews as hnmod
        from tools import openalex as oamod
        from tools import openlibrary as olmod
        from tools import pubmed as pmmod
        from tools import semanticscholar as s2mod
        from tools import wikidata as wdmod
        from tools import zenodo as zenmod

        if key in {"multi", "all"}:
            return olmod.MultiAdapter()
        if key in {"hackernews", "hn", "algolia"}:
            return hnmod.HackerNewsAdapter()
        if key in {"arxiv", "papers", "preprint"}:
            return axmod.ArxivAdapter()
        if key in {"crossref", "doi", "works"}:
            return xrmod.CrossrefAdapter()
        if key in {"semanticscholar", "s2", "scholar"}:
            return s2mod.SemanticScholarAdapter()
        if key in {"pubmed", "ncbi", "medline"}:
            return pmmod.PubMedAdapter()
        if key in {"europepmc", "epmc", "europe"}:
            return epmcmod.EuropePMCAdapter()
        if key in {"openalex", "oa", "works-oa"}:
            return oamod.OpenAlexAdapter()
        if key in {"zenodo", "zen", "records"}:
            return zenmod.ZenodoAdapter()
        if key in {"datacite", "dc", "dois"}:
            return dcmod.DataCiteAdapter()
        if key in {"doaj", "oa-journals", "journals"}:
            return doajmod.DoajAdapter()
        if key in {"wikidata", "wd", "entities"}:
            return wdmod.WikidataAdapter()
        return olmod.OpenLibraryAdapter()
    cls = ADAPTERS.get(key)
    if cls is None:
        known = ", ".join(sorted(set(ADAPTERS) | LIVE_EXTRA))
        raise ValueError(f"Unknown search backend {name!r}. Known: {known}")
    return cls()


def default_adapter() -> SearchAdapter:
    return WikipediaAdapter()
