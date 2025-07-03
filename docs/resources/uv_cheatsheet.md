# uv  Cheatsheet

!!! note "AI Assisted (Claude Sonnet 4)"

## What is uv?

**uv** is a fast Python package manager and project manager written in Rust by Astral. It's designed as a drop-in replacement for pip, pip-tools, and virtualenv, offering significantly faster performance and better dependency resolution.

Key benefits:

- **10-100x faster** than pip for most operations
- **Unified tool** replacing pip, pip-tools, virtualenv, and more
- **Better dependency resolution** with conflict detection
- **Cross-platform** support (Windows, macOS, Linux)
- **Compatible** with existing Python packaging standards

## Installation

### Install uv

```bash
# Using the official installer (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Using pip
pip install uv

# Using Homebrew (macOS)
brew install uv

# Using winget (Windows)
winget install --id=astral-sh.uv -e
```

### Verify Installation

```bash
uv --version
```

## Project Management

### Creating a New Project

```bash
# Create a new Python project
uv init my-project
cd my-project

# Create with specific Python version
uv init --python 3.11 my-project

# Create in current directory
uv init .
```

**What this does:** Creates a new directory with a `pyproject.toml` file, a basic project structure, and initializes a virtual environment.

### Project Structure

After `uv init`, you'll see:

```
my-project/
├── pyproject.toml      # Project configuration
├── src/
│   └── my_project/
│       └── __init__.py
├── tests/
│   └── __init__.py
└── README.md
```

## Virtual Environment Management

### Why Virtual Environments?

Virtual environments isolate your project's dependencies from your system Python and other projects, preventing version conflicts.

### Creating Virtual Environments

```bash
# Create virtual environment (uv automatically manages this)
uv venv

# Create with specific Python version
uv venv --python 3.11

# Create with custom name
uv venv my-env

# Create in specific location
uv venv /path/to/my-env
```

### Activating Virtual Environments

```bash
# On Unix/macOS
source .venv/bin/activate

# On Windows
.venv\Scripts\activate

# Or use uv run (automatically uses project's venv)
uv run python script.py
```

## Package Installation

### Basic Installation

```bash
# Install a package
uv add requests

# Install multiple packages
uv add requests numpy pandas

# Install with version constraints
uv add "requests>=2.25.0"
uv add "django>=4.0,<5.0"
```

**What happens:** uv resolves dependencies, updates `pyproject.toml`, and creates/updates `uv.lock` for reproducible installs.

### Development Dependencies

```bash
# Install development dependencies
uv add --dev pytest black flake8

# Install optional dependencies
uv add --optional test pytest coverage
```

### Installing from Different Sources

```bash
# Install from PyPI (default)
uv add requests

# Install from Git repository
uv add git+https://github.com/user/repo.git

# Install from local path
uv add ./local-package

# Install from URL
uv add https://files.pythonhosted.org/packages/.../package.whl
```

## Package Management

### Listing Packages

```bash
# List installed packages
uv pip list

# Show dependency tree
uv pip tree

# Show package information
uv pip show requests
```

### Updating Packages

```bash
# Update all packages
uv lock --upgrade

# Update specific package
uv add requests --upgrade

# Update to latest compatible version
uv add "requests>=2.25.0" --upgrade
```

### Removing Packages

```bash
# Remove a package
uv remove requests

# Remove multiple packages
uv remove requests numpy pandas

# Remove development dependencies
uv remove --dev pytest
```

## Lock Files and Reproducibility

### Understanding Lock Files

The `uv.lock` file contains exact versions of all dependencies and their dependencies. This ensures reproducible installs across different environments.

```bash
# Generate/update lock file
uv lock

# Install from lock file
uv sync

# Install without updating lock file
uv sync --frozen
```

### Synchronizing Environments

```bash
# Sync environment with pyproject.toml
uv sync

# Sync only production dependencies
uv sync --no-dev

# Sync specific groups
uv sync --group test
```

## Global Tool Management (pipx Replacement)

### Understanding pipx vs uv Tools

**pipx** is a tool that installs CLI (command-line) applications in their own isolated environments while making them globally accessible. Think of it as an "App Store for Python CLI tools" where each app is self-contained but available everywhere.

**The Problem pipx Solves:**
```bash
# ❌ Traditional global installation causes conflicts
pip install black    # black needs requests==2.25.0
pip install ruff     # ruff needs requests==2.30.0
# Conflict! Dependencies clash in global environment

# ✅ pipx solution: each tool gets its own environment
pipx install black   # black + its dependencies in environment #1
pipx install ruff    # ruff + its dependencies in environment #2
# No conflicts, both work perfectly!
```

