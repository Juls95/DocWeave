#!/bin/bash
# Installation script for DocWeave

set -e

echo "🔗 Installing DocWeave..."

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Installing..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi

# Navigate to DocWeave directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Install dependencies
echo "📦 Installing dependencies..."
poetry install

# Build package
echo "🔨 Building package..."
poetry build

# Install globally
echo "📥 Installing globally..."
pip install --user dist/docweave-*.whl

# Add to PATH
BIN_PATH="$HOME/.local/bin"
if [[ ":$PATH:" != *":$BIN_PATH:"* ]]; then
    echo "📝 Adding to PATH..."
    if [[ "$SHELL" == *"zsh"* ]]; then
        echo "export PATH=\"$BIN_PATH:\$PATH\"" >> ~/.zshrc
        echo "✅ Added to ~/.zshrc. Run: source ~/.zshrc"
    elif [[ "$SHELL" == *"bash"* ]]; then
        echo "export PATH=\"$BIN_PATH:\$PATH\"" >> ~/.bashrc
        echo "✅ Added to ~/.bashrc. Run: source ~/.bashrc"
    fi
fi

echo ""
echo "✅ DocWeave installed successfully!"
echo ""
echo "To use DocWeave:"
echo "  1. Reload your shell: source ~/.zshrc (or ~/.bashrc)"
echo "  2. Navigate to any git repository"
echo "  3. Run: docweave analyze"
echo ""
