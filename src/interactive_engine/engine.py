from typing import Callable, Optional

from interactive_engine.utils.get_action import get_action
from interactive_engine.data_classes import Action, ActionType, Player, Scene
from interactive_engine.strings import SceneStrings, SystemStrings

on_exit_def = Callable[[], None]
"""
Type alias for the callable signature used when setting an "on exit" method.
"""

class InteractiveEngine:
    """
    Core class for the Interactive Engine itself. This is a singleton that handles the processing for all
    actions and gameplay states
    """
    _on_exit = lambda: None

    _instance = None

    _system_actions = {
        ActionType.HELP: Action(
            action_type=ActionType.HELP,
            on_action=lambda e,a,s,p: SystemStrings.HELP_TEXT
        ),
        ActionType.EXIT: Action(
            action_type=ActionType.EXIT,
            on_action=lambda e,a,s,p: SystemStrings.EXIT_TEXT
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

    def on_exit(self, on_exit: on_exit_def) -> None:
        """
        Set a callable to be executed when the engine detects an "exit" action.
        """
        self._on_exit = on_exit

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

        # Build the output text
        out_text = ''
        if scene.start_text:
            out_text = f"{scene.start_text}{SceneStrings.SCENE_DESCRIPTION_TRANSITION}{scene.text}"
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

        current_scene = self.current_scene
        try:
            # Get actions from the current scene and system actions
            action = get_action(run_str, current_scene.actions | self._system_actions)
        except ValueError as e:
            return str(e)

        # Handle exit action special case
        if action.action_type == ActionType.EXIT:
            self._on_exit()

        # Return the action text
        return action.run_action(self, current_scene, self.player)
