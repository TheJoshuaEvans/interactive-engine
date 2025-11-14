"""
main.py - Echo Console App
"""

def main():
    print("Echo Console App. Type something and press Enter (Ctrl+C to exit):")
    try:
        while True:
            user_input = input()
            print(user_input)
    except KeyboardInterrupt:
        print("\nExiting.")

if __name__ == "__main__":
    main()
