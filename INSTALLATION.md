# Installation Guide

## Method 1: Install from Source (Recommended)

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd DocWeave
```

### Step 2: Install with Poetry

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies and the CLI
poetry install

# Build the package
poetry build
```

### Step 3: Install Globally

```bash
# Install globally using pip
pip install --user dist/docweave-*.whl

# Or install in development mode (editable)
poetry install
export PATH="$HOME/.local/bin:$PATH"  # Add to ~/.zshrc or ~/.bashrc
```

### Step 4: Add to PATH (if needed)

Add Poetry's bin directory to your PATH. Add this to your `~/.zshrc` or `~/.bashrc`:

```bash
# For Poetry
export PATH="$HOME/.local/bin:$PATH"

# For Poetry virtualenv (if using poetry run)
export PATH="$HOME/Library/Python/3.9/bin:$PATH"  # Adjust Python version as needed
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

### Step 5: Verify Installation

```bash
docweave --help
```

## Method 2: Install as Editable Package (Development)

If you want to develop DocWeave and have changes reflect immediately:

```bash
cd DocWeave
poetry install
export PATH="$(poetry env info --path)/bin:$PATH"
```

## Method 3: Use Poetry Run (No Global Install)

You can use DocWeave without installing it globally:

```bash
cd DocWeave
poetry run docweave analyze --path /path/to/your/repo
```

## Troubleshooting

### "command not found: docweave"

1. **Check if it's installed:**
   ```bash
   which docweave
   pip show docweave
   ```

2. **Add to PATH:**
   ```bash
   # Find where pip installed it
   python3 -m pip show -f docweave | grep Location
   
   # Add that bin directory to PATH
   export PATH="$HOME/.local/bin:$PATH"
   ```

3. **Reinstall:**
   ```bash
   cd DocWeave
   poetry build
   pip install --user --force-reinstall dist/docweave-*.whl
   ```

### "Module not found" errors

Make sure you're using the same Python version that Poetry uses:

```bash
poetry env info
poetry run python --version
```

### Using in Another Repository

Once installed globally, you can use it from any directory:

```bash
cd /path/to/any/git/repo
docweave analyze
```

## Quick Test

```bash
# Test in the DocWeave repository itself
cd DocWeave
docweave analyze

# Or test in another repository
cd /path/to/other/repo
docweave analyze
```
