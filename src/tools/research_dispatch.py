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
    "openaire",
    "oaire",
    "graph",
    "core",
    "coreac",
    "works-core",
    "s2graph",
    "graph-s2",
    "s2-extra",
    "unpaywall",
    "upw",
    "oa-status",
    "xrefextra",
    "cr-extra",
    "cites-xr",
    "oaextra",
    "oa-extra",
    "cites-oa",
    "oairextra",
    "oaire-extra",
    "cites-oaire",
    "epmcextra",
    "epmc-extra",
    "cites-epmc",
    "orcidextra",
    "orcid-extra",
    "ids-orcid",
    "dcextra",
    "dc-extra",
    "cites-dc",
    "crfunder",
    "funders-cr",
    "cites-funder",
    "oafunder",
    "funders-oa",
    "cites-funder-oa",
    "orcidworks",
    "works-orcid",
    "orcid-works",
    "oatopic",
    "topics-oa",
    "cites-topic-oa",
    "oaconcept",
    "concepts-oa",
    "cites-concept-oa",
    "oasource",
    "sources-oa",
    "cites-source-oa",
    "oapublisher",
    "publishers-oa",
    "cites-publisher-oa",
    "oainstitution",
    "institutions-oa",
    "cites-institution-oa",
    "oaauthor",
    "authors-oa",
    "cites-author-oa",
    "oayear",
    "years-oa",
    "works-year-oa",
    "oatype",
    "types-oa",
    "works-type-oa",
    "oalang",
    "languages-oa",
    "works-lang-oa",
    "oaostatus",
    "status-oa",
    "works-oa-status",
    "oacountry",
    "countries-oa",
    "works-country-oa",
    "oacontinent",
    "continents-oa",
    "works-continent-oa",
    "oasrctype",
    "source-types-oa",
    "works-source-type-oa",
    "oaretracted",
    "retracted-oa",
    "works-retracted-oa",
    "oaparatext",
    "paratext-oa",
    "works-paratext-oa",
    "oadoi",
    "doi-oa",
    "works-doi-oa",
    "oahasoa",
    "hasoa-oa",
    "works-hasoa-oa",
    "oahaspmid",
    "haspmid-oa",
    "works-haspmid-oa",
    "oahaspmcid",
    "haspmcid-oa",
    "works-haspmcid-oa",
    "oahasisn",
    "hasissn-oa",
    "works-hasissn-oa",
    "oahasorcid",
    "hasorcid-oa",
    "works-hasorcid-oa",
    "oahasaffil",
    "hasaffil-oa",
    "works-hasaffil-oa",
    "oahasrefs",
    "hasrefs-oa",
    "works-hasrefs-oa",
    "oahasabs",
    "hasabs-oa",
    "works-hasabs-oa",
    "oahaspdf",
    "haspdf-oa",
    "works-haspdf-oa",
    "oahasft",
    "hasft-oa",
    "works-hasft-oa",
    "oahasoaap",
    "hasoaap-oa",
    "works-hasoaap-oa",
    "oahasoasub",
    "hasoasub-oa",
    "works-hasoasub-oa",
    "oahasoarepo",
    "hasoarepo-oa",
    "works-hasoarepo-oa",
    "oahasogold",
    "hasogold-oa",
    "works-hasogold-oa",
    "oahasoahybrid",
    "hasoahybrid-oa",
    "works-hasoahybrid-oa",
    "oahasobronze",
    "hasobronze-oa",
    "works-hasobronze-oa",
    "oahasogreen",
    "hasogreen-oa",
    "works-hasogreen-oa",
    "oahasodiamond",
    "hasodiamond-oa",
    "works-hasodiamond-oa",
    "oaisoa",
    "isoa-oa",
    "works-isoa-oa",
    "oahasoanyrepo",
    "hasoanyrepo-oa",
    "works-hasoanyrepo-oa",
    "oahasoapub",
    "hasoapub-oa",
    "works-hasoapub-oa",
    "oahasoadomain",
    "hasoadomain-oa",
    "works-hasoadomain-oa",
    "oahasoofile",
    "hasoafile-oa",
    "works-hasoafile-oa",
    "oahasoaurl",
    "hasoaurl-oa",
    "works-hasoaurl-oa",
    "oahasoaver",
    "hasoaver-oa",
    "works-hasoaver-oa",
    "oahasoaalic",
    "hasoaalic-oa",
    "works-hasoaalic-oa",
    "oahasoaalicid",
    "hasoaalicid-oa",
    "works-hasoaalicid-oa",
    "oabestlic",
    "bestlic-oa",
    "works-bestlic-oa",
    "oabestlicid",
    "bestlicid-oa",
    "works-bestlicid-oa",
    "multi",
    "all",
}


