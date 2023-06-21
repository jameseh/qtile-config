# -*- coding: utf-8 -*-

from libqtile.config import Key, Drag, Click
from libqtile.lazy import lazy

from groups import group_names


# Set modifier key
mod = "mod4"

# Set default terminal emulator
terminal = "alacritty"

keys = [
    # Window managment keybinds
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "Right",
        lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down",
        lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "Left",
        lazy.layout.grow_main(), desc="Grow window main"),
    Key([mod, "control"], "Right",
        lazy.layout.shrink_main(), desc="Shrink window main"),
    Key([mod, "control"], "Left", lazy.layout.grow(), desc="Grow window"),
    Key([mod, "control"], "Right", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod], "period", lazy.next_screen(), desc="Next monitor"),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_main(),
        desc="Grow window main"),
    Key([mod, "control"], "l", lazy.layout.shrink_main(),
        desc="Shrink window main"),
    Key([mod, "control"], "j", lazy.layout.grow(), desc="Grow window"),
    Key([mod, "control"], "k", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod, "control"], "u", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "Return", lazy.spawn(f"{terminal}"), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "p", lazy.window.kill(), desc="Kill focused window"),

    # Qtile keybinds
    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "control"], "l", lazy.spawn('lock'), desc="Locks Screen"),

    # Sound management keybinds
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "amixer sset Master 5%+"), desc="Raise Volume by 5%"),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "amixer sset Master 5%-"), desc="Lower Volume by 5%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"),
        desc="Play/Pause player"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"),
        desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"),
        desc="Skip to previous"),

    # Take screenshots - wayland
    Key([mod], "Print", lazy.spawn("grim $(xdg-user-dir PICTURES)/$(date"
                                   + " +'%Fx%s_screen-shot.png')' -e 'mv $f $$"
                                   + "(xdg-user-dir PICTURES/screenshots);"
                                   + " viewnior $$(xdg-user-dir PICTURES)"
                                   + "/screenshots/$f'"),
        desc="Takes a Screenshot"),
    # Take screenshot - x11
    Key([mod], "Print", lazy.spawn("scrot ~/Pictures/screenshots/"
                                   + "%Y-%m-%d-%T-screenshot.png"),
        desc="Takes a Screenshot"),

    # App keybinds
    Key([mod, "shift"], "b", lazy.spawn('firefox-developer-edition'),
        desc="Launches Firefox Web Browser"),
    Key([mod, "shift"], "f", lazy.spawn('pcmanfm'),
        desc="Launches Pcmanfm File Manager"),
    Key([mod, "shift"], "s", lazy.spawn('spotify'), desc="Launches Spotify"),
    Key([mod, "shift"], "d", lazy.spawn('discord'), desc="Launches Discord"),
    Key([mod, "shift"], "c", lazy.spawn('copyq toggle')),

    # Rofi launcher
    Key([mod], "space", lazy.spawn(
        '/home/james/.config/rofi/scripts/launcher_t1')),

    # Bitwarden
    Key([mod], "BackSpace", lazy.spawn(
        'bwmenu --auto-lock 12000 --clear 120 -- -location 2')),

    # Toggle floating windows
    Key([mod], "f", lazy.window.toggle_floating())
    ]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.focus())
]

# Bind the key combinations to switch to the groups.
for num, name in enumerate(group_names, 1):
    keys.append(Key([mod], str(num), lazy.group[name].toscreen()))
    keys.append(Key([mod, "shift"], str(num), lazy.window.togroup(name)))
