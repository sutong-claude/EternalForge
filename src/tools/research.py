"""Research tool with a pluggable SearchAdapter interface.

Live backends: Wikipedia OpenSearch, DuckDuckGo Instant Answer,
Open Library, Hacker News Algolia, arXiv, Crossref, Semantic Scholar,
PubMed, Europe PMC, OpenAlex, Zenodo, DataCite, DOAJ, Wikidata, OpenAIRE,
CORE, Semantic Scholar Graph extras, Unpaywall, Crossref extras, OpenAlex
extras, OpenAIRE extras, Europe PMC extras, ORCID extras, DataCite extras,
Crossref funder extras, OpenAlex funder extras, ORCID works extras,
OpenAlex topics extras, OpenAlex concepts extras, OpenAlex sources extras,
OpenAlex publishers extras,
and OpenAlex institutions extras
(stdlib urllib; CORE key optional via CORE_API_KEY; Unpaywall email via
UNPAYWALL_EMAIL; Crossref extras/funders mailto via CROSSREF_MAILTO; OpenAlex
extras/funders/topics/concepts/sources/publishers/institutions mailto via OPENALEX_MAILTO). Tests
inject FixtureAdapter or call parse_*_payload helpers so they never hit the
network. Backend ``multi`` merges the live adapters.

Implementation is split into research_models / research_wiki / research_dispatch;
this module is the public facade so imports stay `tools.research`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from core.memory import Journal, MemoryEntry, normalize_tags
from tools.research_dispatch import ADAPTERS, LIVE_EXTRA, default_adapter, get_adapter
from tools.research_models import FixtureAdapter, Hit, SearchAdapter, unavailable
from tools.research_wiki import (
    DuckDuckGoAdapter,
    USER_AGENT,
    WikipediaAdapter,
    parse_duckduckgo_payload,
    parse_wikipedia_payload,
)

# Keep the historical private name used by some tests/callers.
_unavailable = unavailable
_LIVE_EXTRA = LIVE_EXTRA


def search(
    query: str,
    max_results: int = 5,
    adapter: SearchAdapter | None = None,
) -> list[Hit]:
    backend = adapter or default_adapter()
    return backend.search(query, max_results=max_results)


def summarize(text: str, max_length: int = 300) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_length:
        return compact
    return compact[: max_length - 3] + "..."


def format_hits(hits: list[Hit]) -> str:
    if not hits:
        return "(no results)"
    lines: list[str] = []
    for i, hit in enumerate(hits, 1):
        label = f"{hit.title} [{hit.source}]" if hit.source else hit.title
        lines.append(f"{i}. {label}")
        if hit.url:
            lines.append(f"   {hit.url}")
        if hit.snippet:
            lines.append(f"   {summarize(hit.snippet, 180)}")
    return "\n".join(lines)


def record_hits(
    query: str,
    hits: list[Hit],
    journal: Journal | None = None,
    root: Path | None = None,
    tags: Iterable[str] | None = None,
) -> MemoryEntry:
    """Append a kind=research journal entry summarizing the hits."""
    log = journal or Journal((root or Path.cwd()) / "memory" / "journal.jsonl")
    extra = list(tags) if tags is not None else []
    sources = [hit.source for hit in hits if hit.source]
    entry = MemoryEntry.now(
        "research",
        f"Research {query!r}: {len(hits)} hit(s)",
        format_hits(hits),
        tags=normalize_tags(["research", *sources, *extra]),
    )
    log.append(entry)
    return entry


def parse_openlibrary_payload(payload: dict, limit: int = 5):
    from tools.openlibrary import parse_openlibrary_payload as _parse
    return _parse(payload, limit=limit)


def parse_hackernews_payload(payload: dict, limit: int = 5):
    from tools.hackernews import parse_hackernews_payload as _parse
    return _parse(payload, limit=limit)


def parse_arxiv_payload(payload: dict, limit: int = 5):
    from tools.arxiv import parse_arxiv_payload as _parse
    return _parse(payload, limit=limit)


def parse_crossref_payload(payload: dict, limit: int = 5):
    from tools.crossref import parse_crossref_payload as _parse
    return _parse(payload, limit=limit)


def parse_semanticscholar_payload(payload: dict, limit: int = 5):
    from tools.semanticscholar import parse_semanticscholar_payload as _parse
    return _parse(payload, limit=limit)


def parse_pubmed_payload(payload: dict, limit: int = 5):
    from tools.pubmed import parse_pubmed_payload as _parse
    return _parse(payload, limit=limit)


def parse_europepmc_payload(payload: dict, limit: int = 5):
    from tools.europepmc import parse_europepmc_payload as _parse
    return _parse(payload, limit=limit)


def parse_openalex_payload(payload: dict, limit: int = 5):
    from tools.openalex import parse_openalex_payload as _parse
    return _parse(payload, limit=limit)


def parse_zenodo_payload(payload: dict, limit: int = 5):
    from tools.zenodo import parse_zenodo_payload as _parse
    return _parse(payload, limit=limit)


def parse_datacite_payload(payload: dict, limit: int = 5):
    from tools.datacite import parse_datacite_payload as _parse
    return _parse(payload, limit=limit)


def parse_doaj_payload(payload: dict, limit: int = 5):
    from tools.doaj import parse_doaj_payload as _parse
    return _parse(payload, limit=limit)


def parse_wikidata_payload(payload: dict, limit: int = 5):
    from tools.wikidata import parse_wikidata_payload as _parse
    return _parse(payload, limit=limit)


def parse_openaire_payload(payload: dict, limit: int = 5):
    from tools.openaire import parse_openaire_payload as _parse
    return _parse(payload, limit=limit)


def parse_core_payload(payload: dict, limit: int = 5):
    from tools.core import parse_core_payload as _parse
    return _parse(payload, limit=limit)


def parse_s2graph_payload(payload: dict, limit: int = 5):
    from tools.s2graph import parse_s2graph_payload as _parse
    return _parse(payload, limit=limit)


def parse_unpaywall_payload(payload: dict, limit: int = 5):
    from tools.unpaywall import parse_unpaywall_payload as _parse
    return _parse(payload, limit=limit)


def parse_xrefextra_payload(payload: dict, limit: int = 5):
    from tools.xrefextra import parse_xrefextra_payload as _parse
    return _parse(payload, limit=limit)


def parse_oaextra_payload(payload: dict, limit: int = 5):
    from tools.oaextra import parse_oaextra_payload as _parse
    return _parse(payload, limit=limit)


def parse_oairextra_payload(payload: dict, limit: int = 5):
    from tools.oairextra import parse_oairextra_payload as _parse
    return _parse(payload, limit=limit)


def parse_epmcextra_payload(payload: dict, limit: int = 5):
    from tools.epmcextra import parse_epmcextra_payload as _parse
    return _parse(payload, limit=limit)


def parse_orcidextra_payload(payload: dict, limit: int = 5):
    from tools.orcidextra import parse_orcidextra_payload as _parse
    return _parse(payload, limit=limit)


def parse_dcextra_payload(payload: dict, limit: int = 5):
    from tools.dcextra import parse_dcextra_payload as _parse
    return _parse(payload, limit=limit)


def parse_crfunder_payload(payload: dict, limit: int = 5):
    from tools.crfunder import parse_crfunder_payload as _parse
    return _parse(payload, limit=limit)


def parse_oafunder_payload(payload: dict, limit: int = 5):
    from tools.oafunder import parse_oafunder_payload as _parse
    return _parse(payload, limit=limit)


def parse_orcidworks_payload(payload: dict, limit: int = 5, orcid: str = ""):
    from tools.orcidworks import parse_orcidworks_payload as _parse
    return _parse(payload, limit=limit, orcid=orcid)


def parse_oatopic_payload(payload: dict, limit: int = 5):
    from tools.oatopic import parse_oatopic_payload as _parse
    return _parse(payload, limit=limit)


def parse_oaconcept_payload(payload: dict, limit: int = 5):
    from tools.oaconcept import parse_oaconcept_payload as _parse
    return _parse(payload, limit=limit)


def parse_oasource_payload(payload: dict, limit: int = 5):
    from tools.oasource import parse_oasource_payload as _parse
    return _parse(payload, limit=limit)


def parse_oapublisher_payload(payload: dict, limit: int = 5):
    from tools.oapublisher import parse_oapublisher_payload as _parse
    return _parse(payload, limit=limit)


def parse_oainstitution_payload(payload: dict, limit: int = 5):
    from tools.oainstitution import parse_oainstitution_payload as _parse
    return _parse(payload, limit=limit)


def merge_hits(*groups, limit: int = 5):
    from tools.openlibrary import merge_hits as _merge
    return _merge(*groups, limit=limit)


def __getattr__(name: str):
    if name in {"OpenLibraryAdapter", "MultiAdapter"}:
        from tools import openlibrary as olmod
        return getattr(olmod, name)
    if name == "HackerNewsAdapter":
        from tools.hackernews import HackerNewsAdapter
        return HackerNewsAdapter
    if name == "ArxivAdapter":
        from tools.arxiv import ArxivAdapter
        return ArxivAdapter
    if name == "CrossrefAdapter":
        from tools.crossref import CrossrefAdapter
        return CrossrefAdapter
    if name == "SemanticScholarAdapter":
        from tools.semanticscholar import SemanticScholarAdapter
        return SemanticScholarAdapter
    if name == "PubMedAdapter":
        from tools.pubmed import PubMedAdapter
        return PubMedAdapter
    if name == "EuropePMCAdapter":
        from tools.europepmc import EuropePMCAdapter
        return EuropePMCAdapter
    if name == "OpenAlexAdapter":
        from tools.openalex import OpenAlexAdapter
        return OpenAlexAdapter
    if name == "ZenodoAdapter":
        from tools.zenodo import ZenodoAdapter
        return ZenodoAdapter
    if name == "DataCiteAdapter":
        from tools.datacite import DataCiteAdapter
        return DataCiteAdapter
    if name == "DoajAdapter":
        from tools.doaj import DoajAdapter
        return DoajAdapter
    if name == "WikidataAdapter":
        from tools.wikidata import WikidataAdapter
        return WikidataAdapter
    if name == "OpenaireAdapter":
        from tools.openaire import OpenaireAdapter
        return OpenaireAdapter
    if name == "CoreAdapter":
        from tools.core import CoreAdapter
        return CoreAdapter
    if name == "S2GraphAdapter":
        from tools.s2graph import S2GraphAdapter
        return S2GraphAdapter
    if name == "UnpaywallAdapter":
        from tools.unpaywall import UnpaywallAdapter
        return UnpaywallAdapter
    if name == "XrefExtraAdapter":
        from tools.xrefextra import XrefExtraAdapter
        return XrefExtraAdapter
    if name == "OaExtraAdapter":
        from tools.oaextra import OaExtraAdapter
        return OaExtraAdapter
    if name == "OaireExtraAdapter":
        from tools.oairextra import OaireExtraAdapter
        return OaireExtraAdapter
    if name == "EpmcExtraAdapter":
        from tools.epmcextra import EpmcExtraAdapter
        return EpmcExtraAdapter
    if name == "OrcidExtraAdapter":
        from tools.orcidextra import OrcidExtraAdapter
        return OrcidExtraAdapter
    if name == "DataCiteExtraAdapter":
        from tools.dcextra import DataCiteExtraAdapter
        return DataCiteExtraAdapter
    if name == "CrFunderAdapter":
        from tools.crfunder import CrFunderAdapter
        return CrFunderAdapter
    if name == "OaFunderAdapter":
        from tools.oafunder import OaFunderAdapter
        return OaFunderAdapter
    if name == "OrcidWorksAdapter":
        from tools.orcidworks import OrcidWorksAdapter
        return OrcidWorksAdapter
    if name == "OaTopicAdapter":
        from tools.oatopic import OaTopicAdapter
        return OaTopicAdapter
    if name == "OaConceptAdapter":
        from tools.oaconcept import OaConceptAdapter
        return OaConceptAdapter
    if name == "OaSourceAdapter":
        from tools.oasource import OaSourceAdapter
        return OaSourceAdapter
    if name == "OaPublisherAdapter":
        from tools.oapublisher import OaPublisherAdapter
        return OaPublisherAdapter
    if name == "OaInstitutionAdapter":
        from tools.oainstitution import OaInstitutionAdapter
        return OaInstitutionAdapter
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "ADAPTERS",
    "DuckDuckGoAdapter",
    "FixtureAdapter",
    "Hit",
    "LIVE_EXTRA",
    "SearchAdapter",
    "USER_AGENT",
    "WikipediaAdapter",
    "default_adapter",
    "format_hits",
    "get_adapter",
    "merge_hits",
    "parse_arxiv_payload",
    "parse_core_payload",
    "parse_crfunder_payload",
    "parse_crossref_payload",
    "parse_datacite_payload",
    "parse_dcextra_payload",
    "parse_doaj_payload",
    "parse_duckduckgo_payload",
    "parse_epmcextra_payload",
    "parse_europepmc_payload",
    "parse_hackernews_payload",
    "parse_oaconcept_payload",
    "parse_oaextra_payload",
    "parse_oafunder_payload",
    "parse_oairextra_payload",
    "parse_oainstitution_payload",
    "parse_oapublisher_payload",
    "parse_oasource_payload",
    "parse_oatopic_payload",
    "parse_openaire_payload",
    "parse_openalex_payload",
    "parse_openlibrary_payload",
    "parse_orcidextra_payload",
    "parse_orcidworks_payload",
    "parse_pubmed_payload",
    "parse_s2graph_payload",
    "parse_semanticscholar_payload",
    "parse_unpaywall_payload",
    "parse_wikidata_payload",
    "parse_wikipedia_payload",
    "parse_xrefextra_payload",
    "parse_zenodo_payload",
    "record_hits",
    "search",
    "summarize",
]
