from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tools import review
from tools.review_const import PERIODS
from tools.review_digest import write_cycle_digest as digest_write
from tools.review_files import classify_review_name
from tools.review_sketch import write_cycle_daily as daily_write
from tools.review_window import normalize_period


def test_review_facade_reexports_split_modules() -> None:
    assert review.PERIODS == PERIODS
    assert review.classify_review_name is classify_review_name
    assert review.normalize_period is normalize_period
    assert review.write_cycle_daily is daily_write
    assert review.write_cycle_digest is digest_write
    assert review.normalize_period("w") == "weekly"
    assert review.classify_review_name("digest-2026-09-17.md") == ("digest", "2026-09-17")
