from typing import Any
from .activity_logger import Activity_Logger
from io import StringIO
from pathlib import Path
import sysrsync

class Sync_Provider:

    def synchronize(self, if_sync: bool):
        #this is a method to copy files over or even compare then copy where needed
        pass

#
class Rsync_Provider():
    # singleton
    #insert logic that's sctricly just for the provider

    _instance = None

    def __new__(cls, config: Any, clear: bool = False):
        if cls._instance == None or clear:
            print("Creating Instance")
            cls._instance = object.__new__(cls)
        else:
            print("Existing instance found!")
        print("Instance Returned")
        return cls._instance
    
    def __init__(self, config: Any, clear: bool = False):
        self.source_folder = config.source_folder
        self.destination_folder = config.destination_folder
        self.remote_ip = config.remote_ip
        self.ssh_user = config.ssh_user
        if config.ssh_private_key == str:
            self.ssh_private_key = StringIO(config.ssh_private_key)
        else:
            self.ssh_private_key = config.ssh_private_key
        self.activity_logger = Activity_Logger()  #I think this should be included in a config manager

    def synchronize(self):
        # if this finishes then input dictionary key "completed_sync_commit_sha" : commited_sha
        ## decomp - gathering data of activity and process of saving it in the activity log
        ## ? Perhaps you don't need to save the source commit sha 
        ## ? This application should be agnostic of which is the source commit sha until you gather latest commit

        sysrsync.run(verbose=True, source=self.source_folder, destination=self.destination_folder,
             destination_ssh=f"{self.ssh_user}@{self.remote_ip}", options=["-arvc"], private_key=self.ssh_private_key, sync_source_contents=True, strict_host_key_checking=False)
       #sudo code: 
       # activity_logger.log_activity('current commit sha as copied from the source commit sha') 

   



class Repo_Provider():
    # insert repo configuration
    _instance = None

    def __new__(cls, data: dict, filename: str, clear: bool = False):
        if cls._instance == None or clear:
            print("Creating Instance")
            cls._instance = object.__new__(cls)
        else:
            print("Existing instance found!")
        print("Instance Returned")

    # compare github01 latest commit on main and log
    # leverage function to synch_check_requirement
    #

    def synchronize(self, fn_sync_check_requirement):
        
        pass

    def IsSynchronizationRequired(self):
