from pathlib import Path
from github import Github, Auth
from icecream import ic
import os
# REFERENCE GITHUB ACTIONS ENVIRONMENT VALUES as constants
PAT_SUPER_ALL_REPOS = os.environ['PAT_SUPER_ALL_REPOS']
AWS1_IP = os.environ["AWS1_IP"]
AWS1_SSH_KEY = os.environ["AWS1_SSH_KEY"]
AWS1_USER = os.environ["AWS1_USER"]


# SOURCE FOLDERS:
source_folders = []
destination_folders = []

# remote repo
base_url = "https://github.com/normanclt/github_actions.git"
remote_repo = Github(base_url=base_url)

repos = remote_repo.get_repo()

# remote repo we will be observing
# auth
auth = Auth.Token(PAT_SUPER_ALL_REPOS)
github01 = Github(auth=auth, base_url=base_url)

print(type(github01))
