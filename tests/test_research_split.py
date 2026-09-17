from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools import research
from tools.research_dispatch import LIVE_EXTRA, get_adapter as dispatch_get
from tools.research_models import FixtureAdapter, Hit
from tools.research_wiki import WikipediaAdapter, parse_wikipedia_payload


def test_research_facade_reexports_split_modules() -> None:
    assert research.LIVE_EXTRA == LIVE_EXTRA
    assert research.get_adapter is dispatch_get
    assert research.WikipediaAdapter is WikipediaAdapter
    assert research.FixtureAdapter is FixtureAdapter
    assert research.parse_wikipedia_payload is parse_wikipedia_payload
    hits = research.search("eternalforge", adapter=FixtureAdapter())
    assert hits and isinstance(hits[0], Hit)
    assert research.get_adapter("fixture").name == "fixture"
