from enum import Enum
from typing import Callable, Optional

from interactive_engine.strings import PlayerStrings, SystemStrings

on_action_base = Callable[[object, 'Action', 'Scene', 'Player'], None]
"""
Type alias for the callable signature used for the on_action attribute in the Action class.

Args:
    object: The engine instance (not typed to avoid circular imports)
    Action: The action being performed
    Scene: The current scene
    Player: The current player
"""

class ActionType(Enum):
    """Enumeration of possible action types in the interactive engine."""
    # Scene actions
    MOVE = "move"
    LOOK = "look"
    LISTEN = "listen"
    SPEAK = "speak"
    TOUCH = "touch"
    TAKE = "take"

    # Item actions
    EXAMINE = "examine"
    USE = "use"

    # Player actions
    INVENTORY = "inventory"
    COMBINE = "combine"

    # system actions
    HELP = "help"
    # SAVE = "save"
    # LOAD = "load"
    # CONTINUE = "continue"
    # RESTART = "restart"
    EXIT = "exit"

    # Meta actions
    EMPTY = "empty"

class Action:
    """Class representing an action in the interactive engine."""
    def __init__(
            self,
            text: str,
            action_type: Optional[ActionType] = None,
            success_text: Optional[str] = None,
            fail_text_lack_items: Optional[str] = None,
            target_scene: Optional['Scene'] = None,
            gives_items: Optional[list['Item']] = None,
            requires_items: Optional[list['Item']] = None,
            removes_items: Optional[list['Item']] = None
        ):
        # Required attributes
        self.text = text
        """The text to display when the action is called"""

        # Optional attributes
        self.action_type = action_type
        """This action's type"""

        self.success_text: Optional[str] = success_text
        """The text to display on successful completion of the action, if applicable"""

        self.fail_text_lack_items: Optional[str] = fail_text_lack_items
        """The text to display if the action lacks required items, if applicable"""

        self.target_scene: Optional[Scene] = target_scene
        """The scene this action leads to, if any"""

        self.gives_items: Optional[list[Item]] = gives_items
        """Items this action gives to the player, if any"""

        self.requires_items: Optional[list[Item]] = requires_items
        """Items required to perform this action, if any"""

        self.removes_items: Optional[list[Item]] = removes_items
        """Items this action removes from the player, if any"""

        self.on_action: on_action_base = lambda engine, action, scene, player: None
        """Callable to execute when the action is performed"""

    def run_action(self, engine, scene: 'Scene', player: 'Player'):
        """
        Perform side-effects of running an action

        Args:
            scene (Scene): The current scene
            player (Player): The current player
        """
        if self.on_action:
            self.on_action(engine, self, scene, player)

    def __str__(self):
        return f"Action(action_type={self.action_type}, text={self.text})"

empty_action = Action(SystemStrings.MISSING_ACTION_TEXT, ActionType.EMPTY)
"""Commonly used "empty" action instance"""

class Player:
    """Class representing a player. There must always be at least one player"""
    def __init__(
            self,
            name: str = PlayerStrings.DEFAULT_NAME,
            description: str = PlayerStrings.DEFAULT_DESCRIPTION
        ):
        self.name = name
        """The name of the player. This is what they will be referred to as."""

        self.description = description
        """The description of the player."""

        self.actions = {
            ActionType.INVENTORY: empty_action,
            ActionType.COMBINE: empty_action
        }
        """
        A dictionary mapping ActionTypes to the Action objects that can be performed on this player. Typical
        action types are INVENTORY and COMBINE.
        """

        self.inventory = [] # type: list[Item]
        """The list of items the player currently has in their inventory."""

    def add_inventory_items(self, items: list['Item']):
        """
        Adds items to the player's inventory

        Args:
            items (list[Item]): The items to add
        """
        self.inventory.extend(items)

    def remove_inventory_items(self, items: list['Item']):
        """
        Removes items from the player's inventory

        Args:
            items (list[Item]): The items to remove
        """
        for item in items:
            if item in self.inventory:
                self.inventory.remove(item)

class Item:
    """Class representing an item that a player can put into their inventory."""
    def __init__(self, name: str, description: str):
        self.name = name
        """The name of the item. This is what it must be referred to as in commands."""

        self.description = description
        """The description of the item"""

        self.actions = {
            ActionType.EXAMINE: empty_action,
            ActionType.USE: empty_action
        }
        """
        A dictionary mapping ActionTypes to the Action objects that can be performed on this item. Typical
        action types are EXAMINE and USE.
        """

class Scene:
    """
    A single continuous play-space that the user can explore via allowed actions that represents a
    particular state of the game world
    """
    def __init__(
            self,
            name: str, text: str,
            start_text: Optional[str] = None,
            end_text: Optional[str] = None,
        ):
        self.name = name
        """The name of the scene"""

        self.text = text
        """The text description of the scene"""

        self.start_text = start_text
        """Optional text to display when the player first enters the scene"""

        self.end_text = end_text
        """Optional text to display when the player leaves the scene"""

        self.actions = {
            ActionType.MOVE: {},
            ActionType.LOOK: {},
            ActionType.LISTEN: {},
            ActionType.SPEAK: {},
            ActionType.TOUCH: {},
            ActionType.TAKE: {},
        } # type: dict[ActionType, dict[str, Action]]
        """
        A dictionary mapping ActionTypes to the Action objects that can be performed on this scene. Typical
        action types are MOVE, LOOK, LISTEN, SPEAK, TOUCH, and TAKE.
        """

        self.child_scenes = [] # type: list[Scene]
        """A list of child scenes that inherit actions from this scene."""

    def add_action(self, action_type: ActionType, keyword: str, action: Action):
        """
        Adds an action to the scene

        Args:
            action_type (ActionType): The type of action to add
            keyword (str): The keyword to trigger the action
            action (Action): The action to add

        Returns:
            action (Action): The action that was added
        """
        # Set the type in the action, for convenience
        action.action_type = action_type

        # Save the action in the action dictionary
        self.actions[action_type][keyword] = action

        return action

