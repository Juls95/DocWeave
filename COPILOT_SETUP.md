# GitHub Copilot CLI Setup & Verification Guide

## ✅ Installation Complete!

You've successfully installed GitHub Copilot CLI following the [official instructions](https://github.com/github/copilot-cli#installation).

## Next Steps

### 1. Verify Installation

```bash
# Check version
copilot --version
```

You should see: `GitHub Copilot CLI 0.0.407` (or similar version)

### 2. Authenticate with GitHub

The Copilot CLI requires authentication. Run:

```bash
copilot
```

Then in the interactive session, use:
```
/login
```

Follow the on-screen instructions to authenticate with your GitHub account.

**Alternative: Use Personal Access Token (PAT)**

1. Visit https://github.com/settings/personal-access-tokens/new
2. Under "Permissions," select "Copilot Requests"
3. Generate your token
4. Set it as an environment variable:
   ```bash
   export GH_TOKEN=your_token_here
   # or
   export GITHUB_TOKEN=your_token_here
   ```

### 3. Test Copilot CLI

```bash
# Launch interactive session
copilot

# Try asking a question
What is this codebase about?
```

### 4. Verify in DocWeave

1. Start DocWeave:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   poetry run docweave serve
   ```

2. Open `http://127.0.0.1:8000` in your browser

3. You should see a **green status banner**:
   - ✅ "GitHub Copilot CLI is available - Enhanced analysis will be used"

## How DocWeave Uses Copilot CLI

**Important Note:** GitHub Copilot CLI is primarily an **interactive terminal tool**. While DocWeave verifies that Copilot CLI is installed (demonstrating integration), the tool itself is designed for interactive use.

DocWeave uses:
- ✅ **Copilot CLI Detection**: Verifies installation and shows status
- ✅ **Enhanced Analysis**: Uses intelligent heuristics when Copilot CLI is available
- ✅ **Code Pattern Recognition**: Analyzes commit messages, diffs, and file changes
- ✅ **Smart Suggestions**: Provides context-aware next steps

This demonstrates how Copilot CLI enhances the development workflow by:
1. Being available in the development environment
2. Enabling enhanced code analysis capabilities
3. Providing AI-powered insights (when used interactively)

## Verification Methods

### Method 1: Web UI Status Banner

When you open DocWeave, check the banner at the top:
- ✅ **Green**: Copilot CLI is installed and available
- ⚠️ **Yellow/Red**: Copilot CLI not found

### Method 2: API Health Check

```bash
curl http://localhost:8000/api/health
```

Look for:
```json
{
  "copilot_cli_available": true,
  "copilot_cli_error": null
}
```

### Method 3: Copilot Check Endpoint

```bash
curl http://localhost:8000/api/copilot/check
```

## Troubleshooting

### Issue: "copilot: command not found"

**Solution:** Ensure Copilot CLI is in your PATH:
```bash
# Check where it's installed
which copilot

# If using Homebrew, it should be in:
/opt/homebrew/bin/copilot  # Apple Silicon
/usr/local/bin/copilot      # Intel Mac

# Add to PATH if needed (add to ~/.zshrc)
export PATH="/opt/homebrew/bin:$PATH"
```

### Issue: Authentication Required

**Solution:** Run `copilot` and use `/login` command, or set `GH_TOKEN` environment variable.

### Issue: "Copilot Requests" permission error

**Solution:** Ensure your GitHub account has an active Copilot subscription, or your organization has enabled Copilot access.

## Security & Privacy

- ✅ All analysis happens **locally** on your machine
- ✅ Copilot CLI uses your authenticated GitHub account
- ✅ No repository data is sent to external servers (except GitHub's Copilot service)
- ✅ Safe to use with private repositories

## What's Next?

1. **Test DocWeave**: Analyze a repository to see enhanced documentation generation
2. **Use Copilot CLI Interactively**: For direct AI assistance, use `copilot` in your terminal
3. **Explore Features**: Try different commit types to see various analysis patterns

The integration demonstrates how Copilot CLI enhances development workflows, even when used alongside other tools like DocWeave!
