[![GitHub Release](https://img.shields.io/github/v/release/TheJoshuaEvans/interactive-engine?label=Latest%20Release)](https://github.com/TheJoshuaEvans/interactive-engine/releases/latest) [![Latest Build](https://img.shields.io/github/actions/workflow/status/TheJoshuaEvans/interactive-engine/on-push-branch-main.yml?label=Latest%20Build)](https://github.com/TheJoshuaEvans/interactive-engine/actions/workflows/on-push-branch-main.yml) [![Latest Tests](https://img.shields.io/github/actions/workflow/status/TheJoshuaEvans/interactive-engine/on-push.yml?label=Latest%20Build)](https://github.com/TheJoshuaEvans/interactive-engine/actions/workflows/on-push.yml) 


# TJE Interactive: Engine

A python-based text-based adventure engine with some games

Currently in pre-alpha development of "Wizard Emergency" (Working title)

# Releases
[[Release Page](https://github.com/TheJoshuaEvans/interactive-engine/releases)]

The "Wizard Emergency" game is available as a single executable for linux, windows, and mac. Within each release folder are three binaries:
- `wizard_emergency` - **Linux** executable
- `wizard_emergency.exe` - **Windows** executable
- `wizard_emergency_mac` - **MacOS** executable

# Development

## 1. Install Python v3.12
I use us `uv` (https://github.com/astral-sh/uv) to handle python versions, and this project is configured to automatically use the correct version when using `uv`. When running a script with `uv`, replace `python` with `uv` or `uv run` depending on the context. Other platforms may also have different "python" path strings

## 2. Set up environment
Set up python dependencies
```sh
python venv
python pip install -r requirements.txt
```

## 3. Run unit tests
Run all the unit tests
```sh
python -m unittest discover -s src -p "test*.py"
```

## 4. Run the game
Before running the game, ensure the `PYTHONPATH` environment variable is set to "src"

Linux:
```sh
export PYTHONPATH=src
```

Windows (Powershell):
```ps
$env:PYTHONPATH = "src"
```

Once the envar is set for the current session, you can run the main game file directly

```sh
python wizard_emergency.py
```

## 5. Build the game
The build will be for the current system. On Ubuntu it generates a runnable library, on Windows it generates a .exe, etc
```sh
python pyinstaller wizard_emergency.spec
```

# `uv` Commands
For convenience, all the commands in the "uv" format:
```sh
uv venv
uv pip install -r requirements.txt
uv run wizard_emergency.py
uv run -m unittest discover -s src -p "test*.py"
uv run pyinstaller wizard_emergency.spec
```
---

[Developed using Copilot](https://github.com/features/copilot)
