from console.console_manager import ConsoleManager

from interactive_engine.engine import InteractiveEngine
from interactive_engine.data_classes import ActionType, Action, Item, Player, Scene

has_started = False

exit_text = "\nGoodbye, wizard! Stay safe out there."
engine = InteractiveEngine()

def start_game(console: ConsoleManager) -> None:
    """Establish the game state and write the starting text to the console, if the game has not already started."""
    global has_started
    if has_started:
        return

    console.write("Welcome to Wizard Emergency! You are a wizard and there is an emergency!")
    console.write("Type 'exit' to quit or 'help' for assistance. Run an empty command to re-render the console.")
    console.draw_dinkus()

    engine.player = Player(
        name="The Wizard",
        description="You are a wizard Harry! Or... Is that your name? Your head kind of hurts..."
    )

    starting_scene = Scene(
        name="Dusty Cell",
        start_text="You awake in a small room. The air is thick with dust, dimly lit by a flickering magic candle. Your wand and spellbook are missing, and you have been dressed in simple grey robes.\n\nYou have woken up in stranger predicaments, so you aren't actually that worried. At least nothing is exploding. Yet.",
        text="You are in a small, dusty, dimly lit room. There is a door to the north and a key hanging next to the door. Your magic wizard hat sits on a small stool in the corner, covered in dust."
    )
    starting_scene_no_hat = Scene(
        name="Dusty Cell",
        text="You are in a small, dusty, dimly lit room. There is a door to the north and a key hanging next to the door. There is an empty stool in the corner where your wizard hat used to be, untouched by dust."
    )
    starting_scene_no_key = Scene(
        name="Dusty Cell",
        text="You are in a small, dusty, dimly lit room. There is a door to the north with an empty nail and a dust mark next to it, where the key used to hang. Your magic wizard hat sits on a small stool in the corner, covered in dust."
    )
    starting_scene_no_key_no_hat = Scene(
        name="Dusty Cell",
        text="You are in a small, dusty, dimly lit room. There is a door to the north with an empty nail and a dust mark next to it, where the key used to hang. There is an empty stool in the corner where your wizard hat used to be, untouched by dust."
    )

    wizard_hat_item = Item(
        name="Wizard Hat",
        description="An old, dusty wizard hat with a distinguished point. It doesn't actually help you cast spells, but no self-respecting wizard would be caught dead without one."
    )
    starting_scene.add_action(
        action_type=ActionType.TAKE,
        keyword='hat',
        action=Action(
            text="You pick up the dusty old had from the stool, give it a quick shake, and place it on your head. You don't feel any more magical, but you do feel far less naked. The dust from the hat tickles your nose.",
            gives_items=[wizard_hat_item],
            target_scene=starting_scene_no_hat
        ),
    )
    starting_scene_no_key.add_action(
        action_type=ActionType.TAKE,
        keyword='hat',
        action=Action(
            text="You pick up the dusty old had from the stool, give it a quick shake, and place it on your head. You don't feel any more magical, but you do feel far less naked. The dust from the hat tickles your nose.",
            gives_items=[wizard_hat_item],
            target_scene=starting_scene_no_key_no_hat
        ),
    )

    key_item = Item(
        name="Cell Key",
        description="A small, rusty key that looks like it could open a cell door. It has an old tag attached that reads 'Cell Key'."
    )
    starting_scene.add_action(
        action_type=ActionType.TAKE,
        keyword='key',
        action=Action(
            text="You take the rusty key from the nail. It feels cold in your hand.",
            gives_items=[key_item],
            target_scene=starting_scene_no_key
        ),
    )
    starting_scene_no_hat.add_action(
        action_type=ActionType.TAKE,
        keyword='key',
        action=Action(
            text="You take the rusty key from the nail. It feels cold in your hand.",
            gives_items=[key_item],
            target_scene=starting_scene_no_key_no_hat
        ),
    )

    start_text = engine.set_starting_scene(starting_scene)
    console.write(start_text)

def main():
    console = ConsoleManager()
    start_game(console)

    # Game loop
    try:
        while True:
            user_input = console.input("> ")

            # Detect Refresh
            if user_input.lower() == '':
                # Do nothing to trigger another call to console.input - which will redraw the screen
                continue

            # Print an empty line between messages for readability
            console.write_empty()

            # Run the input through the engine and get the output
            output_text = engine.run(user_input)
            console.write(output_text)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        console.write(exit_text)

if __name__ == "__main__":
    main()
