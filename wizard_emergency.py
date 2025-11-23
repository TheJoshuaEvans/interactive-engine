import sys
import time

from console.console_manager import ConsoleManager

from interactive_engine.engine import InteractiveEngine
from interactive_engine.data_classes import ActionType, Action, Item, Player, Scene

# Import all the strings
from wizard_emergency_utils.strings import GameStrings, StateKeys
from wizard_emergency_utils.strings import ActionStrings, ItemStrings, PlayerStrings, SceneStrings

has_started = False

exit_text = "\nGoodbye, wizard! Stay safe out there."
engine = InteractiveEngine()

actions_remaining: str|int = "∞"

def start_game(console: ConsoleManager) -> None:
    """Establish the game state and write the starting text to the console, if the game has not already started."""
    global has_started
    if has_started:
        return

    console.write(GameStrings.WELCOME_TEXT)
    console.draw_dinkus()

    #* Update default system hooks
    # Custom exit action text
    engine._system_actions[ActionType.EXIT].on_action=lambda e,a,s,p: GameStrings.EXIT_TEXT

    # Graceful exit handling
    def on_exit_handler() -> None:
        # Print the exit text, wait a second, then exit
        console.write(GameStrings.EXIT_TEXT)
        time.sleep(1)
        sys.exit(0)

    engine.on_exit(on_exit_handler)

    #* Define the player
    engine.player = Player(
        name=PlayerStrings.NAME,
        description=PlayerStrings.DESCRIPTION
    )

    #* Define the starting scene - the dusty cell
    dusty_cell = Scene(
        name=SceneStrings.DustyCell.NAME,
        start_text=SceneStrings.DustyCell.START_TEXT,
        text=SceneStrings.DustyCell.INITIAL_TEXT
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

    #* Add actions to the scene
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

    def on_move_door(e,a:Action,s:Scene,p:Player) -> str:
        if not s.state.get(StateKeys.DOOR_OPEN, False):
            return ActionStrings.MoveDoor.FAIL_NOT_OPEN_TEXT

        if not p.inventory_contains([wizard_hat_item]):
            return ActionStrings.MoveDoor.FAIL_NO_HAT_TEXT

        return ActionStrings.MoveDoor.TEXT
    dusty_cell.add_action(
        action_type=ActionType.MOVE,
        keyword=ActionStrings.MoveDoor.CODE,
        action=Action(
            on_action=on_move_door
        ),
    )

    console.border_text = f" - Actions Remaining: {actions_remaining} - "

    start_text = engine.set_starting_scene(dusty_cell)
    console.write(start_text)

def main():
    console = ConsoleManager()
    start_game(console)

    # Game loop
    try:
        while True:
            # Wait for the user enter a command
            user_input = console.input("> ")

            # Detect Refresh
            if user_input.lower() == '':
                # Do nothing to trigger another call to console.input - which will redraw the screen
                continue

            # Print an empty line between messages for readability
            console.write_empty()

            # Run the input through the engine and get the output
            output_text = engine.run(user_input)
            console.write(output_text)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        console.write(GameStrings.EXIT_TEXT)

if __name__ == "__main__":
    main()
