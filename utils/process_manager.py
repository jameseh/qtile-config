# -*- coding: utf-8 -*-

import sys
import subprocess
from pathlib import Path


class ProcessManager:
    def __init__(self, programs_file):
        self.programs_file = Path(programs_file)
        self.processes = []

    def start_processes(self):
        if not self.programs_file.exists():
            raise FileNotFoundError(
                    f"FileNotFoundError: '{self.programs_file}'"
                    )

        with open(self.programs_file, "r") as f:
            for line in f:
                # Remove leading and trailing whitespace
                stripped_line = line.strip()

                # Only start a process if the line isn't empty
                if stripped_line:
                    process = subprocess.Popen(stripped_line, shell=True)
                    self.processes.append(process)

    def kill_processes(self):
        for process in self.processes:
            # Only try to kill the process if it's still running
            if process.poll() is None:
                try:
                    process.terminate()
                    try:
                        # Give the process some time to terminate gracefully
                        process.wait(timeout=5)

                    except subprocess.TimeoutExpired:
                        # If the process didn't terminate within the timeout,
                        # kill it
                        process.kill()

                except OSError:
                    pass


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please provide a programs list .txt file")
        sys.exit(1)

    programs_file = sys.argv
    process_manager = ProcessManager(programs_file)
    process_manager.start_processes()
    process_manager.kill_processes()
