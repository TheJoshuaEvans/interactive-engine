from typing import Optional

from interactive_engine.utils.get_action import get_action
from interactive_engine.data_classes import Action, ActionType, Player, Scene
from interactive_engine.strings import SystemStrings

class InteractiveEngine:
    """
    Core class for the Interactive Engine itself. This is a singleton that handles the processing for all
    actions and gameplay states
    """
    _instance = None

    _system_actions = {
        ActionType.HELP: Action(
            text=SystemStrings.HELP_TEXT,
            action_type=ActionType.HELP
        ),
        ActionType.EXIT: Action(
            text=SystemStrings.EXIT_TEXT,
            action_type=ActionType.EXIT
        ),
    }

    def __new__(cls):
        """
        Ensures only one instance of InteractiveEngine exists (Singleton pattern).
        """
        if not cls._instance:
            cls._instance = super(InteractiveEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.current_scene = None # type: Optional[Scene]
        """The current scene the player is in. Will only be None before the game starts."""

        self.player = Player() # type: Player
        """The player"""

    def set_starting_scene(self, scene: Scene) -> str:
        """
        Sets the starting scene of the game and applies default actions. Returns the start scene text (or
        the regular scene text if no start text is provided).

        Args:
            scene (Scene): The scene to set as the starting scene

        Returns:
            out (str): The text to display upon entering the starting scene
        """
        # Set the current scene
        self.current_scene = scene

        # Add a default LOOK action that shows the scene text
        self.current_scene.add_action(
            action_type=ActionType.LOOK,
            keyword='scene',
            action=Action(text=scene.text)
        )

        # Build the output text
        out_text = ''
        if scene.start_text:
            out_text = f"{scene.start_text}\n\nTaking a look around you see...\n\n{scene.text}"
        else:
            out_text = scene.text

        return out_text

    def set_system_action(self, action: Action) -> None:
        """
        Sets a system-wide action that can be used in any scene

        Args:
            action (Action): The action to set as a system action
        """
        if action.action_type is None:
            raise ValueError("System action must have an action_type set")

        self._system_actions[action.action_type] = action

    def run(self, run_str: str) -> str:
        """
        Run a given action string through the engine and return the resulting text
        """
        # Try to find an action matching the action_str and target_str in the current scene
        if not self.current_scene:
            # This should never ever happen if the engine is used correctly
            return "FATAL ERROR: No current scene set in engine."

        try:
            action = get_action(run_str, self.current_scene.actions | self._system_actions)
        except ValueError as e:
            return str(e)

        # Perform any side effects of the action
        if action.gives_items:
            self.player.add_inventory_items(action.gives_items)
        if action.removes_items:
            self.player.remove_inventory_items(action.removes_items)
        if action.target_scene:
            # Add a default LOOK action that shows the scene text
            action.target_scene.add_action(
                action_type=ActionType.LOOK,
                keyword='scene',
                action=Action(text=action.target_scene.text)
            )
            self.current_scene = action.target_scene

        # Return the action text
        return action.text
