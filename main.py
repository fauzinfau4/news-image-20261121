"""Deliver the finished front page to the grader's output folder.

The picture is rendered by draw.py and stored here as entry.png; this
entrypoint only copies those bytes to $MAKEFUN_OUTPUT_DIR (or /output
when the variable is unset). Standard library only: no network, no
clock, no rendering here, so two runs always write identical bytes.
"""

import os
import shutil

from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
FALLBACK = Path("/output")


def target_path():
    """Resolve the destination from the environment, with a fallback."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    folder = Path(raw) if raw else FALLBACK
    return folder / "entry.png"


def main():
    dest = target_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, dest)
    print("Wrote %s (%d bytes)" % (dest, dest.stat().st_size))


main()
