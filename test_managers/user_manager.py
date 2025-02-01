from colorama import Fore
from test_managers.text_formatter import TextFormatter
from test_managers.time_manager import TimeManager
from menu.menu import Menu


class UserManager:
    def __init__(self):
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
            print(TextFormatter.colorize(message, Fore.RED))
            TimeManager.display_sleep(1.8)
            Menu.clear_console()
            self.set_user_name()

    @staticmethod
    def validate_user_input(user_input):
        """Validate input for dictionary words"""
        messages = {
            1: "Input cannot be empty.",
            2: "Input cannot be a space.",
            3: "Input must contain more than one character.",
            4: f"{Fore.YELLOW}Are you sure you want to enter a number?"
               f" (y/n): {Fore.RESET}",
            5: "This cannot be a number.",
        }

        if user_input == "":
            raise ValueError(messages[1])
        elif user_input.isspace():
            raise ValueError(messages[2])
        elif len(user_input) == 1:
            raise ValueError(messages[3])
        elif user_input.isnumeric():
            decision = input(messages[4])
            if decision.lower() == "n":
                raise ValueError(messages[5])
        return True
