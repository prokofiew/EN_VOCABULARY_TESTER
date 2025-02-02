import random
import time
from colorama import Fore

from test_managers.text_formatter import TextFormatter


class QuestionManager:
    def __init__(self, data):
        self.data = data
        self.questions_amount = 0
        self.selected_category = None

    def set_category(self, category):
        self.selected_category = category

    def set_questions_amount(self):
        """ Let user choose number of questions in test"""
        try:
            questions_amount = int(input("Enter number of questions: "))
            available_questions = self.__get_available_questions_count()

            if questions_amount > available_questions:
                message = (
                    "Warning, requested number of questions exceeds "
                    "available questions. Adjusting maximum available -> "
                    f"{available_questions}")
                print(f"{TextFormatter.colorize(message, Fore.YELLOW)}")
                self.questions_amount = available_questions
            else:
                self.questions_amount = questions_amount

            return self.questions_amount

        except ValueError:
            message = "Invalid value. Enter a number"
            print(TextFormatter.colorize(message, Fore.RED))
            time.sleep(1.8)
            return self.set_questions_amount()

    def __get_available_questions_count(self):
        """ Check if there are enough questions in selected category"""
        if self.selected_category == "All categories":
            return len(self.data)
        else:
            # list of selected categories
            selected_categories = (
                [self.selected_category]
                if isinstance(self.selected_category, str)
                else self.selected_category
            )
            return len(self.data[
                self.data["category_name"].isin(selected_categories)]
            )

    def get_questions_and_answers(self, test_language_version):
        """ Prepare questions and answers for test from filtered data"""
        filtered_data = self.__filter_data()

        questions_data = filtered_data[test_language_version].tolist()
        correct_answers = filtered_data[
            "PL" if test_language_version == "EN" else "EN"].tolist()

        selected_indices = random.sample(
            range(len(questions_data)), self.questions_amount)

        questions_data = [questions_data[idx] for idx in selected_indices]
        correct_answers = [correct_answers[idx] for idx in selected_indices]

        return questions_data, correct_answers

    def __filter_data(self):
        """" Filter data by selected category"""
        if self.selected_category == "All categories":
            return self.data
        elif isinstance(self.selected_category, list):
            return self.data[
                self.data["category_name"].isin(self.selected_category)
            ]
        else:
            return self.data[
                self.data["category_name"] == self.selected_category
            ]
