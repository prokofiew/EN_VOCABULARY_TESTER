from colorama import Fore
from test_managers.text_formatter import TextFormatter
from test_managers.time_manager import TimeManager
from menu.menu import Menu


class UserManager:
    def __init__(self):
        self.text_formatter = TextFormatter()
        self.user_name = None

    def get_user_name(self):
        return self.user_name

    def set_user_name(self):
        try:
            user_name = input("Enter your name: ").strip()
            if self.validate_user_input(user_name):
                self.user_name = user_name
        except ValueError as error:
            message = f"ERROR! {error} "
            print(self.text_formatter.colorize(message, Fore.RED))
            TimeManager.display_sleep(1.8)
            Menu.clear_console()
            self.set_user_name()

    @staticmethod
    def validate_user_input(user_input):
        """Validate input for dictionary words"""
        if user_input == "":
            raise ValueError("Input cannot be empty.")
        elif user_input.isspace():
            raise ValueError("Input cannot be a space.")
        elif len(user_input) == 1:
            raise ValueError(
                "Input must contain more than one character.")
        elif user_input.isnumeric():
            decision = input(
                "Are you sure you want to enter a number? (y/n): ")
            if decision.lower() == "n":
                raise ValueError("This cannot be a number.")
        return True
