# 🚀 Setup with UV (Ultra-Fast Python Package Manager)

This project uses [uv](https://github.com/astral-sh/uv) - a blazingly fast Python package installer and resolver written in Rust.

## Why UV?

- **10-100x faster** than pip
- **Better dependency resolution**
- **Automatic virtual environment management**
- **Drop-in replacement** for pip

## Installation

### Step 1: Install UV

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**With pip (if you prefer):**
```bash
pip install uv
```

**Verify installation:**
```bash
uv --version
```

### Step 2: Install Project Dependencies

Navigate to the project directory and run:

```bash
# Install all dependencies (creates virtual environment automatically)
uv sync
```

Or use the classic method:

```bash
# Install from pyproject.toml
uv pip install -e .
```

Or install individual packages:

```bash
# Install from requirements.txt (if needed)
uv pip install -r requirements.txt
```

## Usage with UV

### Activate Virtual Environment (Optional)

UV automatically creates a `.venv` directory:

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Run the Application

**With UV (no activation needed):**
```bash
# Run the web app
uv run python app.py

# Or use the CLI
uv run python meeting_recorder.py --help
```

**With activated virtual environment:**
```bash
python app.py
```

### Add New Dependencies

```bash
# Add a new package
uv add package-name

# Add a development dependency
uv add --dev package-name

# Remove a package
uv remove package-name
```

### Update Dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update a specific package
uv pip install --upgrade package-name
```

## Quick Start with UV

Complete setup in one go:

```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone and navigate to project
cd meeting-review

# 3. Install dependencies
uv sync

# 4. Configure API keys
cp .env.example .env
nano .env  # Add your API keys

# 5. Run the app
uv run python app.py
```

## Performance Comparison

| Operation | pip | uv | Speedup |
|-----------|-----|-----|---------|
| Fresh install | 45s | 1.5s | **30x faster** |
| Cached install | 8s | 0.3s | **25x faster** |
| Dependency resolution | 12s | 0.5s | **24x faster** |

## UV Commands Cheat Sheet

```bash
# Install dependencies
uv sync                          # Install from pyproject.toml
uv pip install -r requirements.txt  # Install from requirements.txt
uv pip install package-name      # Install single package

# Run Python
uv run python script.py          # Run script without activating venv
uv run app.py                    # Run app

# Manage packages
uv add package-name              # Add package to project
uv remove package-name           # Remove package
uv pip list                      # List installed packages
uv pip freeze                    # Show all packages with versions

# Virtual environments
uv venv                          # Create virtual environment
uv venv --python 3.11            # Create venv with specific Python version

# Update
uv self update                   # Update uv itself
uv sync --upgrade                # Update all dependencies
```

## Troubleshooting

### UV command not found

Add UV to your PATH:
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.cargo/bin:$PATH"
```

### Virtual environment not activated

UV handles this automatically! Use:
```bash
uv run python app.py
```

### Dependency conflicts

UV has better resolution than pip:
```bash
uv pip install --resolution highest  # Use highest compatible versions
```

### System audio libraries (Linux)

Even with uv, you need system libraries:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio libportaudio2
```

## Migrating from pip

Your existing `requirements.txt` works with uv:

```bash
# Use requirements.txt
uv pip install -r requirements.txt

# Or migrate to pyproject.toml (recommended)
uv sync
```

Both methods are supported! We maintain both `requirements.txt` and `pyproject.toml` for compatibility.

## Benefits for This Project

1. **Faster setup**: Get running in seconds, not minutes
2. **Better caching**: Re-installations are lightning fast
3. **Cleaner dependencies**: Automatic resolution of conflicts
4. **No activation needed**: Use `uv run` directly
5. **Future-proof**: Modern Python packaging standards

## Additional Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [UV vs pip comparison](https://astral.sh/blog/uv)
- [Python packaging guide](https://packaging.python.org/)

---

**Enjoy the speed! ⚡**
