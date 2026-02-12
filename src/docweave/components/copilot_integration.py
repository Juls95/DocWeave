"""Component: Integration with GitHub Copilot CLI."""

import asyncio
import json
from pathlib import Path
from typing import Optional

from docweave.types.models import CodeAnalysis


async def analyze_with_copilot(
    code_diff: str, commit_message: str, context: Optional[str] = None
) -> CodeAnalysis:
    """
    Use GitHub Copilot CLI to analyze code changes.

    Args:
        code_diff: The git diff of the changes
        commit_message: The commit message
        context: Optional additional context

    Returns:
        CodeAnalysis object with insights

    Raises:
        RuntimeError: If Copilot CLI is not available or fails
    """
    # Build the prompt for Copilot
    prompt = f"""Analyze this code change and provide:
1. A brief summary of what changed
2. Why this change was made (purpose/benefit)
3. Suggested next steps (2-3 actionable items)
4. Importance level (low/medium/high)

Commit message: {commit_message}

Code diff:
{code_diff}

{f'Additional context: {context}' if context else ''}

Respond in JSON format:
{{
  "summary": "...",
  "why": "...",
  "next_steps": ["...", "..."],
  "importance": "..."
}}
"""

    try:
        # Call gh copilot explain
        # The prompt is passed via stdin for better handling
        process = await asyncio.create_subprocess_exec(
            "gh",
            "copilot",
            "explain",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate(input=prompt.encode())

        if process.returncode != 0:
            # Fallback if Copilot CLI fails
            error_msg = stderr.decode() if stderr else "Unknown error"
            return _create_fallback_analysis(commit_message, code_diff, error_msg)

        response = stdout.decode().strip()

        # Try to parse JSON response
        try:
            # Extract JSON from response (might have markdown code blocks)
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()

            data = json.loads(response)
            return CodeAnalysis(
                summary=data.get("summary", "Code changes detected"),
                why=data.get("why", "Change made to improve functionality"),
                next_steps=data.get("next_steps", []),
                importance=data.get("importance", "medium"),
            )
        except json.JSONDecodeError:
            # If not JSON, parse as text
            return _parse_text_response(response, commit_message)

    except FileNotFoundError:
        raise RuntimeError(
            "GitHub Copilot CLI not found. Please install it with: gh extension install github/gh-copilot"
        )
    except Exception as e:
        raise RuntimeError(f"Error calling Copilot CLI: {str(e)}")


def _create_fallback_analysis(
    commit_message: str, code_diff: str, error: str
) -> CodeAnalysis:
    """Create a fallback analysis when Copilot CLI is unavailable."""
    # Simple heuristic-based analysis
    files_changed = len(code_diff.split("\n---")) if code_diff else 0

    if "test" in commit_message.lower():
        importance = "high"
        why = "Test changes ensure code quality and prevent regressions"
    elif "fix" in commit_message.lower() or "bug" in commit_message.lower():
        importance = "high"
        why = "Bug fix addresses issues in the codebase"
    else:
        importance = "medium"
        why = "Feature addition or code improvement"

    return CodeAnalysis(
        summary=f"Changes detected in commit: {commit_message[:50]}...",
        why=why,
        next_steps=[
            "Review the changes carefully",
            "Add tests if applicable",
            "Update related documentation",
        ],
        importance=importance,
    )


def _parse_text_response(response: str, commit_message: str) -> CodeAnalysis:
    """Parse a text response from Copilot into CodeAnalysis."""
    # Simple parsing - in production, use more sophisticated NLP
    lines = response.split("\n")
    summary = lines[0] if lines else f"Analysis of: {commit_message}"

    why = "Change improves codebase functionality"
    next_steps = []
    importance = "medium"

    for i, line in enumerate(lines):
        if "why" in line.lower() or "reason" in line.lower():
            why = line.split(":", 1)[-1].strip() if ":" in line else line
        elif "next" in line.lower() or "todo" in line.lower():
            # Try to extract next steps
            if i + 1 < len(lines):
                next_steps.append(lines[i + 1].strip("- ").strip())

    if not next_steps:
        next_steps = ["Review changes", "Add tests", "Update docs"]

    return CodeAnalysis(
        summary=summary,
        why=why,
        next_steps=next_steps[:3],  # Limit to 3 steps
        importance=importance,
    )
