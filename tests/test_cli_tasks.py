from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from interfaces.cli import build_parser, main
from tools.tasks import add_task, save_tasks, set_task_status


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
    assert ns.overdue is False
    assert ns.due_soon is None
    assert ns.query is None
    assert ns.status is None
    assert ns.priority is None
    assert ns.tags is None
    assert ns.since is None
    assert ns.until is None


def test_cli_parses_task_list_due_soon_overdue_query() -> None:
    ns = build_parser().parse_args(
        ["task", "list", "--overdue", "--due-soon", "3", "--query", "arxiv"]
    )
    assert ns.overdue is True
    assert ns.due_soon == "3"
    assert ns.query == "arxiv"

    bare = build_parser().parse_args(["task", "list", "--due-soon"])
    assert bare.due_soon == 7


def test_cli_parses_task_list_tag_status_priority_since_until() -> None:
    ns = build_parser().parse_args(
        [
            "task",
            "list",
            "--status",
            "done",
            "--priority",
            "high",
            "--tag",
            "#Research",
            "--tag",
            "papers",
            "--since",
            "2026-09-10",
            "--until",
            "2026-09-16",
        ]
    )
    assert ns.status == "done"
    assert ns.priority == "high"
    assert ns.tags == ["#Research", "papers"]
    assert ns.since == "2026-09-10"
    assert ns.until == "2026-09-16"


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


def test_cli_task_list_due_soon_overdue_query(tmp_path: Path, capsys) -> None:
    late = add_task(tmp_path, "Late arXiv follow-up", due="2026-09-01")
    soon = add_task(tmp_path, "Soon taxes", notes="arxiv stipend", due="2026-09-18")
    far = add_task(tmp_path, "Far planning", notes="next quarter", due="2026-12-01")
    done_late = add_task(tmp_path, "Finished late arXiv", due="2026-08-01")
    set_task_status(tmp_path, done_late.id, "done")

    rc = main(["--root", str(tmp_path), "task", "list", "--overdue"])
    assert rc == 0
    out = capsys.readouterr().out
    assert late.id in out
    assert "OVERDUE" in out
    assert soon.id not in out
    assert done_late.id not in out

    rc = main(["--root", str(tmp_path), "task", "list", "--due-soon", "7"])
    assert rc == 0
    out = capsys.readouterr().out
    assert soon.id in out
    assert "DUE-SOON" in out
    assert late.id not in out
    assert far.id not in out

    rc = main(["--root", str(tmp_path), "task", "list", "--query", "ARXIV"])
    assert rc == 0
    out = capsys.readouterr().out
    assert late.id in out
    assert soon.id in out
    assert done_late.id in out
    assert far.id not in out


def test_cli_task_list_tag_status_priority_since_until(tmp_path: Path, capsys) -> None:
    research = add_task(
        tmp_path,
        "Index papers",
        tags=["research", "papers"],
        priority="high",
    )
    chores = add_task(tmp_path, "Pay taxes", tags=["admin"], priority="low")
    done = add_task(tmp_path, "Shipped digest", tags=["research"], priority="high")
    set_task_status(tmp_path, done.id, "done")
    research.created = "2026-09-12T10:00:00Z"
    chores.created = "2026-09-08T10:00:00Z"
    done.created = "2026-09-14T10:00:00Z"
    save_tasks(tmp_path, [research, chores, done])

    rc = main(["--root", str(tmp_path), "task", "list", "--status", "done"])
    assert rc == 0
    out = capsys.readouterr().out
    assert done.id in out
    assert research.id not in out
    assert chores.id not in out

    rc = main(["--root", str(tmp_path), "task", "list", "--priority", "high"])
    assert rc == 0
    out = capsys.readouterr().out
    assert research.id in out
    assert done.id in out
    assert chores.id not in out
    assert "p=high" in out

    rc = main(["--root", str(tmp_path), "task", "list", "--tag", "#Research"])
    assert rc == 0
    out = capsys.readouterr().out
    assert research.id in out
    assert done.id in out
    assert chores.id not in out

    rc = main(
        [
            "--root",
            str(tmp_path),
            "task",
            "list",
            "--tag",
            "admin",
            "--tag",
            "papers",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert research.id in out
    assert chores.id in out
    assert done.id not in out

    rc = main(
        [
            "--root",
            str(tmp_path),
            "task",
            "list",
            "--since",
            "2026-09-12",
            "--until",
            "2026-09-13",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert research.id in out
    assert chores.id not in out
    assert done.id not in out
