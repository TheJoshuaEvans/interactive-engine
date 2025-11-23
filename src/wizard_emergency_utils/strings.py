from typing import ClassVar

# ================ System Strings ===================
class GameStrings:
    """General strings for the Wizard Emergency game."""
    WELCOME_TEXT = (
        "Welcome to Wizard Emergency! You are a wizard and there is an emergency!\n"
        "Type 'exit' to quit or 'help' for assistance. Run an empty command to re-render the console."
    )
    EXIT_TEXT = "Goodbye, wizard! Stay safe out there."

class StateKeys:
    """Keys used in scene state dictionaries for the Wizard Emergency game."""

    HAT_TAKEN = "hat_taken"
    """Key indicating whether the wizard hat has been taken."""

    KEY_TAKEN = "key_taken"
    """Key indicating whether the cell door key has been taken."""

# ================ Gameplay Strings ===================

class ActionStrings:
    """Strings for various actions in the Wizard Emergency game."""
    class TakeWizardHat:
        TEXT = (
            "You pick up the dusty old hat from the stool, give it a quick shake, and place it on your head. "
            "You don't feel any more magical, but you do feel far less naked. "
            "The dust from the hat tickles your nose."
        )

    class TakeCellDoorKey:
        TEXT = (
            "You take the rusty key from the nail. It feels cold in your hand."
        )

class ItemStrings:
    """Strings for various items in the Wizard Emergency game."""
    class WizardHat:
        NAME = "Wizard Hat"

        CODE = "hat"

        DESCRIPTION = (
            "An old, dusty wizard hat with a distinguished point. "
            "It doesn't actually help you cast spells, but no self-respecting wizard would be caught dead without one."
        )

    class CellDoorKey:
        NAME = "Cell Key"

        CODE = "key"

        DESCRIPTION = (
            "A small, rusty key that looks like it could open a cell door. "
            "It has an old tag attached that reads 'Cell Key'."
        )

class PlayerStrings:
    """Strings for the player in the Wizard Emergency game."""
    NAME = "The Wizard"

    DESCRIPTION = "You are a wizard Harry! Or... Is that your name? Your head kind of hurts..."

class SceneStrings:
    """Strings for various scenes in the Wizard Emergency game."""
    class DustyCell:
        NAME = "Dusty Cell"

        class Snippets:
            BASE_DESCRIPTION = "You are in a small, dusty, dimly lit room."

            HAT_NOT_TAKEN = "Your magic wizard hat sits on a small stool in the corner, covered in dust."
            KEY_NOT_TAKEN = "There is a key hanging next to the door."

            HAT_TAKEN = "There is an empty stool in the corner where your wizard hat used to be, untouched by dust."
            KEY_TAKEN = "There is a door to the north with an empty nail and a dust mark next to it, where the key used to hang."

        START_TEXT = (
            "You awake in a small room. The air is thick with dust, dimly lit by a flickering magic candle. "
            "Your wand and spellbook are missing, and you have been dressed in simple grey robes.\n\n"
            "You have woken up in stranger predicaments, so you aren't actually that worried. At least nothing is exploding. Yet."
        )

        INITIAL_TEXT = f"{Snippets.BASE_DESCRIPTION} {Snippets.KEY_NOT_TAKEN} {Snippets.HAT_NOT_TAKEN}"
        HAT_TAKEN_TEXT = f"{Snippets.BASE_DESCRIPTION} {Snippets.KEY_NOT_TAKEN} {Snippets.HAT_TAKEN}"
        KEY_TAKEN_TEXT = f"{Snippets.BASE_DESCRIPTION} {Snippets.KEY_TAKEN} {Snippets.HAT_NOT_TAKEN}"
        KEY_HAT_TAKEN_TEXT = f"{Snippets.BASE_DESCRIPTION} {Snippets.KEY_TAKEN} {Snippets.HAT_TAKEN}"
