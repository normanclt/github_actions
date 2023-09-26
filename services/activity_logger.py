import os
from datetime import datetime
from pathlib import Path
from typing import *
from icecream.icecream import ic


class Activity_Logger(object):
    _instance = None
    _log_directory = Path(r'../data/logs')

    def __new__(cls, identifier: str, filename: str, clear: bool = False):
        if cls._instance == None or clear:
            ic("Creating Instance")
            cls._instance = object.__new__(cls)
        else:
            ic()
            print("Existing instance found!")
        ic()
        print("Instance Returned")
        return cls._instance

    def __init__(self, identifier: str | None, clear: bool = False):
        ic()
        self.setup_log_file()
        if identifier != None:
            self.log_activity(identifier)

    def __call__(self, identifier) -> None:
        self.log_activity(identifier)

    def log_activity(self, identifier):
        with open(self._log_file_path, "r") as f:
            list = f.readlines()
            list.insert(0, (f"{identifier},\n"))
        with open(self._log_file_path, "w") as f:
            f.writelines(list)

    def get_latest_activity(self) -> str:
        with open(self._log_file_path, "r") as input_stream:
            input_stream.seek(0)
            latest_activity = input_stream.readline().strip("\n").strip(",")
            if latest_activity == "":
                return None
            return eval(latest_activity)

    # this is temporary - there's no need for this
    def get_activities(self, activity_line_number: int | None) -> dict | list:
        with open(self.filename, "r") as output_stream:
            if activity_line_number == int:
                return output_stream.readlines()[activity_line_number].strip("\n").strip(",")
            activities = output_stream.readlines()
            return activities

    def setup_log_file(self) -> None:
        self._log_file_path = Path(os.path.join(
            self._log_directory, f"{str(datetime.now().date())}.log"))

    def get_log_file_path(self) -> Path:
        if not hasattr(self, "_log_file_path") or self._log_file_path == "":
            self.setup_log_file()
        return self._log_directory
