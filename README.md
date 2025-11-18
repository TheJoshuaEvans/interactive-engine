# TJE Interactive: Engine

A python-based text-based adventure engine with some games

Currently in pre-alpha development of "Wizard Emergency" (Working title)

# Development

## 1. Install uv (Optional)
Follow instructions at https://github.com/astral-sh/uv to install `uv`. If you are not using "uv" replace `uv`/`uv run` in the following scripts with your python path name

## 2. Set up environment
```sh
uv venv
uv pip install -r requirements.txt
```

## 3. Run the game
Note that the PYTHONPATH environment variable must be set to "src" to run the raw python file. Also, the game _must_ be run from the project root
```sh
PYTHONPATH=src uv run wizard_emergency.py
```

> ### Run on Windows
> Use these commands to run the game in powershell
> ```ps
> $env:PYTHONPATH = "src"
> uv run wizard_emergency.py
> ```
> Note that the environment variable only needs to be set once per session

## 4. Build the game
Note that the build will be for the current system. On Ubuntu it generates a runnable library, on Windows it generates a .exe, etc
```sh
uv run pyinstaller wizard_emergency.spec
```

---

[Developed using Copilot](https://github.com/features/copilot)
