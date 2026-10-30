#!/usr/bin/env python3
"""Compare reviewed files with HOME; copy into the repository only with --capture."""
import argparse
from pathlib import Path
import re
import shutil
import sys


def content(path):
    data = path.read_bytes()
    if path.name == 'settings.json':
        # Keep personal spelling dictionaries out of the public backup.
        data = re.sub(rb'(?m)^\s*"cSpell\.userWords":\s*\[[\s\S]*?\],?\s*\n', b'', data)
    return data


def sync(root, home, capture=False):
    entries = [line.split('\t') for line in (root / 'files.tsv').read_text().splitlines()]
    pending = []
    for stored, live in entries:
        src, dst = home / live, root / stored
        for base, rel in [(home, live), (root, stored)]:
            path = Path(rel)
            if path.is_absolute() or '..' in path.parts:
                raise ValueError(f'Unsafe manifest path: {rel}')
            if any((base / Path(*path.parts[:i])).is_symlink() for i in range(1, len(path.parts) + 1)):
                raise ValueError(f'Review symlink before capture: {rel}')
        if not src.is_file():
            raise ValueError(f'Missing live file: {live}')
        data = content(src)
        if not dst.exists() or dst.read_bytes() != data or (dst.stat().st_mode & 0o777) != (src.stat().st_mode & 0o777):
            pending.append((src, dst, data))
    for src, dst, data in pending:
        print(f'{"Capture" if capture else "Different"}: {dst.relative_to(root)}')
        if capture:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
            shutil.copymode(src, dst)
    return bool(pending)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture', action='store_true', help='overwrite repository copies after reviewing live files for secrets')
    args = parser.parse_args()
    try:
        changed = sync(Path(__file__).resolve().parent.parent, Path.home(), args.capture)
    except (OSError, ValueError) as exc:
        sys.exit(str(exc))
    sys.exit(1 if changed and not args.capture else 0)
