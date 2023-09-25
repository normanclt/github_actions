from pathlib import Path
from github import Github, Auth
from icecream import ic
import os
from models.commit_info import Commit_Info
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


# remote repo we will be observing
# auth
auth = Auth.Token(PAT_SUPER_ALL_REPOS)
github = Github(auth=auth)

staging_repo = github.get_repo("normanclt/staging_repo")
main_branch = staging_repo.get_branch('main')

main_branch_current_commit = Commit_Info(main_branch)

print(main_branch_current_commit.sha)


# create an observer class/function
# the observer is tasked to just compare the staging repo's commit vs. source commit sha
# staging_repo.sha != source.commit.sha then "need sync"
# staging_repo.sha == source.commit.sha then "no sync necessary"
# get_sync_requirement -> sync or no sync

# syncer class/function


# orchestrator
