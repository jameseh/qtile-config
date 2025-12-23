from libqtile import widget, bar
from libqtile.lazy import lazy
from color_scheme import colors


def base(fg='text', bg='base'):
    return {
        'foreground': colors[fg],
        'background': colors[bg]
    }


def separator():
    return widget.Sep(**base(), linewidth=0, padding=5)


def powerline_arrow(fg, bg):
    return widget.TextBox(
        **base(fg, bg),
        text="",   # Powerline arrow
        fontsize=37,
        padding=0
    )


def icon(fg='text', bg='base', fontsize=16, text="?"):
    return widget.TextBox(
        **base(fg, bg),
        fontsize=fontsize,
        text=text,
        padding=3
    )


widget_list = [
    widget.Sep(linewidth=0, padding=6, background=colors["base"]),
    widget.GroupBox(
        font="JetBrainsMono Nerd Font",
        fontsize=18,
        margin_y=0,
        margin_x=0,
        padding_y=10,
        padding_x=10,
        borderwidth=3,
        active=colors["mauve"],
        inactive=colors["lavender"],
        rounded=False,
        highlight_method='line',
        highlight_color=[colors["base"], colors["base"]],
        this_current_screen_border=colors["green"],
        this_screen_border=colors["green"],
        other_current_screen_border=colors["lavender"],
        other_screen_border=colors["lavender"],
        foreground=colors["lavender"],
        background=colors["base"],
        block_highlight_text_color=colors["green"]
    ),

    widget.Spacer(length=bar.STRETCH, background=colors["base"]),

    # --- System Usage Group (Mauve) ---
    powerline_arrow("mauve", "base"),
    icon(fg="base", bg="mauve", text=""),  # CPU Icon
    widget.CPU(
        format='{load_percent}%',
        foreground=colors["base"],
        background=colors["mauve"],
        update_interval=5
    ),
    icon(fg="base", bg="mauve", text="﬙"),   # RAM Icon
    widget.Memory(
        format='{MemUsed:.0f}M',
        foreground=colors["base"],
        background=colors["mauve"],
        update_interval=5
    ),

    # --- Net Group (Blue) ---
    powerline_arrow("blue", "mauve"),
    icon(fg="base", bg="blue", text=""),   # Wifi Icon
    widget.Net(
        foreground=colors["base"],
        background=colors["blue"],
        update_interval=5
    ),

    # --- Volume Group (Pink) ---
    powerline_arrow("pink", "blue"),
    icon(fg="base", bg="pink", text=""),  # Volume Icon
    widget.Volume(
        foreground=colors["base"],
        background=colors["pink"],
        fmt='{}',
    ),

    # --- Clock (Lavender) ---
    powerline_arrow("lavender", "pink"),
    icon(fg="base", bg="lavender", text=""),   # Calendar Icon
    widget.Clock(
        format='%a %d %b %H:%M',
        foreground=colors["base"],
        background=colors["lavender"],
    ),

    widget.Sep(linewidth=0, padding=10, background=colors["lavender"]),

    powerline_arrow("green", "lavender"),
    widget.Systray(
        background=colors["green"],
        icon_size=20,
        padding=20,
        borderwidth=0,
        border_color=colors["base"]),

    widget.Sep(linewidth=0, padding=10, background=colors["green"]),
]
