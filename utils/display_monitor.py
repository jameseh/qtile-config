#!/bin/python
import sys
import subprocess
import asyncio

import tkinter as tk
from Xlib import X
from Xlib import display as X_display
from Xlib.ext import randr


class DisplayMonitor:
    """A class to monitor and set xorg display configuations."""

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
        print(event)
        if event.type == X.ConfigureNotify:
            displays = self.connected_displays()
            if displays > self.prev_displays:
                self.prev_displays = self.displays
                self.displays = displays
                self.show_dialog()

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
                if output == primary_output:
                    displays.append(
                            (display_name, display_modes, "primary",
                             "active" if output_info.crtc != 0 else "inactive")
                            )
                else:
                    displays.append(
                            (display_name, display_modes,
                             "active" if output_info.crtc != 0 else "inactive")
                            )
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

    def turn_on_display(self, display_name, mode, primary):
        subprocess.Popen(f"xrandr --output {display_name} \
        {'--primary' if primary else ''} --mode {mode} --pos 0x0 \
        --rotate  normal", shell=True)

    def turn_off_display(self, display_name):
        subprocess.Popen(f"xrandr --output {display_name} --off", shell=True)

    def show_dialog(self):
        dialog = DisplayDialog(self)
        dialog.show()


class DisplayDialog:
    def __init__(self, display_monitor):
        self.display_monitor = display_monitor
        self.displays = self.display_monitor.connected_displays()
        self.root = tk.Tk()
        self.root.title("Displays")
        self.root.call('tk', 'scaling', 5)
        self.selected_displays = []

    def show(self):
        frame = tk.Frame(self.root)
        label = tk.Label(frame, text="Select the monitors to turn on/off:")
        label.grid(row=0, column=0, columnspan=2)

        for i, display_info in enumerate(self.displays):
            display_name = display_info[0]
            modes = display_info[1][:10]  # Limit to the first 10 modes

            display_frame = tk.Frame(frame)
            display_frame.grid(row=i // 2, column=i % 2)

            display_label = tk.Label(display_frame, text=f"{display_name}")
            display_label.grid(row=0, column=0, columnspan=5)

            var_display = tk.IntVar(
                    value=1 if display_name in
                    self.display_monitor.connected_displays() else 0)
            display_check_box = tk.Checkbutton(
                    display_frame, variable=var_display)
            display_check_box.grid(row=1, column=0, columnspan=5)
            display_check_box.config(
                    command=self.create_toggle_modes_func(var_display, i))

            var_modes = []
            for j, mode in enumerate(modes):
                var_mode = tk.IntVar(value=1 if j == 0 else 0)
                mode_check_box = tk.Checkbutton(
                        display_frame, text=mode, variable=var_mode,
                        state=tk.DISABLED)
                mode_check_box.grid(row=(j // 5) + 2, column=j % 5)
                var_modes.append((mode, mode_check_box, var_mode))

            self.selected_displays.append(
                    (display_name, var_display, var_modes))

        button = tk.Button(frame, text="Submit", command=self.submit)
        button.grid(row=(len(self.displays) // 2) + 3, column=0, columnspan=5)

        frame.pack()
        self.root.mainloop()

    def create_toggle_modes_func(self, var_display, index):
        def toggle_modes():
            var_modes = self.selected_displays[index][2]
            state = tk.NORMAL if var_display.get() == 1 else tk.DISABLED
            for _, mode_check_box, _ in var_modes:
                mode_check_box.configure(state=state)
        return toggle_modes

    def submit(self):
        for display_name, var_display, var_modes in self.selected_displays:
            if var_display.get() == 0:
                self.display_monitor.turn_off_display(display_name)
            else:
                selected_mode = None
                for mode, mode_check_box, mode_var in var_modes:
                    if mode_var.get() == 1:
                        selected_mode = mode
                        break

                if selected_mode:
                    self.display_monitor.turn_on_display(
                            display_name, selected_mode, primary=False)
                else:
                    # If no mode is selected, turn on display with first mode
                    self.display_monitor.turn_on_display(
                            display_name, var_modes[0][0], primary=False)

        self.root.destroy()


if __name__ == "__main__":
    display_monitor = DisplayMonitor()
