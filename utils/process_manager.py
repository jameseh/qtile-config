import subprocess
import sys
from pathlib import Path
import psutil
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ProcessManager:
    """
    A simple process manager that can start and kill processes.

    Usage:
        process_manager = ProcessManager("programs.txt")
        process_manager.start_processes()
        print(f"{len(process_manager.processes)} processes are running")
        process_manager.kill_processes()

    Programs file format:
        The programs file contains lines in the format `program_name number_of_instances`.
        If the number of instances is not specified, it defaults to 1.

        Example:
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
            raise FileNotFoundError(f"'{self.programs_file}' not found.")

        with open(self.programs_file, "r") as f:
            for line_num, line in enumerate(f, start=1):
                stripped_line = line.strip()
                if stripped_line:
                    try:
                        parts = stripped_line.split(maxsplit=1)
                        program_name = parts[0]
                        number_of_instances = int(parts[1]) if len(parts) > 1 else 1
                    except ValueError:
                        logging.error(f"Invalid format on line {line_num}: '{line.strip()}'")
                        continue

                    running_processes = self._count_running_instances(program_name)
                    instances_to_start = number_of_instances - running_processes

                    for _ in range(instances_to_start):
                        try:
                            process = subprocess.Popen([program_name], shell=False)
                            self.processes.append(process)
                            logging.info(f"Started '{program_name}' (PID: {process.pid})")
                        except Exception as e:
                            logging.error(f"Failed to start '{program_name}': {e}")

        self.all_processes_launched = True

    def _count_running_instances(self, program_name):
        """Helper method to count currently running instances of a given program."""
        return sum(1 for p in psutil.process_iter(attrs=["name"]) if p.info["name"] == program_name)

    def kill_processes(self):
        for process in self.processes:
            try:
                logging.info(f"Terminating process PID: {process.pid}")
                process.terminate()
                gone, alive = psutil.wait_procs([process], timeout=5, callback=self._on_terminate)

                for child in alive:
                    logging.warning(f"Killing child process PID: {child.pid}")
                    child.kill()
            except psutil.NoSuchProcess:
                logging.warning(f"Process PID {process.pid} does not exist.")
            except Exception as e:
                logging.error(f"Error terminating process PID {process.pid}: {e}")
        self.processes.clear()

    def _on_terminate(self, proc):
        logging.info(f"Process PID: {proc.pid} has terminated.")

    def __del__(self):
        if self.processes:
            logging.info("Cleaning up remaining processes...")
            self.kill_processes()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Usage: python process_manager.py <programs_file>")
        sys.exit(1)

    programs_file = sys.argv[1]
    process_manager = ProcessManager(programs_file)
    
    try:
        process_manager.start_processes()
    finally:
        process_manager.kill_processes()
