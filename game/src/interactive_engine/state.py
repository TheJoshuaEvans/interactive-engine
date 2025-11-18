from enum import Enum
from typing import Optional

class ActionType(Enum):
    """
    Enum representing different types of actions that can be performed in the interactive engine.
    """
    MOVE = 'move'
    TAKE = 'take'
    DROP = 'drop'
    USE = 'use'
    LOOK = 'look'

class Action:
    """
    Represents an action that can be performed in the interactive engine, that will change the state of the game
    """
    def __init__(
            self,
            action_type: ActionType,
            target: 'State'
        ):
        """
        Args:
            action_type (ActionType): The type of action to perform.
            target (State): The state the action will transition the player into.
        """
        self.action_type = action_type
        self.target = target

class State:
    """
    The current state of the interactive engine. This includes the current room the player is in, as well
    as any other relevant state information.
    """
    def __init__(
            self,
            init_text: str,

        ):
        """
        Args:
            init_text (str): The text to display when the state is initialized.
        """
        self.init_text = init_text



