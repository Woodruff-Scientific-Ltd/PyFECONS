#!/bin/bash

# Development setup script for PyFECONS
# This script sets up the development environment with pre-commit hooks

echo "🚀 Setting up PyFECONS development environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Install package in development mode
echo "📦 Installing package in development mode..."
pip install -e .

# Install pre-commit hooks
echo "🔗 Installing pre-commit hooks..."
pre-commit install

# Run pre-commit on all files to ensure everything is formatted
echo "✨ Running initial formatting..."
pre-commit run --all-files

echo "✅ Development environment setup complete!"
echo ""
echo "📋 What was installed:"
echo "   • Virtual environment with all dependencies"
echo "   • Pre-commit hooks for automatic formatting"
echo "   • Black code formatter"
echo "   • isort import sorter"
echo "   • Flake8 linter"
echo ""
echo "🎯 Next steps:"
echo "   • Make your changes"
echo "   • Commit your code (hooks will run automatically)"
echo "   • Or run './format.sh' to format all files"
