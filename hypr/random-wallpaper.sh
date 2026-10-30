#!/usr/bin/env bash
LOCKFILE="/tmp/random-wallpaper.lock"

exec 9>"$LOCKFILE"
flock -n 9 || exit 0

WALLPAPER_DIR="$HOME/Pictures/wallpapers"

if ! awww query >/dev/null 2>&1; then
    # The daemon must not inherit the rotation script's lock.
    awww-daemon 9>&- &
    for ((attempt = 0; attempt < 50; attempt++)); do
        awww query >/dev/null 2>&1 && break
        sleep 0.1
    done
    awww query >/dev/null 2>&1 || exit 1
fi

while true; do
    WALL=$(find "$WALLPAPER_DIR" -type f | grep -Ei '\.(jpg|jpeg|png|webp)$' | shuf -n1)
    [ -n "$WALL" ] && awww img "$WALL"
    sleep 600
done
