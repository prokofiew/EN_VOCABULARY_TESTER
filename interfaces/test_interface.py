from abc import ABC
from abc import abstractmethod

# Test iterface with abstract methods


class Test(ABC):

    @abstractmethod
    def start_test(self):
        pass

    @abstractmethod
    def get_questions_and_answers_data(self):
        pass

    @abstractmethod
    def submit_answer(self, answer):
        pass

    @abstractmethod
    def get_results(self):
        pass

    @abstractmethod
    def end_test(self):
        pass

    @abstractmethod
    def save_results(self):
        pass
