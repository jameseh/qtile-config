# -*- coding: utf-8 -*-
from libqtile.config import Screen
from libqtile import bar

from color_scheme import colors
from widgets import widget_list


# Define screens and bar
screens = [
        Screen(
            top=bar.Bar(
                widgets=widget_list,
                size=40,
                opacity=1,
                border_width=3,
                border_color=colors["background"][1],
                margin=[0, 0, 0, 0],
                background=colors["background"][0],
            ),
        ),
        Screen(
            top=bar.Bar(
                widgets=widget_list,
                size=40,
                opacity=1,
                border_width=3,
                border_color=colors["background"][1],
                margin=[0, 0, 0, 0],
                background=colors["background"][0],
            ),
        ),
    ]
