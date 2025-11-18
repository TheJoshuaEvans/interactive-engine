"""
main.py - Echo Console App
"""

from ..src.console.console_manager import ConsoleManager
from ..src.interactive_engine.state import State

def main():
    console = ConsoleManager()
    state = State(init_text="Welcome to the Wizard Emergency!")
    console.write(state.init_text)

    while True:
        try:
            command = console.input()
            console.write(f"You entered: {command}")
        except KeyboardInterrupt:
            console.write("Gracefully exiting...")
            break
if __name__ == "__main__":
    main()
