import sys
import utlis.description as description
import pandas as pd
import os

from test.test import NewTest
from menu.menu import Menu
from test_managers.user_manager import UserManager

TEST_DATABASE = os.path.join("test_database", "tester_database.xlsx")


class App_Controller:
    def __init__(self):
        self.data = None
        self.dictionaries = None
        self.vocabluary = None
        self.user_manager = UserManager()
        self._data_load()

    def _data_load(self):
        try:
            file_data = pd.ExcelFile(TEST_DATABASE)
            self.dictionaries = file_data.parse(sheet_name="categories")
            self.vocabluary = file_data.parse(sheet_name="vocabluary")
            self.data = pd.merge(
                self.vocabluary,
                self.dictionaries,
                left_on="category",
                right_on="category_id")
        except FileNotFoundError:
            print("Database file: tester_database.xlsx not found.")
            sys.exit()

    # Funkcje akcji
    def setup_main_menu(self):
        self.main_menu = Menu("Main menu", self)

    def _validate_user_input(self, user_input):
        return UserManager.validate_user_input(user_input)

    def _get_user_input(self, prompt):
        user_input = input(prompt).lower()
        self._validate_user_input(user_input)
        return user_input

    def _join_data_frames(self, base_data_frame, added_data_frame):
        return pd.concat([
            base_data_frame, added_data_frame], ignore_index=True)

    def _save_to_database(self, data_frame, sheet_name):
        with pd.ExcelWriter(
            TEST_DATABASE, mode="a", if_sheet_exists="overlay"
        ) as writer:
            data_frame.to_excel(writer, sheet_name=sheet_name, index=False)

    def _create_new_category(self, new_category):
        new_category_id = int(self.dictionaries["category_id"].max() + 1)
        new_category_data_frame = pd.DataFrame(
            {
                "category_id": [new_category_id],
                "category_name": [new_category]
            }
        )
        return new_category_id, new_category_data_frame

    def add_vocabluary(self, category_id):
        words_added = False
        while True:
            Menu.clear_console()
            try:
                new_word_EN = self._get_user_input(
                    "Enter new word in English: ")
                new_word_PL = self._get_user_input(
                    "Enter translation in Polish: ")

                new_word = pd.DataFrame({
                    "EN": [new_word_EN],
                    "PL": [new_word_PL],
                    "category": [category_id],
                })
                self.vocabluary = self._join_data_frames(
                    self.vocabluary, new_word)
                words_added = True

                if input(
                        "Do you want to add another word? (y/n): "
                        ).lower() == "n":
                    break

            except ValueError as error:
                print(f"An error occurred: {error}")
                if input("Do you want to try again? (y/n): ").lower() == "n":
                    break

        if words_added:
            self._save_to_database(self.vocabluary, "vocabluary")
        return words_added

    def add_dictionary(self):
        print("Adding a new dictionary...")
        new_category_id = self._process_new_category()
        if new_category_id:
            self._display_new_category_info(new_category_id)
        self.back_to_prev_menu()

    def _process_new_category(self):
        try:
            new_category = self._get_user_input(
                "\nEnter category name: ").capitalize()
            if new_category in self.dictionaries["category_name"].values:
                raise ValueError("Category already exists.")

            new_category_id, category_df = self._create_new_category(
                new_category)
            if self.add_vocabluary(new_category_id):
                self._update_dictionaries(category_df)
                return new_category_id
        except ValueError as error:
            print(f"\nError: {error}")
        return None

    def _update_dictionaries(self, new_category_df):
        self.dictionaries = pd.concat([
            self.dictionaries, new_category_df], ignore_index=True)
        self._save_to_database(self.dictionaries, "categories")
        self._data_load()

    def _display_new_category_info(self, category_id):
        Menu.clear_console()
        print("\nNew category added successfully!")
        print(self.vocabluary[category_id == self.vocabluary["category"]])

    def display_dictionaries(self):
        Menu.clear_console()
        print("Available dictionaries:")
        dictionaries_df = self.dictionaries.set_index("category_id")
        formatted_dictionaries = [
            f"{idx}. {category}"
            for idx, category in enumerate(dictionaries_df["category_name"], 1)
        ]
        print("\n".join(formatted_dictionaries))
        self.back_to_prev_menu()

    def about_program_display(self):
        # Wyświetlanie informacji o programie
        Menu.clear_console()
        print("===================================")
        print(f"Author: {description.__author__}")
        print(f"Version: {description.__version__}")
        print("Description:")
        print(description.__description__)
        print("===================================")
        self.back_to_prev_menu()

    def start_test(self):
        NewTest(TEST_DATABASE, self.data, self.main_menu)

    def back_to_prev_menu(self):
        input("\nPress Enter to return to the previous menu...")

    def exit_program(self):
        Menu.clear_console()
        print("Thanks for using. You have successfully exited the program.\n")
        sys.exit()
