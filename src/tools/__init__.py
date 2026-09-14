"""Tools for the EternalForge agent."""

from tools.capture import CaptureResult, capture
from tools.research import Hit, SearchAdapter, search, summarize

__all__ = [
    "Hit",
    "SearchAdapter",
    "search",
    "summarize",
    "capture",
    "CaptureResult",
]
