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

# Global strings used across the system for various messages and prompts
class SystemStrings:
    MISSING_ACTION_TEXT: ClassVar[str] = "You cannot do that."
    """
    Default text to display when an action is missing or cannot be performed.
    """

    INVALID_COMMAND_PARTS: ClassVar[str] = "Please enter a valid action and target separated by a space."
    """Text to display when a command does not have the correct number of parts."""
