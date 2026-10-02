#!/usr/bin/env python3
"""Create a new manuscript directory from the bundled IEEE example; never overwrite."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="New manuscript directory")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    source = root / "assets" / "ieee-conference-2019"
    manifest = json.loads((root / "assets" / "template-sha256.json").read_text())
    mapping = {"conference_101719.tex": "main.tex", "IEEEtran.cls": "IEEEtran.cls", "fig1.png": "fig1.png"}
    # Validate assets before creating any user output.
    for name in mapping:
        file = source / name
        if hashlib.sha256(file.read_bytes()).hexdigest() != manifest[name]:
            parser.error(f"Bundled template checksum mismatch: {name}")
    output = args.output.expanduser().absolute()
    try:
        output.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error(f"Output already exists; nothing overwritten: {output}")
    for old, new in mapping.items():
        shutil.copy2(source / old, output / new)
    (output / "figures").mkdir()
    (output / "validation").mkdir()
    print(f"Created {output}")
    print("main.tex is the template example. Replace all sample content before delivery.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
