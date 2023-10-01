from services.config_manager_temp import Config_Manager
from github import Github, Auth
from icecream import ic
from typing import Any
from paramiko import SSHClient, SFTP, AutoAddPolicy, Ed25519Key, client
from sshfs import SSHFileSystem
from datetime import datetime

from pathlib import Path
from io import StringIO


class Resource_Connector:
    @property
    def state_identifier(self):
        pass

    def read_file(self, filepath: str) -> list:
        pass

    def write_file(self, filepath: str, data):
        pass

    def create_file(self, filepath: str):
        pass

    def exists(self, filepath: str) -> bool:
        pass


class Github_Connector():
    _instance = None

    def __new__(cls, config: Config_Manager, clear: bool = False):
        if cls._instance == None or clear:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, config: Config_Manager, clear: bool = False):
        auth = Auth.Token(config.github_api_token)
        self.config = config
        self._repo = Github(auth=auth).get_repo(
            f"{config.organization_name}/{config.repo_name}")
        self._branch = self._repo.get_branch(f"{config.branch_name}")

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

    def retrieve_file(self):
        pass

    def write_to_file(self):
        pass

    def exists(self):
        pass

    def ls(self, path: Any, detail: bool = True, **kwargs: Any) -> list:
        pass


class SSH_Connector(SSHClient):
    _instance = None

    def __new__(cls, config: Config_Manager, clear: bool = False):
        if cls._instance == None or clear:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Config_Manager, clear: bool = False):
        super().__init__()
        self.set_missing_host_key_policy(AutoAddPolicy())
        self.config_manager = config

    def exec_connect(self) -> SSHClient:
        self.connect(self.config_manager.remote_ip,
                     username=self.config_manager.ssh_user,
                     key_filename=self.config_manager.ssh_private_key
                     )

    def read_file(self, filepath: str):
        self.exec_connect()
        with self.open_sftp() as sftp:
            with sftp.file(filepath, "r'") as file:
                return file.read()

    def readline(self, filepath: str):
        self.exec_connect()
        with self.open_sftp() as sftp:
            with sftp.file(filepath, "r'") as file:
                return file.readline().strip("\n")


class SSHFS_Connector(SSHFileSystem):
    _instance = None

    def __new__(cls, config: Config_Manager, clear: bool = False):
        if cls._instance == None or clear:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Config_Manager, clear: bool = False):
        self.config_manager = config
        super().__init__(config.remote_ip,
                         username=config.ssh_user,
                         client_keys=config.ssh_private_key)

    @property
    def state_identifier(self):
        try:
            with self.open(f"{self.config_manager.log_directory}{datetime.now()}.log", "r") as stream:
                return stream.readline()
        except FileNotFoundError as e:
            return None

    def read_file(self, filepath):
        try:
            with self.open(filepath, "r") as stream:
                return stream.readlines()
        except Exception as e:
            print(e)
            return None

    def write_file(self, filepath, data):
        try:
            with self.open(filepath, "w") as stream:
                stream.writelines(data)
        except Exception as e:
            print(e)

    def create_file(self, filepath):
        try:
            print(f"Filepath passed:{filepath}")
            self.touch(f"{filepath}")
        except Exception as e:
            print(e)

    def exists(self, filepath: str) -> bool:
        print(f"Testing existence of \"{filepath}\"")
        try:
            with self.open(filepath, "r") as stream:
                return True
        except Exception as e:
            print(e)
            return False
