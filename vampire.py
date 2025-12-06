import sys
import time
from typing import Optional

from console.console_manager import ConsoleManager
from console.console_styles import BrightColors

from interactive_engine.engine import InteractiveEngine
from interactive_engine.data_classes import ActionType, Action, Item, Player, Scene
from utils.get_version import get_version

# Import all the strings
from wizard_emergency_utils.strings import GameStrings, StateKeys
from wizard_emergency_utils.strings import ActionStrings, ItemStrings, PlayerStrings, SceneStrings

# Global references to the core libraries
console: Optional[ConsoleManager] = None

def graceful_exit(pause_time_seconds: float = 1) -> None:
    """
    Handle graceful exit of the game.

    Args:
        pause_time_seconds (float): Time to wait before exiting, default is 1 second.
    """
    global console
    if console:
        console.write(GameStrings.EXIT_TEXT)

    time.sleep(pause_time_seconds)
    sys.exit(0)

def start_game(console: ConsoleManager) -> None:
    console.top_border_text = " == 1000 Year Old Vampire == "
    console.write(GameStrings.WELCOME_TEXT)
    console.draw_dinkus()


def main():
    global console
    console = ConsoleManager()
    start_game(console)

    # Game loop
    while True:
        # Wait for the user enter a command
        user_input = console.input("> ")

        # Detect Refresh
        if user_input.lower() == '':
            # Do nothing to trigger another call to console.input - which will redraw the screen
            continue

        # Print the user's input back to the console
        console.write_empty(render=False)
        console.write(f"> {user_input}", render=False)
        console.write_empty(render=False)

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        # Keyboard interrupt (Ctrl+C) gets a graceful exit with no pause
        graceful_exit(0)

    except Exception as e:
        # Everything else can stay ugly
        raise e
