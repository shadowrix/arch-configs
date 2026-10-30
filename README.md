# Arch configuration backup

Reviewed configuration snapshots for this Arch Linux / Hyprland setup. Live files remain ordinary files: edit them normally, capture reviewed changes here, then use Git to version them. No symlinks or automatic apply hooks are installed.

## Layout

```text
arch-configs/
├── hypr/                 # Existing Hyprland, lock, idle and wallpaper configuration
├── waybar/               # Existing modules, CSS and VPN/reload scripts
├── home/                 # Other files, with their original home-relative paths
├── files.tsv             # Exact mapping: repository path<TAB>home-relative target
├── packages/             # Explicit official/foreign packages and editor extensions
├── scripts/              # Compare/capture helper and its small self-check
├── docs/inventory.md     # Discovery, exclusions, machine settings and validation
├── .gitignore
└── README.md
```

Existing `hypr/` and `waybar/` were preserved byte for byte. See [inventory](docs/inventory.md) for all files, dependencies and known issues.

## Management choice and Git prerequisite

Chezmoi was not installed during inspection. More importantly, `.git/` was exposed as an empty, read-only directory and Git reported `not a git repository`. Branch, remote, tracked files, uncommitted changes and history could not be inspected. No Git initialization, branch/remote change, commit or push was attempted. **Restore access to the original Git metadata before committing. Do not run `git init` here.**

This deliberately uses a simple explicit file mapping, avoiding migration of existing folders and requiring only Python 3 for capture. Chezmoi has not been configured, and this is not a chezmoi source tree; do not run `chezmoi apply` against it. Reconsider migration after the original repository and an installed chezmoi version can be inspected. No second repository is needed.

## Dependencies and packages

Runtime dependencies include Hyprland, Waybar, Ghostty, Rofi, awww, hypridle, hyprlock, hyprpolkitagent, PipeWire/WirePlumber, brightnessctl, playerctl, grim, slurp, wl-clipboard, NetworkManager, Blueman, pavucontrol and inotify-tools. The desktop launches Nemo, Chrome, Spotify, Telegram, Mattermost, AmneziaVPN and a manually supplied Hiddify AppImage. Shell dependencies: Bash, Starship and NVM. Fonts/themes: JetBrainsMono Nerd Font, Montserrat (availability needs checking), Adwaita-dark, Adwaita icons and Bibata-Modern-Ice. Python 3 runs the capture helper.

The package lists contain **explicit installations only**, not dependency closure. Review them on new hardware: kernel, NVIDIA, Intel microcode, bootloader, display manager and network choices are machine-specific. The lists are a snapshot, not pinned package versions or a system installer.

Refresh on the original machine:

```bash
pacman -Qqen | LC_ALL=C sort > packages/official.txt
pacman -Qqem | LC_ALL=C sort > packages/foreign.txt
code --list-extensions | LC_ALL=C sort > packages/vscode-extensions.txt
cursor --list-extensions | LC_ALL=C sort > packages/cursor-extensions.txt
```

Editor lists were initially extracted from installed extension metadata without launching either editor. Inspect extension IDs before publishing if using private extensions.

## Restore on another Arch installation

Start with a working Arch system and networking. Install Git and clone your **existing repository URL** to `~/Projects/arch-configs` (substitute the URL shown by `git remote get-url origin` on the original machine). No repository URL was recoverable in this session.

After reviewing `packages/official.txt`, an administrator may run:

```bash
cd ~/Projects/arch-configs
sudo pacman -S --needed - < packages/official.txt
```

Foreign packages are listed separately in `packages/foreign.txt`; inspect their current PKGBUILDs and install them with your chosen AUR workflow. If you already use yay, the corresponding command is `yay -S --needed - < packages/foreign.txt`. Foreign does not necessarily mean AUR: some packages may require another source. These commands were not run.

Restore Starship (`/usr/local/bin/starship` on the original host), NVM/desired Node versions, Hiddify AppImage and Claude Code separately from their trusted installers. These binaries, runtime installations and credentials are not backed up. Recreate VPN connections and secrets privately. Configure Git identity separately with `git config --global user.name` and `git config --global user.email`; run `git lfs install` if using Git LFS.

