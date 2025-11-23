from typing import ClassVar

from console.console_styles import Colors

class ActionStrings:
    EMPTY_ACTION_TEXT = "You could do that, but not in this case."

class PlayerStrings:
    DEFAULT_NAME: ClassVar[str] = "The player"

    DEFAULT_DESCRIPTION: ClassVar[str] = "What shall you be today?"

    INVENTORY_EMPTY_TEXT: ClassVar[str] = "Your inventory is empty."

    INVENTORY_LIST_TEXT: ClassVar[str] = "You are carrying:\n- {items}"

class SceneStrings:
    SCENE_DESCRIPTION_TRANSITION: ClassVar[str] = "\n\nTaking a look around you see...\n\n"

# Global strings used across the system for various messages and prompts
class SystemStrings:
    EXIT_TEXT: ClassVar[str] = "Exiting game... Thanks for playing!"

    HELP_TEXT: ClassVar[str] = (
        "Available commands:\n"
        "\n"
        "Scene actions:\n"
        f"- {Colors.GREEN}move <target>{Colors.RESET}: Move to or through the target.\n"
        f"- {Colors.GREEN}look <target|item>{Colors.RESET}: Look at the target or item.\n"
        f"- {Colors.GREEN}look player{Colors.RESET}: Describe yourself.\n"
        f"- {Colors.GREEN}look scene{Colors.RESET}: Describe the current scene.\n"
        # f"- {Colors.GREEN}listen <target>{Colors.RESET}: Listen to the target.\n"
        # f"- {Colors.GREEN}speak <target>{Colors.RESET}: Speak to or with the target.\n"
        # f"- {Colors.GREEN}touch <target>{Colors.RESET}: Touch or interact with the target.\n"
        f"- {Colors.GREEN}take <item>{Colors.RESET}: Pick up the specified item.\n"
        f"- {Colors.GREEN}use <item> [<target>]{Colors.RESET}: Use the specified item, optionally on a target.\n"
        "\n"
        "Player actions:\n"
        f"- {Colors.GREEN}inventory{Colors.RESET}: Describe your current inventory.\n"
        # f"- {Colors.GREEN}combine <item_a> <item_b>{Colors.RESET}: Combine two items in your inventory.\n"
        "\n"
        "System actions:\n"
        f"- {Colors.GREEN}help{Colors.RESET}: Show this help message!\n"
        f"- {Colors.GREEN}exit{Colors.RESET}: Exit the game.\n"
        f"- {Colors.GREEN}list actions{Colors.RESET}: List all currently available actions."
    )

    MISSING_ACTION_TEXT: ClassVar[str] = "You cannot do that."
