from libqtile import qtile, widget, bar
from libqtile.lazy import lazy

from color_scheme import colors
from keybinds import terminal

# Define widgets to be used on screen bar
widget_list = [
    widget.Spacer(
        length=30,
        background=colors["background"][0]),

    widget.Image(
        filename="~/.config/qtile/logo.png",
        background=colors["background"][0],
        margin=3),

    widget.GroupBox(
        font="Material Icons",
        fontsize=26,
        padding=20,
        borderwidth=2,
        highlight_method='text',
        foreground=colors["primary"][0],
        background=colors["background"][0],
        this_current_screen_border=colors["primary"][0],
        active=colors["secondary"][0],
        inactive=colors["text"][1]),

    widget.Spacer(
        length=bar.STRETCH,
        background=colors["background"][0]),

    widget.TextBox(
        font="Material Icons",
        fontsize=26,
        text="cable",
        foreground=colors["primary"][1],
        background=colors["background"][0]),

    widget.Spacer(
        length=5,
        backgrou1nd=colors["background"][0]),

    widget.CPU(
        format="{freq_current}GHz {load_percent}%",
        foreground=colors["text"][0],
        background=colors["background"][0],
        mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
            f"{terminal} -e htop")}),

    widget.Spacer(
        length=20,
        background=colors["background"][0]),

    widget.TextBox(
        font="Material Icons",
        fontsize=26,
        text="device_thermostat",
        foreground=colors["primary"][2],
        background=colors["background"][0]),

    widget.Spacer(
        length=5,
        background=colors["background"][0]),

    widget.ThermalSensor(
        format='{temp:.0f}{unit}',
        threshold=90,
        foreground_alert=colors["additional"][1],
        foreground=colors["text"][0],
        background=colors["background"][0],
        mouse_callbacks={lazy.spawn('cpupower-gui')},
        update_interval=1),

    widget.Spacer(
        length=20,
        background=colors["background"][0]),

    widget.TextBox(
        font="Material Icons",
        fontsize=26,
        text="memory",
        foreground=colors["primary"][3],
        background=colors["background"][0]),

    widget.Spacer(
        length=5,
        background=colors["background"][0]),

    widget.Memory(
        format="{MemUsed:.0f}{mm}",
        foreground=colors["text"][0],
        background=colors["background"][0],
        update_interval=1,
        mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
            f"{terminal} -e htop")}),

    widget.Spacer(
        length=bar.STRETCH,
        background=colors["background"][0]),

    widget.Systray(
        background=colors["background"][0],
        icon_size=26,
        padding=20,
        borderwidth=0,
        border_color=colors["additional"][0]),

    widget.Spacer(
        length=20,
        background=colors["background"][0]),

    widget.TextBox(
        font="Material Icons",
        fontsize=26,
        text="wifi",
        foreground=colors["primary"][4],
        background=colors["background"][0]),

    widget.Spacer(
        length=5,
        background=colors["background"][0]),

    widget.Net(
        foreground=colors["text"][0],
        background=colors["background"][0],
        update_interval=1,
        mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
            "wofi-wifi-menu")}),

    widget.Spacer(
        length=20,
        background=colors["background"][0]),

    widget.TextBox(
        font="Material Icons",
        fontsize=26,
        text="volume_up",
        foreground=colors["primary"][5],
        background=colors["background"][0]),

    widget.Spacer(
        length=5,
        background=colors["background"][0]),

    widget.Volume(
        foreground=colors["text"][0],
        background=colors["background"][0],
        format="{percent:1.0%}",
        update_interval=1),

    widget.Spacer(
        length=20,
        background=colors["background"][0]),

    widget.TextBox(
        font="Material Icons",
        fontsize=26,
        text="battery_std",
        foreground=colors["primary"][6],
        background=colors["background"][0]),

    widget.Spacer(
        length=5,
        background=colors["background"][0]),

    widget.Battery(
        foreground=colors["text"][0],
        background=colors["background"][0],
        format="{percent:1.0%}"),

    widget.Spacer(
        length=20,
        background=colors["background"][0]),

    widget.TextBox(
        font="Material Icons",
        fontsize=26,
        text="calendar_month",
        foreground=colors["primary"][7],
        background=colors["background"][0]),

    widget.Spacer(
        length=5,
        background=colors["background"][0]),

    widget.Clock(
        format='%b %d-%Y',
        foreground=colors["text"][0],
        background=colors["background"][0]),

    widget.Spacer(
        length=5,
        background=colors["background"][0]),

    widget.TextBox(
        font="Material Icons",
        fontsize=26,
        text="access_time",
        foreground=colors["primary"][8],
        background=colors["background"][0]),
    widget.Spacer(
        length=10,
        background=colors["background"][0]),

    widget.Clock(
        format='%I:%M:%S %p',
        foreground=colors["text"][0],
        background=colors["background"][0]),

    widget.Spacer(
        length=30,
        background=colors["background"][0])]
