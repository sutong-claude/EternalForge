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

from tools.research_live import LIVE_EXTRA, get_live_adapter


def get_adapter(name: str | None = None) -> SearchAdapter:
    key = (name or "wikipedia").strip().lower()
    if key in LIVE_EXTRA:
        return get_live_adapter(key)
    cls = ADAPTERS.get(key)
    if cls is None:
        known = ", ".join(sorted(set(ADAPTERS) | LIVE_EXTRA))
        raise ValueError(f"Unknown search backend {name!r}. Known: {known}")
    return cls()


def default_adapter() -> SearchAdapter:
    return WikipediaAdapter()
