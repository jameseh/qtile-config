# -*- coding: utf-8 -*-

from libqtile import layout

from color_scheme import colors


layout_floating = layout.Floating(
    float_rules=[*layout.Floating.default_float_rules])

# Define layouts
layouts = [
    layout.MonadTall(
        font="Noto Sans Mono",
        font_size=16,
        border_focus=colors["secondary"][0],
        border_width=3,
        border_normal=colors["background"][1],
        margin=0
        ),
    layout.Max(
        font="Noto Sans Mono",
        font_size=16,
        border_width=0,
        margin=0
        ),
]
