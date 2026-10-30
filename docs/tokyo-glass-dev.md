# Tokyo Glass Dev

A restrained Tokyo Night desktop: navy glass islands, blue/violet workspace pills and borders, opaque focused windows and translucent inactive windows, and a lightly translucent terminal. This design uses existing applications and the existing `files.tsv` copy workflow. No shell/prompt, monitor, input, binding, application command, wallpaper or VPN script changes are included.

## Components and changed files

| File | Design |
| --- | --- |
| `waybar/config.jsonc` | 38px bar, 10px top/14px side margins, fixed center clock, compact time/date toggle, per-output workspaces and a tray. Existing modules/actions retained. Calendar colors harmonized; removed duplicate scroll actions already overridden in the old JSONC. |
| `waybar/style.css` | Three independent 88% opaque navy surfaces, 16px rounding, blue-tinted outlines, small shadows, blue/violet workspace pills, 150ms hover transitions, quiet system indicators and matching tooltips/menus. Transparent space surrounds the islands. |
| `hypr/hyprland.lua` | Gaps 7/14, rounding 14, 2px blue/violet gradient border, muted inactive border, soft dark shadow. Focused windows stay opaque; inactive windows use 80% opacity. One blur pass, short ease-out animations with only 96–98% window pop-in, and alpha-masked Waybar/Rofi/Mako layer blur. Existing hardware/input/layout/startup/bindings remain unchanged. |
| `hypr/hyprlock.conf` | Tokyo text, blue outline, purple checking/pink failure accents, rounded field, JetBrainsMono font and one screenshot blur pass. Existing lock command, monitor coverage and authentication behavior remain unchanged. |
| `home/.config/ghostty/config.ghostty` | Installed `TokyoNight Night` theme, 94% background opacity, violet block cursor, navy background, legible selection and 14px/12px padding. Existing font size 14 and cursor behavior retained. This filename is the installed Ghostty version's documented default. |
| `home/.config/rofi/config.rasi` | Existing launcher configuration now references the new theme and installed Adwaita icon theme. Existing drun/run commands, bindings, timeout and file-browser options retained. |
| `home/.local/share/rofi/themes/tokyo-glass-dev.rasi` | Centered 36%-width dialog, 16px corners, dark translucent surface, inset search field, eight balanced list rows, blue text/violet selection edge. Previous spotlight themes remain available. |
| `home/.config/mako/config` | Installed Mako receives matching rounded navy notifications, blue borders and pink critical accents. Default actions, expiration, history, sorting and daemon activation remain unchanged. Mako has no native notification-center widget, so no polling module or replacement daemon was added. |

`files.tsv` includes the new Rofi theme and Mako config. `scripts/theme.py` previews/applies these nine files (including the [Spotify helper](spotify-waybar.md)) and restores its backups; `scripts/test_theme.py` exercises it against a temporary home. README and this guide document the workflow.

## Apply from the repository

This implementation environment allows writes only in the repository and `/tmp`, and cannot access the live compositor or session bus. Live files were backed up for inspection, but **the redesign has not been applied to the running desktop**. Run these commands from your normal terminal:

```bash
cd ~/Projects/arch-configs
python scripts/theme.py                         # preview exactly nine targets
python scripts/test_theme.py                    # temporary-home self-check
Hyprland --verify-config --config "$PWD/hypr/hyprland.lua"
ghostty +validate-config --config-file="$PWD/home/.config/ghostty/config.ghostty"
python scripts/theme.py --apply
```

The helper refuses symlinked targets/parents, backs up every existing destination under private `backups/tokyo-live-<timestamp>/` before overwriting any file, and records newly created files for rollback. This directory is Git-ignored. Keep its printed full path. If copying fails after backup, restore using that path before retrying. No processes are killed or started by the helper. Hyprland can automatically reload when its config is copied; it is copied last, after all other files and assets.

The separate `backups/tokyo-glass-before/` directory contains the repository and live theme files inspected before editing, along with original live hashes. It is a local safety copy, not a portable Git artifact. The apply helper creates its own full backup at apply time, including a record of absent files; only those `tokyo-live-*` backups are accepted by its restore workflow.

Before applying, review any live edits made since inspection. Applying replaces the nine target files with repository versions; it leaves unrelated files alone. In particular, the VPN scripts are not part of this theme and their previously pending rename is unaffected.

## Reload and check the running session

After applying, run from your normal graphical session:

```bash
hyprctl reload
hyprctl configerrors
pkill -SIGUSR2 -x waybar    # reload existing Waybar instances; does not start a second bar
# Only if Mako is already your active notification daemon:
makoctl reload
```

Rofi reads the new theme at its next launch. In Ghostty, use its existing default `Ctrl+Shift+,` reload binding; new windows also read the config. Do not launch another notification daemon over an existing service. Mako will use its config the next time its existing activation mechanism starts it. The lock design is read at the next lock; do not test authentication by terminating your current session.

For error logs, inspect your existing launch/service logs. If these apps are systemd user services, use `journalctl --user -b -u waybar -u mako --no-pager -n 80`; unmanaged processes may log elsewhere. Do not publish logs without reviewing them. `hyprctl configerrors` should report no configuration errors.

Inspect the laptop and every external display for centered clock placement, workspace highlighting, tray icons, clipping, launcher sizing, notification text and legibility over wallpapers. No output selector restricts Waybar to one monitor; workspaces are shown per output. Fixed-center keeps the clock at monitor center when space permits; very narrow displays, many tray icons or a long alternate date can still force Waybar to reflow. This requires a live check.

