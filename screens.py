import subprocess

from libqtile.config import Screen
from libqtile import bar, widget

from color_scheme import colors
from widgets import widget_list


command = "xrandr --listmonitors"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
stdout, _ = process.communicate()
monitor_count = stdout[-1]

# Define screens and bar
screens = [
        Screen(
            top=bar.Bar(
                widgets=widget_list,
                size=30,
                opacity=1,
                border_width=3,
                border_color=colors["background"][1],
                margin=[0, 0, 0, 0],
                background=colors["background"][0],
            ),
        ),
    ]

# Create a new list of widgets for each additional screen
for i in range(1, int(monitor_count)):
    _widget_list = []
    for item in widget_list:
        if not isinstance(item, widget.Systray):
            _widget_list.append(item)

    screens.append(
        Screen(
            top=bar.Bar(
                widgets=_widget_list,
                size=30,
                opacity=1,
                border_width=3,
                border_color=colors["background"][1],
                margin=[0, 0, 0, 0],
                background=colors["background"][0])
            )
        )
