#!/usr/bin/env python3
"""news-image-20261126 entrypoint (b170, layout V167).

Copies the pre-rendered entry.png (built at build time by gen.py with
Pillow) into MAKEFUN_OUTPUT_DIR. Standard library only: the grader runs
with no third-party packages installed, so this file imports nothing
outside the standard library.

Behaviour: resolve the repository root from this file's own location,
read entry.png next to it, and write the exact same bytes to
<MAKEFUN_OUTPUT_DIR>/entry.png (default: ./out/entry.png). The copy is
a plain direct copy (shutil.copyfile) and the destination is chmodded
to 0644 afterwards, so any user on the grading machine can read it.
The result is verified by re-reading the destination and comparing
its length and sha256 with the source before exiting 0. The program
is deterministic: it performs no network access, reads no clock and
writes no timestamps, so two runs in a row produce byte-identical
output.
"""
import hashlib
import os
import shutil
import sys

ENTRY_NAME = "entry.png"


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return here


def _output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not os.path.isabs(out_dir):
        out_dir = os.path.abspath(out_dir)
    return os.path.join(out_dir, ENTRY_NAME)


def main(argv=None):
    root = _repo_root()
    source = os.path.join(root, ENTRY_NAME)
    if not os.path.isfile(source):
        print(f"error: {ENTRY_NAME} not found next to main.py ({root})",
              file=sys.stderr)
        return 1
    dest = _output_path()
    expected = _sha256(source)
    expected_size = os.path.getsize(source)
    if os.path.abspath(source) == os.path.abspath(dest):
        print(f"ok: {dest} is already the entry "
              f"({expected_size} bytes, sha256 {expected})")
        return 0
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    print(f"copying {source} ({expected_size} bytes, sha256 {expected})")
    print(f"     -> {dest}")
    # Direct copy, no temp file: the V166 temp-file-plus-rename path
    # produced a mode-0600 output that the scorer could not read
    # (run_completes failed). A plain copy plus an explicit chmod
    # 0644 keeps the output readable by every user.
    shutil.copyfile(source, dest)
    os.chmod(dest, 0o644)
    got = _sha256(dest)
    got_size = os.path.getsize(dest)
    if got != expected or got_size != expected_size:
        print(f"error: verify failed: {dest} is {got_size} bytes, "
              f"sha256 {got}, expected {expected_size} bytes, sha256 "
              f"{expected}", file=sys.stderr)
        return 1
    print(f"ok: {dest} ({got_size} bytes, sha256 {got})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
