# GitHub Copilot CLI Setup & Verification Guide

DocWeave invokes the **standalone GitHub Copilot CLI** (`copilot`) via subprocess for AI-powered analysis. You need the `copilot` command in your PATH—**gh** is not required.

## Installation

### Install Copilot CLI (Standalone)

Choose one method. See [official docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/install-copilot-cli) for more.

```bash
# macOS/Linux (Homebrew)
brew install copilot-cli

# npm (requires Node.js 22+)
npm install -g @github/copilot

# Install script
curl -fsSL https://gh.io/copilot-install | bash
```

**Note:** The older `gh extension install github/gh-copilot` is deprecated. DocWeave uses the standalone `copilot` CLI.

### 1. Verify Installation

```bash
copilot --version
```

You should see output like: `GitHub Copilot CLI 0.0.407` (or similar).

### 2. Authenticate with GitHub

The Copilot CLI requires authentication. Run:

```bash
copilot
```

In the interactive session, use:
```
/login
```

Follow the on-screen instructions.

**Alternative: Personal Access Token**

1. Visit https://github.com/settings/personal-access-tokens/new
2. Under "Permissions," select **Copilot Requests**
3. Generate your token
4. Set as environment variable:
   ```bash
   export GH_TOKEN=your_token_here
   # or
   export GITHUB_TOKEN=your_token_here
   ```

### 3. Verify in DocWeave

**CLI:**
```bash
cd /path/to/any/git/repo
docweave analyze -l 2
```

You should see:
- ✅ "GitHub Copilot CLI is available - using enhanced analysis"
- Per-commit AI analysis (may take ~30–60 seconds per commit)

**Web UI (optional):**
```bash
poetry run docweave serve
# Open http://127.0.0.1:8000
```

Green banner = Copilot CLI available.

## How DocWeave Uses Copilot CLI

DocWeave **invokes Copilot programmatically** via `copilot -p "prompt"` for:

- ✅ **Per-commit analysis**: Each commit’s diff + message sent to Copilot; JSON parsed for summary, rationale, next steps, importance
- ✅ **Deep diagrams**: Copilot generates Mermaid architecture, sequence, and state diagrams
- ✅ **Narrative**: Technical and business narrative across commits
- ✅ **Integration insights**: Answers like "Where are integrations? Best way to solve login?" in `INTEGRATION.md`

When Copilot is unavailable or fails, DocWeave falls back to heuristic analysis. Output is always generated.

## Verification Methods

### CLI

Run `docweave analyze` and check the output:
- ✅ "GitHub Copilot CLI is available - using enhanced analysis" → Copilot is used
- ⚠️ "GitHub Copilot CLI not available" → Fallback heuristics only

### Web UI (when `docweave serve` is running)

- ✅ **Green banner**: Copilot CLI available
- ⚠️ **Yellow/Red**: Copilot not found

### API (when `docweave serve` is running)

```bash
curl http://localhost:8000/api/health
# or
curl http://localhost:8000/api/copilot/check
```

## Troubleshooting

### "copilot: command not found"

Ensure Copilot CLI is in your PATH:
```bash
which copilot

# Homebrew locations:
# /opt/homebrew/bin/copilot  (Apple Silicon)
# /usr/local/bin/copilot     (Intel Mac)

export PATH="/opt/homebrew/bin:$PATH"  # Add to ~/.zshrc if needed
```

### Authentication Required

Run `copilot` → `/login`, or set `GH_TOKEN` / `GITHUB_TOKEN`.

### "Copilot Requests" permission error

Ensure your GitHub account has an active Copilot subscription (or org access).

## Security & Privacy

- Analysis runs locally; diffs/commits are sent to GitHub’s Copilot service for AI processing
- Copilot CLI uses your authenticated GitHub account
- Safe to use with private repositories (same trust as using Copilot in VS Code)

## What's Next?

1. Run `docweave analyze` on any git repo
2. Check `DocweaveDocs/` for CHANGES.md, DIAGRAMS.md, NARRATIVE.md, INTEGRATION.md, NEXT_STEPS.md
3. Use `copilot` interactively for ad-hoc questions
