from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from interfaces import cli
from interfaces.cli_const import BACKEND_HELP
from interfaces.cli_parser import build_parser as parser_build


def test_cli_facade_reexports_split_modules() -> None:
    assert cli.BACKEND_HELP == BACKEND_HELP
    assert cli.build_parser is parser_build
    p = cli.build_parser()
    ns = p.parse_args(["status"])
    assert ns.cmd == "status"
    assert "pubmed" in BACKEND_HELP
