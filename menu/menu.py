import time
import os

from interfaces.menu_interface import MenuInterface
from menu.menu_option import MenuOption

# Class responsible for initialization end display of Main menu.
# Implements menu_inteface and its methods
# Provides static method to clear console


class Menu(MenuInterface):
    def __init__(self, title, controller, parent_menu=None):
        self.title = title
        self.options = {}
        self.controller = controller
        self.parent_menu = parent_menu
        self.__initialize_menu_options()

    @staticmethod
    def clear_console():
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def __initialize_menu_options(self):
        # private method to initialize Main menu
        if self.title == "Main menu":
            self.add_option(1, MenuOption(
                "Start new test", action=self.controller.start_test))
            self.add_option(2, MenuOption(
                "Settings", submenu=Menu("Settings", self.controller, self)))
            self.add_option(3, MenuOption(
                "Exit", action=self.controller.exit_program))
        elif self.title == "Settings":
            self.add_option(1, MenuOption(
                "Add dictionary", action=self.controller.add_dictionary))
            self.add_option(2, MenuOption(
                "Display dictionaries",
                action=self.controller.display_dictionaries))
            self.add_option(3, MenuOption(
                "About program", action=self.controller.about_program_display))
            self.add_option(4, MenuOption(
                "Return to main menu", action=self.back_to_prev_menu))

    def add_option(self, key, option):
        # public method to add an option to menu
        self.options[key] = option

    def display(self):
        # public method to display menu
        self.clear_console()
        print(f"\n==== {self.title} ====")
        for key, option in self.options.items():
            if key == "confirm_selection":
                continue
            print(f"{key}. {option.label}")

        choice = self.select_option()
        if isinstance(choice, list):
            self.options['confirm_selection'].execute(*choice)
        elif choice is not None:
            self.options[choice].execute()
            self.display()

    def select_option(self):
        try:
            choice = input("\nSelect an option: ").strip()
            if choice.isdigit() and int(choice) in self.options:
                return int(choice)
            self.__display_error_message(
                "Invalid option!\n\nPlease try again.")
            return None
        except ValueError:
            self.__display_error_message("Please enter a valid number.")
            return None

    def __display_error_message(self, message):
        """ Displaying error message,
        clearing console and returning to menu. """
        self.clear_console()
        print(message)
        time.sleep(1.5)
        self.display()

    def back_to_prev_menu(self):
        if self.parent_menu:
            self.parent_menu.display()
