from services.push_providers import *
from services.config_manager import Config_Manager
from services.activity_logger import Activity_Logger
from services.resource_connectors import Github_Connector, SSHFS_Connector
from io import StringIO, BytesIO
import subprocess


class Sync_Controller():
    _instance = None

    def __new__(cls, config_manager: Config_Manager,
                activity_logger: Activity_Logger,
                sshfs_connector: SSHFS_Connector,
                github_connector: Github_Connector,
                rsync: Rsync_Provider,
                clear: bool = False):
        if cls._instance == None or clear:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, config_manager: Config_Manager,
                 sshfs_connector: SSHFS_Connector,
                 activity_logger: Activity_Logger,
                 github_connector: Github_Connector,
                 rsync_provider: Rsync_Provider,
                 clear: bool = False):
        self.config_manager = config_manager
        self.sshfs_connector = sshfs_connector
        self.activity_logger = activity_logger
        self.github_connector = github_connector
        self.rsync_provider = rsync_provider

    def generate_private_key(self):

        ssh_private_key_filepath = "ssh_private_key"
        with open(ssh_private_key_filepath, "w") as stream:
            stream.write(self.config_manager.ssh_private_key)
        chmod_private_key = subprocess.run(
            ["chmod", "0600", ssh_private_key_filepath],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"STDOUT: {chmod_private_key.stdout}")
        print(f"STDERR: {chmod_private_key.stderr}")
        return ssh_private_key_filepath

    def status_check(self):
        fixlet_repo_identifier = self.github_connector.state_identifier
        remote_aws_identifier = self.activity_logger.latest_activity
        print("=================================================")
        print(f"fixlet_repo_identifier:{fixlet_repo_identifier}")
        print(f"remote_aws_identifier:{remote_aws_identifier}")
        print("=================================================")

    def exec_sync(self) -> bool:
        if self.github_connector.state_identifier != self.sshfs_connector.state_identifier:
            result = self.rsync_provider.push(
                self.github_connector.state_identifier)
            print(result)
            print(dir(result))
            print(result.returncode)
