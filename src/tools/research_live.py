"""Live SearchAdapter factory (no-key extras + multi)."""
from __future__ import annotations

import importlib

from tools.research_models import SearchAdapter

_SPECS: list[tuple[tuple[str, ...], str, str]] = [
    (("hackernews", "hn", "algolia"), "hackernews", "HackerNewsAdapter"),
    (("arxiv", "papers", "preprint"), "arxiv", "ArxivAdapter"),
    (("crossref", "doi", "works"), "crossref", "CrossrefAdapter"),
    (("semanticscholar", "s2", "scholar"), "semanticscholar", "SemanticScholarAdapter"),
    (("pubmed", "ncbi", "medline"), "pubmed", "PubMedAdapter"),
    (("europepmc", "epmc", "europe"), "europepmc", "EuropePMCAdapter"),
    (("openalex", "oa", "works-oa"), "openalex", "OpenAlexAdapter"),
    (("zenodo", "zen", "records"), "zenodo", "ZenodoAdapter"),
    (("datacite", "dc", "dois"), "datacite", "DataCiteAdapter"),
    (("doaj", "oa-journals", "journals"), "doaj", "DoajAdapter"),
    (("wikidata", "wd", "entities"), "wikidata", "WikidataAdapter"),
    (("openaire", "oaire", "graph"), "openaire", "OpenaireAdapter"),
    (("core", "coreac", "works-core"), "core", "CoreAdapter"),
    (("s2graph", "graph-s2", "s2-extra"), "s2graph", "S2GraphAdapter"),
    (("unpaywall", "upw", "oa-status"), "unpaywall", "UnpaywallAdapter"),
    (("xrefextra", "cr-extra", "cites-xr"), "xrefextra", "XrefExtraAdapter"),
    (("oaextra", "oa-extra", "cites-oa"), "oaextra", "OaExtraAdapter"),
    (("oairextra", "oaire-extra", "cites-oaire"), "oairextra", "OaireExtraAdapter"),
    (("epmcextra", "epmc-extra", "cites-epmc"), "epmcextra", "EpmcExtraAdapter"),
    (("orcidextra", "orcid-extra", "ids-orcid"), "orcidextra", "OrcidExtraAdapter"),
    (("dcextra", "dc-extra", "cites-dc"), "dcextra", "DataCiteExtraAdapter"),
    (("crfunder", "funders-cr", "cites-funder"), "crfunder", "CrFunderAdapter"),
    (("oafunder", "funders-oa", "cites-funder-oa"), "oafunder", "OaFunderAdapter"),
    (("orcidworks", "works-orcid", "orcid-works"), "orcidworks", "OrcidWorksAdapter"),
    (("oatopic", "topics-oa", "cites-topic-oa"), "oatopic", "OaTopicAdapter"),
    (("oaconcept", "concepts-oa", "cites-concept-oa"), "oaconcept", "OaConceptAdapter"),
    (("oasource", "sources-oa", "cites-source-oa"), "oasource", "OaSourceAdapter"),
    (("oapublisher", "publishers-oa", "cites-publisher-oa"), "oapublisher", "OaPublisherAdapter"),
    (("oainstitution", "institutions-oa", "cites-institution-oa"), "oainstitution", "OaInstitutionAdapter"),
    (("oaauthor", "authors-oa", "cites-author-oa"), "oaauthor", "OaAuthorAdapter"),
    (("oayear", "years-oa", "works-year-oa"), "oayear", "OaYearAdapter"),
    (("oatype", "types-oa", "works-type-oa"), "oatype", "OaTypeAdapter"),
    (("oalang", "languages-oa", "works-lang-oa"), "oalang", "OaLangAdapter"),
    (("oaostatus", "status-oa", "works-oa-status"), "oaostatus", "OaOaStatusAdapter"),
    (("oacountry", "countries-oa", "works-country-oa"), "oacountry", "OaCountryAdapter"),
    (("oacontinent", "continents-oa", "works-continent-oa"), "oacontinent", "OaContinentAdapter"),
    (("oasrctype", "source-types-oa", "works-source-type-oa"), "oasrctype", "OaSrcTypeAdapter"),
    (("oaretracted", "retracted-oa", "works-retracted-oa"), "oaretracted", "OaRetractedAdapter"),
    (("oaparatext", "paratext-oa", "works-paratext-oa"), "oaparatext", "OaParatextAdapter"),
    (("oadoi", "doi-oa", "works-doi-oa"), "oadoi", "OaDoiAdapter"),
    (("oahasoa", "hasoa-oa", "works-hasoa-oa"), "oahasoa", "OaHasOaAdapter"),
    (("oahaspmid", "haspmid-oa", "works-haspmid-oa"), "oahaspmid", "OaHasPmidAdapter"),
    (("oahaspmcid", "haspmcid-oa", "works-haspmcid-oa"), "oahaspmcid", "OaHasPmcidAdapter"),
    (("oahasisn", "hasissn-oa", "works-hasissn-oa"), "oahasisn", "OaHasIssnAdapter"),
    (("oahasorcid", "hasorcid-oa", "works-hasorcid-oa"), "oahasorcid", "OaHasOrcidAdapter"),
    (("oahasaffil", "hasaffil-oa", "works-hasaffil-oa"), "oahasaffil", "OaHasAffilAdapter"),
    (("oahasrefs", "hasrefs-oa", "works-hasrefs-oa"), "oahasrefs", "OaHasRefsAdapter"),
    (("oahasabs", "hasabs-oa", "works-hasabs-oa"), "oahasabs", "OaHasAbsAdapter"),
    (("oahaspdf", "haspdf-oa", "works-haspdf-oa"), "oahaspdf", "OaHasPdfAdapter"),
    (("oahasft", "hasft-oa", "works-hasft-oa"), "oahasft", "OaHasFtAdapter"),
    (("oahasoaap", "hasoaap-oa", "works-hasoaap-oa"), "oahasoaap", "OaHasOaapAdapter"),
    (("oahasoasub", "hasoasub-oa", "works-hasoasub-oa"), "oahasoasub", "OaHasOaSubAdapter"),
    (("oahasoarepo", "hasoarepo-oa", "works-hasoarepo-oa"), "oahasoarepo", "OaHasOaRepoAdapter"),
    (("oahasogold", "hasogold-oa", "works-hasogold-oa"), "oahasogold", "OaHasOaGoldAdapter"),
    (("oahasoahybrid", "hasoahybrid-oa", "works-hasoahybrid-oa"), "oahasoahybrid", "OaHasOaHybridAdapter"),
    (("oahasobronze", "hasobronze-oa", "works-hasobronze-oa"), "oahasobronze", "OaHasOaBronzeAdapter"),
    (("oahasogreen", "hasogreen-oa", "works-hasogreen-oa"), "oahasogreen", "OaHasOaGreenAdapter"),
    (("oahasodiamond", "hasodiamond-oa", "works-hasodiamond-oa"), "oahasodiamond", "OaHasOaDiamondAdapter"),
    (("oaisoa", "isoa-oa", "works-isoa-oa"), "oaisoa", "OaIsOaAdapter"),
    (("oahasoanyrepo", "hasoanyrepo-oa", "works-hasoanyrepo-oa"), "oahasoanyrepo", "OaHasOaAnyRepoAdapter"),
    (("oahasoapub", "hasoapub-oa", "works-hasoapub-oa"), "oahasoapub", "OaHasOaPubAdapter"),
    (("oahasoadomain", "hasoadomain-oa", "works-hasoadomain-oa"), "oahasoadomain", "OaHasOaDomainAdapter"),
    (("oahasoofile", "hasoafile-oa", "works-hasoafile-oa"), "oahasoofile", "OaHasOaFileAdapter"),
    (("oahasoaurl", "hasoaurl-oa", "works-hasoaurl-oa"), "oahasoaurl", "OaHasOaUrlAdapter"),
    (("oahasoaver", "hasoaver-oa", "works-hasoaver-oa"), "oahasoaver", "OaHasOaVerAdapter"),
    (("oahasoaalic", "hasoaalic-oa", "works-hasoaalic-oa"), "oahasoaalic", "OaHasOaLicAdapter"),
    (("oahasoaalicid", "hasoaalicid-oa", "works-hasoaalicid-oa"), "oahasoaalicid", "OaHasOaLicIdAdapter"),
    (("oabestlic", "bestlic-oa", "works-bestlic-oa"), "oabestlic", "OaBestLicAdapter"),
    (("oabestlicid", "bestlicid-oa", "works-bestlicid-oa"), "oabestlicid", "OaBestLicIdAdapter"),
    (("oabestver", "bestver-oa", "works-bestver-oa"), "oabestver", "OaBestVerAdapter"),
    (("oabestsrc", "bestsrc-oa", "works-bestsrc-oa"), "oabestsrc", "OaBestSrcAdapter"),
    (("oabestsrcid", "bestsrcid-oa", "works-bestsrcid-oa"), "oabestsrcid", "OaBestSrcIdAdapter"),
    (("oabestsrctype", "bestsrctype-oa", "works-bestsrctype-oa"), "oabestsrctype", "OaBestSrcTypeAdapter"),
    (("oabestissn", "bestissn-oa", "works-bestissn-oa"), "oabestissn", "OaBestIssnAdapter"),
    (("oabesthost", "besthost-oa", "works-besthost-oa"), "oabesthost", "OaBestHostAdapter"),
    (("oabesthoname", "besthoname-oa", "works-besthoname-oa"), "oabesthoname", "OaBestHoNameAdapter"),
    (("oabestholineage", "bestholineage-oa", "works-bestholineage-oa"), "oabestholineage", "OaBestHoLineageAdapter"),
    (("oabestholinames", "bestholinames-oa", "works-bestholinames-oa"), "oabestholinames", "OaBestHoLinamesAdapter"),
    (("oabestdoaj", "bestdoaj-oa", "works-bestdoaj-oa"), "oabestdoaj", "OaBestDoajAdapter"),
    (("oabestcore", "bestcore-oa", "works-bestcore-oa"), "oabestcore", "OaBestCoreAdapter"),
    (("oabestisoa", "bestisoa-oa", "works-bestisoa-oa"), "oabestisoa", "OaBestIsOaAdapter"),
    (("oabestissns", "bestissns-oa", "works-bestissns-oa"), "oabestissns", "OaBestIssnsAdapter"),
    (("oabestdname", "bestdname-oa", "works-bestdname-oa"), "oabestdname", "OaBestDnameAdapter"),
    (("oapridname", "pridname-oa", "works-pridname-oa"), "oapridname", "OaPriDnameAdapter"),
    (("oapriissns", "priissns-oa", "works-priissns-oa"), "oapriissns", "OaPriIssnsAdapter"),
    (("oapriissn", "priissn-oa", "works-priissn-oa"), "oapriissn", "OaPriIssnAdapter"),
    (("oapriisoa", "priisoa-oa", "works-priisoa-oa"), "oapriisoa", "OaPriIsOaAdapter"),
    (("oapridoaj", "pridoaj-oa", "works-pridoaj-oa"), "oapridoaj", "OaPriDoajAdapter"),
]

_LIVE = {alias: (mod, cls) for aliases, mod, cls in _SPECS for alias in aliases}
LIVE_EXTRA = set(_LIVE) | {"multi", "all", "openlibrary", "ol", "books"}


def get_live_adapter(key: str) -> SearchAdapter:
    if key in {"multi", "all"}:
        from tools.openlibrary import MultiAdapter
        return MultiAdapter()
    spec = _LIVE.get(key)
    if spec is None:
        from tools.openlibrary import OpenLibraryAdapter
        return OpenLibraryAdapter()
    mod_name, cls_name = spec
    return getattr(importlib.import_module(f"tools.{mod_name}"), cls_name)()
