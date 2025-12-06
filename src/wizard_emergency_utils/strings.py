from console.console_styles import BrightColors, Codes, style

# ================ System Strings ===================
class GameStrings:
    """General strings for the Wizard Emergency game."""
    WELCOME_TEXT = (
        "Welcome to Wizard Emergency! You are a wizard and there is an emergency!\n"
        "Type 'exit' to quit or 'help' for assistance. Run an empty command to re-render the console."
    )

    GAME_TITLE_TEXT = f" {BrightColors.BLUE}=== Wizard Emergency v{{version}} ==={BrightColors.RESET} "

    ACTIONS_REMAINING_TEXT = f" {BrightColors.BLUE}- Actions remaining: {{actions_remaining}} -{BrightColors.RESET} "

    EXIT_TEXT = "\nGoodbye, wizard! Stay safe out there."

class StateKeys:
    """Keys used in scene state dictionaries for the Wizard Emergency game."""

    HAT_TAKEN = "hat_taken"
    """Key indicating whether the wizard hat has been taken."""

    KEY_TAKEN = "key_taken"
    """Key indicating whether the cell door key has been taken."""

    DOOR_OPEN = "door_open"
    """Key indicating whether the cell door has been opened."""

# ================ Gameplay Strings ===================

class ActionStrings:
    """Strings for various actions in the Wizard Emergency game."""
    class TakeWizardHat:
        TEXT = (
            "You pick up the dusty old hat from the stool, give it a quick shake, and place it on your head. "
            "You don't feel any more magical, but you do feel far less naked. "
            "The dust from the hat tickles your nose."
        )

    class TakeStool:
        CODE = "stool"

        TEXT = (
            "You consider taking the clean stool, but you don't."
        )

    class TakeCellDoorKey:
        TEXT = (
            "You take the rusty key from the nail. It feels cold in your hand."
        )

    class UseCellDoorKeyOnDoor:
        CODE = "key door"

        TEXT = (
            "You insert the rusty key into the cell door's lock and turn it. "
            "With a satisfying click, the door unlocks and creaks open, revealing a strange mist beyond - "
            "but the key breaks off in the lock and you are unable to retrieve it."
        )

        FAIL_TEXT = (
            "You don't have the key to use on the door. It's still hanging on the wall."
        )

    class MoveDoor:
        CODE = "door"

        TEXT = (
            "You step through the open cell door and into the strange mist beyond. "
            "What adventures await? We shall find out soon enough..."
        )

        FAIL_NO_HAT_TEXT = (
            "You can't possibly leave without your wizard hat, what kind of wizard are you!?"
        )

        FAIL_NOT_OPEN_TEXT = (
            "The door is still closed. You need to use the key on it first."
        )

    class LookStatue:
        CODE = "statue"

        TEXT = (
            "You take a closer look at the shimmering statue. As you approach, it seems to ripple and shift, "
            "almost as if it's made of liquid light. You feel a strange pull towards it, as if it's calling to you."
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
            "A small key that looks like it could open the cell door. "
            "This ancient key has seen better days, its metal worn and tarnished by time and... sea salt? "
        )

class PlayerStrings:
    """Strings for the player in the Wizard Emergency game."""
    NAME = "The Wizard"

    DESCRIPTION = "You're a wizard Brian! Or... Is that your name? Your head kind of hurts..."

class SceneStrings:
    """Strings for various scenes in the Wizard Emergency game."""
    class DustyCell:
        NAME = "Dusty Cell"

        class Snippets:
            BASE_DESCRIPTION = "You are in a small, dusty, dimly lit room with a sturdy wooden door on one wall and a bench on the other."

            DOOR_OPEN = "The cell door stands open, leading into a strange mist. You do no know what lies beyond."

            HAT_NOT_TAKEN = "Your magic wizard hat sits on a small stool in the corner, covered in dust."
            HAT_TAKEN = "There is an empty stool in the corner where your wizard hat once sat. The stool is completely absent of dust."

            KEY_NOT_TAKEN = "There is a key hanging next to the door."
            KEY_TAKEN = "A dust mark hangs next to the door, where the key used to be."

        START_TEXT = (
            "You awake in a small room. The air is thick with dust, dimly lit by a flickering magic candle. "
            "Your wand and spellbook are missing, and you have been dressed in simple grey robes.\n\n"
            "You have woken up in stranger predicaments, so you aren't actually that worried. At least nothing is exploding. Yet."
        )

        INITIAL_TEXT = f"{Snippets.BASE_DESCRIPTION} {Snippets.KEY_NOT_TAKEN} {Snippets.HAT_NOT_TAKEN}"
        HAT_TAKEN_TEXT = f"{Snippets.BASE_DESCRIPTION} {Snippets.KEY_NOT_TAKEN} {Snippets.HAT_TAKEN}"
        KEY_TAKEN_TEXT = f"{Snippets.BASE_DESCRIPTION} {Snippets.KEY_TAKEN} {Snippets.HAT_NOT_TAKEN}"
        KEY_HAT_TAKEN_TEXT = f"{Snippets.BASE_DESCRIPTION} {Snippets.KEY_TAKEN} {Snippets.HAT_TAKEN}"
        DOOR_OPEN_TEXT = f"{Snippets.BASE_DESCRIPTION} {Snippets.DOOR_OPEN} {Snippets.KEY_TAKEN} {Snippets.HAT_NOT_TAKEN}"
        DOOR_OPEN_HAT_TAKEN_TEXT = f"{Snippets.BASE_DESCRIPTION} {Snippets.DOOR_OPEN} {Snippets.KEY_TAKEN} {Snippets.HAT_TAKEN}"

    class MistyExpanse:
        NAME = "Misty Expanse"

        START_TEXT = (
            f"\n{style(Codes.COLOR_GREEN, Codes.BG_COLOR_MAGENTA, Codes.BLINK)}CONGRATULATIONS!{style(Codes.RESET)}\n\n"
            "You have escaped the dusty cell and stepped into the unknown misty expanse beyond. "
            "New adventures will be coming soon - this is only the beginning!\n\n"
            "There is nothing more to do here. Type 'exit' to leave the game.\n\n"
            "Thanks for playing!"
        )

        TEXT = (
            "You are standing in a vast expanse of swirling mist. "
            "The mist glows faintly with an ethereal light, making it impossible to see very far. "
            "Strange shapes seem to move within the mist, but you can't quite make them out. "
            "It's almost as if the mist itself is alive, and is preparing new trials for you to face..."
        )

    class StatueChamber:
        NAME = "Statue Chamber"

        START_TEXT = (
            "As you pass through the strange mist, you find yourself in a grand hall filled floor-to-ceiling with ancient statues in every shape imaginable. "
            "The door behind you vanishes into the mist, leaving you with no choice but to move forward."
        )

        TEXT = (
            "You are in a grand hall filled with ancient statues. The air is thick with dust and the scent of old stone. "
            "The statues seem to watch you as you move, their eyes following your every step. "
            "At the far end of the hall, the massive statue on the obsidian pedestal seems to shimmer and shift, "
            "as if it is not entirely solid. You feel a strange pull towards it, as if it is calling to you."
        )
