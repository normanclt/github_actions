import os
from datetime import datetime
from pathlib import Path
from typing import *
from icecream.icecream import ic
from services.resource_connectors import *
from services.config_manager import Config_Manager


class Activity_Logger(object):
    _instance = None

    def __new__(cls, config_manager: Config_Manager, resource_connector: Resource_Connector, clear: bool = False):
        if cls._instance == None or clear:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, config_manager: Config_Manager, resource_connector: Resource_Connector, clear: bool = False):
        self.config_manager = config_manager
        self.resource_connector = resource_connector
        self.setup_log_file()

    def log_activity(self, identifier):
        file_entries = self.resource_connector.read_file(self.log_file)
        print(file_entries)
        file_entries.insert(0, f"{identifier}\n")
        self.resource_connector.write_file(self.log_file, file_entries)

    def setup_log_file(self) -> None:
        self.log_file = f"{self.config_manager.log_directory}{datetime.now().date()}.log"
        if not self.resource_connector.exists(self.log_file):
            print("no log file exists, creating")
            self.resource_connector.create_file(self.log_file)

    @property
    def latest_activity(self):
        activities = self.resource_connector.read_file(self.log_file)
        if len(activities) == 0:
            return None
        return activities[0].strip("\n")
