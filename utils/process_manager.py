# -*- mode: python ; coding: utf-8 -*-

import sys
import subprocess
from pathlib import Path

import psutil


class ProcessManager:
    """
       A simple process manager that can start and kill processes.

       The process manager takes a list of programs and the number of instances
       to start for each program. It will start the specified number of
       instances of each program, and will kill all of the processes when it
       is destroyed.

    Usage:

        ```
        process_manager = ProcessManager("programs.txt")
        process_manager.start_processes()
        print(f"{len(process_manager.processes)} processes are running")
        process_manager.kill_processes()
        ```

    Programs file format:

        The programs file is a text file that contains a list of programs and
        the number of instances to start for each program. Each line in the
        file should be in the format program_name number_of_instances. If the
        number of instances is not specified, it defaults to 1.

        For example, the following lines would start two instances of the
        alacritty program and one instance of the firefox program:

        ```
        alacritty 2
        firefox
        ```
    """
    def __init__(self, programs_file):
        self.programs_file = Path(programs_file)
        self.processes = []
        self.all_processes_launched = False

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
                    try:
                        # Get the program name and number of instances to start
                        (program_name,
                         number_of_instances) = line.rsplit()
                    except ValueError:
                        # Ignore empty lines and lines with only program name
                        program_name = line.strip()
                        number_of_instances = 1

                    # Count the number of instances of the app running
                    running_processes = len(
                        [process for process in psutil.process_iter()
                         if process.name() == program_name])

                    # Start the remaining instances of the app
                    for _ in range(int(number_of_instances)
                                   - int(running_processes)):
                        try:
                            # Start the process directly
                            process = subprocess.Popen(
                                    Path(program_name),
                                    shell=False)
                            self.processes.append(process)
                        except Exception:
                            # Ignore any errors that occur
                            pass

        self.all_processes_launched = True

    def kill_processes(self):
        for process in self.processes:
            # Terminate the process and all of its children
            gone, alive = psutil.wait_procs(
                    [process], timeout=5, callback=on_terminate)

            # If any child processes are still alive, kill them
            for child_process in alive:
                child_process.kill()


def on_terminate(proc):
    print(f"process {proc} terminated with exit code {proc.returncode}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please provide a programs list .txt file")
        sys.exit(1)

    programs_file = sys.argv[1]
    process_manager = ProcessManager(programs_file)
    process_manager.start_processes()
    print(f"{len(process_manager.processes)} processes are running")
    process_manager.kill_processes()
