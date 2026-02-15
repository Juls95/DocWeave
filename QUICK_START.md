# Quick Start Guide

## Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) (or pip + venv)
- **GitHub Copilot CLI** (optional but recommended for AI analysis): `brew install copilot-cli` — see [COPILOT_SETUP.md](COPILOT_SETUP.md)

## Installation

### Option A: Install Script (Recommended)

```bash
git clone <your-repo-url>
cd DocWeave
./install.sh
source ~/.zshrc   # or source ~/.bashrc
```

### Option B: Poetry

```bash
cd DocWeave
poetry install
export PATH="$(poetry env info --path)/bin:$PATH"
```

### Option C: pip (if Poetry unavailable)

```bash
cd DocWeave
python3 -m venv .venv
. .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install .
# Run with: docweave (from activated venv) or .venv/bin/docweave
```

### Verify Installation

```bash
docweave --help
```

You should see:
```
Usage: docweave [OPTIONS] COMMAND [ARGS]...

  DocWeave - Documentation companion powered by GitHub Copilot CLI.

Commands:
  analyze  Analyze a git repository and generate documentation.
```

## Using DocWeave

### Basic Usage

1. **Navigate to any git repository:**
   ```bash
   cd /path/to/your/repo
   ```

2. **Run analysis:**
   ```bash
   docweave analyze
   ```

3. **View generated documentation:**
   ```bash
   ls DocweaveDocs/
   # CHANGES.md      - Detailed commit analysis (AI-powered when Copilot available)
   # NARRATIVE.md    - Development narrative
   # DIAGRAMS.md     - Mermaid diagrams (architecture, flows, timelines)
   # INTEGRATION.md  - Integration & architecture insights (Copilot only)
   # NEXT_STEPS.md   - Suggested next steps
   ```

### Example: Analyzing a GitHub Repository

```bash
# Clone a repository
git clone https://github.com/owner/repo.git
cd repo

# Analyze it
docweave analyze

# Or with options
docweave analyze --limit 20 --days 7
```

### Options

```bash
# Analyze specific repository
docweave analyze --path /path/to/repo
# or short: docweave analyze -p /path/to/repo

# Analyze more commits (default: 10)
docweave analyze --limit 20
# or short: docweave analyze -l 20

# Analyze commits from last 7 days only
docweave analyze --days 7
# or short: docweave analyze -d 7

# Combine options
docweave analyze -p ./my-repo -l 15 -d 30
```

**Note:** With Copilot CLI available, each commit analysis uses AI (~30–60 seconds per commit). Without Copilot, fallback heuristics run immediately.

## Troubleshooting

### "command not found: docweave"

1. **Check if installed:**
   ```bash
   which docweave
   pip show docweave
   # or with Poetry: poetry run docweave --help
   ```

2. **Add to PATH:**
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   # Or for Poetry venv: export PATH="$(poetry env info --path)/bin:$PATH"
   # Add to ~/.zshrc or ~/.bashrc
   ```

3. **Reinstall:**
   ```bash
   cd DocWeave
   ./install.sh
   # or: poetry install && pip install dist/docweave-*.whl
   ```

### "Module not found" errors

Make sure you're using the correct Python version. DocWeave requires Python 3.10+.

```bash
python3 --version  # Should be 3.10 or higher
```

## Next Steps

- [README.md](README.md) — Full documentation
- [INSTALLATION.md](INSTALLATION.md) — Advanced install options
- [COPILOT_SETUP.md](COPILOT_SETUP.md) — GitHub Copilot CLI setup (required for AI analysis)
