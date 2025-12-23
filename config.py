import re
import subprocess
from pathlib import Path

from libqtile import hook, qtile, layout, widget, bar
from libqtile.config import Key, Click, Drag, Group, Screen
from libqtile.lazy import lazy
from utils.process_manager import ProcessManager
from color_scheme import colors
from widgets_config import widget_list
from keys_config import keys, mod
from groups_config import groups


home = Path.home()
programs_file = Path.home().joinpath(".config", "qtile", "programs.txt")


# Bind the key combinations to switch to the groups.
for i, group in enumerate(groups, 1):
    keys.append(Key([mod], str(i), lazy.group[group.name].toscreen()))
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(group.name)))

# Colors imported from color_scheme.py
widget_defaults = dict(
        font='JetBrainsMono Nerd Font',
        fontsize=14,
        padding=4,
)

layout_floating = layout.Floating(
        float_rules=[*layout.Floating.default_float_rules])

# Define layouts
layouts = [
        layout.MonadTall(
                font="JetBrainsMono Nerd Font",
                font_size=14,
                border_focus=colors["green"],
                border_width=2,
                border_normal=colors["lavender"],
                margin=8
        ),
        layout.Max(
                font="JetBrainsMono Nerd Font",
                font_size=14,
                border_width=0,
                margin=8
        ),
]


# Widget list imported from widgets_config.py


command = "xrandr --listmonitors"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
stdout, _ = process.communicate()
monitor_count = stdout[-1]

# Define screens and bar
screens = [
        Screen(
            top=bar.Bar(
                widgets=widget_list,
                size=33,
                opacity=1.0,
                border_width=4,
                border_color=colors["mantle"],
                margin=[4, 4, 0, 4],
                background=colors["base"],
            ),

        ),
    ]


@hook.subscribe.client_new
def assign_window_to_group(client):
    group = None

    # Compile regular expressions to match the window classes or
    # titles
    firefox_regex = re.compile(r"^Mozilla/.*$", re.IGNORECASE)
    alacritty_regex = re.compile(r"^Alacritty$", re.IGNORECASE)
    discord_regex = re.compile(r"^Discord$", re.IGNORECASE)
    signal_regex = re.compile(r"^Signal$", re.IGNORECASE)
    libreoffice_regex = re.compile(r"^LibreOffice$", re.IGNORECASE)
    pycharm_regex = re.compile(r"^PyCharm$", re.IGNORECASE)
    webstorm_regex = re.compile(r"^WebStorm$", re.IGNORECASE)
    idea_regex = re.compile(r"^IntelliJ IDEA$", re.IGNORECASE)
    rider_regex = re.compile(r"^Rider$", re.IGNORECASE)
    vlc_regex = re.compile(r"^VLC$", re.IGNORECASE)
    steam_regex = re.compile(r"^Steam$", re.IGNORECASE)
    copyq_regex = re.compile(r"^copyq$", re.IGNORECASE)

    floating_window_classes_regexes = [
            re.compile(r"^confirmreset$", re.IGNORECASE),
            re.compile(r"^makebranch$", re.IGNORECASE),
            re.compile(r"^maketag$", re.IGNORECASE),
            re.compile(r"^ssh-askpass$", re.IGNORECASE),
            re.compile(r"^moni-py.*$", re.IGNORECASE),
            copyq_regex,
    ]
    floating_window_titles_regexes = [
            re.compile(r"^branchdialog$", re.IGNORECASE),
            re.compile(r"^pinentry$", re.IGNORECASE),
    ]
    # Assign the window to the appropriate group.
    if firefox_regex.match(client.window.get_wm_class()[0]):
        group = qtile.groups_map[groups[0].name] # Browser

    elif alacritty_regex.match(client.window.get_wm_class()[0]):
        group = qtile.groups_map[groups[1].name] # Terminal

    elif any(
            regex.match(client.window.get_wm_class()[0]) for regex in
            [pycharm_regex, webstorm_regex, idea_regex, rider_regex]
    ):
        group = qtile.groups_map[groups[2].name] # Code

    elif steam_regex.match(client.window.get_wm_class()[0]) or \
            vlc_regex.match(client.window.get_wm_class()[0]):
        group = qtile.groups_map[groups[3].name] # Music/Video

    elif discord_regex.match(client.window.get_wm_class()[0]) or \
            signal_regex.match(client.window.get_wm_class()[0]):
        group = qtile.groups_map[groups[4].name] # Chat

    elif libreoffice_regex.match(client.window.get_wm_class()[0]):
        group = qtile.groups_map[groups[5].name] # Text

    elif any(
            regex.match(client.window.get_wm_class()[0])
            for regex in floating_window_classes_regexes
    ) or any(
            regex.match(client.window.get_name())
            for regex in floating_window_titles_regexes
    ):
        client.floating = True

    if copyq_regex.match(client.window.get_wm_class()[0]):
        client.togroup()

    if group:
        client.togroup(group.name)


@hook.subscribe.startup_once
def start_apps():
    # Initiate process manager class to autostart and kill applications
    process_manager = ProcessManager(programs_file)
    process_manager.start_processes()

    @hook.subscribe.shutdown
    def exit_qtile():
        process_manager.kill_processes()


follow_mouse_focus = True
bring_front_click = True
cursor_warp = True
auto_fullscreen = True
focus_on_window_activation = "focus"
reconfigure_screens = True
auto_minimize = False
wmname = "LG2D"
