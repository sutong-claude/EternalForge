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
    normalize_due_soon_days,
    normalize_priority,
    normalize_query,
    normalize_sort,
    normalize_status,
    set_task_status,
    sort_tasks,
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


def test_normalize_sort() -> None:
    assert normalize_sort(None) == "due"
    assert normalize_sort("PRI") == "priority"
    try:
        normalize_sort("alpha")
    except ValueError as exc:
        assert "sort" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_normalize_due_soon_days() -> None:
    assert normalize_due_soon_days(None) == 7
    assert normalize_due_soon_days("soon") == 7
    assert normalize_due_soon_days(0) == 0
    assert normalize_due_soon_days("3") == 3
    try:
        normalize_due_soon_days(-1)
    except ValueError as exc:
        assert "due-soon" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_normalize_query() -> None:
    assert normalize_query(None) == ""
    assert normalize_query("  Write   Tests ") == "write tests"


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
    text = format_tasks(listed, today="2026-01-01")
    assert "p=high" in text
    assert "due=2026-04-15" in text
    updated = update_task(tmp_path, task.id, due="2026-04-30", priority="urgent")
    assert updated.due == "2026-04-30"
    assert updated.priority == "urgent"
    stored = load_tasks(tmp_path)[0]
    assert stored.due == "2026-04-30"
    assert stored.priority == "urgent"


def test_sort_and_overdue(tmp_path: Path) -> None:
    late = add_task(tmp_path, "Late", due="2026-09-01", priority="low")
    soon = add_task(tmp_path, "Soon", due="2026-09-20", priority="urgent")
    undated = add_task(tmp_path, "Someday", priority="high")
    done = add_task(tmp_path, "Finished", due="2026-08-01", priority="urgent")
    set_task_status(tmp_path, done.id, "done")
    today = "2026-09-15"
    by_due = list_tasks(tmp_path, sort="due", today=today)
    assert [t.id for t in by_due] == [done.id, late.id, soon.id, undated.id]
    by_pri = list_tasks(tmp_path, sort="priority", today=today)
    assert [t.id for t in by_pri] == [done.id, soon.id, undated.id, late.id]
    overdue = list_tasks(tmp_path, overdue=True, today=today)
    assert [t.id for t in overdue] == [late.id]
    assert late.is_overdue(today)
    assert not soon.is_overdue(today)
    assert not done.is_overdue(today)
    text = format_tasks(overdue, today=today)
    assert "OVERDUE" in text
    assert late.id in text
    ranked = sort_tasks([undated, soon, late], sort="priority")
    assert [t.id for t in ranked] == [soon.id, undated.id, late.id]


def test_list_by_tag_and_due_soon(tmp_path: Path) -> None:
    core = add_task(tmp_path, "Core work", tags=["Core"], due="2026-09-16")
    admin = add_task(tmp_path, "Admin", tags=["admin"], due="2026-09-30")
    late = add_task(tmp_path, "Late core", tags=["#core"], due="2026-09-01")
    today = "2026-09-15"
    tagged = list_tasks(tmp_path, tag="#CORE", today=today)
    assert {t.id for t in tagged} == {core.id, late.id}
    any_tag = list_tasks(tmp_path, tag=["admin", "missing"], today=today)
    assert [t.id for t in any_tag] == [admin.id]
    soon = list_tasks(tmp_path, due_soon=7, today=today)
    assert [t.id for t in soon] == [core.id]
    assert not late.is_due_soon(7, today=today)
    assert core.is_due_soon(7, today=today)
    assert not admin.is_due_soon(7, today=today)
    text = format_tasks([core, late], today=today)
    assert "DUE-SOON" in text
    assert "OVERDUE" in text


def test_list_by_query(tmp_path: Path) -> None:
    title_hit = add_task(tmp_path, "Review arXiv hits", notes="skim abstracts")
    notes_hit = add_task(tmp_path, "File taxes", notes="Include arXiv stipend receipt")
    miss = add_task(tmp_path, "Water plants", notes="kitchen")
    assert title_hit.matches_query("ARXIV")
    assert notes_hit.matches_query("arxiv")
    assert not miss.matches_query("arxiv")
    assert miss.matches_query("")
    rows = list_tasks(tmp_path, query="  ArXiv ")
    assert [t.id for t in rows] == [title_hit.id, notes_hit.id]
    assert list_tasks(tmp_path, query="kitchen")[0].id == miss.id
    assert list_tasks(tmp_path, query="missing token") == []


def test_update_notes_and_tags(tmp_path: Path) -> None:
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    task = add_task(tmp_path, "Annotate me", notes="old", tags=["alpha"], journal=journal)
    updated = update_task(
        tmp_path,
        task.id,
        notes="new note",
        tags=["#Beta", "gamma"],
        journal=journal,
    )
    assert updated.notes == "new note"
    assert updated.tags == ["beta", "gamma"]
    stored = load_tasks(tmp_path)[0]
    assert stored.notes == "new note"
    assert stored.tags == ["beta", "gamma"]
    last = json.loads(journal.path.read_text(encoding="utf-8").splitlines()[-1])
    assert "notes" in last["summary"]
    assert "#beta" in last["summary"]
    assert last["details"] == "new note"
    cleared = update_task(tmp_path, task.id, notes="", tags=[], journal=journal)
    assert cleared.notes == ""
    assert cleared.tags == []
    untouched = update_task(tmp_path, task.id, priority="high", journal=journal)
    assert untouched.notes == ""
    assert untouched.tags == []
    assert untouched.priority == "high"


def test_update_title(tmp_path: Path) -> None:
    journal = Journal(tmp_path / "memory" / "journal.jsonl")
    task = add_task(tmp_path, "Old title", journal=journal)
    updated = update_task(tmp_path, task.id, title="  New title  ", journal=journal)
    assert updated.title == "New title"
    stored = load_tasks(tmp_path)[0]
    assert stored.title == "New title"
    last = json.loads(journal.path.read_text(encoding="utf-8").splitlines()[-1])
    assert "title=New title" in last["summary"]
    leftover = update_task(tmp_path, task.id, priority="low", journal=journal)
    assert leftover.title == "New title"
    try:
        update_task(tmp_path, task.id, title="   ", journal=journal)
    except ValueError as exc:
        assert "title" in str(exc)
    else:
        raise AssertionError("expected ValueError")
    assert load_tasks(tmp_path)[0].title == "New title"


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
