#!/usr/bin/env python3
"""news-image-20261126 entrypoint (b170, layout V166).

Copies the pre-rendered entry.png (built at build time by gen.py with
Pillow) into MAKEFUN_OUTPUT_DIR. Standard library only: the grader runs
with no third-party packages installed, so this file must not import
PIL, numpy or anything outside the standard library.

Behaviour: resolve the repository root from this file's own location,
read entry.png next to it, and write the exact same bytes to
<MAKEFUN_OUTPUT_DIR>/entry.png (default: ./out/entry.png). The write
is atomic-ish (temp file + rename) and the result is verified by
re-reading the destination and comparing its length and sha256 with
the source before exiting 0. The program is deterministic: it performs
no network access, reads no clock and writes no timestamps, so two
runs in a row produce byte-identical output.
"""
import hashlib
import os
import shutil
import sys
import tempfile

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
    if os.path.abspath(source) == os.path.abspath(dest):
        print(f"ok: {dest} is already the entry "
              f"({expected_size} bytes, sha256 {expected})")
        return 0
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    expected = _sha256(source)
    expected_size = os.path.getsize(source)
    print(f"copying {source} ({expected_size} bytes, sha256 {expected})")
    print(f"     -> {dest}")
    fd, tmp = tempfile.mkstemp(prefix=".entry-", dir=os.path.dirname(dest))
    try:
        with os.fdopen(fd, "wb") as out_handle:
            with open(source, "rb") as in_handle:
                shutil.copyfileobj(in_handle, out_handle, 1024 * 1024)
        os.replace(tmp, dest)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
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
