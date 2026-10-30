#!/usr/bin/env python3
"""Event-driven Spotify labels for Waybar; only the title animates."""
import argparse
import html
import json
import signal
import sys
import time

import gi
gi.require_version('Playerctl', '2.0')
from gi.repository import GLib, GLibUnix, Playerctl

WIDTH = 22                 # Text cells; also adjust Waybar min/max-length (WIDTH + 2).
STEP_MS = 250              # One character every 250 ms, without metadata polling.
HOLD_SECONDS = 2
GRAPHEMES = GLib.Regex.new(r'(\X)', 0, 0)


def cells(text):
    # PCRE's Unicode graphemes keep combining accents and emoji sequences together.
    return [(part, 2 if any(GLib.unichar_iswide(c) for c in part) else 1)
            for part in GRAPHEMES.split(text, 0)[1::2]]


class Marquee:
    def __init__(self, text, width=WIDTH):
        self.parts = cells(text)
        self.width = width
        self.long = sum(size for _, size in self.parts) > width
        self.offset = 0
        self.resume_at = time.monotonic() + HOLD_SECONDS

    def frame(self):
        result, used = '', 0
        for part, size in self.parts[self.offset:]:
            if used + size > self.width:
                break
            result += part
            used += size
        return result + ' ' * (self.width - used)

    def advance(self):
        if time.monotonic() < self.resume_at:
            return
        remaining = sum(size for _, size in self.parts[self.offset:])
        if remaining <= self.width:
            self.offset = 0
            self.resume_at = time.monotonic() + HOLD_SECONDS
        else:
            self.offset += 1
            if sum(size for _, size in self.parts[self.offset:]) <= self.width:
                self.resume_at = time.monotonic() + HOLD_SECONDS


def track(metadata):
    artist = metadata.get('xesam:artist', [])
    if isinstance(artist, (list, tuple)):
        artist = ', '.join(artist)
    title = metadata.get('xesam:title', '')
    return ' '.join(' — '.join(str(s) for s in (artist, title) if s).split()) or 'Spotify'


def spotify_names(manager):
    # Browser MPRIS names cannot reliably identify a Spotify tab. Never select them.
    return sorted((n for n in manager.props.player_names if n.name == 'spotify'),
                  key=lambda n: n.instance)


class Widget:
    def __init__(self, mode):
        self.mode = mode
        self.player = None
        self.timer = None
        self.last = None
        self.marquee = Marquee('Spotify offline')
        self.full = 'Spotify offline'
        self.status = 'inactive'
        self.manager = Playerctl.PlayerManager()
        self.manager.connect('name-appeared', self.appeared)
        self.manager.connect('player-vanished', self.vanished)
        self.attach()

    def attach(self):
        if self.player is not None:
            return
        for name in spotify_names(self.manager):
            try:
                self.player = Playerctl.Player.new_from_name(name)
                self.player.connect('metadata', self.changed)
                self.player.connect('playback-status', self.changed)
                self.manager.manage_player(self.player)
                break
            except GLib.Error:
                self.player = None  # The application may exit during discovery.
        self.changed()

    def appeared(self, manager, name):
        if name.name == 'spotify':
            self.attach()

    def vanished(self, manager, player):
        if player == self.player:
            self.player = None
            self.attach()

    def changed(self, *_):
        if self.timer:
            GLib.source_remove(self.timer)
            self.timer = None
        self.status, self.full = 'inactive', 'Spotify offline'
        if self.player is not None:
            try:
                self.status = self.player.props.playback_status.value_nick.lower()
                self.full = track(self.player.props.metadata.unpack())
                if self.status == 'stopped':
                    self.full = 'Spotify · stopped'
            except GLib.Error:
                pass
        self.marquee = Marquee(self.full)
        self.emit()
        if self.mode == 'title' and self.marquee.long:
            self.timer = GLib.timeout_add(STEP_MS, self.tick)

    def tick(self):
        self.marquee.advance()
        self.emit()
        return GLib.SOURCE_CONTINUE

    def emit(self):
        icons = {'previous': '󰒮', 'toggle': '󰏤' if self.status == 'playing' else '󰐊',
                 'next': '󰒭'}
        text = self.marquee.frame() if self.mode == 'title' else icons[self.mode]
        tooltip = self.full + '\n' + self.status.capitalize()
        if self.mode != 'title':
            tooltip += '\n' + {'previous': 'Previous track', 'toggle': 'Play / pause',
                               'next': 'Next track'}[self.mode]
        data = json.dumps({'text': html.escape(text), 'tooltip': html.escape(tooltip),
                           'class': self.status}, ensure_ascii=False)
        if data != self.last:
            print(data, flush=True)
            self.last = data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['title', 'previous', 'toggle', 'next'])
    parser.add_argument('--action', action='store_true')
    args = parser.parse_args()
    if args.action:
        names = spotify_names(Playerctl.PlayerManager())
        if names and args.mode != 'title':
            player = Playerctl.Player.new_from_name(names[0])
            getattr(player, {'toggle': 'play_pause', 'previous': 'previous', 'next': 'next'}[args.mode])()
        return
    loop = GLib.MainLoop()
    GLibUnix.signal_add(GLib.PRIORITY_DEFAULT, signal.SIGTERM, loop.quit)
    widget = Widget(args.mode)
    loop.run()


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
    except (GLib.Error, KeyboardInterrupt) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
