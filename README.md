# 🔗 DocWeave

**Documentation companion powered by GitHub Copilot CLI**

DocWeave is a web application that analyzes your git repository and generates beautiful documentation using GitHub Copilot CLI. It transforms your commit history into organized markdown docs, Mermaid diagrams, and AI-powered insights.

## ✨ Features

- 🤖 **AI-Powered Analysis**: Uses GitHub Copilot CLI to understand code changes and provide context
- 📊 **Visual Diagrams**: Generates Mermaid diagrams (timelines, file relationships, importance charts)
- 📝 **Auto-Documentation**: Creates organized markdown files in `/docs/` folder
- 🎯 **Next Steps**: Suggests actionable next steps based on code analysis
- 🌐 **Modern Web UI**: Beautiful, responsive interface for easy interaction
- ⚡ **Real-time Progress**: See analysis progress as it happens

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

  **Note:** DocWeave will work without Copilot CLI but will use fallback analysis. The application will show you the Copilot CLI status when you start it.

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd DocWeave

# Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Start the web application
poetry run docweave serve
```

The application will be available at `http://127.0.0.1:8000`

### Development Mode

```bash
# Run with auto-reload
poetry run docweave serve --reload
```

## 📖 Usage

1. **Start the server**:
   ```bash
   poetry run docweave serve
   ```

2. **Open your browser** to `http://127.0.0.1:8000`

3. **Enter your repository path** (e.g., `/path/to/repo` or `.` for current directory)

4. **Configure analysis**:
   - Set the number of commits to analyze (default: 10)
   - Optionally set days back to limit the time range

5. **Click "Analyze with Copilot CLI"** and watch the magic happen!

6. **View results**:
   - See commit analysis with AI-powered insights
   - Review generated documentation
   - Check suggested next steps
   - Explore Mermaid diagrams

## 📁 Generated Documentation

DocWeave creates a `/docs/` folder in your repository with:

- **CHANGES.md**: Detailed analysis of each commit with summaries, reasons, and importance
- **NARRATIVE.md**: Storytelling narrative of your development journey
- **DIAGRAMS.md**: Mermaid diagrams (timelines, file relationships, importance charts)
- **NEXT_STEPS.md**: Actionable next steps based on code analysis

## 🏗️ Architecture

```
src/docweave/
├── app.py              # FastAPI web application
├── cli.py              # CLI entrypoint
├── components/         # Reusable components
│   ├── copilot_integration.py  # GitHub Copilot CLI integration
│   └── doc_generator.py        # Documentation generation
├── features/           # Business logic
│   └── commit_analysis.py      # Git commit analysis
├── lib/                # Utilities
│   └── utils.py
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

1. **Runtime Integration**: Uses `gh copilot explain` to analyze code diffs and provide AI-powered insights
2. **Development Workflow**: Demonstrates how Copilot CLI enhances post-commit documentation tasks
3. **AI-Powered Insights**: Shows how Copilot CLI can understand context and provide meaningful analysis
4. **Verification & Status**: The app checks Copilot CLI availability and shows status in the UI
5. **Graceful Fallback**: Includes fallback mechanisms when Copilot CLI is unavailable, ensuring the app always works

### Verifying Copilot CLI Usage

The application provides several ways to verify Copilot CLI is being used:

1. **Status Banner**: When you open the app, a banner shows if Copilot CLI is available
2. **API Endpoint**: Check `/api/copilot/check` to see Copilot CLI status
3. **Analysis Results**: The results message indicates how many commits were analyzed with Copilot CLI
4. **Health Endpoint**: `/api/health` includes Copilot CLI availability information

### Example Output

When Copilot CLI is available:
```
✅ Successfully analyzed 5 commit(s) and generated documentation 
   (Copilot CLI used for 5/5 commits)
```

When Copilot CLI is not available:
```
✅ Successfully analyzed 5 commit(s) and generated documentation 
   (Using fallback analysis - Copilot CLI not available)
```

## 🔧 Configuration

### Server Options

```bash
# Custom host and port
poetry run docweave serve --host 0.0.0.0 --port 8080

# Development mode with auto-reload
poetry run docweave serve --reload
```

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

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [GitHub Copilot CLI](https://github.com/github/gh-copilot)
- Uses [Mermaid](https://mermaid.js.org/) for diagrams

---

**Made with ❤️ to showcase the power of GitHub Copilot CLI**
