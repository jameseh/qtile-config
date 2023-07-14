# -*- coding: utf-8 -*-

import re
from pathlib import Path

from libqtile.lazy import lazy
from libqtile import hook, qtile
from libqtile.config import Key, Match

from keybinds import keys, mouse, mod
from groups import groups
from screens import screens
from layouts import layouts, layout_floating
from utils.process_manager import ProcessManager


# Path to text file containing programs to start/kill.
programs_file = Path.home().joinpath(".config", "qtile", "programs.txt")


# Assign and send new clients to their respective group/workspace
@hook.subscribe.client_new
def assign_window_to_group(client):
    group = None

    # Compile regular expressions to match the window classes or titles
    firefox_regex = re.compile(r"^Mozilla\/(.*)", re.IGNORECASE)
    alacritty_regex = re.compile(r"^Alacritty$", re.IGNORECASE)
    discord_regex = re.compile(r"^Discord$", re.IGNORECASE)
    signal_regex = re.compile(r"^Signal$", re.IGNORECASE)
    libreoffice_regex = re.compile(r"^LibreOffice$", re.IGNORECASE)
    pycharm_regex = re.compile(r"^PyCharm$", re.IGNORECASE)
    webstorm_regex = re.compile(r"^WebStorm$", re.IGNORECASE)
    idea_regex = re.compile(r"^IntelliJ IDEA$", re.IGNORECASE)
    rider_regex = re.compile(r"^Rider$", re.IGNORECASE)
    vlc_regex = re.compile(r"^VLC$", re.IGNORECASE)

    floating_window_classes_regexes = [
        re.compile(r"^confirmreset$", re.IGNORECASE),
        re.compile(r"^makebranch$", re.IGNORECASE),
        re.compile(r"^maketag$", re.IGNORECASE),
        re.compile(r"^ssh-askpass$", re.IGNORECASE),
        re.compile(r"^moni-py(.*)", re.IGNORECASE),
        re.compile(r"^copyq$", re.IGNORECASE),
        ]
    floating_window_titles_regexes = [
        re.compile(r"^branchdialog$", re.IGNORECASE),
        re.compile(r"^pinentry$", re.IGNORECASE),
        ]

    # Assign the window to the appropriate group.
    if firefox_regex.match(client.window.get_wm_class()[0]):
        group = qtile.groups_map["language"]

    elif alacritty_regex.match(client.window.get_wm_class()[0]):
        group = qtile.groups_map["terminal"]

    elif any(regex.match(client.window.get_wm_class()[0]) for regex in
             [pycharm_regex, webstorm_regex, idea_regex, rider_regex]):
        group = qtile.groups_map["code"]

    elif vlc_regex.match(client.window.get_wm_class()[0]):
        group = qtile.groups_map["music"]

    elif discord_regex.match(client.window.get_wm_class()[0]) or \
            signal_regex.match(client.window.get_wm_class()[0]):
        group = qtile.groups_map["chat"]

    elif libreoffice_regex.match(client.window.get_wm_class()[0]):
        group = qtile.groups_map["text_snippet"]

    elif any(regex.match(client.window.get_wm_class()[0])
             for regex in floating_window_classes_regexes) or any(
                     regex.match(client.window.get_name())
                     for regex in floating_window_titles_regexes):
        client.floating = True

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


# Set widget defaults
widget_defaults = dict(
    font='Noto Sans Mono',
    fontsize=12,
    padding=5,
)

follow_mouse_focus = True
bring_front_click = True
cursor_warp = True
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = False
wmname = "LG3D"
