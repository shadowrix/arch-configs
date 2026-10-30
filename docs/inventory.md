# Initial inspection and backup inventory

This records the initial backup. For the subsequent desktop redesign, current Git accessibility, new managed files and pending live apply, see [Tokyo Glass Dev](tokyo-glass-dev.md).

Inspected 2026-10-30. Home: `/home/shadowrix`; source: `~/Projects/arch-configs`.

## Existing repository and management

The starting tree contained only six files under `hypr/` and five under `waybar/`, plus restricted metadata directories. No README, setup script, ignore file, dotfiles manager metadata or configuration symlinks were found in those folders. All eleven files matched their live counterparts; none were overwritten. `.git` appeared empty/read-only, so Git did not recognize the directory as a repository. This may reflect the execution environment's restricted metadata view; it does not establish that the original repository/history is absent. Recover its visibility in your normal shell; do not initialize or replace it. Existing tracked files and uncommitted work could not be identified.

Chezmoi is absent from PATH. No chezmoi configuration or alternate repository was created. The explicit mapping is the current management method; chezmoi source-directory setup and diff validation are therefore not applicable. There was no installed version whose configuration procedure could be verified.

## Discovered customizations

| Area | Findings |
| --- | --- |
| Shell | Login shell `/usr/bin/bash`; interactive process is Bash. `.bash_profile` sources `.bashrc`; color aliases for ls/grep, fallback PS1, Starship initialization, local-bin PATH, NVM loading and Bash completion. No custom Bash functions; Zellij auto-start is commented out. `.bash_aliases`, `.profile`, `.zshrc`, `.zprofile` absent. |
| Desktop | Hyprland Lua and legacy stub configuration, monitor, input, gestures, workspace/window bindings, application launch shortcuts, startup programs, screenshot binding, awww random wallpaper script, hypridle and hyprlock. |
| Bar | Waybar workspace/submap, clock/calendar, audio, language, Bluetooth, VPN, network, CPU, RAM and battery modules; CSS, reload loop and VPN status/toggle scripts. |
| Launcher | Rofi configuration plus spotlight light/dark themes attributed to Newman Sanchez. Dark theme referenced by absolute path. |
| Terminals | Ghostty Catppuccin Mocha, green block cursor, JetBrainsMono Nerd Font, size 14. Kitty installed but its config directory contains no files. Zellij custom bindings/default locked mode. |
| Editors | VS Code and Cursor settings, keybindings and installed extension IDs; Ayu Mirage Bordered, Material Icon Theme, language formatters, terminal profiles and editing preferences. No user snippet files found. Vim/Neovim use system clipboard. |
| Appearance | GTK2/3/4 Adwaita-dark and Adwaita icons, Xft settings, xsettingsd, nwg-look export preferences and gsettings export. Hyprland independently requests Bibata-Modern-Ice at size 30. |
| Integration | Browser/Claude URI associations, Claude desktop entry, Mattermost and Remmina autostart entries. |
| Development | Global Git ignore for local Claude settings. Global Git config has identity and Git LFS filters; identity excluded. Git LFS restore instructions retained. |
| SSH | `.ssh` contains private/public key files, agent directory and known-host records. No SSH client `config` file found. Only directory metadata inspected; no key contents copied. |

Installed application evidence comes from pacman and file references. The session's process view showed Bash/Codex and inspection processes, so an active Hyprland session and exact running desktop applications could not be confirmed. Installed mako has no user config; wofi and swaync configurations were absent. No user systemd units, custom fontconfig, `~/.themes`, `~/.icons` or `~/.fonts` were found. `~/.local/bin` contains uv/uvx binaries and a Claude executable symlink, not custom scripts. Nemo's local scripts/actions contain no files. Local icons contain application-generated launch icons, not an identified custom theme.

## Excluded deliberately

