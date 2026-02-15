# 🔗 DocWeave

**CLI tool powered by GitHub Copilot CLI that analyzes git repositories and generates beautiful documentation**

DocWeave is a command-line tool that analyzes your git repository and generates organized documentation using GitHub Copilot CLI. It transforms your commit history into markdown docs, Mermaid diagrams, and AI-powered insights.

## ✨ Features

- 🤖 **AI-Powered Analysis**: Uses GitHub Copilot CLI to understand code changes and provide context
- 📊 **Visual Diagrams**: Generates Mermaid diagrams (timelines, file relationships, importance charts)
- 📝 **Auto-Documentation**: Creates organized markdown files in `DocweaveDocs/` folder
- 🎯 **Next Steps**: Suggests actionable next steps based on code analysis
- ⚡ **Simple CLI**: Just run `docweave analyze` in any git repository
- 🔄 **Graceful Fallback**: Works even without Copilot CLI using intelligent heuristics

## 🚀 Installation

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management
- **GitHub Copilot CLI** (optional but recommended for AI-powered analysis)

### Quick Install

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

### Manual Installation

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
```

### Use with Poetry Run (No Global Install)

```bash
cd DocWeave
poetry install
poetry run docweave analyze --path /path/to/repo
```

## 📖 How the CLI Process Works

### Step-by-Step Process

When you run `docweave analyze`, here's what happens:

#### 1. **Repository Detection** 📂
```
📊 Detecting git repository...
✅ Detected git repository: your-repo
ℹ️  Repository path: /path/to/your/repo
```
- DocWeave checks if the current directory (or specified path) is a git repository
- It looks for a `.git` folder, checking up to 5 parent directories if needed
- If no git repository is found, it shows a clear error message with instructions

#### 2. **GitHub Copilot CLI Check** 🤖
```
📊 Checking GitHub Copilot CLI...
✅ GitHub Copilot CLI is available - using enhanced analysis
```
**OR if not available:**
```
⚠️  GitHub Copilot CLI not available: [error message]
ℹ️  Using fallback analysis (still generates great docs!)
```

**What happens if GitHub credentials aren't detected:**

- **Copilot CLI Not Installed**: DocWeave detects this and automatically falls back to heuristic-based analysis. You'll see a warning message, but the tool continues working.
- **Copilot CLI Installed but Not Authenticated**: Same behavior - fallback analysis is used. The tool will still generate documentation, just without AI-powered insights.
- **Copilot CLI Available and Authenticated**: Enhanced AI-powered analysis is used for each commit, providing deeper insights, better summaries, and more contextual next steps.

**Key Point**: DocWeave **always works**, regardless of Copilot CLI status. It gracefully degrades to intelligent heuristics when Copilot isn't available.

#### 3. **Commit Analysis** 📊
```
📊 Analyzing recent commits (limit: 5)...
✅ Found 5 commit(s) to analyze

📊 Analyzing commits with AI-powered insights...
  [1/5] abc1234 - Fix bug in login... ✅ ✓
  [2/5] def5678 - Add new feature... ✅ ✓
  ...
```

For each commit:
- **With Copilot CLI**: The commit diff and message are analyzed using AI to extract:
  - Summary of changes
  - Why the change was made
  - Suggested next steps
  - Importance level (low/medium/high)
- **Without Copilot CLI**: Intelligent heuristics analyze:
  - Commit message patterns (e.g., "fix", "feat", "test")
  - File types changed
  - Code diff patterns
  - Generates similar insights using rule-based analysis

#### 4. **Documentation Generation** 📝
```
📊 Generating documentation...
✅ Documentation generated successfully!
```

DocWeave creates:
- **CHANGES.md**: Detailed analysis of each commit
- **NARRATIVE.md**: Storytelling narrative of development journey
- **DIAGRAMS.md**: Mermaid diagrams (timelines, file relationships, importance charts)
- **NEXT_STEPS.md**: Actionable next steps based on analysis

#### 5. **Output Summary** 📁
```
📁 Generated Files:
  ✓ CHANGES.md - Detailed commit analysis
  ✓ NARRATIVE.md - Development narrative
  ✓ DIAGRAMS.md - Mermaid diagrams
  ✓ NEXT_STEPS.md - Suggested next steps

