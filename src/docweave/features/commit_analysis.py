"""Feature: Analyze git commits and extract changes."""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from git import Repo
from git.exc import InvalidGitRepositoryError

from docweave.types.models import CommitInfo


async def analyze_recent_commits(
    repo_path: Path, limit: int = 10, days_back: Optional[int] = None
) -> list[CommitInfo]:
    """
    Analyze recent commits in a git repository.

    Args:
        repo_path: Path to the git repository
        limit: Maximum number of commits to analyze
        days_back: Optional number of days to look back

    Returns:
        List of CommitInfo objects

    Raises:
        ValueError: If repo_path is not a valid git repository
    """
    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        raise ValueError(f"{repo_path} is not a valid git repository")

    if not repo.bare:
        # Get commits
        commits = list(repo.iter_commits(max_count=limit))

        if days_back:
            cutoff_date = datetime.now() - timedelta(days=days_back)
            commits = [
                c
                for c in commits
                if datetime.fromtimestamp(c.committed_date) >= cutoff_date
            ]

        commit_infos: list[CommitInfo] = []

        for commit in commits:
            # Get files changed in this commit
            files_changed = [item.a_path for item in commit.stats.files.keys()]

            # Calculate additions and deletions
            stats = commit.stats.total
            additions = stats.get("insertions", 0)
            deletions = stats.get("deletions", 0)

            commit_info = CommitInfo(
                sha=commit.hexsha[:7],
                message=commit.message.strip(),
                author=commit.author.name,
                date=datetime.fromtimestamp(commit.committed_date),
                files_changed=files_changed,
                additions=additions,
                deletions=deletions,
            )

            commit_infos.append(commit_info)

        return commit_infos

    return []


async def get_commit_diff(repo_path: Path, commit_sha: str) -> str:
    """
    Get the diff for a specific commit.

    Args:
        repo_path: Path to the git repository
        commit_sha: SHA of the commit

    Returns:
        Diff string
    """
    try:
        repo = Repo(repo_path)
        commit = repo.commit(commit_sha)
        return commit.diff(commit.parents[0] if commit.parents else None).__str__()
    except Exception:
        return ""
