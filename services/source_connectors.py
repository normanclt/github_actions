from services.config_manager import Config_Manager
from github import Github, Auth
from icecream import ic
from typing import Any
from paramiko import SSHClient, SFTP, AutoAddPolicy, Ed25519Key, client


from pathlib import Path
from io import StringIO


class Repo_API_Connector:
    @property
    def state_identifier(self):
        pass

    @property
    def retrieve_file(self):
        pass

    @property
    def write_to_file(self):
        pass


class Github_Source():
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
        self.config = config
        self._repo = Github(auth=auth).get_repo(
            f"{config.organization_name}/{config.repo_name}")
        self._branch = self._repo.get_branch(f"{config.branch_name}")

    '''returns latest commit'''

    '''returns a github branch reference'''
    @property
    def branch(self):
        return self._branch

    '''return a github repo reference'''
    @property
    def repo(self):
        return self._repo

    @property
    def state_identifier(self):
        return self._branch.commit.sha

    '''Prepared for file read'''
    @property
    def retrieve_file(self):
        pass

    @property
    def write_to_file(self):
        pass


class SSH_Connector():
    _instance = None

    def __new__(cls, config: Config_Manager, clear: bool = False):
        if cls._instance == None or clear:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, config: Config_Manager, clear: bool = False):
        self.sshclient = SSHClient()
        self.sshclient.set_missing_host_key_policy(AutoAddPolicy())
        self.config_manager = config

    def connect(self) -> SSHClient:
        self.sshclient.connect(hostname=self.config_manager.remote_ip,
                               username=self.config_manager.ssh_user,
                               key_filename=self.config_manager.ssh_private_key
                               )

    def read_file(self, filepath: str):
        self.connect()
        with self.sshclient.open_sftp() as sftp:
            with sftp.file(filepath, "r'") as file:
                return file.read()

    def readline(self, filepath: str):
        self.connect()
        with self.sshclient.open_sftp() as sftp:
            with sftp.file(filepath, "r'") as file:
                return file.readline().strip("\n")
