"""Research tool skeleton. Hourly runs will replace placeholders with real search."""

from __future__ import annotations

from typing import TypedDict


class Hit(TypedDict):
    title: str
    url: str
    snippet: str


def search(query: str, max_results: int = 5) -> list[Hit]:
    _ = max_results
    return [
        {
            "title": f"Queued research: {query}",
            "url": "",
            "snippet": "Connect a live search backend in a later cycle.",
        }
    ]


def summarize(text: str, max_length: int = 300) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_length:
        return compact
    return compact[: max_length - 3] + "..."
