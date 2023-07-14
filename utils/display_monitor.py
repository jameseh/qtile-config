#!/bin/python
import sys
import subprocess
import asyncio

import gi
from gi.repository import Gtk

from Xlib import X
from Xlib import display as X_display
from Xlib.ext import randr


class DisplayMonitor:
    """A class to monitor and set xorg display configurations."""

    def __init__(self):
        self.display = X_display.Display()
        self.root_window = self.display.screen().root
        self.event_mask = X.StructureNotifyMask
        self.root_window.change_attributes(event_mask=self.event_mask)
        self.check_for_extensions()
        self.displays = self.connected_displays()
        self.prev_displays = self.displays
        self.pre_wait_on_events()
        asyncio.run(self.wait_for_events())

    async def wait_for_events(self):
        while True:
            event = self.display.next_event()
            if event:
                self.handle_event(event)
            await asyncio.sleep(1)

    def handle_event(self, event):
        if event.type == X.ConfigureNotify:
            displays = self.connected_displays()
            primary_display = next(
                (display for display in self.displays if display[2] == "primary"), None
            )
            if all(display[3] == "inactive" for display in displays):
                self.turn_on_display(
                    primary_display[0], primary_display[1], primary_display[2], primary_display[3]
                )
            elif len(self.prev_displays) < len(displays):
                self.show_dialog()

            self.prev_displays = self.displays
            self.displays = self.connected_displays()


    def connected_displays(self):
        resources = self.root_window.xrandr_get_screen_resources()
        primary_output = resources.crtcs[0]
        displays = []
        for output in resources.outputs:
            output_info = randr.get_output_info(
                self.display, output, X.CurrentTime)
            if output_info.connection == randr.Connected:
                display_name = output_info.name
                display_modes = []
                for mode in resources.modes:
                    width = mode.width
                    height = mode.height
                    display_modes.append(f"{width}x{height}")
                display_status = "active" if output_info.crtc != 0 else "inactive"
                if output_info.crtc == primary_output:
                    primary_display = (display_name, display_modes, "primary", display_status)
                else:
                    displays.append(
                        (display_name, display_modes, "extended", display_status)
                    )
        if primary_display:
            displays.insert(0, primary_display)
        return displays

    def check_for_extensions(self):
        randr_extension = self.display.query_extension('RANDR')
        if not randr_extension.present:
            sys.stderr.write(
                '{}: server does not have the RANDR extension\n'.format(
                    sys.argv[0]))
            sys.exit(1)

        r = self.display.xrandr_query_version()
        print('RANDR version %d.%d' % (r.major_version, r.minor_version))

    def pre_wait_on_events(self):
        if self.displays:
            print(self.displays)
            if len(self.displays) > 1:
                self.show_dialog()

    def calculate_display_position(self):
        active_displays = [display for display in self.displays if display[3] == "active"]
        if active_displays:
            previous_display = active_displays[-1]
            previous_width = int(previous_display[1][0].split("x")[0])
            position = f"{previous_width}x0"
        else:
            position = "0x0"
        return position

    def turn_on_display(self, display_name, modes, primary, state):
        if state == "inactive":
            position = self.calculate_display_position(display_name)
            primary_option = "--primary" if primary == "primary" else ""
            mode_option = "--mode " + modes[0] if modes else ""
            subprocess.Popen(
                f"xrandr --output {display_name} {primary_option} {mode_option} "
                f"--pos {position} --rotate normal",
                shell=True
            )

    def turn_off_display(self, display_name, state):
        if state == "active":
            subprocess.Popen(f"xrandr --output {display_name} --off", shell=True)

    def show_dialog(self):
        dialog = DisplayDialog(self)
        dialog.show()


