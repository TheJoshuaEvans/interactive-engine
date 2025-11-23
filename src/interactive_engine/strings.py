from typing import ClassVar

# Global strings used by the Player data class
class PlayerStrings:
    DEFAULT_NAME: ClassVar[str] = "The player"
    """
    Default player name
    """

    DEFAULT_DESCRIPTION: ClassVar[str] = "What shall you be today?"
    """
    Default player description
    """

class SceneStrings:
    SCENE_DESCRIPTION_TRANSITION: ClassVar[str] = "\n\nTaking a look around you see...\n\n"
    """
    Text to display between the scene intro text and the scene description text
    """

# Global strings used across the system for various messages and prompts
class SystemStrings:
    EXIT_TEXT: ClassVar[str] = "Exiting game... Thanks for playing!"
    """Default exit message when the player chooses to exit the game."""

    HELP_TEXT: ClassVar[str] = (
        "Available commands:\n"
        "\n"
        "Scene actions:\n"
        "- MOVE <target>: Move to or through the target.\n"
        "- LOOK <target>: Look at the target.\n"
        "- LOOK SCENE: Describe the current scene.\n"
        "- LISTEN <target>: Listen to the target. (not yet implemented).\n"
        "- SPEAK <target>: Speak to or with the target. (not yet implemented).\n"
        "- TOUCH <target>: Touch or interact with the target. (not yet implemented).\n"
        "- TAKE <item>: Pick up the specified item.\n"
        "\n"
        "Player actions:\n"
        "- INVENTORY: Describe your current inventory.\n"
        "- COMBINE <item1> <item2>: Combine two items in your inventory.\n"
        "\n"
        "Item actions:\n"
        "- EXAMINE <item>: Examine the specified item.\n"
        "- USE <item> [<target>]: Use the specified item. Optionally use the item on the target.\n"
        "\n"
        "System actions:\n"
        "- HELP: Show this help message!\n"
        "- EXIT: Exit the game.\n"
    )
    """
    Default help message listing available commands.
    """

    MISSING_ACTION_TEXT: ClassVar[str] = "You cannot do that."
    """
    Default text to display when an action is missing or cannot be performed.
    """
