import unicodedata
from colorama import Style, init


class TextFormatter:
    def __init__(self):
        init(autoreset=True)

    @staticmethod
    def normalize_text(text):
        """
        Removing diacritics, converting to lowercase, and stripping whitespace
        """
        if not isinstance(text, str):
            return text
        text = text.strip()  # Remove leading and trailing whitespace
        normalized_text = unicodedata.normalize("NFD", text)
        return "".join(
            c for c in normalized_text if unicodedata.category(c) != "Mn"
        ).replace('ł', 'l').lower()

    def colorize(self, text, color):
        """
        Applies the specified color to the text.
        """
        return f"{color}{text}{Style.RESET_ALL}" if color else text

    def center_text(self, text, total_width, fill_char="="):
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
