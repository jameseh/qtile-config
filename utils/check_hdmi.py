# -*- mode: python ; coding: utf-8 -*-

import subprocess


class HDMIMonitor:
  """
     A class to check if the HDMI monitor is plugged in and execute the
     xrandr command.
  """

  def __init__(self):
    """Initialize the class."""
    self.hdmi_connected = False

  def check_hdmi(self):
    """Check if the HDMI monitor is plugged in."""
    output = subprocess.check_output(["xrandr", "--query"])
    for line in output.decode("utf-8").splitlines():
      if "HDMI-1-0" in line:
        self.hdmi_connected = True

  def execute_xrandr_command(self):
    """Execute the xrandr command."""
    subprocess.call([
        "xrandr", "--output", "eDP-1", "--off",
                  "--output", "HDMI-1-0", "--primary", "--mode",
                      "2560x1440", "--pos", "0x0", "--rotate", "normal"])


if __name__ == "__main__":
  hdmi_monitor = HDMIMonitor()
  hdmi_monitor.check_hdmi()

  if hdmi_monitor.hdmi_connected:
    hdmi_monitor.execute_xrandr_command()
  else:
    print("HDMI is not plugged in")

