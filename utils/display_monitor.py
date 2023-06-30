import subprocess
import time
import tk


class DisplayMonitor:
    """A class to monitor and set xorg display configuations."""

    def __init__(self, primary_display):
        self.primary_display = primary_display
        self.monitor_is_active = False
        self.displays = self.active_displays()

    def connected_displays(self):
        """Checks if the monitor is connected."""
        output = subprocess.check_output(["xrandr", "--listmonitors"])
        displays = []
        for line in output.decode("utf-8").splitlines()[2:]:
            columns = line.split()
            displays.append(columns[0])
        return displays

    def active_displays(self):
        displays = self.connected_displays()
        for display in displays:
            if display.is_turned_on():
                self.displays.append(display)

    def monitor_displays(self):
        """Monitors for connected and disconnected displays."""
        if self.monitor_is_active:
            displays = self.connected_displays()
            for display in displays:
                if display not in self.displays:
                    self.displays.append(display)
                    self.display_dialog = DisplayDialog(self, self.displays)
                    self.display_dialog.select_display_configuration(
                            self.displays)
                else:
                    displays.remove(display)
            time.sleep(1)

    def start_monitoring_displays(self):
        """Starts monitoring displays."""
        self.monitor_is_active = True

    def stop_monitoring_displays(self):
        """Stops monitoring displays."""
        self.monitor_is_active = False

    def turn_on_display(self, display):
        """Turns on a display."""
        subprocess.call(["xrandr", "--output", display, "--on"])

    def turn_off_display(self, display):
        """Turns off a display."""
        subprocess.call(["xrandr", "--output", display, "--off"])

    def is_turned_on(self, display):
        """Checks if the display monitor is turned on."""
        output = subprocess.check_output(["xrandr", "--query"])
        for line in output.decode("utf-8").splitlines():
            columns = line.split()
            if line == display:
                if columns[2] == "connected":
                    return True
                else:
                    return False
        return False


class DisplayDialog:
    def __init__(self, display_monitor, displays):
        self.display_monitor = display_monitor
        self.displays = displays

    def select_display_configuration(self):
        """
           Launches a tkinter dialog and allows you to select the display
           configuration.
        """
        root = tk.Tk()

        label = tk.Label(root, text="Select the monitors to turn on/off:")
        label.pack()

        checked_displays = []
        for i in range(len(self.displays)):
            check_box = tk.Checkbutton(root, text=str(i + 1))
            check_box.pack()
            if check_box.select():
                checked_displays.append(self.displays[i])

        self.display_monitor.active_displays = checked_displays

        button = tk.Button(root, text="Submit", command=root.destroy)
        button.pack()

        root.mainloop()

        selected_displays = []
        for i in range(len(checked_displays)):
            if checked_displays[i].get():
                selected_displays.append(i + 1)

        return selected_displays


if __name__ == "__main__":
    display_monitor = DisplayMonitor("eDP-1")
    display_monitor.start_monitoring_displays()
    # Call stop_monitoring_displays on desktop environment or window
    # manaager close.
    display_monitor.stop_monitoring_displays()
