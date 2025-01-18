import datetime
import pandas as pd

from colorama import Fore
from interfaces.test_interface import Test
from menu.menu import Menu
from menu.menu_option import MenuOption
from test_managers.text_formatter import TextFormatter
from test_managers.question_manager import QuestionManager
from test_managers.result_manager import ResultManager
from test_managers.time_manager import TimeManager
from test_managers.file_manager import FileManager
from test_managers.user_manager import UserManager


class NewTest(Test):
    def __init__(self, data_file, data, main_menu):

        self.test_duration = None
        self.data_file = data_file  # path of excel file for saivng results
        self.__main_menu = main_menu  # allowing user to use main menu
        self.__data = data  # Data from database as DataFrame
        self.__test_language_version = None
        self.__selected_category = None
        self.__test_datetime = datetime.datetime.now()
        self.__point_score = 0
        self.__percentage_score = 0
        self.__user_name = None
        self.__test_time_limit_in_seconds = None
        self.__text_formatter = TextFormatter()
        self.__question_manager = QuestionManager(data, self.__text_formatter)
        self.__time_manager = TimeManager()
        self.__file_manager = FileManager()
        self.__user_manager = UserManager()
        self.__initiate_language_menu()
        self.__initiate_category_menu()
        self.__initiate_test()

    def __initiate_language_menu(self):
        """ initiates language menu,
        if the language is choosen,
        directs user to category setup"""
        def choose_en():
            self.__test_language_version = "EN"
            self.__set_category()

        def choose_pl():
            self.__test_language_version = "PL"
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
        if the category is choosen,
        directs user to question amount setup"""
        def choose_categories(*indices):
            if len(indices) == 1:
                self.__selected_category = categories[indices[0] - 1][1]
            else:
                self.__selected_category = [
                    categories[idx - 1][1] for idx in indices]
            self.__question_manager.set_category(self.__selected_category)
            self.__get_questions_amount()

        def choose_all():
            self.__selected_category = "All categories"
            self.__question_manager.set_category(self.__selected_category)
            self.__get_questions_amount()

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
                           action=lambda category_id=category_id:
                           choose_categories(category_id)))

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
        """ initiating test by getting and settin usernme,
        redirecting to language setup """
        print("\nStarting new test...\n")
        self.__user_manager.set_user_name()
        self.__user_name = self.__user_manager.get_user_name()
        self.__set_language()

    def __set_language(self):
        self.language_menu.display()

    def __set_category(self):
        self.category_menu.display()

    def __get_questions_amount(self):
        """ Gets and sets question amount from the user"""
        self.questions_amount = self.__question_manager.set_questions_amount()
        self.__set_test_time_limit()

    def __set_test_time_limit(self):
        """ Sets time limit for the test """
        if self.__time_manager.set_test_time_limit():
            self.__test_time_limit_in_seconds = \
                self.__time_manager.get_test_time_limit()
            self.start_test()

    def get_questions_and_answers_data(self):
        """ Based on category choice creates data for questions and answers"""
        return self.__question_manager.get_questions_and_answers(
            self.__test_language_version)

    def start_test(self):
        """ Starts the actual test,
        displays summary of users choices,
        displays importnt information about test"""

        if self.__test_language_version and self.__selected_category:
            Menu.clear_console()
            print(f"Starting test.\nChoosen options:\n"
                  f"1. Translating from: {self.__test_language_version}.\n"
                  f"2. Category: "
                  f"{self.__selected_category if isinstance(
                      self.__selected_category, str) else ', '.join(
                          map(str, self.__selected_category))}.\n"
                  f"3. Number of questions: {self.questions_amount}.\n"
                  f"4. Test time limit: "
                  f"{self.__test_time_limit_in_seconds // 60} min.\n")

            if self.__test_language_version == "EN":
                message = "*** You can enter answers with or without polish " \
                          "letters. Text will be normalized. ***\n"
                print(self.__text_formatter.colorize(message, Fore.GREEN))

            questions, answers = self.get_questions_and_answers_data()
            user_answers, test_stopped = self.submit_answer(questions)

            if test_stopped:
                print("Test stopped. No Results available")
                TimeManager.display_sleep(2)
                return self.__main_menu.display()

            test_results = self.get_results(answers, user_answers, questions)
            self.end_test(test_results)

    @TimeManager.measure_time  # TimeManager decorator to measure test time
    def submit_answer(self, questions_data):
        """ responsible for displaing questions and gathering answers,
        checking if test was stoped"""
        user_answers = []
        print(self.__text_formatter.colorize(
            "*** To stop test, enter: \"Stop test\" ***\n",
              Fore.LIGHTYELLOW_EX))

        TimeManager.test_delay()

        for expression in questions_data:
            answer = input(
                f"Enter translation of: \"{expression}\".\n")
            if answer.lower() == "stop test":
                return user_answers, True
            else:
                user_answers.append(answer.strip())

        # Return the answers and flag whether the test was stopped
        return user_answers, False

    def get_results(self, correct_answers, user_answers, expressions):
        """ gets questions, correct answers
        and user answers into a DataFrame, normalizes text,
        compares test data and points wrong and correct answers,
        modifies DataFrame to display text information (map),
        calculates points and percentage"""

        test_data = pd.DataFrame({
            "Questions": expressions,
            "Correct answers": correct_answers,
            "Your answers": user_answers,
        })

        # Normalize text
        test_data["Normalized Correct"] = test_data[
            "Correct answers"].apply(TextFormatter.normalize_text)
        test_data["Normalized User"] = test_data[
            "Your answers"].apply(TextFormatter.normalize_text)

        # Comparing data
        test_data["Correct/Wrong"] = test_data[
            "Normalized Correct"] == test_data["Normalized User"]
        test_data["Points"] = test_data["Correct/Wrong"].astype(int)

        # Map to text
        test_data["Correct/Wrong"] = test_data[
            "Correct/Wrong"].map({True: "Correct", False: "Wrong"})

        # Calculating the results
        self.__percentage_score = test_data["Points"].mean() * 100
        self.__point_score = test_data["Points"].sum()

        return test_data

    def save_results(self):
        save_decision = input("Do you want to save the results? (y/n): ")
        if save_decision.lower() == "y":
            self.__file_manager.results_to_file(self)
        else:
            print("Results not saved")

    def end_test(self, test_data):
        """ passing data to result manger """
        result_manager = ResultManager(
            self.__test_datetime,
            self.__user_name,
            self.__point_score,
            self.questions_amount,
            self.__percentage_score,
            self.test_duration,
            self.__test_time_limit_in_seconds,
            test_data
        )

        Menu.clear_console()
        # display summary table
        result_manager.display_results_table(test_data)

        # display test data like points ect.
        result_manager.display_test_outcome()

        self.save_results()

        input("\nPress 'ENTER' to return to main menu")
        self.__main_menu.display()
