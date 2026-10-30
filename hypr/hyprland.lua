-- This is an example Hyprland Lua config file.
-- Refer to the wiki for more information.
-- https://wiki.hypr.land/Configuring/Start/

-- Please note not all available settings / options are set here.
-- For a full list, see the wiki

-- You can (and should!!) split this configuration into multiple files
-- Create your files separately and then require them like this:
-- require("myColors")


------------------
---- MONITORS ----
------------------

-- See https://wiki.hypr.land/Configuring/Basics/Monitors/
hl.monitor({
    output   = "eDP-1",
    mode     = "1920x1200@165",
    position = "0x0",
    scale    = "1.07",
})


---------------------
---- MY PROGRAMS ----
---------------------

-- Set programs that you use
local terminal    = "ghostty"
local fileManager = "nemo"
local music       = "spotify"
local browser     = "google-chrome-stable"
--local browser     = "google-chrome-stable --proxy-server=127.0.0.1:12334" -- browser with hiddify proxy
--local browser_i   = "google-chrome-stable --incognito --proxy-server=127.0.0.1:12334"
local browser_i   = "google-chrome-stable --incognito"
local launcher    = "rofi -show drun -show-icons"
local runner      = "rofi -show run"
local hiddify     = "~/apps/Hiddify-Linux-x64-AppImage.AppImage"
local amnezia     = "AmneziaVPN"
local telegram    = "Telegram"
local mattermost  = "mattermost-desktop"
local lock_screen = "hyprlock"

-------------------
---- AUTOSTART ----
-------------------

-- See https://wiki.hypr.land/Configuring/Basics/Autostart/

-- Autostart necessary processes (like notifications daemons, status bars, etc.)
-- Or execute your favorite apps at launch like this:
--
hl.on("hyprland.start", function ()  
  hl.exec_cmd('mpvpaper --slideshow 300 -o "no-audio shuffle hwdec=auto panscan=1" ALL "' .. os.getenv("HOME") .. '/Video/Wallpapers/"')

  hl.exec_cmd("waybar")
  hl.exec_cmd("systemctl --user start hyprpolkitagent")
  hl.exec_cmd("hyprctl setcursor Bibata-Modern-Ice 30")
  hl.exec_cmd("hypridle")
end)


-------------------------------
---- ENVIRONMENT VARIABLES ----
-------------------------------

-- See https://wiki.hypr.land/Configuring/Advanced-and-Cool/Environment-variables/

hl.env("XCURSOR_SIZE", "30")
hl.env("HYPRCURSOR_SIZE", "30")
hl.env("QT_QPA_PLATFORMTHEME", "qt6ct")

-----------------------
----- PERMISSIONS -----
-----------------------

-- See https://wiki.hypr.land/Configuring/Advanced-and-Cool/Permissions/
-- Please note permission changes here require a Hyprland restart and are not applied on-the-fly
-- for security reasons

-- hl.config({
--   ecosystem = {
--     enforce_permissions = true,
--   },
-- })

-- hl.permission("/usr/(bin|local/bin)/grim", "screencopy", "allow")
-- hl.permission("/usr/(lib|libexec|lib64)/xdg-desktop-portal-hyprland", "screencopy", "allow")
-- hl.permission("/usr/(bin|local/bin)/hyprpm", "plugin", "allow")


-----------------------
---- LOOK AND FEEL ----
-----------------------

-- Refer to https://wiki.hypr.land/Configuring/Basics/Variables/
hl.config({
    general = {
        gaps_in  = 7,
        gaps_out = 14,

        border_size = 2,

        col = {
            active_border   = { colors = {"rgba(7aa2f7cc)", "rgba(bb9af7cc)"}, angle = 45 },
            inactive_border = "rgba(41486899)",
        },

        -- Set to true to enable resizing windows by clicking and dragging on borders and gaps
        resize_on_border = false,

        -- Please see https://wiki.hypr.land/Configuring/Advanced-and-Cool/Tearing/ before you turn this on
        allow_tearing = false,

        layout = "dwindle",
    },

    decoration = {
        rounding       = 14,
        rounding_power = 2,

        -- Change transparency of focused and unfocused windows
        active_opacity   = 1.0,
        inactive_opacity = 0.8,

        shadow = {
            enabled      = true,
            range        = 14,
            render_power = 3,
            color        = 0x550b0e18,
        },

        blur = {
            enabled   = true,
            size      = 3,
            passes    = 1,
            vibrancy  = 0.10,
        },
    },

    animations = {
        enabled = true,
    },
})

