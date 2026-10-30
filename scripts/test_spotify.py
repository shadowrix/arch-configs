"""Run with python3 scripts/test_spotify.py; private D-Bus never touches real players."""
import importlib.util
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parent.parent
HELPER = ROOT / 'waybar/scripts/spotify.py'


def service():
    from gi.repository import Gio, GLib
    path = '/org/mpris/MediaPlayer2'
    interface = 'org.mpris.MediaPlayer2.Player'
    props = {'PlaybackStatus': GLib.Variant('s', 'Paused'),
             'Metadata': GLib.Variant('a{sv}', {'xesam:title': GLib.Variant('s', 'Short')}),
             **{name: GLib.Variant('b', True) for name in
                ['CanControl', 'CanPlay', 'CanPause', 'CanGoNext', 'CanGoPrevious', 'CanSeek']}}
    xml = '<node><interface name="' + interface + '">' + ''.join(
        f'<property name="{key}" type="{value.get_type_string()}" access="read"/>'
        for key, value in props.items()) + ''.join(
        f'<method name="{name}"/>' for name in ['PlayPause', 'Next', 'Previous']) + '</interface></node>'
    info = Gio.DBusNodeInfo.new_for_xml(xml).interfaces[0]

    def connect(name):
        bus = Gio.DBusConnection.new_for_address_sync(os.environ['DBUS_SESSION_BUS_ADDRESS'],
            Gio.DBusConnectionFlags.AUTHENTICATION_CLIENT | Gio.DBusConnectionFlags.MESSAGE_BUS_CONNECTION,
            None, None)
        bus.call_sync('org.freedesktop.DBus', '/org/freedesktop/DBus',
            'org.freedesktop.DBus', 'RequestName', GLib.Variant('(su)', (name, 0)), None,
            Gio.DBusCallFlags.NONE, -1, None)
        return bus

    def method(bus, sender, obj, iface, name, parameters, invocation):
        print(json.dumps({'action': name, 'browser': bus == browser}), flush=True)
        if name == 'PlayPause':
            props['PlaybackStatus'] = GLib.Variant('s',
                'Playing' if props['PlaybackStatus'].unpack() != 'Playing' else 'Paused')
            changed({'PlaybackStatus': props['PlaybackStatus']})
        invocation.return_value(None)

    def register(bus):
        bus.register_object(path, info, method, lambda *args: props[args[-1]], None)

    def changed(values):
        spotify.emit_signal(None, path, 'org.freedesktop.DBus.Properties', 'PropertiesChanged',
                            GLib.Variant('(sa{sv}as)', (interface, values, [])))

    browser = connect('org.mpris.MediaPlayer2.chromium.instance123')
    register(browser)
    spotify = None

    def command(*_):
        nonlocal spotify
        line = sys.stdin.readline()
        if not line:
            return False
        data = json.loads(line)
        if data['cmd'] == 'open':
            spotify = connect('org.mpris.MediaPlayer2.spotify.instance456')
            register(spotify)
        elif data['cmd'] == 'close':
            spotify.close_sync(None)
            spotify = None
        elif data['cmd'] == 'metadata':
            props['Metadata'] = GLib.Variant('a{sv}', {
                key: GLib.Variant('as' if isinstance(value, list) else 's', value)
                for key, value in data['value'].items()})
            changed({'Metadata': props['Metadata']})
        print(json.dumps({'ack': data['cmd']}), flush=True)
        return True

    GLib.io_add_watch(sys.stdin, GLib.IO_IN, command)
    print(json.dumps({'ready': True}), flush=True)
    GLib.MainLoop().run()


