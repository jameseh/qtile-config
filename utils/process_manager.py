# -*- coding: utf-8 -*-

import psutil
from pathlib import Path


class ProcessManager:
    def __init__(self, programs_file_path):
        self.programs_file_path = programs_file_path

    def start_processes(self):
        with open(self.programs_file_path, "r") as f:
            for line in f:
                process = psutil.Process(line.strip())
                process.start()

    def kill_processes(self):
        with open(self.programs_file_path, "r") as f:
            for line in f:
                process = psutil.Process(line.strip())
                process.kill()


if __name__ == "__main__":
    programs_file_path = Path("../programs.txt")
    process_manager = ProcessManager(programs_file_path)
    process_manager.start_processes()
    process_manager.kill_processes()
