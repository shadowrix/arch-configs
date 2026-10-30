LOCKFILE="/tmp/random-wallpaper.lock"

exec 9>"$LOCKFILE"
flock -n 9 || exit 0

WALLPAPER_DIR="$HOME/Pictures/desctop_backgrounds"

while true; do
    WALL=$(find "$WALLPAPER_DIR" -type f | grep -Ei '\.(jpg|jpeg|png|webp)$' | shuf -n1)
    [ -n "$WALL" ] && awww img "$WALL"
    sleep 600
done