📂 Documentation saved to: /path/to/repo/DocweaveDocs
```

All files are saved in the `DocweaveDocs/` folder in your repository root.

### Process Flow Diagram

```
User runs: docweave analyze
    │
    ├─→ Detect git repository
    │   └─→ Error if not found → Exit with instructions
    │
    ├─→ Check Copilot CLI
    │   ├─→ Available → Use AI-powered analysis
    │   └─→ Not available → Use fallback heuristics
    │
    ├─→ Analyze commits
    │   ├─→ Get commit diffs
    │   ├─→ Analyze with Copilot (if available) or heuristics
    │   └─→ Extract insights (summary, why, next steps, importance)
    │
    ├─→ Generate documentation
    │   ├─→ Create markdown files
    │   ├─→ Generate Mermaid diagrams
    │   └─→ Write narrative and next steps
    │
    └─→ Save to DocweaveDocs/
        └─→ Show summary and completion message
```

## 🔧 GitHub Copilot CLI Setup

### Why Copilot CLI?

GitHub Copilot CLI provides AI-powered analysis that:
- Understands code context and intent
- Provides deeper insights into why changes were made
- Suggests more relevant next steps
- Generates better summaries

### Installation

**Option 1: Homebrew (macOS/Linux)**
```bash
brew install copilot-cli
```

**Option 2: npm (requires Node.js 22+)**
```bash
npm install -g @github/copilot
```

**Option 3: Install Script**
```bash
curl -fsSL https://gh.io/copilot-install | bash
```

### Authentication

**Method 1: Interactive Login**
```bash
copilot
# In the interactive session, type:
/login
# Follow the on-screen instructions
```

**Method 2: Personal Access Token**
1. Visit https://github.com/settings/personal-access-tokens/new
2. Under "Permissions," select **Copilot Requests**
3. Generate your token
4. Set as environment variable:
   ```bash
   export GH_TOKEN=your_token_here
   # or
   export GITHUB_TOKEN=your_token_here
   ```

### Verification

```bash
# Check if installed
copilot --version
# Should show: GitHub Copilot CLI 0.0.407 (or similar)

# Test in DocWeave
cd /path/to/git/repo
docweave analyze
# Look for: ✅ "GitHub Copilot CLI is available - using enhanced analysis"
```

### What Happens Without Copilot CLI?

**DocWeave works perfectly fine without Copilot CLI!** Here's what you get:

- ✅ **Full Documentation Generation**: All files are still created
- ✅ **Intelligent Analysis**: Heuristic-based analysis using:
  - Commit message patterns
  - File change types
  - Code diff analysis
  - Best practices inference
- ⚠️ **Less AI Context**: Insights are rule-based rather than AI-powered
- ⚠️ **Simpler Summaries**: Still useful, but less nuanced

**Example Output Without Copilot:**
```
⚠️  GitHub Copilot CLI not available: GitHub Copilot CLI (copilot) is not installed
ℹ️  Using fallback analysis (still generates great docs!)
```

The tool continues and generates complete documentation - you just won't see the "Enhanced analysis with Copilot CLI" message.

## 📖 Usage

### Basic Usage

```bash
# Navigate to any git repository
cd /path/to/your/repo

# Analyze last 5 commits (default)
docweave analyze

# Analyze only the last commit (quick)
docweave analyze --last
```

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
# or short: docweave analyze -p /path/to/repo

# Analyze commits from last 7 days only
docweave analyze --days 7
# or short: docweave analyze -d 7

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

### CHANGES.md
Detailed analysis of each commit including:
- Commit SHA, author, date
- Summary of changes
- Why the change was made (purpose/benefit)
- Importance level (low/medium/high)
- Files changed
- Suggested next steps

### NARRATIVE.md
A storytelling narrative that:
- Summarizes the development journey
- Highlights key themes and patterns
- Provides context for the codebase evolution
- Makes the project more approachable for new contributors

### DIAGRAMS.md
Mermaid diagrams including:
- **Commit Timeline**: Gantt chart showing commit timeline
- **Files Changed**: Graph showing relationships between modified files
- **Importance Distribution**: Pie chart showing changes by importance level

### NEXT_STEPS.md
Actionable next steps based on analysis:
- Prioritized suggestions
- Specific actions to take
- Best practices recommendations

## 🏗️ Architecture

```
src/docweave/
├── cli.py              # CLI entrypoint and command handling
├── components/         # Reusable components
│   ├── copilot_integration.py  # GitHub Copilot CLI integration
│   └── doc_generator.py        # Documentation generation
├── features/           # Business logic
│   └── commit_analysis.py      # Git commit analysis
├── lib/                # Utilities
│   ├── copilot_check.py        # Copilot CLI availability check
│   ├── repo_utils.py           # Repository path utilities
│   └── utils.py               # General utilities
└── types/              # Type definitions
    └── models.py               # Data models