### pipx vs uv Tool Commands

| Task | pipx Command | uv Equivalent | Notes |
|------|--------------|---------------|-------|
| Install tool globally | `pipx install black` | `uv tool install black` | Tool available system-wide |
| Run without installing | `pipx run cowsay hello` | `uvx cowsay hello` | Temporary execution |
| List installed tools | `pipx list` | `uv tool list` | Show all global tools |
| Upgrade tool | `pipx upgrade black` | `uv tool upgrade black` | Update to latest version |
| Upgrade all tools | `pipx upgrade-all` | `uv tool upgrade --all` | Update everything |
| Uninstall tool | `pipx uninstall black` | `uv tool uninstall black` | Remove tool |
| Run specific version | `pipx run --spec black==22.0.0 black` | `uvx black@22.0.0` | Use particular version |

### Installing Global Development Tools

```bash
# Traditional pipx approach
pipx install black          # Code formatter
pipx install ruff           # Linter  
pipx install mypy           # Type checker
pipx install pytest        # Testing framework
pipx install pre-commit     # Git hooks

# uv approach (much faster!)
uv tool install black ruff mypy pytest pre-commit

# Now available globally from any directory:
black my_file.py
ruff check .
mypy src/
```

### Running Tools Without Installation

```bash
# Try tools without permanent installation
uvx cowsay "Hello World!"           # Fun utility
uvx httpie http GET httpbin.org/json # HTTP client
uvx rich --help                     # Rich text demo
uvx speedtest-cli                   # Internet speed test

# Run with specific versions
uvx black@23.1.0 my_file.py
uvx ruff@0.1.0 check .

# Run with additional dependencies
uvx --with pandas python -c "import pandas; print('Works!')"
```

### Advanced Tool Management

```bash
# Install with specific Python version
uv tool install --python 3.11 black

# Install with extras
uv tool install 'jupyter[lab]'

# Install from Git repository
uv tool install git+https://github.com/user/tool.git

# Install from local path
uv tool install ./my-local-tool
```

### Tool Environment Isolation

When you install tools with uv, each gets its own isolated environment:

```
~/.local/share/uv/tools/
├── black/           # Black's isolated environment
├── ruff/            # Ruff's isolated environment  
├── pytest/         # Pytest's isolated environment
└── mypy/            # Mypy's isolated environment
```

Benefits:
- **No dependency conflicts** between tools
- **Clean system Python** remains untouched
- **Independent updates** for each tool
- **Easy removal** without leftover dependencies

## Running Python Code

### Direct Execution

```bash
# Run Python script with project dependencies
uv run python script.py

# Run module
uv run -m pytest

# Run with arguments
uv run python script.py --verbose

# Run interactive Python
uv run python
```

### Running Tools

```bash
# Run tools without installing globally
uv run --with black black .
uv run --with flake8 flake8 src/

# Run with specific Python version
uv run --python 3.11 python script.py
```

## Working with Requirements Files

### Converting from pip

```bash
# Install from requirements.txt
uv pip install -r requirements.txt

# Generate requirements.txt from current environment
uv pip freeze > requirements.txt

# Convert requirements.txt to pyproject.toml
uv add -r requirements.txt
```

### Exporting Dependencies

```bash
# Export to requirements.txt format
uv export --format requirements-txt > requirements.txt

# Export only production dependencies
uv export --no-dev --format requirements-txt > requirements.txt
```

## Python Version Management

### Installing Python Versions

```bash
# List available Python versions
uv python list

# Install specific Python version
uv python install 3.11

# Install multiple versions
uv python install 3.10 3.11 3.12

# Use specific Python for project
uv python pin 3.11
```

### Finding Python Installations

```bash
# List installed Python versions
uv python list --only-installed

# Find Python executable
uv python find 3.11
```

## Configuration

### Global Configuration

```bash
# Set global configuration
uv config set global.index-url https://pypi.org/simple/

# View configuration
uv config list

# Edit configuration file
uv config edit
```

### Project Configuration

Edit `pyproject.toml`:

```toml
[tool.uv]
# Custom index URL
index-url = "https://pypi.org/simple/"

# Additional index URLs
extra-index-url = ["https://private-pypi.company.com/simple/"]

# Exclude packages from updates
constraint-dependencies = ["numpy==1.24.0"]
```

## Advanced Features

### Dependency Groups

Define optional dependency groups in `pyproject.toml`:

