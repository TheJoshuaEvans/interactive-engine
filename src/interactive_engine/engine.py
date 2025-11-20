from typing import Optional

from interactive_engine.data_classes import Action, ActionType, Player, Scene
from interactive_engine.strings import SystemStrings

class InteractiveEngine:
    """
    Core class for the Interactive Engine itself. This is a singleton that handles the processing for all
    actions and gameplay states
    """
    _instance = None

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

    def run(self, run_str: str) -> str:
        """
        Run a given action string through the engine and return the resulting text
        """
        # Split the run string using the first space to get the action and target
        parts = run_str.strip().split(' ', 1)
        if len(parts) != 2:
            return SystemStrings.INVALID_COMMAND_PARTS

        action_str, target_str = parts

        # Try to find an action matching the action_str and target_str in the current scene
        if not self.current_scene:
            # This should never ever happen if the engine is used correctly
            return "FATAL ERROR: No current scene set in engine."

        action_type = ActionType._value2member_map_.get(action_str.lower()) # type: ActionType # type: ignore
        if (not action_type):
            return SystemStrings.MISSING_ACTION_TEXT + f" (Unknown action: {action_str})"

        action_dict = self.current_scene.actions[action_type]
        if (not action_dict):
            return SystemStrings.MISSING_ACTION_TEXT + f" (No actions of type: {action_type.value})"

        action = action_dict.get(target_str.lower())
        if not action:
            return SystemStrings.MISSING_ACTION_TEXT + f" (No action found for target: {target_str})"

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
