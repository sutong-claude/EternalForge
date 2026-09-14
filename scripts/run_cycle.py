#!/usr/bin/env python3
"""Convenience entry: python scripts/run_cycle.py --dry-run"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from interfaces.cli import main  # noqa: E402

if __name__ == "__main__":
    args = sys.argv[1:] or ["status"]
    raise SystemExit(main(["--root", str(ROOT), *args]))
