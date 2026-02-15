"""Component: Integration with GitHub Copilot CLI."""

import asyncio
import json
import re
from pathlib import Path
from typing import Optional

from docweave.types.models import CodeAnalysis

# Max diff chars to send to Copilot (avoid prompt limits)
MAX_DIFF_CHARS = 6000
# Subprocess timeout per Copilot call (seconds)
COPILOT_TIMEOUT = 60


async def _invoke_copilot(prompt: str) -> str:
    """
    Invoke GitHub Copilot CLI with a prompt.

    Uses `copilot -p "prompt"` for non-interactive programmatic mode.

    Returns:
        Raw stdout from Copilot (may include usage stats at end)
    """
    # Truncate prompt if too long (CLI tools often have limits)
    max_prompt_len = 25000
    if len(prompt) > max_prompt_len:
        prompt = prompt[:max_prompt_len] + "\n\n[... prompt truncated ...]"

    process = await asyncio.create_subprocess_exec(
        "copilot",
        "-p",
        prompt,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=COPILOT_TIMEOUT
        )
    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        raise RuntimeError("Copilot CLI timed out")

    if process.returncode != 0:
        err = stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"Copilot CLI failed (exit {process.returncode}): {err}")

    return stdout.decode("utf-8", errors="replace")


def _strip_usage_stats(text: str) -> str:
    """Remove Copilot usage/stats block from end of response."""
    # Match from "Total usage" or "API time" to end
    patterns = [
        r"\n\s*Total usage est:.*$",
        r"\n\s*API time spent:.*$",
        r"\n\s*Total session time:.*$",
        r"\n\s*Breakdown by AI model:.*$",
    ]
    result = text
    for p in patterns:
        result = re.sub(p, "", result, flags=re.DOTALL)
    return result.strip()


def _parse_copilot_json_response(response: str) -> Optional[CodeAnalysis]:
    """Parse Copilot response expecting JSON. Returns None if parse fails."""
    cleaned = _strip_usage_stats(response)
    # Try to find JSON block (```json ... ``` or raw { ... })
    json_match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", cleaned)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try raw JSON
        brace = cleaned.find("{")
        if brace >= 0:
            depth = 0
            end = brace
            for i, c in enumerate(cleaned[brace:], brace):
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        end = i
                        break
            json_str = cleaned[brace : end + 1]
        else:
            return None

    try:
        data = json.loads(json_str)
        return CodeAnalysis(
            summary=str(data.get("summary", "")) or "Analysis of commit",
            why=str(data.get("why", "")) or "Code change",
            next_steps=list(data.get("next_steps", []))[:5]
            or ["Review changes", "Add tests", "Update docs"],
            importance=str(data.get("importance", "medium")).lower()
            or "medium",
        )
    except (json.JSONDecodeError, TypeError):
        return None


async def analyze_with_copilot(
    code_diff: str, commit_message: str, context: Optional[str] = None
) -> CodeAnalysis:
    """
    Use GitHub Copilot CLI to analyze code changes.

    Invokes Copilot via subprocess with a structured prompt. Falls back
    to heuristic analysis if Copilot fails or returns unparseable output.

    Args:
        code_diff: The git diff of the changes
        commit_message: The commit message
        context: Optional additional context

    Returns:
        CodeAnalysis object with insights
    """
    diff_truncated = (
        code_diff[:MAX_DIFF_CHARS] + "\n\n[ diff truncated for length ]"
        if len(code_diff) > MAX_DIFF_CHARS
        else code_diff
    )

    prompt = f"""Analyze this git commit and code change. Provide a deep technical and business-oriented analysis.

Commit message:
{commit_message}

Code diff:
{diff_truncated}
{f'Additional context: {context}' if context else ''}

Respond with ONLY a valid JSON object (no markdown, no extra text):
{{
  "summary": "1-2 sentence technical summary of what changed and its impact",
  "why": "Business/technical rationale - why was this change made, what problem does it solve",
  "next_steps": ["actionable item 1", "actionable item 2", "actionable item 3"],
  "importance": "low" or "medium" or "high"
}}

Importance: high = critical (security, bugs, core logic), medium = features/refactors, low = docs/style."""

    try:
        raw = await _invoke_copilot(prompt)
        analysis = _parse_copilot_json_response(raw)
        if analysis:
            return analysis
        return _parse_text_response(raw, commit_message)
    except Exception:
        return _create_enhanced_analysis(commit_message, code_diff)


