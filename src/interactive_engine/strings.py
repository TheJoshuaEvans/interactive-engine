from typing import ClassVar

class ActionStrings:
    EMPTY_ACTION_TEXT = "You could do that, but not in this case."

class PlayerStrings:
    DEFAULT_NAME: ClassVar[str] = "The player"

    DEFAULT_DESCRIPTION: ClassVar[str] = "What shall you be today?"

class SceneStrings:
    SCENE_DESCRIPTION_TRANSITION: ClassVar[str] = "\n\nTaking a look around you see...\n\n"

# Global strings used across the system for various messages and prompts
class SystemStrings:
    EXIT_TEXT: ClassVar[str] = "Exiting game... Thanks for playing!"

    HELP_TEXT: ClassVar[str] = (
        "Available commands:\n"
        "\n"
        "Scene actions:\n"
        "- MOVE <target>: Move to or through the target.\n"
        "- LOOK <target|item>: Look at the target or item .\n"
        "- LOOK PLAYER: Describe yourself.\n"
        "- LOOK SCENE: Describe the current scene.\n"
        # "- LISTEN <target>: Listen to the target.\n"
        # "- SPEAK <target>: Speak to or with the target.\n"
        # "- TOUCH <target>: Touch or interact with the target.\n"
        "- TAKE <item>: Pick up the specified item.\n"
        "- USE <item> [<target>]: Use the specified item, optionally on a target.\n"
        "\n"
        "Player actions:\n"
        "- INVENTORY: Describe your current inventory. (not yet implemented).\n"
        # "- COMBINE <item_a> <item_b>: Combine two items in your inventory.\n"
        "\n"
        "System actions:\n"
        "- HELP: Show this help message!\n"
        "- EXIT: Exit the game.\n"
        "- CHEAT: List all currently available actions. (not yet implemented)"
    )

    MISSING_ACTION_TEXT: ClassVar[str] = "You cannot do that."