-- Tokyo Glass Dev: short ease-out motion, without spring bounce.
hl.curve("tokyoEase", { type = "bezier", points = { {0.16, 1}, {0.3, 1} } })
hl.animation({ leaf = "global",        enabled = true, speed = 3,   bezier = "tokyoEase" })
hl.animation({ leaf = "border",        enabled = true, speed = 3,   bezier = "tokyoEase" })
hl.animation({ leaf = "windows",       enabled = true, speed = 3,   bezier = "tokyoEase" })
hl.animation({ leaf = "windowsIn",     enabled = true, speed = 3,   bezier = "tokyoEase", style = "popin 96%" })
hl.animation({ leaf = "windowsOut",    enabled = true, speed = 2,   bezier = "tokyoEase", style = "popin 98%" })
hl.animation({ leaf = "fade",          enabled = true, speed = 2,   bezier = "tokyoEase" })
hl.animation({ leaf = "layers",        enabled = true, speed = 2,   bezier = "tokyoEase", style = "fade" })
hl.animation({ leaf = "workspaces",    enabled = true, speed = 3,   bezier = "tokyoEase", style = "slide" })

-- Ignore transparent pixels so blur follows the islands, not the full bar.
hl.layer_rule({ name = "tokyo-waybar", match = { namespace = "waybar" }, blur = true, ignore_alpha = 0.1 })
hl.layer_rule({ name = "tokyo-rofi", match = { namespace = "rofi" }, blur = true, ignore_alpha = 0.1 })
hl.layer_rule({ name = "tokyo-notifications", match = { namespace = "notifications" }, blur = true, ignore_alpha = 0.1 })

-- Ref https://wiki.hypr.land/Configuring/Basics/Workspace-Rules/
-- "Smart gaps" / "No gaps when only"
-- uncomment all if you wish to use that.
-- hl.workspace_rule({ workspace = "w[tv1]", gaps_out = 0, gaps_in = 0 })
-- hl.workspace_rule({ workspace = "f[1]",   gaps_out = 0, gaps_in = 0 })
-- hl.window_rule({
--     name  = "no-gaps-wtv1",
--     match = { float = false, workspace = "w[tv1]" },
--     border_size = 0,
--     rounding    = 0,
-- })
-- hl.window_rule({
--     name  = "no-gaps-f1",
--     match = { float = false, workspace = "f[1]" },
--     border_size = 0,
--     rounding    = 0,
-- })

-- See https://wiki.hypr.land/Configuring/Layouts/Dwindle-Layout/ for more
hl.config({
    dwindle = {
        preserve_split = true, -- You probably want this
    },
})

-- See https://wiki.hypr.land/Configuring/Layouts/Master-Layout/ for more
hl.config({
    master = {
        new_status = "master",
    },
})

-- See https://wiki.hypr.land/Configuring/Layouts/Scrolling-Layout/ for more
hl.config({
    scrolling = {
        fullscreen_on_one_column = true,
    },
})

----------------
----  MISC  ----
----------------

hl.config({
    misc = {
        force_default_wallpaper = -1,    -- Set to 0 or 1 to disable the anime mascot wallpapers
        disable_hyprland_logo   = true,
    },
})


---------------
---- INPUT ----
---------------

hl.config({
    input = {
        kb_layout = "us,ru",
    	kb_options = "grp:alt_shift_toggle",
	kb_variant = "",
        kb_model   = "",
        kb_rules   = "",

        follow_mouse = 1,

        sensitivity = 0, -- -1.0 - 1.0, 0 means no modification.

        touchpad = {
            natural_scroll = true,
	    scroll_factor = 0.2
        },
    },
})

hl.gesture({
    fingers = 3,
    direction = "horizontal",
    action = "workspace"
})

-- Example per-device config
-- See https://wiki.hypr.land/Configuring/Advanced-and-Cool/Devices/ for more
hl.device({
    name        = "epic-mouse-v1",
    sensitivity = -0.5,
})


---------------------
---- KEYBINDINGS ----
---------------------

local mainMod = "SUPER" -- Sets "Windows" key as main modifier
local secondMod = "SUPER + SHIFT"


local closeWindowBind = hl.bind(mainMod .. " + Q", hl.dsp.window.close())
hl.bind(mainMod .. " + T", hl.dsp.exec_cmd(terminal))
hl.bind(mainMod .. " + F", hl.dsp.exec_cmd(fileManager))
hl.bind(mainMod .. " + B", hl.dsp.exec_cmd(browser))
hl.bind(secondMod .. " + B", hl.dsp.exec_cmd(browser_i))
hl.bind(mainMod .. " + M", hl.dsp.exec_cmd(music))
hl.bind(secondMod .. " + M", hl.dsp.exec_cmd(mattermost))
hl.bind(mainMod .. " + Space", hl.dsp.exec_cmd(launcher))
hl.bind(secondMod .. " + Space", hl.dsp.exec_cmd(runner))
hl.bind(mainMod .. " + H", hl.dsp.exec_cmd(hiddify))
hl.bind(mainMod .. " + A", hl.dsp.exec_cmd(amnezia))
hl.bind(secondMod .. " + T", hl.dsp.exec_cmd(telegram))
hl.bind(secondMod .. " + L", hl.dsp.exec_cmd(lock_screen))
-- screenshots
hl.bind("Print", hl.dsp.exec_cmd("grim -g \"$(slurp)\" ~/Pictures/screenshots/screenshot-$(date +%F_%T).png && wl-copy < ~/Pictures/screenshots/screenshot-$(date +%F_%T).png"))


