Use this command to run unit tests (replace PATH/TO/FILE.py with the actual path to the test file, relative to the src directory):
```sh
uv run -m unittest src/PATH/TO/FILE.py -v
```

"uv" is used for python version management and must be used when running commands instead of "python" (so `python file.py` becomes `uv run file.py` and `python pip install` becomes `uv pip install`). "uv" documentation can be found here: https://github.com/astral-sh/uv

The application must be run from the project root directory - it is NOT globally installed.

Project root directory for TheJoshuaEvans local machine:
```
/root/dev/tje/interactive-engine
```
