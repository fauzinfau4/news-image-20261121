# main.py -- entrypoint for news-image-20261121 v3.
# Draws the one-page broadsheet for Saturday 21 November 2026 and writes it
# to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when set).
import os

from draw import build_entry


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    build_entry(path)
    print("wrote", path)


if __name__ == "__main__":
    main()
