from typing import ClassVar

# Global strings used by the Player data class
class SceneStrings:
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
