from dataclasses import dataclass
import typing
from github.GitCommit import GitCommit
from github.Repository import Repository
from github.Branch import Branch


@dataclass
class Commit_Info:
    sha: str
    committer: str
    last_modified: str

    def __init__(self, branch: Branch):
        self.sha = branch.commit.commit.sha
        self.committer = branch.commit.committer
        self.last_modified = branch.commit.commit.last_modified
