#!/usr/bin/env python3
"""Preview/apply Tokyo Glass Dev using files.tsv, or restore an apply backup."""
import argparse
import json
from pathlib import Path
import shutil
from datetime import datetime

# Assets first; Hyprland last because it watches its configuration for changes.
FILES = (
    'home/.local/share/rofi/themes/tokyo-glass-dev.rasi',
    'home/.config/mako/config',
    'home/.config/ghostty/config.ghostty',
    'home/.config/rofi/config.rasi',
    'waybar/style.css',
    'waybar/config.jsonc',
    'hypr/hyprlock.conf',
    'hypr/hyprland.lua',
)


def safe_path(base, relative):
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or '..' in parts:
        raise ValueError(f'Unsafe path: {relative}')
    for i in range(1, len(parts) + 1):
        if (base / Path(*parts[:i])).is_symlink():
            raise ValueError(f'Review symlink first: {relative}')
    path = base / relative
    if path.exists() and not path.is_file():
        raise ValueError(f'Expected a file: {relative}')
    return path


def run(root, home, apply=False, restore=None):
    mapping = dict(line.split('\t') for line in (root / 'files.tsv').read_text().splitlines())
    targets = {stored: mapping[stored] for stored in FILES}
    if restore:
        backup = Path(restore).resolve()
        originals = json.loads((backup / 'originals.json').read_text())
        if set(originals) != set(targets.values()) or any(type(v) is not bool for v in originals.values()):
            raise ValueError('Backup does not match this theme manifest')
        # Check every path before changing anything.
        for rel, existed in originals.items():
            safe_path(home, rel)
            if existed and not safe_path(backup, rel).is_file():
                raise ValueError(f'Missing backup: {rel}')
        for rel, existed in originals.items():
            dst = home / rel
            if existed:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup / rel, dst)
            elif dst.exists():
                dst.unlink()
        print(f'Restored live files from {backup}')
        return
    for stored, rel in targets.items():
        if not safe_path(root, stored).is_file():
            raise ValueError(f'Missing source: {stored}')
        dst = safe_path(home, rel)
        print(f'{"Apply" if apply else "Preview"}: {stored} -> ~/{rel}'
              f' ({"replace" if dst.exists() else "new"})')
    if not apply:
        return
    backup = root / 'backups' / ('tokyo-live-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    backup.mkdir(parents=True, mode=0o700)
    originals = {}
    # Finish every backup before overwriting any live file.
    for rel in targets.values():
        src = home / rel
        originals[rel] = src.exists()
        if src.exists():
            dst = backup / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    (backup / 'originals.json').write_text(json.dumps(originals, indent=2) + '\n')
    print(f'Backup: {backup}', flush=True)
    for stored, rel in targets.items():
        dst = home / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / stored, dst)
    print('Files applied. Reload applications as documented; no processes were restarted.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--apply', action='store_true')
    group.add_argument('--restore', type=Path, metavar='BACKUP')
    args = parser.parse_args()
    try:
        run(Path(__file__).resolve().parent.parent, Path.home(), args.apply, args.restore)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'{exc}\n')
