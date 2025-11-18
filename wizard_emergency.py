from console.console_manager import ConsoleManager

def main():
    console = ConsoleManager()
    console.write("Welcome to Wizard Emergency! You are a wizard and there is an emergency!")
    console.write("\n...Actually, it just echos your input for now. Enter 'exit' to exit. Press Enter to redraw a screen.\n")

    exit_text = "\nGoodbye, wizard! Stay safe out there."

    # Game loop
    try:
        while True:
            user_input = console.input("> ")

            # Detect Exit game
            if user_input.lower() == 'exit':
                console.write(exit_text)
                return

            # Detect Refresh
            if user_input.lower() == '':
                console.redraw_screen()
                continue

            console.write(f"You entered: {user_input}")
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        console.write(exit_text)
if __name__ == "__main__":
    main()
