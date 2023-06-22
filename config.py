# -*- coding: utf-8 -*-

import re
from pathlib import Path

from libqtile.lazy import lazy
from libqtile import hook, qtile
from libqtile.config import Key

from keybinds import keys, mouse, mod
from groups import groups
from screens import screens
from layouts import layouts
from utils.process_manager import ProcessManager


# Initiate processmanager to autostart and kill applications
programs_file = Path.home().joinpath(".config", "qtile", "programs.txt")
process_manager = ProcessManager(programs_file)

# Set widget defaults
widget_defaults = dict(
    font='Noto Sans Mono',
    fontsize=12,
    padding=5,
)

# Follow the mouse cursor when you move it between windows.
follow_mouse_focus = True

# Bring the window that you click to the front, even if it is not the
# focused window.
bring_front_click = False

# Warp the cursor to the focused window when you focus it.
cursor_warp = True

# Automatically fullscreen windows when they are maximized.
auto_fullscreen = True

# Focus the window that is activated.
focus_on_window_activation = "focus"

# Reconfigure its layout when the screens are resized or moved.
reconfigure_screens = True

# Automatically minimize windows when they are not focused.
auto_minimize = False

# Set its window manager name to "LG3D"
wmname = "LG3D"


# Assign and send new clients to their respective group/workspace
@hook.subscribe.client_new
def assign_window_to_group(client):
    # Compile regular expressions to match the window classes or titles
    firefox_regex = re.compile(r"^mozilla.*", re.IGNORECASE)
    alacritty_regex = re.compile(r"^alacritty$", re.IGNORECASE)
    discord_regex = re.compile(r"^discord.*", re.IGNORECASE)
    signal_regex = re.compile(r"^signal$", re.IGNORECASE)
    libreoffice_regex = re.compile(r"^libre.*", re.IGNORECASE)
    pycharm_regex = re.compile(r"^pycharm$", re.IGNORECASE)
    webstorm_regex = re.compile(r"^webstorm$", re.IGNORECASE)
    idea_regex = re.compile(r"^intellij idea$", re.IGNORECASE)
    rider_regex = re.compile(r"^rider$", re.IGNORECASE)
    vlc_regex = re.compile(r"^vlc$", re.IGNORECASE)

    # Assign the window to the appropriate group.
    if firefox_regex.match(client.window.get_wm_class()[0]) or "firefox" in \
            client.name.lower():
        group = qtile.groups_map["language"]
        keys.append(Key([mod], str(0), lazy.group[client].toscreen()))
        keys.append(Key([mod, "shift"], str(0), lazy.window.togroup(group)))

    elif alacritty_regex.match(client.window.get_wm_class()[0]) or \
            "alacritty" in client.name.lower():
        group = qtile.groups_map["terminal"]

    elif any(regex.match(client.window.get_wm_class()[0]) for regex in
             [pycharm_regex, webstorm_regex, idea_regex, rider_regex]) and (
                     "pycharm" in client.name.lower() or "webstorm" in
                     client.name.lower() or "intellij idea" in
                     client.name.lower() or "rider" in client.name.lower()):
        group = qtile.groups_map["code"]

    elif vlc_regex.match(client.window.get_wm_class()[0]) or "vlc" in \
            client.name.lower():
        group = qtile.groups_map["music"]

    elif discord_regex.match(client.window.get_wm_class()[0]) or \
            signal_regex.match(client.window.get_wm_class()[0]):
        group = qtile.groups_map["chat"]

    elif libreoffice_regex.match(client.window.get_wm_class()[0]) or \
            "LibreOffice" in client.name:
        group = qtile.groups_map["text_snippet"]

    else:
        # If no matching group is found, assign the window to the "default"
        # group.
        group = qtile.groups_map["default"]

    client.togroup(group.name)


@hook.subscribe.startup
def start_apps():
    process_manager.start_processes()


@hook.subscribe.shutdown
def exit_qtile():
    process_manager.kill_processes()