def _create_enhanced_analysis(
    commit_message: str, code_diff: str
) -> CodeAnalysis:
    """
    Create analysis using heuristics when Copilot is unavailable or fails.
    """
    diff_lines = code_diff.split("\n") if code_diff else []
    has_tests = any("test" in l.lower() for l in diff_lines[:50])
    has_docs = any(
        "doc" in l.lower() or "readme" in l.lower() for l in diff_lines[:50]
    )

    msg_lower = commit_message.lower()

    if "test" in msg_lower or has_tests:
        importance = "high"
        why = "Test changes ensure code quality and prevent regressions."
        summary = f"Test-related: {commit_message.split(chr(10))[0][:60]}"
        next_steps = [
            "Verify test coverage",
            "Run test suite",
            "Consider integration tests",
        ]
    elif "fix" in msg_lower or "bug" in msg_lower:
        importance = "high"
        why = "Bug fix addresses issues in the codebase."
        summary = f"Bug fix: {commit_message.split(chr(10))[0][:60]}"
        next_steps = [
            "Verify fix resolves the issue",
            "Add regression tests",
            "Update docs if behavior changed",
        ]
    elif "feat" in msg_lower or "feature" in msg_lower or "add" in msg_lower:
        importance = "medium"
        why = "Feature addition extends functionality."
        summary = f"New feature: {commit_message.split(chr(10))[0][:60]}"
        next_steps = ["Add unit tests", "Update documentation", "Add examples"]
    elif "refactor" in msg_lower:
        importance = "medium"
        why = "Refactoring improves structure without changing behavior."
        summary = f"Refactoring: {commit_message.split(chr(10))[0][:60]}"
        next_steps = ["Ensure tests pass", "Review performance", "Update comments"]
    elif has_docs:
        importance = "low"
        why = "Documentation updates improve maintainability."
        summary = f"Docs: {commit_message.split(chr(10))[0][:60]}"
        next_steps = ["Verify accuracy", "Check links", "Add examples"]
    else:
        importance = "medium"
        why = "Code changes improve functionality or structure."
        summary = f"Changes: {commit_message.split(chr(10))[0][:60]}"
        next_steps = ["Review changes", "Add tests", "Update docs"]

    return CodeAnalysis(
        summary=summary,
        why=why,
        next_steps=next_steps,
        importance=importance,
    )


def _create_fallback_analysis(
    commit_message: str, code_diff: str, error: str
) -> CodeAnalysis:
    """Create fallback analysis when Copilot CLI is unavailable."""
    return _create_enhanced_analysis(commit_message, code_diff)


async def generate_diagrams_with_copilot(
    commits_text: str, analyses_text: str, repo_name: str
) -> list[str]:
    """
    Use Copilot to generate deep-dive Mermaid diagrams.

    Returns list of Mermaid diagram strings (with ```mermaid wrapper).
    Falls back to empty list on failure.
    """
    prompt = f"""Based on these commits and analyses for repository "{repo_name}", generate 2-4 Mermaid diagrams that provide deep technical and business insight.

COMMITS:
{commits_text[:4000]}

ANALYSES:
{analyses_text[:4000]}

Generate diagrams such as:
- Architecture/component flow showing how changes affect the system
- Data flow or sequence diagram for key changes
- Business logic flow or state transitions
- Timeline or dependency graph

Return ONLY valid Mermaid code blocks, one per diagram. Format each as:
```mermaid
... diagram code ...
```

No other text. Just the ```mermaid blocks."""

    try:
        raw = await _invoke_copilot(prompt)
        cleaned = _strip_usage_stats(raw)
        diagrams = []
        for m in re.finditer(r"```mermaid\s*([\s\S]*?)```", cleaned):
            content = m.group(1).strip()
            if content and len(content) > 20:
                diagrams.append(f"```mermaid\n{content}\n```")
        return diagrams[:4]
    except Exception:
        return []