- SSH/GPG keys and host history, VPN profiles and certificates, browser profiles, sessions, cookies, credential stores, AI-tool authentication/configuration and project files.
- Entire state/data directories for Code/Cursor, Mattermost, Obsidian, Telegram, Remmina, DBeaver, Docker, browsers, qBittorrent, Spotify and other applications. Only the explicitly listed editor preference files were selected.
- Global Git identity (`.gitconfig`); configure name/email privately and recreate Git LFS filters with `git lfs install`.
- VS Code/Cursor personal spelling dictionaries (`cSpell.userWords`) removed from stored settings; live settings unchanged. Other settings/keybindings preserved.
- Qt6ct config contains only generated window geometry, no appearance customization. QtProject, pavucontrol, nwg-look UI/runtime state, dconf binary database, MIME cache, shell/editor history, backup files and editor extension binaries excluded.
- Wallpaper images, screenshots, personal documents, downloads, AppImages, manually installed binaries, NVM runtimes, uv tools, caches and application databases excluded. Preserve private assets separately; the wallpaper script and theme text are included.
- System-wide `/etc` settings, bootloader/driver configuration, service enablement and private network connections are outside this user-configuration backup. Package lists do not recreate those settings.

## Machine-specific settings and existing issues

- Hyprland `0.56.2-4`, Ghostty `1.3.1-2`, Waybar `0.15.0-3` were installed. The Lua config uses the `hl` API; verify support before restoring with another version. The short `.conf` stub coexists with Lua; both are preserved and no assumption was made about which entry point a particular build loads.
- Monitor `eDP-1`, `1920x1200@165`, scale `1.07`; keyboard layouts `us,ru`, Alt+Shift switch; touchpad factor `0.2`; example mouse rule `epic-mouse-v1`. Adjust for new hardware.
- Wallpaper startup uses `~/Pictures/wallpapers` and awww, choosing a random image every ten minutes. Video wallpaper startup is disabled; the videos in `~/Video/Wallpapers` are retained. Screenshots require `~/Pictures/screenshots`. The screenshot binding invokes `date` twice, so crossing a second boundary can make its clipboard step use a different filename. Preserved as requested.
- Both stored Waybar VPN scripts now reference connection name `VPN-W`. The live scripts and NetworkManager profile could not be updated from the restricted environment. Rename the live profile and update both live scripts together before capturing again; otherwise capture will restore the old name in the repository. Recreate the connection and its credentials privately on another machine.
- Waybar clock actions have duplicate `on-scroll-up`/`on-scroll-down` keys; parser behavior may select the last value. Preserved unchanged.
- Rofi theme path, GTK2 include and Claude desktop entry contain `/home/shadowrix`. Adjust before restoring under another username. GTK2 includes `.gtkrc-2.0.mine`, which is absent; create only if needed.
- Ghostty's source file is named `config.ghostty`; preserved exactly. Actual automatic loading was not verified. Do not silently rename it and assume equivalent behavior.
- Starship exists in `/usr/local/bin`, outside the package list. NVM is referenced in Bash startup and needs separate setup. The Claude installation path requires separate installation. Montserrat is referenced by Rofi; its installed font availability was not verified. GTK fonts specify Adwaita Sans.
- Package snapshot includes NVIDIA drivers, Intel microcode, kernel, bootloader and display manager. Review for other hardware. Foreign packages were explicitly installed; their availability in the AUR was not verified.
- Theme attribution comments retained; confirm upstream license terms before redistributing third-party theme text publicly.

## Validation

- 37 explicitly mapped configuration files; 83 explicit official packages, 9 explicit foreign packages; 15 VS Code and 11 Cursor extension IDs.
- At initial backup, original Hyprland and Waybar copies matched live files byte for byte and all 37 live files matched their pre-copy SHA-256 hashes. Subsequently, the two stored VPN scripts were changed to `VPN-W`; the live scripts remain unchanged pending the manual rename.
- Initial default capture comparison passed, including the documented editor dictionary omission. After the requested VPN rename, comparison reports the two VPN scripts until the live setup is updated. Capture self-check covers compare-only behavior, copied contents, dictionary removal, permission preservation, symlink refusal and path traversal refusal.
- Bash syntax checked on stored startup files and shell scripts. No scripts were executed against the desktop or VPN.
- Reviewed selected file contents and scanned repository text for private-key markers, common token formats, suspicious credential assignments and URLs containing passwords; no matches found. This is a best-effort check, not proof of absence.
- Git status/branch/remote/history and tracked-file secret scans remain unavailable: `fatal: not a git repository`. No index, commit or remote was modified. No push, installation, sudo, live apply or restore was performed.
- No GUI reload, session restart, destructive restore or chezmoi apply was run. Restore instructions are based on the exact manifest; end-to-end restoration on a clean Arch machine was not tested.

