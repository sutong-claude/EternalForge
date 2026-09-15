from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core.memory import Journal
from tools.tasks import (
    add_task,
    count_open_tasks,
    format_tasks,
    list_tasks,
    load_tasks,
    normalize_due,
    normalize_priority,
    normalize_status,
    set_task_status,
    update_task,
)


def test_normalize_status_aliases() -> None:
    assert normalize_status("TODO") == "open"
    assert normalize_status("completed") == "done"
    assert normalize_status("canceled") == "cancelled"
    try:
        normalize_status("blocked")
    except ValueError as exc:
        assert "status" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_normalize_priority_and_due() -> None:
    assert normalize_priority(None) == "medium"
    assert normalize_priority("HI") == "high"
    assert normalize_priority("p0") == "urgent"
    assert normalize_due("") == ""
    assert normalize_due("2026-09-20") == "2026-09-20"
    try:
        normalize_priority("banana")
    except ValueError as exc:
        assert "priority" in str(exc)
    else:
        raise AssertionError("expected ValueError")
    try:
        normalize_due("09/20/2026")
    except ValueError as exc:
        assert "YYYY-MM-DD" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_add_and_list_tasks(tmp_path: Path) -> None:
    first = add_task(tmp_path, "Write tests", tags=["core"])
    second = add_task(tmp_path, "Ship CLI", notes="after tests")
    assert first.id == "T001"
    assert second.id == "T002"
    assert first.status == "open"
    assert first.priority == "medium"
    assert first.due == ""
    rows = list_tasks(tmp_path)
    assert [t.id for t in rows] == ["T001", "T002"]
    assert count_open_tasks(tmp_path) == 2
    text = format_tasks(rows)
    assert "T001\topen\tWrite tests #core" in text


def test_due_and_priority_roundtrip(tmp_path: Path) -> None:
    task = add_task(
        tmp_path,
        "File taxes",
        due="2026-04-15",
        priority="high",
        tags=["admin"],
    )
    assert task.due == "2026-04-15"
    assert task.priority == "high"
    listed = list_tasks(tmp_path, priority="high")
    assert [t.id for t in listed] == [task.id]
    assert list_tasks(tmp_path, priority="low") == []
    text = format_tasks(listed)
    assert "p=high" in text
    assert "due=2026-04-15" in text
    updated = update_task(tmp_path, task.id, due="2026-04-30", priority="urgent")
    assert updated.due == "2026-04-30"
    assert updated.priority == "urgent"
    stored = load_tasks(tmp_path)[0]
    assert stored.due == "2026-04-30"
    assert stored.priority == "urgent"


def test_set_status_and_journal(tmp_path: Path) -> None:
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    task = add_task(tmp_path, "Close me", journal=journal)
    updated = set_task_status(tmp_path, task.id.lower(), "done", journal=journal)
    assert updated.status == "done"
    assert count_open_tasks(tmp_path) == 0
    assert list_tasks(tmp_path, status="done")[0].id == task.id
    lines = journal.path.read_text(encoding="utf-8").splitlines()
    kinds = [json.loads(line)["kind"] for line in lines]
    assert kinds == ["task", "task"]
    last = json.loads(lines[-1])
    assert "done" in last["summary"]
    assert "done" in last["tags"]


def test_unknown_id_raises(tmp_path: Path) -> None:
    add_task(tmp_path, "exists")
    try:
        set_task_status(tmp_path, "T999", "done")
    except ValueError as exc:
        assert "unknown" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_empty_title_raises(tmp_path: Path) -> None:
    try:
        add_task(tmp_path, "   ")
    except ValueError as exc:
        assert "title" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_load_skips_bad_lines(tmp_path: Path) -> None:
    path = tmp_path / "memory" / "tasks.jsonl"
    path.parent.mkdir(parents=True)
    path.write_text(
        "{not json}\n"
        + json.dumps({"id": "T001", "title": "ok", "status": "open"}) + "\n"
        + json.dumps({"id": "", "title": "skip"}) + "\n",
        encoding="utf-8",
    )
    rows = load_tasks(tmp_path)
    assert len(rows) == 1
    assert rows[0].title == "ok"
    assert rows[0].priority == "medium"


def test_missing_file_is_empty(tmp_path: Path) -> None:
    assert load_tasks(tmp_path) == []
    assert count_open_tasks(tmp_path) == 0
    assert format_tasks([]) == "(no tasks)"
