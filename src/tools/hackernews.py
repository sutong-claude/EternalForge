"""Hacker News (Algolia) SearchAdapter."""

from __future__ import annotations

import json
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from tools.research import USER_AGENT, Hit, _unavailable


class HackerNewsAdapter:
    """HN search via Algolia. No key required; good for tech discussion."""

    name = "hackernews"
    endpoint = "https://hn.algolia.com/api/v1/search"

    def __init__(self, timeout: float = 8.0) -> None:
        self.timeout = timeout

    def search(self, query: str, max_results: int = 5) -> list[Hit]:
        q = query.strip()
        if not q:
            return []
        limit = max(1, min(max_results, 20))
        url = f"{self.endpoint}?query={quote(q)}&hitsPerPage={limit}"
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError, OSError):
            return _unavailable(self.name, q)
        if not isinstance(payload, dict):
            return []
        return parse_hackernews_payload(payload, limit=limit)


def parse_hackernews_payload(payload: dict, limit: int = 5) -> list[Hit]:
    """Map Algolia HN search hits into research Hits."""
    rows = payload.get("hits") or []
    if not isinstance(rows, list):
        return []
    hits: list[Hit] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        object_id = str(row.get("objectID") or "").strip()
        title = str(row.get("title") or row.get("story_title") or "").strip()
        url = str(row.get("url") or "").strip()
        if not url and object_id:
            url = f"https://news.ycombinator.com/item?id={object_id}"
        author = str(row.get("author") or "").strip()
        points = row.get("points")
        num_comments = row.get("num_comments")
        comment = str(row.get("comment_text") or row.get("story_text") or "").strip()
        bits: list[str] = []
        if author:
            bits.append(author)
        if isinstance(points, (int, float)):
            bits.append(f"{int(points)} pts")
        if isinstance(num_comments, (int, float)):
            bits.append(f"{int(num_comments)} comments")
        snippet = " · ".join(bits)
        if comment:
            snippet = f"{snippet} · {comment}" if snippet else comment
        snippet = snippet or "Hacker News discussion"
        if not title and not url:
            continue
        hits.append(
            Hit(
                title=title or f"HN {object_id}" or "Hacker News",
                url=url,
                snippet=snippet,
                source="hackernews",
            )
        )
    return hits[:limit]
