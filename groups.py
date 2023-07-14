# -*- coding: utf-8 -*-

from libqtile.config import Group


# Set group names to material-icons from material-icons.ttf
group_names = [
        "language",
        "terminal",
        "code",
        "music_video",
        "chat",
        "text_snippet",
        ]

# Set the layouts of each group
groups = [
    Group(name, layout="monadtall") if name not in (
        "language", "text_snippet")
    else Group(name, layout="max") for name in group_names
]