async def generate_integration_insights_with_copilot(
    commits_text: str, analyses_text: str, repo_name: str
) -> str:
    """
    Use Copilot to answer integration and architecture questions.

    Answers: Where is integration generated? Best way to solve login? etc.
    """
    prompt = f"""Based on these commits and analyses for "{repo_name}", provide a concise technical guide.

Answer ONLY these questions in clean markdown (no tool output, no command output, no bullet lists of file operations):

1. Where are integrations generated or configured? (API clients, external services, webhooks)
2. What's the best way to solve login/authentication given the current codebase?
3. Key integration points and how to extend them
4. Any gotchas or conventions for adding new integrations

COMMITS:
{commits_text[:3500]}

ANALYSES:
{analyses_text[:3500]}

Respond with ONLY the guide text. Use ## headings for each topic. Prose paragraphs only."""

    try:
        raw = await _invoke_copilot(prompt)
        cleaned = _strip_usage_stats(raw).strip()
        # Remove Copilot session/tool output artifacts (● List, └ N files, $ command)
        cleaned = re.sub(r"●[^\n]+\n", "", cleaned)
        cleaned = re.sub(r"└[^\n]+\n", "", cleaned)
        cleaned = re.sub(r"\$\s+[^\n]+\n", "", cleaned)
        # Find first ## heading - that's typically where the real content starts
        h2 = cleaned.find("## ")
        if h2 >= 0:
            cleaned = cleaned[h2:]
        return cleaned[:4000] if cleaned else ""
    except Exception:
        return ""


async def generate_narrative_with_copilot(
    commits_text: str, analyses_text: str, repo_name: str
) -> str:
    """
    Use Copilot to generate deeper technical and business narrative.

    Returns narrative string. Falls back to empty string on failure.
    """
    prompt = f"""Based on these commits and analyses for repository "{repo_name}", write a 2-4 paragraph narrative that:
1. Summarizes the development trajectory from a technical perspective
2. Explains the business impact and value of these changes
3. Highlights integration points, architectural decisions, or patterns
4. Addresses questions like: Where are key integrations? What's the best approach for auth/login given the codebase? What technical debt or next steps matter most?

COMMITS:
{commits_text[:4000]}

ANALYSES:
{analyses_text[:4000]}

Write in clear, professional prose. No bullet lists. Paragraphs only."""

    try:
        raw = await _invoke_copilot(prompt)
        cleaned = _strip_usage_stats(raw).strip()
        return cleaned[:3000] if cleaned else ""
    except Exception:
        return ""


def _parse_text_response(response: str, commit_message: str) -> CodeAnalysis:
    """Parse free-form Copilot text response into CodeAnalysis."""
    cleaned = _strip_usage_stats(response)
    lines = [l.strip() for l in cleaned.split("\n") if l.strip()]

    summary = lines[0] if lines else f"Analysis of: {commit_message[:60]}"
    why = "Change improves codebase functionality"
    next_steps = []
    importance = "medium"

    for i, line in enumerate(lines):
        if "why" in line.lower() or "reason" in line.lower():
            why = line.split(":", 1)[-1].strip() if ":" in line else line
        elif "next" in line.lower() or "todo" in line.lower():
            if i + 1 < len(lines):
                next_steps.append(lines[i + 1].lstrip("-• ").strip())
        elif "importance" in line.lower():
            if "high" in line.lower():
                importance = "high"
            elif "low" in line.lower():
                importance = "low"

    if not next_steps:
        next_steps = ["Review changes", "Add tests", "Update docs"]

    return CodeAnalysis(
        summary=summary[:200],
        why=why[:300],
        next_steps=next_steps[:3],
        importance=importance,
    )
