#!/usr/bin/env python3
"""Cutest-picture entry: write the picture to /output/entry.png.

The picture lives beside this program as entry.png (a JPEG image, named
entry.png as the competition requires). This program validates it and
copies it byte-for-byte to the output directory, so both runs of the
program write exactly the same bytes.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def read_dimensions(data: bytes) -> tuple[int, int]:
    """Return (width, height) parsed from PNG or JPEG headers (stdlib only)."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        width, height = struct.unpack(">II", data[16:24])
        return width, height
    if data[:2] == b"\xff\xd8":
        pos = 2
        while pos + 9 < len(data):
            if data[pos] != 0xFF:
                break
            marker = data[pos + 1]
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                pos += 2
                continue
            length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
            if marker in (0xC0, 0xC1, 0xC2):
                height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
                return width, height
            pos += 2 + length
    raise ValueError("not a PNG or JPEG image")


def main() -> int:
    data = SOURCE.read_bytes()
    if len(data) > MAX_BYTES:
        print(f"entry.png is {len(data)} bytes, over the {MAX_BYTES} limit", file=sys.stderr)
        return 1
    width, height = read_dimensions(data)
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"entry.png is {width}x{height}, over the {MAX_SIDE}x{MAX_SIDE} limit", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)
    check = target.read_bytes()
    if hashlib.sha256(check).hexdigest() != hashlib.sha256(data).hexdigest():
        print("written bytes do not match the source", file=sys.stderr)
        return 1
    written_width, written_height = read_dimensions(check)
    if (written_width, written_height) != (width, height):
        print("written image dimensions do not match the source", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(data)} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
