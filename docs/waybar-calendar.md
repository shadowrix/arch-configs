# Compact year calendar

The existing clock now defaults to Waybar's native year calendar: four month
columns and three rows. Each month includes its year. ISO 8601 makes Monday the
first weekday independently of the system locale. Waybar handles date lengths,
leap years, midnight updates and year changes; there is no calendar helper process.

Only `waybar/config.jsonc` (the clock section) and `waybar/style.css` (a tooltip
surface override) changed. The bar layout, clock display and alternate display,
Spotify, tray and other modules remain intact. The existing `files.tsv` copy
mapping is used; no symlinks or new dependencies were introduced.

## Controls

- Hover: display all twelve months by default.
- Right-click: toggle between year and month views; the selected mode persists
  until toggled again or Waybar reloads.
- Scroll up/down: navigate years in year mode, months in month mode.
- Middle-click: reset navigation to the current date, keeping the selected mode.
- Left-click: retain the existing alternate clock display.

Waybar also resets the navigation offset when the pointer leaves the clock.
The tooltip is native GTK and automatically positions below the top bar.

Installed Waybar 0.15.0 supports `mode`, `mode-mon-col`, `iso8601`, and the
`shift_reset` action. This version does not support `first-day-of-week`; setting
`iso8601: true` provides Monday-first behavior. Native formatting styles the
weekday row as a whole, so separate weekend colors are omitted.

References: [version-matched calendar implementation](https://github.com/Alexays/Waybar/blob/0.15.0/src/modules/clock.cpp)
and [supported clock actions](https://github.com/Alexays/Waybar/blob/0.15.0/include/modules/clock.hpp).

## Appearance and adjustment

The calendar uses JetBrainsMono Nerd Font at 10 points, purple month headings,
blue weekday headers, primary text for dates, and a blue background behind today.
The shared tooltip surface uses Tokyo Glass navy with a `#414868` border and the
existing rounded corners. Menu surfaces retain their prior style.

- Font size: change `10` in the clock's `tooltip-format` font description.
- Tooltip padding: adjust `tooltip label { padding: 6px; }` in `waybar/style.css`.
  This affects other tooltips too. Month gaps and row spacing are native Waybar
  defaults and are not exposed as independent configuration settings.
- Three columns × four rows: set `calendar.mode-mon-col` to `3`.
- Monthly default: set `calendar.mode` to `"month"`; retain the year grid for
  right-click switching.

Apply just the config/CSS through their `files.tsv` destinations after making a
backup, then reload with `pkill -SIGUSR2 -x waybar`. The existing
`python3 scripts/theme.py --spotify --apply` option also copies these two files
plus the unchanged Spotify helper, with backups. Avoid a full-theme apply for a
calendar-only adjustment.

## Validation and rollback

Verified on 2026-10-31: JSON and Pango formatting, live reload, actual popup
screenshots showing all twelve months in the 4×3 grid, Monday-first alignment and
the October 31 highlight. Right-click switched to October; scrolling navigated
to November; middle-click restored October. Year navigation displayed 2027, and
middle-click restored 2026. The final view is the current year. The approximately
745×500 logical-pixel popup fits the 1800×1125 logical desktop (1920×1200 physical,
scale 1.0667). Spotify and the other bar modules remained visible.

Two Waybar child processes dumped core during reload while the original main
bar stayed running. No further Waybar/calendar/markup journal entries appeared
during the interaction checks. The main process writes stderr to `/dev/null`, so
the journal is not a complete rendering log. Leap-year/system-date changes and
other physical monitors were not simulated.

The original monthly config/CSS are backed up in
`backups/year-calendar-20261031-014733/.config/waybar/`. To restore the exact
pre-change appearance while preserving the other work from this session:

```bash
cd ~/Projects/arch-configs
cp backups/year-calendar-20261031-014733/.config/waybar/config.jsonc waybar/config.jsonc
cp backups/year-calendar-20261031-014733/.config/waybar/style.css waybar/style.css
cp waybar/config.jsonc ~/.config/waybar/config.jsonc
cp waybar/style.css ~/.config/waybar/style.css
pkill -SIGUSR2 -x waybar
```

Save any later calendar/CSS edits before restoring these snapshots. No commit or
push was made.
