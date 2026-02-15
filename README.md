# 🔗 DocWeave

**CLI tool powered by GitHub Copilot CLI that analyzes git repositories and generates beautiful documentation**

DocWeave is a command-line tool that analyzes your git repository and generates organized documentation using GitHub Copilot CLI. It transforms your commit history into markdown docs, Mermaid diagrams, and AI-powered insights.

## ✨ Features

- 🤖 **AI-Powered Analysis**: Uses GitHub Copilot CLI to understand code changes and provide context
- 📊 **Visual Diagrams**: Generates Mermaid diagrams (timelines, file relationships, importance charts)
- 📝 **Auto-Documentation**: Creates organized markdown files in `DocweaveDocs/` folder
- 🎯 **Next Steps**: Suggests actionable next steps based on code analysis
- ⚡ **Simple CLI**: Just run `docweave analyze` in any git repository

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management
- **GitHub Copilot CLI** (optional but recommended for AI-powered analysis):
  
  **Installation Steps:**
  
  1. Install GitHub CLI (if not installed):
     ```bash
     # macOS
     brew install gh
     
     # Linux/Windows - see https://cli.github.com/
     ```
  
  2. Authenticate with GitHub:
     ```bash
     gh auth login
     ```
  
  3. Install Copilot CLI extension:
     ```bash
     gh extension install github/gh-copilot
     ```
  
  4. Verify installation:
     ```bash
     gh copilot --help
     ```

  **Note:** DocWeave will work without Copilot CLI but will use fallback analysis. The tool will show you the Copilot CLI status when you run it.

### Installation

#### Option 1: Quick Install Script (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd DocWeave

# Run installation script
./install.sh

# Reload your shell
source ~/.zshrc  # or source ~/.bashrc

# Verify installation
docweave --help
```

#### Option 2: Manual Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd DocWeave

# Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies and build
poetry install
poetry build

# Install globally
pip install --user dist/docweave-*.whl

# Add to PATH (add to ~/.zshrc or ~/.bashrc)
export PATH="$HOME/.local/bin:$PATH"

# Reload shell
source ~/.zshrc  # or source ~/.bashrc

# Verify installation
docweave --help
```

#### Option 3: Use with Poetry Run (No Global Install)

```bash
cd DocWeave
poetry install
poetry run docweave analyze --path /path/to/repo
```

**Note:** For detailed installation instructions and troubleshooting, see [INSTALLATION.md](INSTALLATION.md).

## 📖 Usage

### Basic Usage

Simply navigate to any git repository and run:

```bash
# Analyze last 5 commits (default)
docweave analyze

# Or analyze only the last commit (quick)
docweave analyze --last
```

This will:
1. Detect the current directory as a git repository
2. Analyze commits (default: last 5, or use `--last` for just 1)
3. Generate documentation in `DocweaveDocs/` folder

### Options

```bash
# Analyze last commit only (quick analysis)
docweave analyze --last

# Analyze last 5 commits (default)
docweave analyze

# Analyze specific number of commits
docweave analyze --limit 20

# Analyze specific repository
docweave analyze --path /path/to/repo

# Analyze commits from last 7 days only
docweave analyze --days 7

# Combine options
docweave analyze --path ./my-repo --limit 15 --days 30
```

### Example Workflow

```bash
# Clone a repository you want to analyze
git clone https://github.com/owner/repo.git
cd repo

# Run DocWeave
docweave analyze

# View generated documentation
ls DocweaveDocs/
# CHANGES.md      - Detailed commit analysis
# NARRATIVE.md    - Development narrative  
# DIAGRAMS.md     - Mermaid diagrams
# NEXT_STEPS.md   - Suggested next steps
```

## 📁 Generated Documentation

DocWeave creates a `DocweaveDocs/` folder in your repository with:

- **CHANGES.md**: Detailed analysis of each commit with summaries, reasons, and importance
- **NARRATIVE.md**: Storytelling narrative of your development journey
- **DIAGRAMS.md**: Mermaid diagrams (timelines, file relationships, importance charts)
- **NEXT_STEPS.md**: Actionable next steps based on code analysis

## 🏗️ Architecture

```
src/docweave/
├── cli.py              # CLI entrypoint
├── components/         # Reusable components
│   ├── copilot_integration.py  # GitHub Copilot CLI integration
│   └── doc_generator.py        # Documentation generation
├── features/           # Business logic
│   └── commit_analysis.py      # Git commit analysis
├── lib/                # Utilities
│   ├── copilot_check.py
│   └── repo_utils.py
└── types/              # Type definitions
    └── models.py
```

## 🧪 Testing

```bash
# Run tests
poetry run pytest
```

## 🎯 How It Demonstrates Copilot CLI

This application showcases GitHub Copilot CLI in several ways:

1. **Runtime Integration**: Verifies Copilot CLI availability and shows status
2. **Development Workflow**: Demonstrates how Copilot CLI enhances post-commit documentation tasks
3. **AI-Powered Insights**: Uses enhanced analysis when Copilot CLI is available
4. **Verification & Status**: The tool checks Copilot CLI availability and shows status in terminal output
5. **Graceful Fallback**: Includes fallback mechanisms when Copilot CLI is unavailable, ensuring the tool always works

### Verifying Copilot CLI Usage

When you run `docweave analyze`, you'll see:

- ✅ **"GitHub Copilot CLI is available - using enhanced analysis"** = Copilot is working
- ⚠️ **"GitHub Copilot CLI not available"** = Using fallback analysis (still works!)

## 📝 Example Use Cases

- **Solo Developer**: After a coding session, analyze commits and generate documentation
- **Team Collaboration**: Generate changelogs and architecture diagrams for team reviews
- **Code Review**: Auto-document PR changes with AI-powered context
- **Onboarding**: Create up-to-date documentation for new team members

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI
- Powered by [GitHub Copilot CLI](https://github.com/github/copilot-cli)
- Uses [Mermaid](https://mermaid.js.org/) for diagrams

---

**Made with ❤️ to showcase the power of GitHub Copilot CLI**
