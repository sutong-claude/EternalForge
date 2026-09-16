from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.agent import Agent
from core.state import dump_state, ForgeState, parse_state
from interfaces.cli import build_parser, main
from tools.kb import collect_documents, search_kb


def _seed(tmp: Path) -> Path:
    state = ForgeState(
        last_updated="2026-09-16",
        phase="Core Agent",
        progress=0.97,
        current_goal="Build the loop",
        priorities=["Land digest status"],
        metrics={"Files": "1", "Tests": "0", "Features shipped": "1", "Cycles": "0"},
        notes="Keep one task per cycle.",
    )
    (tmp / "STATE.md").write_text(dump_state(state), encoding="utf-8")
    (tmp / "CHANGELOG.md").write_text(
        "# Changelog\n\n## 0.1.0 — 2026-09-16\n\n- bootstrap\n",
        encoding="utf-8",
    )
    return tmp


def test_status_digest_lists_filenames(tmp_path: Path, capsys) -> None:
    root = _seed(tmp_path)
    folder = root / "memory" / "reviews"
    folder.mkdir(parents=True)
    (folder / "daily-2026-09-14.md").write_text("# d\n", encoding="utf-8")
    (folder / "digest-2026-09-16.md").write_text("# coverage note\n", encoding="utf-8")
    text = Agent(root).status(digest=True)
    assert "digests=1" in text
    assert "reviews=2" in text
    assert "- digest-2026-09-16.md" in text
    ns = build_parser().parse_args(["status", "--digest"])
    assert ns.digest is True
    rc = main(["--root", str(root), "status", "--digest"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "digest-2026-09-16.md" in out


def test_cycle_persists_digest_count(tmp_path: Path) -> None:
    root = _seed(tmp_path)
    folder = root / "memory" / "reviews"
    folder.mkdir(parents=True)
    (folder / "digest-2026-09-16.md").write_text("# d\n", encoding="utf-8")
    Agent(root).run_once(dry_run=False)
    state = parse_state((root / "STATE.md").read_text(encoding="utf-8"))
    assert state.metrics["Digests"] == "1"
    log = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "digests=1" in log


def test_kb_classifies_digest_files(tmp_path: Path) -> None:
    reviews = tmp_path / "memory" / "reviews"
    reviews.mkdir(parents=True)
    (reviews / "daily-2026-09-14.md").write_text(
        "# Daily review\nstandup notes\n", encoding="utf-8"
    )
    (reviews / "digest-2026-09-16.md").write_text(
        "# Reviews digest\ncoverage note about reviews\n", encoding="utf-8"
    )
    docs = collect_documents(tmp_path)
    digest = next(d for d in docs if d.source == "digest")
    assert digest.kind == "digest"
    assert digest.path.endswith("digest-2026-09-16.md")
    review = next(d for d in docs if d.source == "review")
    assert review.kind == "review"
    hits = search_kb(tmp_path, "coverage", kind="digest")
    assert hits
    assert all(h.kind == "digest" for h in hits)
