import os
import re
from collections import namedtuple
from typing import List, Optional

from console.console_styles import Colors, remove_styles

ConsoleEntry = namedtuple('ConsoleEntry', ['is_input', 'text'])
"""
A tuple representing a console entry.
"""

class ConsoleManager:
    """
    Singleton class to manage console input/output operations and maintain a history of interactions.
    Includes functionality to customize the console appearance and behavior, including adding a border to
    written text
    """

    # --------- Internal Variables ---------
    # Singleton instance
    _instance = None

    # List to store history of console interactions
    _history: List['ConsoleEntry'] = []

    # Default input prompt prefix
    _input_prefix: str = '> '

    # Default border character
    _border_char: str = '#'

    # Default border color
    _border_color = Colors.BLUE

    # --------- Constructor ---------
    def __new__(cls):
        """
        Ensures only one instance of ConsoleManager exists (Singleton pattern).
        """
        if cls._instance is None:
            cls._instance = super(ConsoleManager, cls).__new__(cls)
        return cls._instance

    # --------- Properties ---------
    @property
    def border_char(self) -> str:
        """
        Gets the current border character for the console window.

        Returns:
            str: The border character.
        """
        return self._border_char

    @border_char.setter
    def border_char(self, char: str) -> None:
        """
        Sets a new border character for the console window.

        Args:
            char (str): The new border character.
        """
        self._border_char = char

    @property
    def border_color(self) -> str:
        """
        Gets the current border color for the console window.

        Returns:
            str: The border color.
        """
        return self._border_color

    @border_color.setter
    def border_color(self, color: str) -> None:
        """
        Sets a new border color for the console window.

        Args:
            color (str): The new border color.
        """
        self._border_color = color

    @property
    def input_prefix(self) -> str:
        """
        Gets the current input prompt prefix.

        Returns:
            str: The input prompt prefix.
        """
        return self._input_prefix

    @input_prefix.setter
    def input_prefix(self, prefix: str) -> None:
        """
        Sets a new input prompt prefix.

        Args:
            prefix (str): The new prefix to use for input prompts.
        """
        self._input_prefix = prefix

    # --------- Private Methods ---------
    def _wrap_text_with_ansi(self, text: str, width: int) -> list[str]:
        """
        Wraps text to the specified width while preserving ANSI escape sequences.
        Words shorter than the width will not be broken apart.

        Args:
            text (str): The text to wrap (may contain ANSI codes).
            width (int): The maximum visible width per line.

        Returns:
            list[str]: List of wrapped lines with ANSI codes preserved.
        """
        # Pattern to match ANSI escape sequences
        ansi_pattern = re.compile(r'(\033\[[0-9;]*m)')

        # Split text into segments (text and ANSI codes)
        segments = ansi_pattern.split(text)

        wrapped_lines = []
        current_line = ''
        current_line_visible_length = 0
        active_styles = []  # Track currently active ANSI codes

        for segment in segments:
            if ansi_pattern.match(segment):
                # This is an ANSI code - add it without affecting visible length
                current_line += segment
                active_styles.append(segment)
            else:
                # This is visible text - split by words
                words = re.split(r'(\s+)', segment)  # Split on whitespace, keeping delimiters

                for word in words:
                    if not word:
                        continue

                    word_length = len(word)

                    # If adding this word would exceed width
                    if current_line_visible_length + word_length > width:
                        # If the word itself is longer than width, we must break it
                        if word_length > width:
                            # Add as much as we can to current line
                            space_left = width - current_line_visible_length
                            if space_left > 0:
                                current_line += word[:space_left]
                                word = word[space_left:]

                            # Start a new line
                            if current_line:
                                wrapped_lines.append(current_line)
                            current_line = ''.join(active_styles)
                            current_line_visible_length = 0

                            # Break remaining word across lines
                            while len(word) > width:
                                current_line += word[:width]
                                wrapped_lines.append(current_line)
                                word = word[width:]
                                current_line = ''.join(active_styles)
                                current_line_visible_length = 0

                            # Add remaining part of word
                            if word:
                                current_line += word
                                current_line_visible_length = len(word)
                        else:
                            # Word fits within width, so move to next line
                            if current_line_visible_length > 0:
                                wrapped_lines.append(current_line)
                                current_line = ''.join(active_styles)
                                current_line_visible_length = 0

                            current_line += word
                            current_line_visible_length = word_length
                    else:
                        # Word fits on current line
                        current_line += word
                        current_line_visible_length += word_length

        # Add the last line if it has content
        if current_line_visible_length > 0 or current_line:
            wrapped_lines.append(current_line)

        return wrapped_lines if wrapped_lines else [text]

    def _clear_console(self) -> None:
        """
        Clears the console screen using the appropriate system command.
        """
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def _print_console_window(self, lines: list[str], width: Optional[int] = None, height: Optional[int] = None) -> None:
        """
        Prints the given lines to fill the console window, padding/truncating as needed. Uses get_console_size
        for default width and height if not provided. Adds a border around the content using the border_char.
        """
        if width is None or height is None:
            width_, height_ = self.get_console_size()
            width = width if width is not None else width_
            height = height if height is not None else height_

        # Go through all the lines and separate new line characters into individual lines
        expanded_lines = []
        for line in lines:
            expanded_lines.extend(line.splitlines())
            if line.endswith('\n'):
                expanded_lines.append('')
        lines = expanded_lines

        # Pad or truncate each line to fit the console width minus borders
        content_width = width - 4  # Account for left, right borders, and horizontal buffer

        padded_lines: list[str] = []
        for line in lines:
            # Visible version without ANSI styles for length calculations
            stripped = remove_styles(line)

            # Break into multiple lines if the visible characters exceed the available content width
            if len(stripped) > content_width:
                # Wrap the text while preserving ANSI escape sequences
                wrapped = self._wrap_text_with_ansi(line, content_width)
                for wrapped_line in wrapped:
                    visible_text = remove_styles(wrapped_line)
                    padding_needed = max(0, content_width - len(visible_text))
                    padded_line = f' {wrapped_line} ' + (' ' * padding_needed)
                    padded_lines.append(padded_line)
            else:
                display_text = line
                visible_text = stripped
                # Compute padding based on visible length only
                padding_needed = max(0, content_width - len(visible_text))
                padded_line = f' {display_text} ' + (' ' * padding_needed)
                padded_lines.append(padded_line)

        # Fill remaining lines with spaces if not enough lines, including vertical buffer
        while len(padded_lines) < height - 2:  # Account for top and bottom vertical buffer
            padded_lines.insert(0, ' ' * (content_width + 2))

        # Include escape codes for border color
        border_chars = f'{self.border_color}{self.border_char}{Colors.RESET}'

        # Ensure the top border is always a single line, regardless of overflow
        top_border = [border_chars * width]  # Single top border line

        # Add vertical buffer (empty line) below the top border
        padded_lines.insert(0, ' ' * (content_width + 2))
        padded_lines.append(' ' * (content_width + 2))

        # Add side borders to each line
        bordered_lines = [border_chars + line + border_chars for line in padded_lines]

        # Add a single bottom border to match the console height
        bottom_border = [border_chars * width]  # Single line of border at the bottom

        # Combine all parts
        final_output = top_border + bordered_lines + bottom_border

        # Actually perform the prints
        self._clear_console()
        for line in final_output:
            print(line, end='')
            print()

    # --------- Methods ---------
    def write(self, text: str, clear: bool = False) -> None:
        """
        Writes text at the bottom of the console and records it in history

        Args:
            text (str): The text to display.
            clear (bool): If True, clears the console before writing.
        """
        if clear:
            self._clear_console()

        history_outputs = [entry.text for entry in self._history if not entry.is_input]

        # Prepare lines to display, including the new line
        lines_to_display = history_outputs.copy()
        lines_to_display.append(text)

        # Print to the console
        self._print_console_window(lines_to_display)

        # Record in history
        self._history.append(ConsoleEntry(False, text))

    def input(self, prompt: Optional[str] = None) -> str:
        """
        Prompts the user for input at the bottom of the console and records it in history

        Args:
            prompt (Optional[str]): Custom prompt to display. If None, uses input_prefix.

        Returns:
            str: The user's input.
        """
        if prompt is None:
            prompt = self.input_prefix

        history_outputs = [entry.text for entry in self._history if not entry.is_input]

        # Adjust the height to account for the top border, bottom border, and two extra lines (empty line + input line)
        console_width, console_height = self.get_console_size()
        adjusted_height = console_height - 4

        # Display previous outputs
        lines_to_display = history_outputs[:]
        self._print_console_window(lines_to_display, width=console_width, height=adjusted_height)

        # Add an empty line between the border and the input
        print()

        # Get and save the user's input
        user_input = input(prompt)
        self._history.append(ConsoleEntry(True, user_input))
        return user_input

    def redraw_screen(self, is_input: bool = True) -> None:
        """
        Manually re-draws the screen with the current history and settings.
        """
        history_outputs = [entry.text for entry in self._history if not entry.is_input]

        # Get the console size
        console_width, console_height = self.get_console_size()

        # Adjust for input height if in input mode
        adjusted_height = console_height
        if is_input:
            adjusted_height = console_height - 4

        # Display the current history
        self._print_console_window(history_outputs, width=console_width, height=adjusted_height)

    def get_history(self) -> List['ConsoleEntry']:
        """
        Returns a copy of the console interaction history.

        Returns:
            List[ConsoleEntry]: List of all input/output entries.
        """
        return self._history.copy()

    def clear_history(self) -> None:
        """
        Clears the console interaction history.
        """
        self._history.clear()

    def get_latest_input(self) -> Optional[str]:
        """
        Retrieves the most recent input text from the history.

        Returns:
            Optional[str]: The latest input text, or None if no input exists.
        """
        for entry in reversed(self._history):
            if entry.is_input:
                return entry.text
        return None

    def get_latest_output(self) -> Optional[str]:
        """
        Retrieves the most recent output text from the history.

        Returns:
            Optional[str]: The latest output text, or None if no output exists.
        """
        for entry in reversed(self._history):
            if not entry.is_input:
                return entry.text
        return None

    def get_console_size(self) -> tuple[int, int]:
        """
        Returns the (width, height) of the console window. Returns a (0, 0) tuple if not
        attached to a terminal.

        Returns:
            tuple: (width, height) of the console window.
        """
        try:
            size = os.get_terminal_size()
            return (size.columns, size.lines)
        except OSError:
            # Fallback if not attached to a terminal
            return (0, 0)
