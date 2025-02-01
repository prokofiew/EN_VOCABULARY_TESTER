import datetime

from interfaces.test_interface import Test
from menu.menu import Menu
from menu.menu_option import MenuOption
from colorama import Fore
from test_managers.question_manager import QuestionManager
from test_managers.result_manager import ResultManager
from test_managers.text_formatter import TextFormatter
from test_managers.time_manager import TimeManager
from test_managers.file_manager import FileManager
from test_managers.user_manager import UserManager


class NewTest(Test):
    def __init__(self, data_file, data, main_menu, controller):
        self._data_file = data_file  # path of Excel file for saving results
        self._user_name = None
        self._test_time_limit_in_seconds = 0
        self._test_language_version = None
        self._selected_category = None
        self._test_duration = 0
        self._questions_amount = 0
        self.__main_menu = main_menu  # allowing user to use main menu
        self.__data = data  # Data from database as DataFrame
        self.__test_datetime = self.set_test_datetime()
        self.__point_score = 0
        self.__percentage_score = 0
        self.__controller = controller
        self.__result_manager = ResultManager(self)
        self.__question_manager = QuestionManager(data)
        self.__time_manager = TimeManager()
        self.__file_manager = FileManager()
        self.__user_manager = UserManager()
        self.__initiate_language_menu()
        self.__initiate_category_menu()
        self.__initiate_test()

    def get_test_datetime(self):
        return self.__test_datetime

    @staticmethod
    def set_test_datetime():
        return datetime.datetime.now()

    def get_point_score(self):
        return self.__point_score

    def set_point_score(self, points_data):
        self.__point_score = points_data

    def get_percentage_score(self):
        return self.__percentage_score

    def set_percentage_score(self, percentage_data):
        self.__percentage_score = percentage_data

    def get_test_duration(self):
        return self._test_duration

    def set_test_duration(self, duration):
        self._test_duration = duration

    def get_questions_amount(self):
        return self._questions_amount

    def set_questions_amount(self):
        self._questions_amount = self.__question_manager.set_questions_amount()
        self.__set_test_time_limit()

    def __initiate_language_menu(self):
        """ initiates language menu,
        if the language is chosen,
        directs user to category setup"""
        def choose_en():
            self._test_language_version = "EN"
            self.__set_category()

        def choose_pl():
            self._test_language_version = "PL"
            self.__set_category()

        def back_to_main():
            self.__main_menu.display()

        self.language_menu = Menu(
            title="Choose Test Language",
            controller=None)

        self.language_menu.add_option(
            1, MenuOption("EN -> PL", action=choose_en))
        self.language_menu.add_option(
            2, MenuOption("PL -> EN", action=choose_pl))
        self.language_menu.add_option(
            3, MenuOption("Back to Main Menu", action=back_to_main))

    def __initiate_category_menu(self):
        """ initiates category menu,
        if the category is chosen,
        directs user to question amount setup"""
        def choose_categories(*indices):
            if len(indices) == 1:
                self._selected_category = categories[indices[0] - 1][1]
            else:
                self._selected_category = [
                    categories[idx - 1][1] for idx in indices]
            self.__question_manager.set_category(self._selected_category)
            self.set_questions_amount()

        def choose_all():
            self._selected_category = "All categories"
            self.__question_manager.set_category(self._selected_category)
            self.set_questions_amount()

        def back_to_language():
            self.__set_language()

        # creating list of categories sorted by category_id
        categories = (
            self.__data[["category_id", "category_name"]]
            .drop_duplicates()
            .sort_values("category_id")
            .values
            .tolist())

        # Category menu tite
        self.category_menu = Menu(
            title="Choose Test Category",
            controller=None)

        # creating category menu options based on list 'categories'
        for category_id, category_name in categories:
            self.category_menu.add_option(
                category_id,
                MenuOption(category_name,
                           action=lambda selected_id=category_id:
                           choose_categories(selected_id)))

        # All categories menu option
        self.category_menu.add_option(
            len(categories) + 1,
            MenuOption(
                "All Categories", action=choose_all))

        # Back to previous menu -> language menu
        self.category_menu.add_option(
            len(categories) + 2,
            MenuOption(
                "Back to Language Settings", action=back_to_language))

        # responsible for confirming selection in multiple category choice
        self.category_menu.add_option(
            'confirm_selection',
            MenuOption(
                "Confirm Selection", action=choose_categories))

    def __initiate_test(self):
        """ initiating test by getting and setting username,
        redirecting to language setup """
        print("\nStarting new test...\n")
        self.__user_manager.set_user_name()
        self._user_name = self.__user_manager.get_user_name()
        self.__set_language()

    def __set_language(self):
        self.language_menu.display()

    def __set_category(self):
        self.category_menu.display()

    def __set_test_time_limit(self):
        """ Sets time limit for the test """
        if self.__time_manager.set_test_time_limit():
            self._test_time_limit_in_seconds = \
                self.__time_manager.get_test_time_limit()
            self.start_test()

    def get_questions_and_answers_data(self):
        """ Based on category choice creates data for questions and answers"""
        return self.__question_manager.get_questions_and_answers(
            self._test_language_version)

    def start_test(self):
        """ Starts the actual test,
        displays summary of users choices,
        displays important information about test"""

        if self._test_language_version and self._selected_category:
            Menu.clear_console()
            print(f"Starting test.\nChosen options:\n"
                  f"1. Translating from: {self._test_language_version}.\n"
                  f"2. Category: "
                  f"{self._selected_category if isinstance(
                      self._selected_category, str) else ', '.join(
                          map(str, self._selected_category))}.\n"
                  f"3. Number of questions: {self._questions_amount}.\n"
                  f"4. Test time limit: "
                  f"{self._test_time_limit_in_seconds // 60} min.\n")

            if self._test_language_version == "EN":
                message = "*** You can enter answers with or without polish " \
                          "letters. Text will be normalized. ***\n"
                print(TextFormatter.colorize(message, Fore.GREEN))

            print(TextFormatter.colorize(
                "*** To stop test, enter: \"Stop test\" ***\n",
                Fore.LIGHTYELLOW_EX))

            questions, answers = self.get_questions_and_answers_data()
            TimeManager.test_delay()
            user_answers, test_stopped = self.submit_answer(questions)

            if test_stopped:
                message = "Test stopped. No Results available"
                print(TextFormatter.colorize(message, Fore.YELLOW))
                TimeManager.display_sleep(2)
                return self.__main_menu.display()

            test_results = self.get_results(answers, user_answers, questions)
            self.end_test(test_results)

    @TimeManager.measure_time  # TimeManager decorator to measure test time
    def submit_answer(self, questions_data):
        """ responsible for displaying questions and gathering answers,
        checking if test was stopped"""
        user_answers = []

        for idx, expression in enumerate(questions_data):
            print(f"Question no.{idx + 1}")
            answer = input(
                f"Enter translation of: \"{expression}\".\nAnswer -> ")
            if answer.lower() == "stop test":
                return user_answers, True
            else:
                user_answers.append(answer.strip())

        # Return the answers and flag whether the test was stopped
        return user_answers, False

    def get_results(self, correct_answers, user_answers, expressions):
        """ Analyzes answers and to get results"""
        return self.__result_manager.analyze_answers(
            correct_answers, user_answers, expressions)

    def save_results(self):
        """ Saves results to Excel file """
        save_decision = input("Do you want to save the results? (y/n): ")
        if save_decision.lower() == "y":
            self.__file_manager.results_to_file(self)
        else:
            print("Results not saved")

    def end_test(self, test_data):
        """
       Displays results of the test as table and summary,
       gives option to the user to save results to Excel file
       and return to main menu.
        """
        Menu.clear_console()
        # display summary table
        self.__result_manager.display_results_table(test_data)

        # display test data like points ect.
        self.__result_manager.display_test_outcome()

        self.save_results()

        self.__controller.back_to_prev_menu()
        self.__main_menu.display()
