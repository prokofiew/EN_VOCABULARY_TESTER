from abc import ABC, abstractmethod


class MenuInterface(ABC):
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def select_option(self):
        pass

    @abstractmethod
    def add_option(self):
        pass

    @abstractmethod
    def back_to_prev_menu(self):
        pass
