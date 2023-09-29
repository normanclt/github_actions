from services.push_providers import *
from services.config_manager import Config_Manager
from services.activity_logger import Activity_Logger
from services.resource_connectors import Github_Connector, SSHFS_Connector
from io import StringIO

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
cm.ssh_private_key = StringIO(AWS1_SSH_KEY)
# Local
# cm.ssh_private_key = Path(
#     r"D:\Projects\keys\aws_instance_1\aws1\aws1_id_ed25519").as_posix()
cm.log_directory = "/home/ec2-user/rsync/logs/"
cm.source_folder = "fixlets/"

# Local
# cm.source_folder = "sync/random_files/"
cm.destination_folder = "/home/ec2-user/rsync/RECIPES"
cm.github_api_token = PAT_FIXLET_REPO

# Local
# cm.github_api_token_filepath = Path(
#     r"D:\Projects\keys\github_swottednorman\norman_read_only_bgfix.txt")
# Local
# with open(cm.github_api_token_filepath, "r") as stream:
#     cm.github_api_token = stream.readline()

github_connector = Github_Connector(cm)
sshfs_connector = SSHFS_Connector(cm)
activity_logger = Activity_Logger(cm, sshfs_connector)
push_provider = Rsync_Provider(cm, activity_logger)

identifier = github_connector.state_identifier
activity_logger.latest_activity
