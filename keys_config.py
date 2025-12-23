from pathlib import Path

from libqtile import bar, layout, widget
from libqtile.config import Drag, Click, Key, Screen
from libqtile.lazy import lazy


mod = "mod4"
terminal = "alacritty"
home = Path.home()

keys = [
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),

    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),

    Key([mod, "control"], "Left", lazy.layout.grow_main()),
    Key([mod, "control"], "Right", lazy.layout.shrink_main()),
    Key([mod, "control"], "Down", lazy.layout.grow()),
    Key([mod, "control"], "up", lazy.layout.shrink()),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    Key([mod, "control"], "h", lazy.layout.grow_main()),
    Key([mod, "control"], "l", lazy.layout.shrink_main()),
    Key([mod, "control"], "j", lazy.layout.grow()),
    Key([mod, "control"], "k", lazy.layout.shrink()),
    Key([mod, "control"], "u", lazy.layout.grow_up()),

    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "m", lazy.layout.next()),
    Key([mod], "period", lazy.next_screen()),
    Key([mod], "Tab", lazy.next_layout()),

    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod, "control"], "o", lazy.spawn('lock')),

    Key([mod], "f", lazy.window.toggle_floating()),
    Key([mod], "p", lazy.window.kill()),

    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-")),
    Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),

    Key([mod], "Print", lazy.spawn("scrot ~/Pictures/ss-%Y-%m-%d-%T.png")),
    Key([mod], "Return", lazy.spawn(f"{terminal}")),
    Key([mod, "shift"], "f", lazy.spawn('firefox-developer-edition')),
    Key([mod, "shift"], "t", lazy.spawn('thunar')),
    Key([mod, "shift"], "s", lazy.spawn('spotify')),
    Key([mod, "shift"], "d", lazy.spawn('discord')),
    Key([mod, "shift"], "c", lazy.spawn('copyq toggle')),
    Key([mod], "space",
        lazy.spawn(f'{home.joinpath(".local", "share", "bin", "rofi")}')),
    ]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.focus())
]