def get_adapter(name: str | None = None) -> SearchAdapter:
    key = (name or "wikipedia").strip().lower()
    if key in LIVE_EXTRA:
        from tools import arxiv as axmod
        from tools import core as coremod
        from tools import crfunder as crfmod
        from tools import crossref as xrmod
        from tools import datacite as dcmod
        from tools import dcextra as dcexmod
        from tools import doaj as doajmod
        from tools import epmcextra as epmcexmod
        from tools import europepmc as epmcmod
        from tools import hackernews as hnmod
        from tools import oaauthor as oaamod
        from tools import oaconcept as oacmod
        from tools import oacontinent as oactmod
        from tools import oacountry as oacnmod
        from tools import oadoi as oadoimod
        from tools import oaextra as oaexmod
        from tools import oafunder as oafmod
        from tools import oahasabs as oaabsmod
        from tools import oahasaffil as oaaffilmod
        from tools import oahasft as oaftmod
        from tools import oahasoa as oahasmod
        from tools import oahasoaap as oaoaapmod
        from tools import oahasobronze as oabronzemod
        from tools import oahasodiamond as oadiamondmod
        from tools import oahasogold as oagoldmod
        from tools import oahasogreen as oagreenmod
        from tools import oahasoahybrid as oahybridmod
        from tools import oahasoanyrepo as oaanyrepomod
        from tools import oahasoadomain as oadomainmod
        from tools import oahasoofile as oafilemod
        from tools import oahasoaurl as oaurlmod
        from tools import oahasoaver as oavermod
        from tools import oahasoaalic as oalicmod
        from tools import oahasoaalicid as oalicidmod
        from tools import oabestlic as oablmod
        from tools import oabestlicid as oablidmod
        from tools import oahasoapub as oapubmod
        from tools import oahasoarepo as oarepomod
        from tools import oahasoasub as oasubmod
        from tools import oahasisn as oaisnmod
        from tools import oahasorcid as oaorcidmod
        from tools import oahaspdf as oapdfmod
        from tools import oahaspmcid as oapmcidmod
        from tools import oahaspmid as oapmidmod
        from tools import oahasrefs as oarefsmod
        from tools import oaisoa as oaisoamod
        from tools import oairextra as oaxmod
        from tools import oainstitution as oaimod
        from tools import oalang as oalmod
        from tools import oaostatus as oaosmod
        from tools import oaparatext as oaptmod
        from tools import oapublisher as oapmod
        from tools import oaretracted as oarmd
        from tools import oasource as oasmod
        from tools import oasrctype as oastmod
        from tools import oatopic as oatmmod
        from tools import oatype as oatpmod
        from tools import oayear as oaymod
        from tools import openaire as oairemod
        from tools import openalex as oamod
        from tools import openlibrary as olmod
        from tools import orcidextra as orcidexmod
        from tools import orcidworks as orcidwmod
        from tools import pubmed as pmmod
        from tools import s2graph as s2gmod
        from tools import semanticscholar as s2mod
        from tools import unpaywall as upwmod
        from tools import wikidata as wdmod
        from tools import xrefextra as xremod
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
        if key in {"openaire", "oaire", "graph"}:
            return oairemod.OpenaireAdapter()
        if key in {"core", "coreac", "works-core"}:
            return coremod.CoreAdapter()
        if key in {"s2graph", "graph-s2", "s2-extra"}:
            return s2gmod.S2GraphAdapter()
        if key in {"unpaywall", "upw", "oa-status"}:
            return upwmod.UnpaywallAdapter()
        if key in {"xrefextra", "cr-extra", "cites-xr"}:
            return xremod.XrefExtraAdapter()
        if key in {"oaextra", "oa-extra", "cites-oa"}:
            return oaexmod.OaExtraAdapter()
        if key in {"oairextra", "oaire-extra", "cites-oaire"}:
            return oaxmod.OaireExtraAdapter()
        if key in {"epmcextra", "epmc-extra", "cites-epmc"}:
            return epmcexmod.EpmcExtraAdapter()
        if key in {"orcidextra", "orcid-extra", "ids-orcid"}:
            return orcidexmod.OrcidExtraAdapter()
        if key in {"dcextra", "dc-extra", "cites-dc"}:
            return dcexmod.DataCiteExtraAdapter()
        if key in {"crfunder", "funders-cr", "cites-funder"}:
            return crfmod.CrFunderAdapter()
        if key in {"oafunder", "funders-oa", "cites-funder-oa"}:
            return oafmod.OaFunderAdapter()
        if key in {"orcidworks", "works-orcid", "orcid-works"}:
            return orcidwmod.OrcidWorksAdapter()
        if key in {"oatopic", "topics-oa", "cites-topic-oa"}:
            return oatmmod.OaTopicAdapter()
        if key in {"oaconcept", "concepts-oa", "cites-concept-oa"}:
            return oacmod.OaConceptAdapter()
        if key in {"oasource", "sources-oa", "cites-source-oa"}:
            return oasmod.OaSourceAdapter()
        if key in {"oapublisher", "publishers-oa", "cites-publisher-oa"}:
            return oapmod.OaPublisherAdapter()
        if key in {"oainstitution", "institutions-oa", "cites-institution-oa"}:
            return oaimod.OaInstitutionAdapter()
        if key in {"oaauthor", "authors-oa", "cites-author-oa"}:
            return oaamod.OaAuthorAdapter()
        if key in {"oayear", "years-oa", "works-year-oa"}:
            return oaymod.OaYearAdapter()
        if key in {"oatype", "types-oa", "works-type-oa"}:
            return oatpmod.OaTypeAdapter()
        if key in {"oalang", "languages-oa", "works-lang-oa"}:
            return oalmod.OaLangAdapter()
        if key in {"oaostatus", "status-oa", "works-oa-status"}:
            return oaosmod.OaOaStatusAdapter()
        if key in {"oacountry", "countries-oa", "works-country-oa"}:
            return oacnmod.OaCountryAdapter()
        if key in {"oacontinent", "continents-oa", "works-continent-oa"}:
            return oactmod.OaContinentAdapter()
        if key in {"oasrctype", "source-types-oa", "works-source-type-oa"}:
            return oastmod.OaSrcTypeAdapter()
        if key in {"oaretracted", "retracted-oa", "works-retracted-oa"}:
            return oarmd.OaRetractedAdapter()
        if key in {"oaparatext", "paratext-oa", "works-paratext-oa"}:
            return oaptmod.OaParatextAdapter()
        if key in {"oadoi", "doi-oa", "works-doi-oa"}:
            return oadoimod.OaDoiAdapter()
        if key in {"oahasoa", "hasoa-oa", "works-hasoa-oa"}:
            return oahasmod.OaHasOaAdapter()
        if key in {"oahaspmid", "haspmid-oa", "works-haspmid-oa"}:
            return oapmidmod.OaHasPmidAdapter()
        if key in {"oahaspmcid", "haspmcid-oa", "works-haspmcid-oa"}:
            return oapmcidmod.OaHasPmcidAdapter()
        if key in {"oahasisn", "hasissn-oa", "works-hasissn-oa"}:
            return oaisnmod.OaHasIssnAdapter()
        if key in {"oahasorcid", "hasorcid-oa", "works-hasorcid-oa"}:
            return oaorcidmod.OaHasOrcidAdapter()
        if key in {"oahasaffil", "hasaffil-oa", "works-hasaffil-oa"}:
            return oaaffilmod.OaHasAffilAdapter()
        if key in {"oahasrefs", "hasrefs-oa", "works-hasrefs-oa"}:
            return oarefsmod.OaHasRefsAdapter()
        if key in {"oahasabs", "hasabs-oa", "works-hasabs-oa"}:
            return oaabsmod.OaHasAbsAdapter()
        if key in {"oahaspdf", "haspdf-oa", "works-haspdf-oa"}:
            return oapdfmod.OaHasPdfAdapter()
        if key in {"oahasft", "hasft-oa", "works-hasft-oa"}:
            return oaftmod.OaHasFtAdapter()
        if key in {"oahasoaap", "hasoaap-oa", "works-hasoaap-oa"}:
            return oaoaapmod.OaHasOaapAdapter()
        if key in {"oahasoasub", "hasoasub-oa", "works-hasoasub-oa"}:
            return oasubmod.OaHasOaSubAdapter()
        if key in {"oahasoarepo", "hasoarepo-oa", "works-hasoarepo-oa"}:
            return oarepomod.OaHasOaRepoAdapter()
        if key in {"oahasogold", "hasogold-oa", "works-hasogold-oa"}:
            return oagoldmod.OaHasOaGoldAdapter()
        if key in {"oahasoahybrid", "hasoahybrid-oa", "works-hasoahybrid-oa"}:
            return oahybridmod.OaHasOaHybridAdapter()
        if key in {"oahasobronze", "hasobronze-oa", "works-hasobronze-oa"}:
            return oabronzemod.OaHasOaBronzeAdapter()
        if key in {"oahasogreen", "hasogreen-oa", "works-hasogreen-oa"}:
            return oagreenmod.OaHasOaGreenAdapter()
        if key in {"oahasodiamond", "hasodiamond-oa", "works-hasodiamond-oa"}:
            return oadiamondmod.OaHasOaDiamondAdapter()
        if key in {"oaisoa", "isoa-oa", "works-isoa-oa"}:
            return oaisoamod.OaIsOaAdapter()
        if key in {"oahasoanyrepo", "hasoanyrepo-oa", "works-hasoanyrepo-oa"}:
            return oaanyrepomod.OaHasOaAnyRepoAdapter()
        if key in {"oahasoapub", "hasoapub-oa", "works-hasoapub-oa"}:
            return oapubmod.OaHasOaPubAdapter()
        if key in {"oahasoadomain", "hasoadomain-oa", "works-hasoadomain-oa"}:
            return oadomainmod.OaHasOaDomainAdapter()
        if key in {"oahasoofile", "hasoafile-oa", "works-hasoafile-oa"}:
            return oafilemod.OaHasOaFileAdapter()
        if key in {"oahasoaurl", "hasoaurl-oa", "works-hasoaurl-oa"}:
            return oaurlmod.OaHasOaUrlAdapter()
        if key in {"oahasoaver", "hasoaver-oa", "works-hasoaver-oa"}:
            return oavermod.OaHasOaVerAdapter()
        if key in {"oahasoaalic", "hasoaalic-oa", "works-hasoaalic-oa"}:
            return oalicmod.OaHasOaLicAdapter()
        if key in {"oahasoaalicid", "hasoaalicid-oa", "works-hasoaalicid-oa"}:
            return oalicidmod.OaHasOaLicIdAdapter()
        if key in {"oabestlic", "bestlic-oa", "works-bestlic-oa"}:
            return oablmod.OaBestLicAdapter()
        if key in {"oabestlicid", "bestlicid-oa", "works-bestlicid-oa"}:
            return oablidmod.OaBestLicIdAdapter()
        return olmod.OpenLibraryAdapter()
    cls = ADAPTERS.get(key)
    if cls is None:
        known = ", ".join(sorted(set(ADAPTERS) | LIVE_EXTRA))
        raise ValueError(f"Unknown search backend {name!r}. Known: {known}")
    return cls()


def default_adapter() -> SearchAdapter:
    return WikipediaAdapter()