## Exact file mapping

Repository paths on the left, paths relative to HOME on the right. This is also stored in machine-readable `files.tsv`.

| Repository | Live target |
| --- | --- |
| `hypr/.luarc.json` | `~/.config/hypr/.luarc.json` |
| `hypr/hypridle.conf` | `~/.config/hypr/hypridle.conf` |
| `hypr/hyprland.conf` | `~/.config/hypr/hyprland.conf` |
| `hypr/hyprland.lua` | `~/.config/hypr/hyprland.lua` |
| `hypr/hyprlock.conf` | `~/.config/hypr/hyprlock.conf` |
| `hypr/random-wallpaper.sh` | `~/.config/hypr/random-wallpaper.sh` |
| `waybar/auto-reload.sh` | `~/.config/waybar/auto-reload.sh` |
| `waybar/config.jsonc` | `~/.config/waybar/config.jsonc` |
| `waybar/scripts/vpn-status.sh` | `~/.config/waybar/scripts/vpn-status.sh` |
| `waybar/scripts/vpn-toggle.sh` | `~/.config/waybar/scripts/vpn-toggle.sh` |
| `waybar/style.css` | `~/.config/waybar/style.css` |
| `home/.bashrc` | `~/.bashrc` |
| `home/.bash_profile` | `~/.bash_profile` |
| `home/.vimrc` | `~/.vimrc` |
| `home/.gtkrc-2.0` | `~/.gtkrc-2.0` |
| `home/.config/starship.toml` | `~/.config/starship.toml` |
| `home/.config/rofi/config.rasi` | `~/.config/rofi/config.rasi` |
| `home/.config/ghostty/config.ghostty` | `~/.config/ghostty/config.ghostty` |
| `home/.config/gtk-3.0/settings.ini` | `~/.config/gtk-3.0/settings.ini` |
| `home/.config/gtk-4.0/settings.ini` | `~/.config/gtk-4.0/settings.ini` |
| `home/.config/xsettingsd/xsettingsd.conf` | `~/.config/xsettingsd/xsettingsd.conf` |
| `home/.config/nvim/init.lua` | `~/.config/nvim/init.lua` |
| `home/.config/zellij/config.kdl` | `~/.config/zellij/config.kdl` |
| `home/.config/git/ignore` | `~/.config/git/ignore` |
| `home/.config/mimeapps.list` | `~/.config/mimeapps.list` |
| `home/.config/autostart/mattermost-desktop.desktop` | `~/.config/autostart/mattermost-desktop.desktop` |
| `home/.config/autostart/remmina-applet.desktop` | `~/.config/autostart/remmina-applet.desktop` |
| `home/.local/share/rofi/themes/spotlight.rasi` | `~/.local/share/rofi/themes/spotlight.rasi` |
| `home/.local/share/rofi/themes/spotlight-dark.rasi` | `~/.local/share/rofi/themes/spotlight-dark.rasi` |
| `home/.local/share/applications/claude-code-url-handler.desktop` | `~/.local/share/applications/claude-code-url-handler.desktop` |
| `home/.config/Code/User/settings.json` | `~/.config/Code/User/settings.json` |
| `home/.config/Code/User/keybindings.json` | `~/.config/Code/User/keybindings.json` |
| `home/.config/Cursor/User/settings.json` | `~/.config/Cursor/User/settings.json` |
| `home/.config/Cursor/User/keybindings.json` | `~/.config/Cursor/User/keybindings.json` |
| `home/.config/nwg-look/config` | `~/.config/nwg-look/config` |
| `home/.local/share/nwg-look/gsettings` | `~/.local/share/nwg-look/gsettings` |
