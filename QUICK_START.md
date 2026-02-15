# Quick Start Guide

## Installation

### Step 1: Install DocWeave

```bash
# Clone and install
git clone <your-repo-url>
cd DocWeave
./install.sh
source ~/.zshrc  # or source ~/.bashrc
```

### Step 2: Verify Installation

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
   # CHANGES.md      - Detailed commit analysis
   # NARRATIVE.md    - Development narrative
   # DIAGRAMS.md     - Mermaid diagrams
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

# Analyze more commits
docweave analyze --limit 20

# Analyze commits from last 7 days only
docweave analyze --days 7

# Combine options
docweave analyze --path ./my-repo --limit 15 --days 30
```

## Troubleshooting

### "command not found: docweave"

1. **Check if installed:**
   ```bash
   which docweave
   pip show docweave
   ```

2. **Add to PATH:**
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   # Add this to ~/.zshrc or ~/.bashrc
   ```

3. **Reinstall:**
   ```bash
   cd DocWeave
   ./install.sh
   ```

### "Module not found" errors

Make sure you're using the correct Python version. DocWeave requires Python 3.10+.

```bash
python3 --version  # Should be 3.10 or higher
```

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [INSTALLATION.md](INSTALLATION.md) for advanced installation options
- See [COPILOT_SETUP.md](COPILOT_SETUP.md) for GitHub Copilot CLI setup
