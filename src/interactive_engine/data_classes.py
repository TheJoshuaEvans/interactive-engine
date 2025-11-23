from enum import Enum
from functools import singledispatchmethod
from typing import Callable, Optional

from interactive_engine.strings import ActionStrings, PlayerStrings, SystemStrings

on_action_def = Callable[[object, 'Action', 'Scene', 'Player'], str]
"""
Type alias for the callable signature used for the on_action attribute in the Action class.

Args:
    object: The engine instance (not typed to avoid circular imports)
    Action: The action being performed
    Scene: The current scene
    Player: The current player
"""

empty_lambda = lambda engine, action, scene, player: ActionStrings.EMPTY_ACTION_TEXT
"""An "empty" lambda that matches the on_action_base signature"""

class ActionType(Enum):
    """Enumeration of possible action types in the interactive engine."""
    # Scene actions
    MOVE = "move"
    LOOK = "look"
    LISTEN = "listen"
    SPEAK = "speak"
    TOUCH = "touch"
    TAKE = "take"
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
    LIST = "list"
    EXIT = "exit"

    # Meta actions
    EMPTY = "empty"

class Action:
    """Class representing an action in the interactive engine."""
    def __init__(
            self,
            action_type: ActionType = ActionType.EMPTY,
            on_action: on_action_def = empty_lambda
        ):
        self.action_type = action_type
        """This action's type"""

        self.on_action: on_action_def = on_action
        """Callable to execute when the action is performed. Returns the action text"""

    def run_action(self, engine, scene: 'Scene', player: 'Player') -> str:
        """
        Perform side-effects of running an action

        Args:
            scene (Scene): The current scene
            player (Player): The current player
        """
        return self.on_action(engine, self, scene, player)

    def __str__(self):
        return f"Action(action_type={self.action_type})"


empty_action = Action(ActionType.EMPTY)
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
            # Default action for the player looking at themselves
            ActionType.LOOK: {
                'player': Action(
                    on_action=lambda e,a,s,p: p.description
                )
            },
            ActionType.INVENTORY: Action(
                on_action=lambda e,a,s,p: PlayerStrings.INVENTORY_EMPTY_TEXT
                if len(p.inventory) == 0 else
                PlayerStrings.INVENTORY_LIST_TEXT.format(
                    items=' (x1)\n- '.join([item.name for item in p.inventory])
                ) + ' (x1)'
            )
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

    def inventory_contains(self, items: list['Item']) -> bool:
        """
        Checks if the player's inventory contains all of the specified items

        Args:
            items (list[Item]): The items to check for

        Returns:
            contains (bool): True if the item is in the inventory, False otherwise
        """
        return all(self.inventory.count(item) > 0 for item in items)

class Item:
    """Class representing an item that a player can put into their inventory."""
    def __init__(self, name: str, code: str, description: str):
        self.name = name
        """The name of the item."""

        self.code = code
        """The keyword used to reference this item in commands."""

        self.description = description
        """The description of the item"""

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
            ActionType.USE: {},
        } # type: dict[ActionType, dict[str, Action]]
        """
        A dictionary mapping ActionTypes to the Action objects that can be performed on this scene. Typical
        action types are MOVE, LOOK, LISTEN, SPEAK, TOUCH, TAKE, and USE.
        """

        self.state = {}
        """A dictionary representing arbitrary state information for the scene."""

        # Add the "look scene" action by default
        self.add_action(
            action_type=ActionType.LOOK,
            keyword='scene',
            action=Action(on_action=lambda e,a,s,p: s.text)
        )

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

    @singledispatchmethod
    def remove_action(self, arg):
        raise NotImplementedError("Unsupported type for remove_action")

    @remove_action.register(ActionType)
    def _(self, action_type: ActionType, keyword: str):
        """
        Removes all actions with a given type and keyword from the scene

        Args:
            action_type (ActionType): The type of action to remove
            keyword (str): The keyword of the action to remove
        """
        if keyword in self.actions[action_type]:
            del self.actions[action_type][keyword]

    @remove_action.register(Action)
    def _(self, action: Action):
        """
        Removes all actions matching the given action instance from the scene

        Args:
            action (Action): The action instance to remove
        """
        for keyword, act in list(self.actions[action.action_type].items()):
            if act == action:
                del self.actions[action.action_type][keyword]
