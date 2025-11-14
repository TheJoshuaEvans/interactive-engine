# Python Echo Console App

This is a minimal Python console application that echoes all input. The project uses the `uv` Python versioning system for environment management and can be built into an executable.

## Features
- Echoes all user input in the console
- Uses `uv` for Python environment and dependency management
- Instructions for building an executable

## Quick Start

### 1. Install uv
Follow instructions at https://github.com/astral-sh/uv to install `uv`.

### 2. Set up environment
```
uv venv
uv pip install -r requirements.txt
```

### 3. Run the app
```
uv run main.py
```

### 4. Build Executable
You can use the provided build script:
```
uv run pyinstaller --onefile main.py
```
This will build the `.exe` using `uv` and `pyinstaller`.
The executable will be in the `dist/` folder as `main`.

> Note: The executable will only be able to be run on the same kind of platform it was built (So a Windows .exe can only be built on a Windows system)

---

Made using Copilot Agent GPT-4.1
