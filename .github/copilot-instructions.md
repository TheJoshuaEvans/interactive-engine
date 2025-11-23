# General Instructions
Use this command to run unit tests (replace PATH/TO/FILE.py with the actual path to the test file, relative to the src directory):
```sh
python -m unittest src/PATH/TO/FILE.py -v
```

The application must be run from the project root directory - it is NOT globally installed.

# Running on TheJoshuaEvans' Local Environment
Project root directory for TheJoshuaEvans' local machine:
```
/root/dev/tje/interactive-engine
```

When running in TheJoshuaEvans' local environment, "uv" is used for python version management and must be used when running commands instead of "python" (so `python file.py` becomes `uv run file.py` and `python pip install` becomes `uv pip install`). "uv" documentation can be found here: https://github.com/astral-sh/uv

Test command on TheJoshuaEvans' local environment:
```sh
cd /root/dev/tje/interactive-engine &&
uv run -m unittest src/PATH/TO/FILE.py -v
```
