"""eternalforge status | next | cycle [--dry-run] | recent | research QUERY | capture | kb QUERY | report | task"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from core.agent import Agent
from tools.capture import DEFAULT_TOPICS, capture
from tools.kb import build_index, format_index_hits, parse_day, search_kb, write_index
from tools.report import write_report
from tools.research import FixtureAdapter, format_hits, get_adapter, record_hits, search
from tools.tasks import add_task, format_tasks, list_tasks, update_task

BACKEND_HELP = (
    "Search backend: wikipedia, duckduckgo, openlibrary, hackernews, arxiv, crossref, "
    "semanticscholar, pubmed, multi, fixture "
    "(aliases: ddg, ol, books, hn, algolia, papers, preprint, doi, works, s2, scholar, "
    "ncbi, medline, all)"
)
