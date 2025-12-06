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
engine = InteractiveEngine()
console: Optional[ConsoleManager] = None

# Temporary. TODO: Add a proper action limit system that integrates with the engine itself
actions_remaining: str|int = "∞"

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
    console.write(GameStrings.WELCOME_TEXT)
    console.draw_dinkus()

    #* Update default system hooks
    # Custom exit action text
    engine._system_actions[ActionType.EXIT].on_action=lambda e,a,s,p: GameStrings.EXIT_TEXT

    engine.on_exit(graceful_exit)

    #* Define the player
    engine.player = Player(
        name=PlayerStrings.NAME,
        description=PlayerStrings.DESCRIPTION
    )

    #* Define the scenes
    # The dusty cell (the starting scene)
    dusty_cell = Scene(
        name=SceneStrings.DustyCell.NAME,
        start_text=SceneStrings.DustyCell.START_TEXT,
        text=SceneStrings.DustyCell.INITIAL_TEXT
    )

    # A mysterious misty expanse (the ending scene)
    misty_expanse = Scene(
        name=SceneStrings.MistyExpanse.NAME,
        start_text=SceneStrings.MistyExpanse.START_TEXT,
        text=SceneStrings.MistyExpanse.TEXT
    )

    #* Define items that are in the dusty cell
    wizard_hat_item = Item(
        name=ItemStrings.WizardHat.NAME,
        code=ItemStrings.WizardHat.CODE,
        description=ItemStrings.WizardHat.DESCRIPTION
    )
    door_key_item = Item(
        name=ItemStrings.CellDoorKey.NAME,
        code=ItemStrings.CellDoorKey.CODE,
        description=ItemStrings.CellDoorKey.DESCRIPTION
    )

    #* Add actions to the dusty cell scene
    # Take the wizard hat
    def on_take_hat(e,a:Action,s:Scene,p:Player) -> str:
        p.add_inventory_items([wizard_hat_item])
        s.state[StateKeys.HAT_TAKEN] = True
        s.remove_action(a)

        if s.state.get(StateKeys.KEY_TAKEN, False):
            s.text = SceneStrings.DustyCell.KEY_HAT_TAKEN_TEXT
        else:
            s.text = SceneStrings.DustyCell.HAT_TAKEN_TEXT

        # Handle taking the hat after the door is open
        if s.state.get(StateKeys.DOOR_OPEN, False):
            s.text = SceneStrings.DustyCell.DOOR_OPEN_HAT_TAKEN_TEXT

        # Now that the hat is taken, maybe take the stool too? (Not actually)
        dusty_cell.add_action(
            action_type=ActionType.TAKE,
            keyword=ActionStrings.TakeStool.CODE,
            action=Action(
                on_action=lambda e,a,s,p: ActionStrings.TakeStool.TEXT
            ),
        )

        return ActionStrings.TakeWizardHat.TEXT

    dusty_cell.add_action(
        action_type=ActionType.TAKE,
        keyword=ItemStrings.WizardHat.CODE,
        action=Action(
            on_action=on_take_hat
        ),
    )

    # Take the cell door key
    def on_take_key(e,a:Action,s:Scene,p:Player) -> str:
        p.add_inventory_items([door_key_item])
        s.state[StateKeys.KEY_TAKEN] = True
        s.remove_action(a)

        if s.state.get(StateKeys.HAT_TAKEN, False):
            s.text = SceneStrings.DustyCell.KEY_HAT_TAKEN_TEXT
        else:
            s.text = SceneStrings.DustyCell.KEY_TAKEN_TEXT
        return ActionStrings.TakeCellDoorKey.TEXT

    dusty_cell.add_action(
        action_type=ActionType.TAKE,
        keyword=ItemStrings.CellDoorKey.CODE,
        action=Action(
            on_action=on_take_key
        ),
    )

    # Use the cell door key on the door
    def on_use_key_on_door(e,a:Action,s:Scene,p:Player) -> str:
        if not p.inventory_contains([door_key_item]):
            return ActionStrings.UseCellDoorKeyOnDoor.FAIL_TEXT

        s.state[StateKeys.DOOR_OPEN] = True
        p.remove_inventory_items([door_key_item])
        s.remove_action(a)

        if s.state.get(StateKeys.HAT_TAKEN, False):
            s.text = SceneStrings.DustyCell.DOOR_OPEN_HAT_TAKEN_TEXT
        else:
            s.text = SceneStrings.DustyCell.DOOR_OPEN_TEXT
        return ActionStrings.UseCellDoorKeyOnDoor.TEXT

    dusty_cell.add_action(
        action_type=ActionType.USE,
        keyword=ActionStrings.UseCellDoorKeyOnDoor.CODE,
        action=Action(
            on_action=on_use_key_on_door
        ),
    )

    # Move through the open door an end the game!
    def on_move_door(e,a:Action,s:Scene,p:Player) -> str:
        if not s.state.get(StateKeys.DOOR_OPEN, False):
            return ActionStrings.MoveDoor.FAIL_NOT_OPEN_TEXT

        if not p.inventory_contains([wizard_hat_item]):
            return ActionStrings.MoveDoor.FAIL_NO_HAT_TEXT

        # Move to the misty expanse
        engine.set_current_scene(misty_expanse)

        # Return only the start text since this is the end of the game!
        return f"{ActionStrings.MoveDoor.TEXT}\n\n{misty_expanse.start_text}"

    dusty_cell.add_action(
        action_type=ActionType.MOVE,
        keyword=ActionStrings.MoveDoor.CODE,
        action=Action(
            on_action=on_move_door
        ),
    )

    console.top_border_text = GameStrings.GAME_TITLE_TEXT.format(version=get_version())
    console.bottom_border_text = GameStrings.ACTIONS_REMAINING_TEXT.format(actions_remaining=actions_remaining)

    start_text = engine.set_current_scene(dusty_cell)
    console.write(start_text)

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

        # Run the input through the engine and get the output
        output_text = engine.run(user_input)
        console.write(output_text, render=False)

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        # Keyboard interrupt (Ctrl+C) gets a graceful exit with no pause
        graceful_exit(0)

    except Exception as e:
        # Everything else can stay ugly
        raise e
