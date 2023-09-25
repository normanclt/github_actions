from github import Github, Auth
from icecream import ic
from typing import Any


class Source_Connector:
    def gather_info(self):
        pass


class Github_Source:
    _instance = None

    def __new__(cls, config: Any, clear: bool = False):
        if cls._instance == None or clear:
            ic("Creating Instance")
            cls._instance = object.__new__(cls)
        else:
            ic()
            print("Existing instance found!")
        ic()
        print("Instance Returned")
        return cls._instance

    def __init__(self, config: Any, clear: bool = False):
        self.auth = Auth.Token(config.github_api_token)
        self.github = Github(self.auth)
        self.repo_name = config.repo_name
        self.branch_name = config.branch_name
        self.organization_name = config.organization_name
        self.github_username = config.github_username
        self.github_password = config.github_password
        self._get_github_api()

    def _get_remote_repo_api(self):
        Github
        return self.github.get_repo(f"{self.github.get_organization(self.organization_name).get_repo(self.repo_name).get_branch(self.branch_name)}")
