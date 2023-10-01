from services.push_providers import *
from services.config_manager_temp import Config_Manager
from services.activity_logger import Activity_Logger
from services.resource_connectors import Github_Connector, SSHFS_Connector
from services.sync_contollers import Sync_Controller
from io import StringIO, BytesIO
import subprocess

# ENV variables from Github Actions Secret
PAT_SUPER_ALL_REPOS = os.environ['PAT_SUPER_ALL_REPOS']
AWS1_IP = os.environ["AWS1_IP"]
AWS1_SSH_KEY = os.environ["AWS1_SSH_KEY"]
AWS1_USER = os.environ["AWS1_USER"]
PAT_FIXLET_REPO = os.environ["PAT_FIXLET_REPO"]
cm = Config_Manager(
    "repo_name",
    "branch_name",
    "organization_name",
    "github_api_token",
    "ssh_user",
    "ssh_private_key",
    "remote_ip",
    "source_folder",
    "destination_folder",
    "log_directory",
    "github_api_token_filepath",
    "github_api_token")

cm.repo_name = 'site_updates_windows_apps_extended'
cm.branch_name = 'publish'
cm.organization_name = 'bigfix'
cm.ssh_user = 'ec2-user'
cm.remote_ip = '52.74.243.47'
# Local
# cm.ssh_private_key = Path(
#     r"D:\Projects\keys\aws_instance_1\aws1\aws1_id_ed25519").as_posix()
cm.log_directory = "/home/ec2-user/rsync/logs"
cm.source_folder = "fixlets/fixlets/"
cm.exclusions = [".git", ".vscode"]
# Local
# cm.source_folder = "sync/random_files/"
cm.destination_folder = "/home/ec2-user/rsync/FIXLETS"
cm.github_api_token = PAT_FIXLET_REPO

# The key needs to be written to disk and permissions changed to accommodate requirements of SSH Server
# use of StringIO didn't work since the SSH key file needs to have permissions changed
ssh_private_key_filepath = "private_key"
with open(ssh_private_key_filepath, "w") as stream:
    stream.write(AWS1_SSH_KEY)
chmod_private_key = subprocess.run(
    ["chmod", "0600", ssh_private_key_filepath],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(f"STDOUT: {chmod_private_key.stdout}")
print(f"STDERR: {chmod_private_key.stderr}")
cm.ssh_private_key = ssh_private_key_filepath


github_connector = Github_Connector(cm)
sshfs_connector = SSHFS_Connector(cm)
activity_logger = Activity_Logger(cm, sshfs_connector)
rsync_provider = Rsync_Provider(cm, activity_logger)
github_connector = Github_Connector(cm)
sync_controller = Sync_Controller(
    cm,
    sshfs_connector,
    activity_logger,
    github_connector,
    rsync_provider)


sync_controller.status_check()
sync_controller.exec_sync()
