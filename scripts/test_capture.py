import tempfile
from pathlib import Path
from capture import sync

with tempfile.TemporaryDirectory() as tmp:
    root, home = Path(tmp) / 'repo', Path(tmp) / 'home'
    root.mkdir()
    home.mkdir()
    (root / 'files.tsv').write_text('home/settings.json\tsettings.json\n')
    source = home / 'settings.json'
    source.write_text('{\n "cSpell.userWords": ["personal"],\n "editor.fontSize": 16\n}\n')
    source.chmod(0o640)
    assert sync(root, home)
    assert not (root / 'home').exists()
    assert sync(root, home, True)
    saved = root / 'home/settings.json'
    assert b'personal' not in saved.read_bytes()
    assert b'editor.fontSize' in saved.read_bytes()
    assert saved.stat().st_mode & 0o777 == 0o640
    assert not sync(root, home)
    saved.unlink()
    saved.symlink_to(source)
    try:
        sync(root, home, True)
    except ValueError:
        pass
    else:
        raise AssertionError('symlink accepted')
    (root / 'files.tsv').write_text('../escape\tsettings.json\n')
    try:
        sync(root, home, True)
    except ValueError:
        pass
    else:
        raise AssertionError('path traversal accepted')
print('capture checks passed')
