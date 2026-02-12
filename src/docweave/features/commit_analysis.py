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
    # Resolve the path to handle relative paths and symlinks
    repo_path = repo_path.resolve()
    
    if not repo_path.exists():
        raise ValueError(f"Path does not exist: {repo_path}")
    
    if not repo_path.is_dir():
        raise ValueError(f"Path is not a directory: {repo_path}")
    
    # Check if it's a git repository
    git_dir = repo_path / ".git"
    if not git_dir.exists() and not git_dir.is_dir():
        # Try parent directories (might be in a subdirectory of a git repo)
        current = repo_path
        found_git = False
        for _ in range(5):  # Check up to 5 levels up
            if (current / ".git").exists():
                repo_path = current
                found_git = True
                break
            if current.parent == current:  # Reached root
                break
            current = current.parent
        
        if not found_git:
            raise ValueError(
                f"{repo_path} is not a git repository. "
                "Please ensure you're in a directory with a .git folder or initialize with 'git init'."
            )
    
    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        raise ValueError(f"{repo_path} is not a valid git repository")
    except Exception as e:
        raise ValueError(f"Error accessing git repository: {str(e)}")

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
        repo_path = repo_path.resolve()
        repo = Repo(repo_path)
        commit = repo.commit(commit_sha)
        
        # Get diff against parent commit
        if commit.parents:
            diff = commit.diff(commit.parents[0], create_patch=True)
        else:
            # First commit - show all files
            diff = commit.diff(None, create_patch=True)
        
        # Format the diff
        diff_str = ""
        for item in diff:
            a_path = item.a_path if item.a_path else "/dev/null"
            b_path = item.b_path if item.b_path else "/dev/null"
            diff_str += f"--- a/{a_path}\n+++ b/{b_path}\n"
            if hasattr(item, 'diff') and item.diff:
                if isinstance(item.diff, bytes):
                    diff_str += item.diff.decode('utf-8', errors='ignore')
                else:
                    diff_str += str(item.diff)
        
        return diff_str if diff_str else f"Commit {commit_sha}: {commit.message[:100]}"
    except Exception as e:
        # Return a minimal diff description instead of empty string
        return f"Error getting diff for commit {commit_sha}: {str(e)}"
