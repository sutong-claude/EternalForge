from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from interfaces.cli import build_parser, main
from tools.tasks import add_task, save_tasks


def test_cli_parses_task_list_exact_id_updated_since_sort_created() -> None:
    ns = build_parser().parse_args(
        [
            "task",
            "list",
            "--exact-id",
            "--id",
            "T001",
            "--updated-since",
            "2026-09-12",
            "--updated-until",
            "2026-09-16",
            "--sort",
            "created",
        ]
    )
    assert ns.cmd == "task"
    assert ns.task_cmd == "list"
    assert ns.exact_id is True
    assert ns.task_id_prefix == "T001"
    assert ns.updated_since == "2026-09-12"
    assert ns.updated_until == "2026-09-16"
    assert ns.sort == "created"


def test_cli_task_list_defaults_omit_exact_id_and_updated_window() -> None:
    ns = build_parser().parse_args(["task", "list"])
    assert ns.exact_id is False
    assert ns.task_id_prefix is None
    assert ns.updated_since is None
    assert ns.updated_until is None
    assert ns.sort == "due"


def test_cli_task_list_exact_id_updated_since_sort_created(tmp_path: Path, capsys) -> None:
    first = add_task(tmp_path, "First")
    second = add_task(tmp_path, "Second")
    first.created = "2026-09-10T12:00:00Z"
    first.updated = "2026-09-12T09:00:00Z"
    second.created = "2026-09-11T08:00:00Z"
    second.updated = "2026-09-16T08:00:00Z"
    save_tasks(tmp_path, [first, second])

    rc = main(
        [
            "--root",
            str(tmp_path),
            "task",
            "list",
            "--id",
            "T001",
            "--exact-id",
            "--updated-since",
            "2026-09-12",
            "--sort",
            "created",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "T001" in out
    assert "T002" not in out

    rc = main(
        [
            "--root",
            str(tmp_path),
            "task",
            "list",
            "--id",
            "T00",
            "--exact-id",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "(no tasks)" in out

    rc = main(
        [
            "--root",
            str(tmp_path),
            "task",
            "list",
            "--updated-since",
            "2026-09-16",
            "--sort",
            "created",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "T002" in out
    assert "T001" not in out