Before copying, inspect `files.tsv`, review each configuration and the machine settings in the inventory. For another username, adjust the absolute paths in the stored Rofi, GTK2 and desktop-entry files. Check any existing target and its parent directories for symlinks (for example, `namei -l ~/.config/hypr/hyprland.lua`). Resolve conflicts manually first. The following Bash loop is intended for a fresh home after that review. It backs up every existing destination outside the repository before prompting for replacements; it does not remove unrelated files:

```bash
cd ~/Projects/arch-configs
(
set -e
backup="$HOME/arch-configs-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -m 700 "$backup"
while IFS=$'\t' read -r stored live; do
    if [ -e "$HOME/$live" ] || [ -L "$HOME/$live" ]; then
        mkdir -p "$backup/$(dirname "$live")"
        cp -a -- "$HOME/$live" "$backup/$live"
    fi
done < files.tsv
# A backup failure stops this subshell before any restore. Keep backups private.
while IFS=$'\t' read -r stored live; do
    mkdir -p "$HOME/$(dirname "$live")"
    cp -i --preserve=mode -- "$stored" "$HOME/$live"
done < files.tsv
mkdir -p ~/Pictures/screenshots ~/Pictures/desctop_backgrounds
)
```

Supply your wallpapers privately in `~/Pictures/desctop_backgrounds` (original spelling). Review Lua/Hyprland compatibility before starting the desktop; the original installed version was `0.56.2-4`. No login-session, system-service, bootloader, driver or system-wide configuration is restored by this file backup. Enable services such as networking, Bluetooth or your display manager deliberately for the new system.

Optionally restore editor extensions after installing the editors:

```bash
while IFS= read -r extension; do code --install-extension "$extension"; done < packages/vscode-extensions.txt
while IFS= read -r extension; do cursor --install-extension "$extension"; done < packages/cursor-extensions.txt
```

## Updating configurations

```bash
cd ~/Projects/arch-configs
python scripts/capture.py          # Report differing paths; exit 1 means differences
# Inspect changed live files locally for secrets before capturing.
python scripts/capture.py --capture
python scripts/capture.py          # Silent / exit 0 when snapshots match
python scripts/test_capture.py
```

Capture uses only `files.tsv`, never an entire directory. It does not modify live files or delete missing entries. It refuses missing files and symlinks; investigate these instead of replacing them blindly. VS Code/Cursor settings retain formatting and preferences but omit `cSpell.userWords` for privacy. Capture is not a secret scanner: newly added tokens must be excluded before copying. To manage another file, inspect it, add an explicit mapping and capture it. Review scripts before executing them on a new machine.

## Git workflow

After original Git metadata is accessible:

```bash
cd ~/Projects/arch-configs
git status --short --branch
git remote -v
git diff --check
git diff --stat
# Inspect changed AND new files locally for secrets before staging.
git add -- README.md .gitignore files.tsv docs packages scripts home hypr waybar
git diff --cached --check
git diff --cached --stat
# Review the staged content locally, then explicitly approve the commit/push:
git commit -m "Organize reviewed Arch configuration backups"
git push
```

Use the existing branch and remote; if no upstream exists, inspect your repository before choosing one. Inspect `git fetch` / `git log HEAD..@{upstream}` before integrating upstream changes; `git pull --ff-only` avoids accidental merge commits but requires a clean, compatible working tree. Back up or commit local work first. Never force push to solve an unexpected divergence.

## Experiments and recovery

Before an experiment, capture the working setup, review and commit it, then use `git switch -c theme-experiment`. Back up live targets before any restore. A Git branch switch changes only repository copies; it does not change your desktop. Restore only the selected files after reviewing differences, then reload the relevant application yourself.

For a committed unwanted change, `git revert <commit>` preserves history. For one stored file, save uncommitted work first, then `git restore --source=<known-good-commit> -- <stored-path>`. Compare with the live target and copy only that file after making a backup. Example: `diff -u hypr/hyprland.lua ~/.config/hypr/hyprland.lua` (inspect locally), then restore after review. Your private `arch-configs-backup-*` directories contain the pre-restore files and can be copied back individually. Do not blindly restore shell startup files or monitor settings while diagnosing a broken login.

No credentials were detected in the reviewed snapshots, but pattern checks cannot prove their absence. Original tracked-file and historical scans remain pending because Git metadata was inaccessible. If an exposed secret is later found, revoke/rotate it: deleting it from the latest tree does **not** remove it from Git history. No history rewriting or credential rotation was performed.
