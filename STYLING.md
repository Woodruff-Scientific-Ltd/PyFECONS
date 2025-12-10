# PyFECONS Styling Guide

This document describes the styling tools and standards used in the PyFECONS project.

## Tools Used

### Core Formatting Tools

- **[Black](https://black.readthedocs.io/en/stable/)** - Uncompromising Python code formatter
  - Line length: 88 characters
  - Automatically formats code to be consistent

- **[isort](https://pycqa.github.io/isort/)** - Import statement organizer
  - Profile: Black (compatible with Black formatting)
  - Line length: 88 characters
  - Automatically sorts and organizes imports

- **[Flake8](https://flake8.pycqa.org/)** - Python linter
  - Line length: 88 characters
  - Ignores common false positives (E203, W503, etc.)
  - Excludes non-code files and directories

### Automation

- **[Pre-commit hooks](https://pre-commit.com/)** - Automatic formatting on commits
  - Runs all formatting tools before each commit
  - Ensures consistent code style across the project

## Quick Start

### For New Developers

1. **Setup development environment:**
   ```bash
   ./setup-dev.sh
   ```

2. **Make your changes**

3. **Commit your code** (hooks run automatically)

### For Existing Developers

1. **Install pre-commit:**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. **Make your changes**

3. **Commit your code** (hooks run automatically)

## Manual Usage

### Format All Files

```bash
# Use the simple script
./format.sh

# Or run pre-commit directly
pre-commit run --all-files
```

### Format Specific Files

```bash
# Format specific files with Black
pre-commit run black --files pyfecons/main.py

# Sort imports for specific files
pre-commit run isort --files pyfecons/main.py

# Lint specific files
pre-commit run flake8 --files pyfecons/main.py
```

### Individual Tools

```bash
# Black formatting
black --line-length=88 .

# isort import sorting
isort --profile=black --line-length=88 .

# Flake8 linting
flake8
```

## Configuration Files

### `.pre-commit-config.yaml`
- Defines which hooks to run
- Specifies tool versions
- Configures tool arguments

### `.flake8`
- Flake8-specific configuration
- Error codes to ignore
- Files and directories to exclude

### `pyproject.toml`
- Black configuration
- isort configuration
- Project-wide settings

## Excluded Files and Directories

The following are excluded from formatting and linting:

- **Customer files**: `customers/`
- **Deployment files**: `deployment/`
- **IDE files**: `.vscode/`, `.idea/`
- **Virtual environments**: `venv/`
- **Temporary files**: `temp/`
- **Test cache**: `.pytest_cache/`
- **Specific legacy files**: Jupyter notebooks and old scripts

## Code Style Rules

### General
- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Trailing commas**: Yes for multi-line structures

### Imports
- **Order**: Standard library → Third-party → Local
- **Grouping**: Alphabetical within groups
- **Style**: Absolute imports preferred

### Naming
- **Functions and variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: Prefix with underscore

## Troubleshooting

### Common Issues

1. **Pre-commit fails on first run**
   - Run `pre-commit run --all-files` to format all files
   - This is normal for the first setup

2. **Flake8 errors persist**
   - Check `.flake8` configuration
   - Some errors may be in excluded files

3. **Black conflicts with other tools**
   - Black is opinionated and should be run first
   - Other tools are configured to work with Black

### Ignored Error Codes

- **E203**: Whitespace before ':' (handled by Black)
- **W503**: Line break before binary operator (handled by Black)
- **F403**: 'from module import *' used
- **F405**: Name may be undefined from star imports
- **F401**: Imported but unused
- **F841**: Local variable assigned but never used
- **E501**: Line too long (handled by Black)
- **E402**: Module level import not at top of file
- **E262**: Inline comment should start with '# '

## Best Practices

1. **Always run pre-commit hooks**
   - They run automatically on commit
   - Fix issues before committing

2. **Use the format script**
   - `./format.sh` runs all checks
   - Useful for manual formatting

3. **Check before pushing**
   - Ensure all hooks pass
   - Fix any remaining issues

4. **Keep configuration updated**
   - Update tool versions when needed
   - Adjust exclusions as project grows

## Contributing

When contributing to PyFECONS:

1. **Follow the existing style**
   - Use the same formatting tools
   - Maintain consistency

2. **Test your changes**
   - Run `./format.sh` before committing
   - Ensure all hooks pass

3. **Update documentation**
   - Keep this guide current
   - Document any new tools or rules
