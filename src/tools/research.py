"""
Research tool skeleton.
Future runs will implement real web research + summarization.
"""

from typing import List, Dict


def search(query: str, max_results: int = 5) -> List[Dict]:
    """Placeholder for web search."""
    return [{"title": f"Placeholder result for: {query}", "url": "", "snippet": ""}]


def summarize(text: str, max_length: int = 300) -> str:
    """Placeholder summarizer."""
    return text[:max_length] + ("..." if len(text) > max_length else "")
