# -*- coding: utf-8 -*-

from libqtile.config import Key, Group
from libqtile.lazy import lazy

from keybinds import keys, mod
from layouts import layouts

group_names = [
        "language",
        "terminal",
        "code",
        "music_video",
        "chat",
        "text_snippet",
        ]

groups = [
    Group(name, layout="monadtall") if name not in ("language", "text_snippet")
    else Group(name, layout="max") for name in group_names
]

# Bind the key combinations to switch to the groups.
for num, name in enumerate(group_names, 1):
    keys.append(Key([mod], str(num), lazy.group[name].toscreen()))
    keys.append(Key([mod, "shift"], str(num), lazy.window.togroup(name)))
