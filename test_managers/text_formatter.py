import unicodedata
from colorama import Style, init


class TextFormatter:
    def __init__(self):
        init(autoreset=True)

    @staticmethod
    def normalize_text(text):
        """
        Removes diacritics, converts to lowercase, and strips whitespace.
        """
        if not isinstance(text, str):
            return text

        # Remove leading and trailing whitespace
        stripped_text = text.strip()

        # Normalize text to decompose diacritic characters
        normalized_text = unicodedata.normalize("NFD", stripped_text)

        # Remove diacritic marks
        without_diacritics = "".join(
            char for char in normalized_text
            if unicodedata.category(char) != "Mn"
        )

        # Replace specific characters and convert to lowercase
        final_text = without_diacritics.replace('ł', 'l').lower()

        return final_text

    @staticmethod
    def colorize(text, color):
        """
        Applies the specified color to the text.
        """
        return f"{color}{text}{Style.RESET_ALL}" if color else text

    @staticmethod
    def center_text(text, total_width, fill_char="="):
        """
        Centers the text within a given width using a specified fill character.
        """
        padding = (total_width - len(text)) // 2
        return f"{fill_char * padding} {text} {fill_char * padding}"

    def format_table_row(self, row_data, col_widths, row_colors=None):
        """
        Formats a single table row based on column widths and optional colors.
        """
        formatted_cells = []
        for i, (value, width) in enumerate(zip(row_data, col_widths)):
            # Convert value to string and handle None
            cell_text = str(value) if value is not None else ""
            # Format with proper width
            formatted_cell = f"{cell_text:<{width}}"
            # Apply color if specified
            color = None
            if row_colors and i < len(row_colors):
                color = row_colors[i]
            formatted_cells.append(self.colorize(formatted_cell, color))

        return " ".join(formatted_cells)
