from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools import tasks
from tools.task_const import STATUSES
from tools.task_model import Task
from tools.task_ops import add_task as ops_add
from tools.task_store import next_id


def test_tasks_facade_reexports_split_modules() -> None:
    assert tasks.STATUSES == STATUSES
    assert tasks.Task is Task
    assert tasks.add_task is ops_add
    assert next_id([]) == "T001"
    assert next_id([Task(id="T002", title="x")]) == "T003"
