"""Check image-daemon startup and rotation without touching the desktop."""
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

source = (Path(__file__).resolve().parent.parent / 'hypr/random-wallpaper.sh').read_text()
for running in (False, True):
    with TemporaryDirectory() as tmp:
        home = Path(tmp)
        images = home / 'Pictures/wallpapers'
        images.mkdir(parents=True)
        (images / 'test image.png').touch()
        binaries = home / 'bin'
        binaries.mkdir()
        commands = {
            'awww': '''#!/bin/bash
if [[ $1 == query ]]; then test -f "$HOME/ready"; exit; fi
[[ $1 == img && -f $2 ]] || exit 1
printf '%s' "$2" > "$HOME/selected"
''',
            'awww-daemon': '''#!/bin/bash
touch "$HOME/started" "$HOME/ready"
''',
            'sleep': '''#!/bin/bash
if [[ $1 == 600 ]]; then kill -TERM "$PPID"; else /usr/bin/sleep 0.01; fi
''',
        }
        for name, text in commands.items():
            executable = binaries / name
            executable.write_text(text)
            executable.chmod(0o755)
        if running:
            (home / 'ready').touch()
        script = home / 'wallpaper.sh'
        script.write_text(source.replace('/tmp/random-wallpaper.lock', str(home / 'test.lock')))
        result = subprocess.run(['bash', str(script)], timeout=5,
            env={**os.environ, 'HOME': str(home), 'PATH': str(binaries) + ':' + os.environ['PATH']})
        assert result.returncode == -15
        assert (home / 'selected').read_text() == str(images / 'test image.png')
        assert (home / 'started').exists() == (not running)
print('Wallpaper daemon startup, reuse, and image selection checks passed')