class DisplayDialog:
    def __init__(self, display_monitor):
        self.display_monitor = display_monitor
        self.displays = self.display_monitor.connected_displays()
        self.selected_displays = []

    def show(self):
        window = Gtk.Window(title="Displays")
        window.set_default_size(300, 200)
        window.set_border_width(20)  # Set the window border width
        window.connect("destroy", Gtk.main_quit)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_box.set_margin_top(20)  # Set top margin
        main_box.set_margin_bottom(20)  # Set bottom margin
        main_box.set_margin_start(20)  # Set left margin
        main_box.set_margin_end(20)  # Set right margin

        window.add(main_box)

        label = Gtk.Label(label="Select the monitors to turn on/off:")
        main_box.pack_start(label, False, False, 0)

        outer_grid = Gtk.Grid()
        outer_grid.set_column_spacing(20)
        outer_grid.set_row_spacing(20)
        main_box.pack_start(outer_grid, False, False, 0)

        row = 0
        column = 0
        for i, display_info in enumerate(self.displays):
            display_name = display_info[0]
            modes = display_info[1][:10]  # Limit to the first 10 modes

            display_grid = Gtk.Grid()
            display_grid.set_column_spacing(10)
            display_grid.set_row_spacing(10)
            outer_grid.attach(display_grid, column, row, 1, 1)

            display_label = Gtk.Label(label=display_name)
            display_grid.attach(display_label, 0, 0, 1, 1)

            display_check_button = Gtk.CheckButton()
            display_check_button.set_active(
                    display_name in [display[0] for display in self.displays])
            display_check_button.connect("toggled", self.toggle_modes, i)
            display_grid.attach(display_check_button, 1, 0, 1, 1)

            mode_grid = Gtk.Grid()
            mode_grid.set_column_spacing(10)
            mode_grid.set_row_spacing(10)
            display_grid.attach(mode_grid, 0, 1, 2, 1)

            var_modes = []
            for j, mode in enumerate(modes):
                mode_check_button = Gtk.CheckButton(label=mode)
                mode_check_button.set_sensitive(j == 0)
                mode_grid.attach(mode_check_button, j % 5, j // 5, 1, 1)
                var_modes.append((mode, mode_check_button))

            self.selected_displays.append((display_name, display_check_button, var_modes))

            column += 1
            if column > 1:
                row += 1
                column = 0

        submit_button = Gtk.Button(label="Submit")
        submit_button.connect("clicked", self.submit)
        outer_grid.attach(submit_button, 0, row + 1, 2, 1)

        window.show_all()
        # Set display check button active if display is active
        for i, display_info in enumerate(self.displays):
            display_name = display_info[0]
            display_check_button = self.selected_displays[i][1]
            if display_info[3] == "active":
                display_check_button.set_active(True)
        Gtk.main()

    def toggle_modes(self, widget, index):
        display_name, _, var_modes = self.selected_displays[index]
        state = widget.get_active()
        for _, mode_check_button in var_modes:
            mode_check_button.set_sensitive(state)

        if not state:
            for _, mode_check_button in var_modes:
                mode_check_button.set_active(False)

    def submit(self, button):
        selected_displays = []
        primary_display_selected = False
        extended_display_selected = False

        for display_name, display_check_button, var_modes in self.selected_displays:
            if display_check_button.get_active():
                selected_modes = [
                    mode for mode, mode_check_button in var_modes if mode_check_button.get_active()
                ]
                if display_name == "primary":
                    primary_display_selected = True
                elif display_name == "extended":
                    extended_display_selected = True

                if selected_modes:
                    state = "active" if is_primary != "primary" \
                            else "inactive"
                    selected_displays.append(
                            (display_name, selected_modes, is_primary, state))

        if not primary_display_selected and not extended_display_selected \
                and len(selected_displays) == 0:
            dialog = Gtk.MessageDialog(
                transient_for=None,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Please select at least one display."
            )
            dialog.run()
            dialog.destroy()
            return

        for display_name, modes, is_primary, state in selected_displays:
            self.display_monitor.turn_on_display(
                    display_name, modes, is_primary, state=state)

        if not primary_display_selected:
            self.display_monitor.turn_off_display(display_name)

        Gtk.main_quit()



if __name__ == "__main__":
    display_monitor = DisplayMonitor()
