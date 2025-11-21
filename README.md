[![GitHub Release](https://img.shields.io/github/v/release/TheJoshuaEvans/interactive-engine?label=Latest%20Release)](https://github.com/TheJoshuaEvans/interactive-engine/releases/latest) [![Latest Build](https://img.shields.io/github/actions/workflow/status/TheJoshuaEvans/interactive-engine/on-push-branch-main.yml?label=Latest%20Build)](https://github.com/TheJoshuaEvans/interactive-engine/actions/workflows/on-push-branch-main.yml) 


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
```sh
python venv
python pip install -r requirements.txt
```

## 3. Run the game
Note that the PYTHONPATH environment variable must be set to "src" to run the raw python file. Also, the game _must_ be run from the project root
```sh
PYTHONPATH=src python wizard_emergency.py
```

> ### Run on Windows
> Use these commands to run the game in powershell
> ```ps
> $env:PYTHONPATH = "src"
> python wizard_emergency.py
> ```
> Note that the environment variable only needs to be set once per session

## 4. Build the game
The build will be for the current system. On Ubuntu it generates a runnable library, on Windows it generates a .exe, etc
```sh
python pyinstaller wizard_emergency.spec
```


# `uv` Commands
For convenience, all the commands in the "uv" format:
```sh
uv venv
uv pip install -r requirements.txt
PYTHONPATH=src uv run wizard_emergency.py
uv run pyinstaller wizard_emergency.spec
```
---

[Developed using Copilot](https://github.com/features/copilot)
