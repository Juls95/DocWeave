"""Type definitions for DocWeave."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CommitInfo:
    """Information about a git commit."""

    sha: str
    message: str
    author: str
    date: datetime
    files_changed: list[str]
    additions: int
    deletions: int


@dataclass
class CodeAnalysis:
    """Analysis result from Copilot CLI."""

    summary: str
    why: str
    next_steps: list[str]
    importance: str


@dataclass
class DocumentationResult:
    """Generated documentation result."""

    markdown_content: str
    mermaid_diagrams: list[str]
    narrative: str
    next_steps: list[str]
    integration_insights: str = ""  # Copilot-generated: where integrations live, login approach


@dataclass
class AnalysisProgress:
    """Progress update for analysis."""

    stage: str
    message: str
    progress: float  # 0.0 to 1.0
