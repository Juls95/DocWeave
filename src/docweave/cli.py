"""CLI entrypoint for DocWeave."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click

from docweave.components.copilot_integration import analyze_with_copilot
from docweave.components.doc_generator import generate_documentation, save_documentation
from docweave.features.commit_analysis import analyze_recent_commits, get_commit_diff
from docweave.lib.copilot_check import check_copilot_cli_installed
from docweave.lib.repo_utils import is_github_url


def print_step(message: str, icon: str = "📊") -> None:
    """Print a step message with icon."""
    click.echo(f"{icon} {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    click.echo(click.style(f"✅ {message}", fg="green"))


def print_error(message: str) -> None:
    """Print an error message."""
    click.echo(click.style(f"❌ {message}", fg="red"), err=True)


def print_warning(message: str) -> None:
    """Print a warning message."""
    click.echo(click.style(f"⚠️  {message}", fg="yellow"))


def print_info(message: str) -> None:
    """Print an info message."""
    click.echo(click.style(f"ℹ️  {message}", fg="blue"))


@click.group()
def cli() -> None:
    """DocWeave - Documentation companion powered by GitHub Copilot CLI."""
    pass


@cli.command()
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to git repository (default: current directory)",
)
@click.option(
    "--limit",
    "-l",
    type=int,
    default=10,
    help="Maximum number of commits to analyze",
    show_default=True,
)
@click.option(
    "--days",
    "-d",
    type=int,
    default=None,
    help="Only analyze commits from the last N days",
)
def analyze(path: Optional[Path], limit: int, days: Optional[int]) -> None:
    """
    Analyze a git repository and generate documentation.
    
    By default, analyzes the current directory. Documentation will be saved
    to DocweaveDocs/ folder in the repository root.
    """
    # Determine repository path
    if path is None:
        repo_path = Path.cwd()
    else:
        repo_path = path.resolve()

    # Check if it's a GitHub URL
    if is_github_url(str(repo_path)):
        print_error(
            "GitHub URLs are not supported directly. Please clone the repository first:\n"
            f"  git clone {repo_path}\n"
            "  cd <repo-name>\n"
            "  docweave analyze"
        )
        sys.exit(1)

    click.echo("\n" + "=" * 60)
    click.echo(click.style("🔗 DocWeave - Documentation Companion", bold=True))
    click.echo("=" * 60 + "\n")

    try:
        # Check if it's a git repository
        print_step("Detecting git repository...")
        if not (repo_path / ".git").exists():
            # Try parent directories
            current = repo_path
            found_git = False
            for _ in range(5):
                if (current / ".git").exists():
                    repo_path = current
                    found_git = True
                    break
                if current.parent == current:
                    break
                current = current.parent

            if not found_git:
                print_error(
                    f"{repo_path} is not a git repository.\n"
                    "Please ensure you're in a directory with a .git folder, "
                    "or initialize with: git init"
                )
                sys.exit(1)

        repo_name = repo_path.name or "repository"
        print_success(f"Detected git repository: {repo_name}")
        print_info(f"Repository path: {repo_path}\n")

        # Check Copilot CLI status
        print_step("Checking GitHub Copilot CLI...")
        copilot_available, copilot_error = asyncio.run(check_copilot_cli_installed())
        if copilot_available:
            print_success("GitHub Copilot CLI is available - using enhanced analysis")
        else:
            print_warning(f"GitHub Copilot CLI not available: {copilot_error}")
            print_info("Using fallback analysis (still generates great docs!)\n")

        # Analyze commits
        print_step(f"Analyzing recent commits (limit: {limit})...")
        commits = asyncio.run(
            analyze_recent_commits(repo_path, limit=limit, days_back=days)
        )

        if not commits:
            print_warning("No recent commits found in the repository.")
            sys.exit(0)

        print_success(f"Found {len(commits)} commit(s) to analyze\n")

        # Analyze each commit
        print_step("Analyzing commits with AI-powered insights...")
        analyses = []
        
        async def analyze_commits():
            commit_analyses = []
            for i, commit in enumerate(commits, 1):
                try:
                    diff = await get_commit_diff(repo_path, commit.sha)
                    if copilot_available:
                        analysis = await analyze_with_copilot(diff, commit.message)
                    else:
                        from docweave.components.copilot_integration import (
                            _create_fallback_analysis,
                        )

                        analysis = _create_fallback_analysis(
                            commit.message, diff, copilot_error or "Copilot CLI not available"
                        )

                    commit_analyses.append(analysis)
                    click.echo(f"  [{i}/{len(commits)}] {commit.sha[:7]} - {commit.message.split(chr(10))[0][:50]}...", nl=False)
                    print_success(" ✓")
                except Exception as e:
                    from docweave.components.copilot_integration import (
                        _create_fallback_analysis,
                    )

                    analysis = _create_fallback_analysis(commit.message, "", str(e))
                    commit_analyses.append(analysis)
                    click.echo(f"  [{i}/{len(commits)}] {commit.sha[:7]} - {commit.message.split(chr(10))[0][:50]}...", nl=False)
                    print_warning(" ⚠ (using fallback)")
            return commit_analyses
        
        analyses = asyncio.run(analyze_commits())
        click.echo()

        # Generate documentation
        print_step("Generating documentation...")
        doc_result = asyncio.run(generate_documentation(commits, analyses, repo_name))

        # Save documentation
        output_path = repo_path / "DocweaveDocs"
        asyncio.run(save_documentation(doc_result, output_path, repo_name))

        print_success(f"Documentation generated successfully!\n")

        # Show summary
        click.echo(click.style("📁 Generated Files:", bold=True))
        files_created = [
            "CHANGES.md - Detailed commit analysis",
            "NARRATIVE.md - Development narrative",
            "DIAGRAMS.md - Mermaid diagrams",
            "NEXT_STEPS.md - Suggested next steps",
        ]
        for file_info in files_created:
            click.echo(f"  ✓ {file_info}")

        click.echo(f"\n📂 Documentation saved to: {output_path}")
        if copilot_available:
            click.echo(
                click.style(
                    f"\n🤖 Enhanced analysis with Copilot CLI: {len(commits)} commits analyzed",
                    fg="green",
                )
            )

        click.echo("\n" + "=" * 60)
        print_success("Analysis complete!")
        click.echo("=" * 60 + "\n")

    except ValueError as e:
        print_error(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\n\n⚠️  Analysis interrupted by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        import traceback

        if "--debug" in sys.argv:
            traceback.print_exc()
        sys.exit(1)


def main() -> None:
    """Main entry point - runs the CLI."""
    cli()


if __name__ == "__main__":
    main()