## Customize and keep the repository authoritative

Palette: background `#1a1b26`, surfaces `#24283b`/`#292e42`, muted border `#414868`, text `#c0caf5`/`#a9b1d6`, blue `#7aa2f7`, violet `#bb9af7`, cyan `#7dcfff`, green `#9ece6a`, pink `#f7768e` reserved for urgency/failure. Colors stay in each application's native file rather than a generator.

Change Waybar's spacing/opacity in CSS, the terminal opacity/padding in Ghostty, and window effects in Hyprland's existing look-and-feel section. Keep background-alpha cutoffs on layer blur rules so fully transparent regions do not become full-width blurred strips. Rofi uses installed Adwaita application icons; Waybar and notification text use the existing installed JetBrainsMono Nerd Font. No font or package installation is required.

Wallpaper startup uses the awww random-image script with `~/Pictures/wallpapers`, switching every ten minutes. The script starts the image daemon when needed. Video wallpaper startup is disabled; source videos and their extracted PNG stills are preserved.

If editing live files normally, **apply this design before capturing**, otherwise capture would overwrite the repository redesign with the old live settings. Then:

```bash
python scripts/capture.py
# Inspect differences and changed live files for secrets before capture.
python scripts/capture.py --capture
git diff --check
git diff
```

Capture includes all managed files, including the VPN scripts, so review any unrelated pending differences before `--capture`. To synchronize after your explicit approval:

```bash
git status --short --branch
git remote -v
git add -- README.md docs/tokyo-glass-dev.md docs/inventory.md files.tsv hypr/hyprland.lua hypr/hyprlock.conf waybar/config.jsonc waybar/style.css home/.config/ghostty/config.ghostty home/.config/rofi/config.rasi home/.config/mako/config home/.local/share/rofi/themes/tokyo-glass-dev.rasi scripts/theme.py scripts/test_theme.py
git diff --cached --check
git diff --cached
git commit -m "Add Tokyo Glass Dev desktop design"
git push -u origin main
```

No remote was configured when this redesign began. If still empty, first add the URL of your intended existing repository with `git remote add origin <YOUR_EXISTING_REPOSITORY_URL>`. Do not replace an existing remote or force push if histories diverge.

## Exact rollback

Restore the pre-apply live files using the backup path printed by the helper (substitute the actual timestamp):

```bash
cd ~/Projects/arch-configs
python scripts/theme.py --restore backups/tokyo-live-YYYYMMDD-HHMMSS-ffffff
hyprctl reload
hyprctl configerrors
pkill -SIGUSR2 -x waybar
# If Mako is active:
makoctl reload
```

Reload Ghostty as above. Restore puts back old contents/modes and removes only files that this apply created where none existed before. It does not stop a daemon or remove directories. Back up any new edits you want to keep before restoring.

For repository rollback, the design started from clean commit `61137f0`. Save any later work first. These exact commands restore the previously tracked theme files and the original capture mapping:

```bash
git restore --source=61137f0 -- README.md files.tsv hypr/hyprland.lua hypr/hyprlock.conf waybar/config.jsonc waybar/style.css home/.config/ghostty/config.ghostty home/.config/rofi/config.rasi
```

The new theme/helper/guide files can remain unused; the restored mapping and launcher no longer reference them. Once this design is committed, prefer `git revert <theme-commit>` to preserve shared history. A Git rollback does not itself restore live files.

## Validation and limitations

- Verified installed versions: Hyprland `0.56.2-4`, Waybar `0.15.0-3`, Ghostty `1.3.1-2`, Rofi `2.0.0-1`, Mako `1.11.0-1`. JetBrainsMono Nerd Font, Adwaita icons and the Ghostty theme are installed.
- Hyprland's real `--verify-config` reports `config ok`; Lua syntax passes. Layer-rule fields were checked against `/usr/share/hypr/stubs/hl.meta.lua`.
- Ghostty's actual validator accepts the config; a deliberately unknown option was rejected in a temporary file, confirming the validation path is effective.
- Waybar JSONC parses; original modules and their settings/actions are preserved except for the requested clock appearance and new tray. Duplicate old scroll actions were resolved to the values the parser already used. GTK 3's CSS provider reports no errors. Runtime Waybar validation was blocked by unavailable display access.
- Rofi parses the RASI theme and configuration with no errors. Its theme path was temporarily resolved to the repository asset for validation; the stored path points to the installed destination.
- Mako options were checked against installed `mako(5)`; daemon startup was blocked by unavailable session-bus access, so runtime notification validation remains pending. Hyprlock styling was not tested by locking the session.
- Temporary-home tests cover preview without writes, backup-before-apply, restoration of contents/modes, removal of newly created targets and symlink refusal. Live pre-edit file hashes remain unchanged.
- Functional Hyprland sections before/after visual settings are identical to the original commit, including monitor, input, workspace bindings, autostart and app commands. Shell files and custom scripts are unchanged.
- No live apply, reload, screenshot, graphical alignment/contrast check, multi-monitor test or performance measurement was possible. The design's visual acceptance criteria remain pending a real session check.
- Online documentation lookup was blocked; installed binaries, version-matched stubs and local manuals were used. No package install, sudo, wallpaper replacement, session termination, commit or push occurred.
