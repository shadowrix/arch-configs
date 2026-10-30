"""Exercise apply and restore against a temporary home, never the desktop."""
from pathlib import Path
from tempfile import TemporaryDirectory
from theme import FILES, SPOTIFY_FILES, run

with TemporaryDirectory() as tmp:
    root, home = Path(tmp) / 'repo', Path(tmp) / 'home'
    root.mkdir()
    home.mkdir()
    mapping = {stored: f'.config/test-{i}' for i, stored in enumerate(FILES)}
    (root / 'files.tsv').write_text(''.join(f'{s}\t{t}\n' for s, t in mapping.items()))
    for stored in FILES:
        src = root / stored
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text('new theme')
    existing = home / mapping[FILES[0]]
    existing.parent.mkdir(parents=True)
    existing.write_text('original live data')
    existing.chmod(0o640)
    run(root, home)
    assert existing.read_text() == 'original live data'
    assert not (root / 'backups').exists()
    run(root, home, apply=True)
    assert all((home / rel).read_text() == 'new theme' for rel in mapping.values())
    backup = next((root / 'backups').iterdir())
    assert backup.stat().st_mode & 0o777 == 0o700
    run(root, home, restore=backup)
    assert existing.read_text() == 'original live data'
    assert existing.stat().st_mode & 0o777 == 0o640
    assert all(not (home / rel).exists() for rel in list(mapping.values())[1:])
    (home / '.config').rename(home / 'real-config')
    (home / '.config').symlink_to(home / 'real-config', target_is_directory=True)
    try:
        run(root, home, apply=True)
    except ValueError:
        pass
    else:
        raise AssertionError('symlink accepted')
print('Theme preview/apply/restore checks passed')

with TemporaryDirectory() as tmp:
    root, home = Path(tmp) / 'repo', Path(tmp) / 'home'
    root.mkdir()
    home.mkdir()
    (root / 'files.tsv').write_text(''.join(f'{s}\t.config/{s}\n' for s in SPOTIFY_FILES))
    for stored in SPOTIFY_FILES:
        src = root / stored
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text('spotify')
    run(root, home, apply=True, files=SPOTIFY_FILES)
    assert all((home / '.config' / s).read_text() == 'spotify' for s in SPOTIFY_FILES)
    backup = next((root / 'backups').iterdir())
    run(root, home, restore=backup, files=SPOTIFY_FILES)
    assert all(not (home / '.config' / s).exists() for s in SPOTIFY_FILES)
print('Spotify-only apply/restore checks passed')

# Backups from before Spotify was added must still restore successfully.
with TemporaryDirectory() as tmp:
    root, home = Path(tmp) / 'repo', Path(tmp) / 'home'
    root.mkdir()
    home.mkdir()
    legacy = tuple(s for s in FILES if s != 'waybar/scripts/spotify.py')
    (root / 'files.tsv').write_text(''.join(f'{s}\t.config/{s}\n' for s in FILES))
    for stored in FILES:
        src = root / stored
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text('theme')
    run(root, home, apply=True, files=legacy)
    run(root, home, restore=next((root / 'backups').iterdir()))
    assert all(not (home / '.config' / s).exists() for s in FILES)
print('Legacy theme backup restore checks passed')
