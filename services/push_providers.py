from typing import Any
from .activity_logger import Activity_Logger
from io import StringIO
from pathlib import Path
import sysrsync
from services.config_manager_temp import Config_Manager
import os


class Push_Provider:

    def push(self, if_sync: bool):
        # reference source
        # reference destination
        # PUSH
        pass

#


class Rsync_Provider(object):
    # singleton
    # insert logic that's sctricly just for the provider

    _instance = None

    def __new__(cls, config_manager: Config_Manager, activity_logger: Activity_Logger, clear: bool = False):
        if cls._instance == None or clear:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, config_manager: Config_Manager, activity_logger: Activity_Logger, clear: bool = False):
        self.source_folder = config_manager.source_folder
        self.destination_folder = config_manager.destination_folder
        self.remote_ip = config_manager.remote_ip
        self.ssh_user = config_manager.ssh_user
        self.ssh_private_key = config_manager.ssh_private_key
        self.exclusions = config_manager.exclusions
        self.activity_logger = activity_logger

    def push(self, identifier: str):
        # consider direction of data flow (source to target)

        print(f"{self.source_folder} is a dir:{os.path.isdir(self.source_folder)}")
        print(
            f"{'../sync/random/files'} is a dir:{os.path.isdir('../sync/random_files')}")
        result = sysrsync.run(verbose=True,
                              source=self.source_folder,
                              destination=self.destination_folder,
                              destination_ssh=f"{self.ssh_user}@{self.remote_ip}",
                              options=["-arvc"],
                              private_key=self.ssh_private_key,
                              exclusions=self.exclusions,
                              sync_source_contents=True,
                              strict_host_key_checking=False)
        if result.returncode == 0 or None:
            self.activity_logger.log_activity(identifier)
       # activity_logger.log_activity('current commit sha as copied from the source commit sha')