```toml
[dependency-groups]
test = ["pytest>=6.0", "coverage>=5.0"]
docs = ["sphinx>=4.0", "sphinx-rtd-theme"]
dev = ["black", "flake8", "mypy"]
```

Install specific groups:

```bash
uv sync --group test
uv sync --group docs --group dev
```

### Workspaces

For multi-package projects, define workspace in `pyproject.toml`:

```toml
[tool.uv.workspace]
members = ["packages/*"]
```

### Scripts

Define custom scripts in `pyproject.toml`:

```toml
[project.scripts]
my-script = "my_package.cli:main"

[tool.uv.scripts]
test = "pytest tests/"
lint = "flake8 src/"
format = "black src/"
```

Run scripts:

```bash
uv run test
uv run lint
uv run format
```

## Common Workflows

### Starting a New Project

```bash
# 1. Create project
uv init my-project
cd my-project

# 2. Add dependencies
uv add requests click

# 3. Add development dependencies
uv add --dev pytest black flake8

# 4. Create your code
# ... write your Python code ...

# 5. Run tests
uv run pytest
```

### Working on Existing Project

```bash
# 1. Clone repository
git clone https://github.com/user/project.git
cd project

# 2. Sync dependencies
uv sync

# 3. Run the project
uv run python main.py
```

### Migrating from pip

```bash
# 1. Install uv
pip install uv

# 2. Create virtual environment
uv venv

# 3. Install existing requirements
uv pip install -r requirements.txt

# 4. Convert to pyproject.toml (optional)
uv add $(cat requirements.txt | tr '\n' ' ')
```

## Performance Tips

### Caching

uv automatically caches packages and builds. Clear cache if needed:

```bash
# Clear all caches
uv cache clean

# Clear specific package cache
uv cache clean requests
```

### Parallel Installation

uv installs packages in parallel by default. Configure concurrency:

```bash
# Limit concurrent downloads
uv pip install --max-concurrent-downloads 4
```

## Troubleshooting

### Common Issues

**Lock file conflicts:**
```bash
# Reset lock file
rm uv.lock
uv lock
```

**Python version issues:**
```bash
# Check available Python versions
uv python list

# Install required Python version
uv python install 3.11
```

**Dependency conflicts:**
```bash
# Show conflict resolution
uv add package-name --verbose

# Override with specific version
uv add "package-name==1.0.0"
```

### Getting Help

```bash
# General help
uv --help

# Command-specific help
uv add --help
uv run --help

# Version information
uv version
```

## Quick Reference

| Task | Command |
|------|---------|
| Create project | `uv init my-project` |
| Add package | `uv add requests` |
| Remove package | `uv remove requests` |
| Install all deps | `uv sync` |
| Run script | `uv run python script.py` |
| Update deps | `uv lock --upgrade` |
| List packages | `uv pip list` |
| Create venv | `uv venv` |
| Install Python | `uv python install 3.11` |
| Export deps | `uv export > requirements.txt` |
| Install global tool | `uv tool install black` |
| Run tool temporarily | `uvx cowsay hello` |

## Best Practices

1. **Always use lock files** for reproducible builds
2. **Pin Python versions** in production projects
3. **Use dependency groups** to organize optional dependencies
4. **Keep pyproject.toml clean** by using `uv add` instead of manual editing
5. **Use `uv run`** instead of activating virtual environments manually
6. **Regularly update** dependencies with `uv lock --upgrade`
7. **Use workspaces** for multi-package projects
8. **Cache Python installations** for faster project setup

## Migration Guide

### From pip + virtualenv

| Old Way | New Way |
|---------|---------|
| `python -m venv .venv` | `uv venv` |
| `pip install requests` | `uv add requests` |
| `pip install -r requirements.txt` | `uv sync` |
| `pip freeze > requirements.txt` | `uv export > requirements.txt` |
| `pip list` | `uv pip list` |

### From Poetry

| Poetry | uv |
|--------|-----|
| `poetry init` | `uv init` |
| `poetry add requests` | `uv add requests` |
| `poetry install` | `uv sync` |
| `poetry run python script.py` | `uv run python script.py` |
| `poetry shell` | `uv run python` (or activate manually) |

### From pipx

| pipx | uv |
|------|-----|
| `pipx install black` | `uv tool install black` |
| `pipx run cowsay hello` | `uvx cowsay hello` |
| `pipx list` | `uv tool list` |
| `pipx upgrade black` | `uv tool upgrade black` |
| `pipx upgrade-all` | `uv tool upgrade --all` |
| `pipx uninstall black` | `uv tool uninstall black` |

---

*[official uv documentation](https://docs.astral.sh/uv/)*