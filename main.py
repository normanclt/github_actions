from pathlib import Path
from git.repo import Repo
from git.objects.commit import Commit
from github import Github, Auth
from icecream import ic


local_repo_path = Path(r"D:\DEV\github_actions")
local_repo = Repo(local_repo_path)
commits = local_repo.iter_commits()
remotes = local_repo.remotes
branches = local_repo.branches

# remote repo
base_url = "https://github.com/normanclt/github_actions.git"
remote_repo = Github(base_url=base_url)

repos = remote_repo.get_repo()
