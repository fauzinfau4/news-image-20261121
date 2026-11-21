"""Entrypoint: copy the front-page image to the output directory.

Standard library only. The image is drawn by draw.py and shipped in this
repository as entry.png; this program only copies those exact bytes, so
two runs always write identical output.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(out_dir, "entry.png"))
    print("wrote entry.png to", out_dir)


if __name__ == "__main__":
    main()
