from abc import ABC, abstractmethod

from menu.menu_option import MenuOption


# Menu interface with abstract methods


class MenuInterface(ABC):
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def select_option(self):
        pass

    @abstractmethod
    def add_option(self, key, option: MenuOption):
        pass

    @abstractmethod
    def back_to_prev_menu(self):
        pass
