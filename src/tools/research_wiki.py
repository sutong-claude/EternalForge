"""Wikipedia OpenSearch and DuckDuckGo Instant Answer adapters."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research_models import Hit, unavailable

USER_AGENT = "EternalForge/0.1 (research tool)"


class WikipediaAdapter:
    """Wikipedia OpenSearch over HTTPS. Safe to call without credentials."""

    name = "wikipedia"
    endpoint = "https://en.wikipedia.org/w/api.php"

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = (
            f"{self.endpoint}?action=opensearch&format=json"
            f"&limit={limit}&namespace=0&search={quote(q)}"
        )
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return unavailable(self.name, q)
        return parse_wikipedia_payload(payload, limit=limit)


def parse_wikipedia_payload(payload: object, limit: int = 5) -> list[Hit]:
    if not isinstance(payload, list) or len(payload) < 4:
        return []
    titles, snippets, urls = payload[1], payload[2], payload[3]
    hits: list[Hit] = []
    for title, snippet, link in zip(titles, snippets, urls):
        hits.append(
            Hit(
                title=str(title),
                url=str(link),
                snippet=str(snippet) or f"Wikipedia article: {title}",
                source="wikipedia",
            )
        )
    return hits[:limit]


class DuckDuckGoAdapter:
    """DuckDuckGo Instant Answer API. No key required."""

    name = "duckduckgo"
    endpoint = "https://api.duckduckgo.com/"

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = (
            f"{self.endpoint}?q={quote(q)}&format=json"
            f"&no_html=1&skip_disambig=1"
        )
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_duckduckgo_payload(payload, limit=limit)


def parse_duckduckgo_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Instant Answer JSON into Hits (abstract + related topics)."""
    hits: list[Hit] = []
    heading = str(payload.get("Heading") or payload.get("AnswerType") or "DuckDuckGo")
    abstract = str(payload.get("AbstractText") or payload.get("Abstract") or "").strip()
    abstract_url = str(payload.get("AbstractURL") or "").strip()
    answer = str(payload.get("Answer") or "").strip()
    if abstract or answer:
        hits.append(
            Hit(
                title=heading,
                url=abstract_url,
                snippet=abstract or answer,
                source="duckduckgo",
            )
        )
    related = payload.get("RelatedTopics") or []
    if isinstance(related, list):
        for item in related:
            if not isinstance(item, dict):
                continue
            if "Topics" in item and isinstance(item["Topics"], list):
                for nested in item["Topics"]:
                    hit = _ddg_topic_hit(nested)
                    if hit:
                        hits.append(hit)
                continue
            hit = _ddg_topic_hit(item)
            if hit:
                hits.append(hit)
    seen: set[tuple[str, str]] = set()
    unique: list[Hit] = []
    for hit in hits:
        key = (hit.title, hit.url)
        if key in seen:
            continue
        seen.add(key)
        unique.append(hit)
    return unique[:limit]


def _ddg_topic_hit(item: object) -> Hit | None:
    if not isinstance(item, dict):
        return None
    text = str(item.get("Text") or "").strip()
    url = str(item.get("FirstURL") or "").strip()
    if not text and not url:
        return None
    title = text.split(" -", 1)[0].strip() or text[:80] or url
    return Hit(title=title, url=url, snippet=text, source="duckduckgo")
