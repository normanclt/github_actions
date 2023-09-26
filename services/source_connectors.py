from services.config_manager import Config_Manager
from github import Github, Auth
from icecream import ic
from typing import Any


class Source_Connector:
    def gather_info(self):
        pass


class Github_Source:
    _instance = None

    def __new__(cls, config: Config_Manager, clear: bool = False):
        if cls._instance == None or clear:
            ic("Creating Instance")
            cls._instance = object.__new__(cls)
        else:
            ic()
            print("Existing instance found!")
        ic()
        print("Instance Returned")
        return cls._instance

    def __init__(self, config: Config_Manager, clear: bool = False):
        auth = Auth.Token(config.github_api_token)
        self.github = Github(auth=auth)
        self.repo_name = config.repo_name
        self.branch_name = config.branch_name
        self.organization_name = config.organization_name
        self.get_branch()

        '''Returns a reference to branch of a repo'''

    def get_branch(self):
        Github
        return self.github.get_repo(f"{self.organization_name}/{self.repo_name}")
