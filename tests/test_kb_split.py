from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools import kb
from tools.kb_collect import collect_documents as collect_impl
from tools.kb_index import build_index as build_impl
from tools.kb_index import search_kb as search_impl
from tools.kb_models import Document, IndexHit, KnowledgeIndex


def test_kb_facade_reexports_split_modules() -> None:
    assert kb.collect_documents is collect_impl
    assert kb.build_index is build_impl
    assert kb.search_kb is search_impl
    assert kb.Document is Document
    assert kb.IndexHit is IndexHit
    assert kb.KnowledgeIndex is KnowledgeIndex
    empty = kb.build_index(documents=[])
    assert empty.document_count() == 0
    assert kb.search_index(empty, "anything") == []
