import sys
import subprocess
from pathlib import Path

import psutil


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
                print(stripped_line)
                # Only start a process if the line isn't empty
                if stripped_line:
                    try:
                        # Get the program name and number of instances to start
                        (program_name,
                         number_of_instances) = stripped_line.split()
                    except ValueError:
                        # Ignore empty lines and lines with only program name
                        program_name = stripped_line
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
                                Path(program_name), shell=False)
                            self.processes.append(process)
                        except subprocess.CalledProcessError:
                            # Ignore any errors that occur
                            pass

    def kill_processes(self):
        for process in self.processes:
            # Only try to kill the process if it's still running
            if process.poll() is None:
                try:
                    # Try to terminate the process gracefully
                    process.terminate()
                    # Give the process some time to terminate gracefully
                    process.wait(timeout=5)

                except subprocess.TimeoutExpired:
                    # If the process didn't terminate within the timeout,
                    # kill it
                    gone, alive = psutil.wait_procs(
                        [process], timeout=5, callback=on_terminate)
                    if process in alive:
                        process.kill()

                except OSError:
                    # Ignore any errors that occur
                    pass

        # Now kill any child processes that are still running
        for process in self.processes:
            for child_process in process.children():
                if child_process.poll() is None:
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
