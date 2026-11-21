#!/usr/bin/env python3
"""Entry program: copy the pre-rendered front page to the output directory.

Standard library only. The image bytes are copied unchanged, so two runs
write byte-identical files.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUT / "entry.png")


if __name__ == "__main__":
    main()