class Stream:
    def __init__(self, args):
        self.proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     text=True, bufsize=1)
        self.lines = queue.Queue()
        self.history = []
        def read():
            for line in self.proc.stdout:
                item = json.loads(line)
                self.history.append(item)
                self.lines.put(item)
        threading.Thread(target=read, daemon=True).start()

    def wait(self, predicate, timeout=5):
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            item = self.lines.get(timeout=max(.01, end - time.monotonic()))
            if predicate(item):
                return item
        raise AssertionError('No expected update')

    def command(self, cmd, **data):
        self.proc.stdin.write(json.dumps({'cmd': cmd, **data}) + '\n')
        self.proc.stdin.flush()
        self.wait(lambda item: item.get('ack') == cmd)

    def close(self):
        self.proc.terminate()
        try:
            self.proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()


def tests():
    spec = importlib.util.spec_from_file_location('spotify', HELPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.cells('é👩‍💻中文') == [('é', 1), ('👩‍💻', 2), ('中', 2), ('文', 2)]
    short = module.Marquee('Short')
    assert not short.long and short.frame() == 'Short'.ljust(module.WIDTH)
    long = module.Marquee('a' * 40)
    assert long.long and len(long.frame()) == module.WIDTH
    long.advance()
    assert long.offset == 0
    for _ in range(18):
        long.resume_at = 0
        long.advance()
    assert long.offset == 18
    assert long.resume_at > time.monotonic()
    long.resume_at = 0
    long.advance()
    assert long.offset == 0
    assert module.track({}) == 'Spotify'
    assert module.track({'xesam:artist': ['A', 'B'], 'xesam:title': '<歌 & "曲">'}) == 'A, B — <歌 & "曲">'
    streams = []
    try:
        server = Stream([sys.executable, __file__, '--service'])
        streams.append(server)
        server.wait(lambda item: item.get('ready'))
        title = Stream([sys.executable, str(HELPER), 'title'])
        toggle = Stream([sys.executable, str(HELPER), 'toggle'])
        streams.extend([title, toggle])
        title.wait(lambda item: item['class'] == 'inactive')
        toggle.wait(lambda item: item['class'] == 'inactive')
        # A browser alone must never become the selected player or receive controls.
        subprocess.run([sys.executable, str(HELPER), 'next', '--action'], check=True)
        server.command('open')
        assert not any('action' in item for item in server.history), 'Offline controls reached a browser'
        title.wait(lambda item: item['class'] == 'paused' and item['text'].strip() == 'Short')
        play = toggle.wait(lambda item: item['class'] == 'paused')['text']
        time.sleep(.5)
        assert title.lines.empty(), 'Short titles must not animate'
        for action, method in [('toggle', 'PlayPause'), ('previous', 'Previous'), ('next', 'Next')]:
            subprocess.run([sys.executable, str(HELPER), action, '--action'], check=True)
            server.wait(lambda item: item.get('action') == method and not item['browser'])
        assert toggle.wait(lambda item: item['class'] == 'playing')['text'] != play
        server.command('metadata', value={'xesam:artist': ['宇多田 & A'],
                       'xesam:title': 'é👩‍💻 <歌> ' + '長いタイトル' * 8})
        update = title.wait(lambda item: '&lt;歌&gt;' in item['tooltip'])
        assert '&amp;' in update['tooltip']
        title.wait(lambda item: item['text'] != update['text'])
        server.command('metadata', value={})
        title.wait(lambda item: item['text'].strip() == 'Spotify')
        server.command('close')
        title.wait(lambda item: item['class'] == 'inactive' and 'offline' in item['text'])
        toggle.wait(lambda item: item['class'] == 'inactive')
        server.command('open')
        title.wait(lambda item: item['class'] == 'playing')
        assert all(not item['browser'] for item in server.history if 'action' in item)
        print('Spotify marquee, Unicode, controls, browser isolation, close/restart checks passed')
    finally:
        for stream in reversed(streams):
            stream.close()


if __name__ == '__main__':
    if '--service' in sys.argv:
        service()
    elif '--private-bus' in sys.argv:
        tests()
    else:
        subprocess.run(['dbus-run-session', '--', sys.executable, __file__, '--private-bus'], check=True)
