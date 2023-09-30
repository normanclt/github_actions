import os
from datetime import datetime
from pathlib import Path
from typing import *
from icecream.icecream import ic
from services.resource_connectors import *
from services.config_manager import Config_Manager


class Activity_Logger(object):
    _instance = None

    def __new__(cls, config_manager: Config_Manager, sshfs_connector: SSHFS_Connector, clear: bool = False):
        if cls._instance == None or clear:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, config_manager: Config_Manager, sshfs_connector: SSHFileSystem, clear: bool = False):
        self.config_manager = config_manager
        self.sshfs_connector = sshfs_connector
        self.setup_log_file()

    def log_activity(self, identifier):
        file_entries = self.sshfs_connector.read_file(self.log_file)
        file_entries.insert(0, f"{identifier}\n")
        self.sshfs_connector.write_file(self.log_file, file_entries)

    def setup_log_file(self) -> None:
        self.log_file = f"{self.config_manager.log_directory}/{datetime.now().date()}.log"
        if not self.sshfs_connector.exists(self.log_file):
            print(f"Log FILE not found. Log file created: {self.log_file}")
            self.sshfs_connector.create_file(self.log_file)
        else:
            print(f"Log File: {self.log_file}")

    @property
    def recent_log_file(self) -> Any:
        ls_list = self.sshfs_connector.ls(
            self.config_manager.log_directory, detail=True)
        log_files = [entry for entry in ls_list if "file" in entry["type"]
                     if entry["name"].endswith(".log")]
        return max(log_files, key=lambda dictio: dictio["mtime"])["name"]

    @property
    def latest_activity(self):
        with self.sshfs_connector.open(self.recent_log_file, "r") as stream:
            activity = stream.readline()
        if len(activity) == 0:
            return None
        return activity.strip("\n")
