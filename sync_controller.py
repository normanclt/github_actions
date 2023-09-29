from services.push_providers import *
from services.config_manager import Config_Manager
from services.activity_logger import Activity_Logger
from services.resource_connectors import *

cm = config_manager = Config_Manager(
    "repo_name",
    "branch_name",
    "organization_name",
    "github_api_token",
    "ssh_user",
    "ssh_private_key",
    "remote_ip",
    "source_folder",
    "destination_folder")

cm.repo_name = 'site_updates_windows_apps_extended'
cm.branch_name = 'publish'
cm.organization_name = 'bigfix'
cm.ssh_user = 'ec2-user'
cm.remote_ip = '52.74.243.47'
cm.ssh_private_key = Path(
    r"D:\Projects\keys\aws_instance_1\aws1\aws1_id_ed25519").as_posix()
cm.log_directory = "/home/ec2-user/rsync/logs/"

github_source = Github_Source(cm)
resource_connect = SSHFS_Connector(cm)
activity_logger = Activity_Logger()


def main():

    _configure_push_provider()
    _configure_activity_logger()
    _configure_resource_connector()
    _configure_config_manager()

    pass


if __name__ == "__main__":
    main()
