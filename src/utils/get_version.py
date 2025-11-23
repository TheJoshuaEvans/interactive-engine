import os
import sys
import toml

def get_pyproject_path():
    """
        Get the path to the pyproject.toml file, whether running in a packaged environment or not.
    """

    if getattr(sys, 'frozen', False):
        # If the application is frozen, use the temporary directory set by PyInstaller
        base_path = sys._MEIPASS # type: ignore
    else:
        # If not frozen, use the current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, 'pyproject.toml')

def get_version():
    """
        Retrieve the current version of the application from the pyproject.toml file in the root directory.
        This method can be safely run in a packaged environment.
    """
    pyproject_path = get_pyproject_path()
    with open(pyproject_path, 'r') as f:
        pyproject_data = toml.load(f)
    return pyproject_data['project']['version']
