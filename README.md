[![GitHub Release](https://img.shields.io/github/v/release/TheJoshuaEvans/interactive-engine?label=Latest%20Release)](https://github.com/TheJoshuaEvans/interactive-engine/releases/latest) [![Latest Build](https://img.shields.io/github/actions/workflow/status/TheJoshuaEvans/interactive-engine/on-push-branch-main.yml?label=Latest%20Build)](https://github.com/TheJoshuaEvans/interactive-engine/actions/workflows/on-push-branch-main.yml)

# TJE Interactive: Engine

A python-based text-based adventure engine that uses the native console!

Currently in pre-alpha development of "Wizard Emergency" (Working title)

Initial development of this project is being done as part of the [LCC CS210 Course](https://lcc-cit.github.io/CS210-CourseMaterials/). This project is meant to satisfy the requirements of Lab 5, Lab 6, Lab 7, and the term project - as enumerated [[here](https://lcc-cit.github.io/CS210-CourseMaterials/LectureNotes/CS210-Unit07-0-Overview.html#assignments-due)]

- [X] Lab 5 - Use "[AI Assisted Coding](https://lcc-cit.github.io/CS210-CourseMaterials/LectureNotes/CS210-Unit07-2-AI-AssistedCoding)" to make a simple text-based adventure engine and make a short demo game
- [ ] Lab 6 - Update the engine to use AI for processing loose input into strict inputs. For example, allowing "i want to go west" instead of restricting the program to specific instruction "move west"
- [ ] Lab 7 - Use modular / agentic AI to give the AI control over writing the prompts and descriptions, with resources that will give the model programmatic access to game state as needed
- [ ] Term Project - Actually make a complete game with a little narrative that can stretch the system a little bit

Once development related to the class is complete, there remains a couple tasks:

- [ ] Early-Access Release - Release game on steam under early access and have players provide their own ChatGPT API key
- [ ] Final Release - Use the system to pre-generate as many responses for as many scenarios as is possible, even up to gigabytes of text - then release a full version of the game that doesn't require an active connection to a cloud AI

# Releases
[[Release Page](https://github.com/TheJoshuaEvans/interactive-engine/releases)]

The "Wizard Emergency" game is available as a single executable for linux, windows, and mac. Within each release folder are three binaries:
- `wizard_emergency` - **Linux** executable
- `wizard_emergency.exe` - **Windows** executable
- `wizard_emergency_mac` - **MacOS** executable

To play the game, just download the correct release for your platform and run the standalone executable!

### Security Note
The binaries are unsigned, since this is just very early days, so your system will likely give you security warnings when running it. The release process is entirely automated using resources publicly available on GitHub (or trusted providers), so feel free to give it an audit if you are concerned. The [deployment workflows themselves](./.github/workflows/on-push-branch-main.yml) are a good place to start

# Development

## 1. Install Python v3.12
Other minor versions may work, but this project is designed to specifically use python v3.12

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