```

## 🧪 Testing

```bash
# Run tests
poetry run pytest
```

## 🎯 How It Demonstrates Copilot CLI

This application showcases GitHub Copilot CLI in several ways:

1. **Runtime Integration**: Verifies Copilot CLI availability and shows status in terminal
2. **Development Workflow**: Demonstrates how Copilot CLI enhances post-commit documentation tasks
3. **AI-Powered Insights**: Uses enhanced analysis when Copilot CLI is available
4. **Verification & Status**: The tool checks Copilot CLI availability and shows clear status messages
5. **Graceful Fallback**: Includes intelligent fallback mechanisms when Copilot CLI is unavailable, ensuring the tool always works

### Verifying Copilot CLI Usage

When you run `docweave analyze`, you'll see:

- ✅ **"GitHub Copilot CLI is available - using enhanced analysis"** = Copilot is working and being used
- ⚠️ **"GitHub Copilot CLI not available"** = Using fallback analysis (still generates complete documentation!)

The final summary will also indicate:
- **With Copilot**: "🤖 Enhanced analysis with Copilot CLI: X commits analyzed"
- **Without Copilot**: No Copilot message (but all docs still generated)

## 📝 Example Use Cases

- **Solo Developer**: After a coding session, analyze commits and generate documentation
- **Team Collaboration**: Generate changelogs and architecture diagrams for team reviews
- **Code Review**: Auto-document PR changes with AI-powered context
- **Onboarding**: Create up-to-date documentation for new team members
- **Project Handoff**: Generate comprehensive documentation before transferring a project

## 💡 Project Background

### Problem Solved

Developers often face "documentation debt" where code evolves faster than docs, leading to:
- Onboarding delays for new team members
- Bugs from misunderstandings
- Reduced productivity (20-50% of dev hours on docs per Gartner reports)

DocWeave automates documentation creation, saving time and improving project maintainability.

### Value Proposition

In a market where tools like GitHub Copilot boost coding speed by 55%, DocWeave extends AI to post-coding tasks. It turns rapid development into professional, well-documented outputs, making developers and teams more efficient.

### Key Features

- **Automated Documentation**: Reduces manual effort and ensures docs evolve with code
- **AI-Powered Insights**: Uses GitHub Copilot CLI for contextual understanding
- **Visual Documentation**: Generates diagrams and narratives, not just technical specs
- **Actionable Guidance**: Provides next steps, not just summaries

## 🔍 Troubleshooting

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

Make sure you're using Python 3.10+:
```bash
python3 --version  # Should be 3.10 or higher
```

### "Path is not a git repository"

- Ensure you're in a directory with a `.git` folder
- Or use `--path` to specify a repository:
  ```bash
  docweave analyze --path /path/to/repo
  ```

### GitHub URL Error

If you see an error about GitHub URLs:
- DocWeave requires local git repositories
- Clone the repository first:
  ```bash
  git clone https://github.com/owner/repo.git
  cd repo
  docweave analyze
  ```

### Copilot CLI Issues

**"copilot: command not found"**
```bash
# Check installation
which copilot
copilot --version

# Install if needed
brew install copilot-cli
# or
npm install -g @github/copilot
```

**"Authentication required"**
```bash
# Authenticate
copilot
# Then type: /login
# Or set token:
export GH_TOKEN=your_token_here
```

**Note**: DocWeave works without Copilot CLI - you'll just get fallback analysis instead of AI-powered insights.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI
- Powered by [GitHub Copilot CLI](https://github.com/github/copilot-cli)
- Uses [Mermaid](https://mermaid.js.org/) for diagrams
- Uses [GitPython](https://gitpython.readthedocs.io/) for git operations

---

**Made with ❤️ to showcase the power of GitHub Copilot CLI**
