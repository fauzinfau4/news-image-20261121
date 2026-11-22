# main.py -- entrypoint for news-image-20261121 v3.
# Draws the one-page broadsheet for Saturday 21 November 2026 and writes it
# to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when set).
# NOTE: the grader runs this as `python3 -P -s /bot/main.py`, and the -P
# (safe_path) flag keeps the script's own directory off sys.path, so the
# sibling import of draw.py fails with ModuleNotFoundError unless we put the
# script directory back on sys.path first. That is what the two lines below
# do, before the import. (Local runs without -P never hit this.)
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from draw import build_entry


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    build_entry(path)
    # make.fun collects /output as a different user than the program runs
    # as, so the file must be world-readable whatever the umask is.
    os.chmod(path, 0o644)
    print("wrote", path)


if __name__ == "__main__":
    main()