-- Example binds, see https://wiki.hypr.land/Configuring/Basics/Binds/ for more

-- closeWindowBind:set_enabled(false)
hl.bind(secondMod .. " + Q", hl.dsp.exec_cmd("command -v hyprshutdown >/dev/null 2>&1 && hyprshutdown || hyprctl dispatch 'hl.dsp.exit()'"))

hl.bind(mainMod .. " + V", hl.dsp.window.float({ action = "toggle" }))
hl.bind(mainMod .. " + P", hl.dsp.window.pseudo())
hl.bind(mainMod .. " + J", hl.dsp.layout("togglesplit"))    -- dwindle only

-- Move focus with mainMod + arrow keys
hl.bind(mainMod .. " + left",  hl.dsp.focus({ direction = "left" }))
hl.bind(mainMod .. " + right", hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + up",    hl.dsp.focus({ direction = "up" }))
hl.bind(mainMod .. " + down",  hl.dsp.focus({ direction = "down" }))

hl.bind(secondMod .. " + left",  hl.dsp.window.move({ direction = "left" }))
hl.bind(secondMod .. " + right", hl.dsp.window.move({ direction = "right" }))
hl.bind(secondMod .. " + up",    hl.dsp.window.move({ direction = "up" }))
hl.bind(secondMod .. " + down",  hl.dsp.window.move({ direction = "down" }))

hl.bind(secondMod .. " + F",  hl.dsp.window.fullscreen({ mode = "maximized" }))


-- Switch workspaces with mainMod + [0-9]
-- Move active window to a workspace with mainMod + SHIFT + [0-9]
for i = 1, 10 do
    local key = i % 10 -- 10 maps to key 0
    hl.bind(mainMod .. " + " .. key,             hl.dsp.focus({ workspace = i}))
    hl.bind(mainMod .. " + SHIFT + " .. key,     hl.dsp.window.move({ workspace = i }))
end

-- Example special workspace (scratchpad)
-- hl.bind(mainMod .. " + S",         hl.dsp.workspace.toggle_special("magic"))
-- hl.bind(mainMod .. " + SHIFT + S", hl.dsp.window.move({ workspace = "special:magic" }))

-- Scroll through existing workspaces with mainMod + scroll
hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mainMod .. " + mouse_up",   hl.dsp.focus({ workspace = "e-1" }))

-- Move/resize windows with mainMod + LMB/RMB and dragging
hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag(),   { mouse = true })
hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })

-- Laptop multimedia keys for volume and LCD brightness
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"), { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"),      { locked = true, repeating = true })
hl.bind("XF86AudioMute",        hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"),     { locked = true, repeating = true })
hl.bind("XF86AudioMicMute",     hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"),   { locked = true, repeating = true })
hl.bind("XF86MonBrightnessUp",  hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%+"),                  { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown",hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%-"),                  { locked = true, repeating = true })

-- Requires playerctl
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd("playerctl next"),       { locked = true })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPlay",  hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd("playerctl previous"),   { locked = true })


--------------------------------
---- WINDOWS AND WORKSPACES ----
--------------------------------

-- See https://wiki.hypr.land/Configuring/Basics/Window-Rules/
-- and https://wiki.hypr.land/Configuring/Basics/Workspace-Rules/

-- Example window rules that are useful

local suppressMaximizeRule = hl.window_rule({
    -- Ignore maximize requests from all apps. You'll probably like this.
    name  = "suppress-maximize-events",
    match = { class = ".*" },

    suppress_event = "maximize",
})
-- suppressMaximizeRule:set_enabled(false)

hl.window_rule({
    -- Fix some dragging issues with XWayland
    name  = "fix-xwayland-drags",
    match = {
        class      = "^$",
        title      = "^$",
        xwayland   = true,
        float      = true,
        fullscreen = false,
        pin        = false,
    },

    no_focus = true,
})

-- Layer rules also return a handle.
-- local overlayLayerRule = hl.layer_rule({
--     name  = "no-anim-overlay",
--     match = { namespace = "^my-overlay$" },
--     no_anim = true,
-- })
-- overlayLayerRule:set_enabled(false)

-- Hyprland-run windowrule
hl.window_rule({
    name  = "move-hyprland-run",
    match = { class = "hyprland-run" },

    move  = "20 monitor_h-120",
    float = true,
})
