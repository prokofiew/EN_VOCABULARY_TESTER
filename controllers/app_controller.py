import sys
import os

import utlis.description as description
import pandas as pd

from test.test import NewTest
from menu.menu import Menu
from colorama import Fore
from test_managers.user_manager import UserManager
from test_managers.text_formatter import TextFormatter

TEST_DATABASE = os.path.join("test_database", "tester_database.xlsx")

# class to manage the app
# loads data when the app is started
# responsible for execution of main menu actions


class AppController:
    def __init__(self):
        self.data = None
        self.dictionaries = None
        self.vocabulary = None
        self.main_menu = None
        self.__data_load()

    def initialize_main_menu(self):
        """ initiating Menu """
        self.main_menu = Menu("Main menu", self)

    def start_test(self):
        NewTest(TEST_DATABASE, self.data, self.main_menu, self)

    def add_dictionary(self):
        """ Adding new category of vocabulary. """
        print("Adding a new dictionary...")
        new_category_id, category_df = self.__process_new_category()
        if new_category_id:
            self.__display_new_category_info(new_category_id, category_df)
        self.back_to_prev_menu()

    def add_vocabulary(self, category_id):
        """ Adding new vocabulary to the category,
        setting flag if words were added"""
        words_added = False
        while True:
            Menu.clear_console()
            try:
                new_word_en = self.get_user_input("Enter new word in English: ")
                new_word_pl = self.get_user_input("Enter translation in Polish: ")

                new_word = pd.DataFrame({
                    "EN": [new_word_en],
                    "PL": [new_word_pl],
                    "category": [category_id],
                })
                self.vocabulary = self.join_data_frames(
                    self.vocabulary,
                    new_word
                )
                words_added = True

                if input(
                        "Do you want to add another word? (y/n): "
                        ).lower() == "n":
                    break

            except ValueError as error:
                message = f"An error occurred: {error}"
                print(TextFormatter.colorize(message, Fore.RED))
                if input("Do you want to try again? (y/n): ").lower() == "n":
                    break

        if words_added:
            self.save_to_database(self.vocabulary, "vocabulary")
        return words_added

    def display_dictionaries(self):
        """ Displays available categories of vocabulary """
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
        """ Printing out description.py content """
        Menu.clear_console()
        print("===================================")
        print(f"Author: {description.__author__}")
        print(f"Version: {description.__version__}")
        print("Description:")
        print(description.__description__)
        print("===================================")
        self.back_to_prev_menu()

    @staticmethod
    def back_to_prev_menu():
        input("\nPress Enter to return to the previous menu...")

    @staticmethod
    def exit_program():
        Menu.clear_console()
        message = "Thanks for using. "\
                  "You have successfully exited the program.\n"
        print(TextFormatter.colorize(message, Fore.CYAN))
        sys.exit()

    @staticmethod
    def get_user_input(prompt):
        """ getter for user input """
        user_input = input(prompt).lower()
        UserManager.validate_user_input(user_input)
        return user_input

    @staticmethod
    def join_data_frames(base_data_frame, added_data_frame):
        """ Private method to join DataFrames with pd.concat """
        return pd.concat([
            base_data_frame, added_data_frame], ignore_index=True)

    @staticmethod
    def save_to_database(data_frame, sheet_name):
        """ Updating database file with new vocabulary"""
        with pd.ExcelWriter(
            TEST_DATABASE, mode="a", if_sheet_exists="overlay"
        ) as writer:
            data_frame.to_excel(writer, sheet_name=sheet_name, index=False)

    def __data_load(self):
        """ Loads database file
        and establishes sheets as properties """
        try:
            file_data = pd.ExcelFile(TEST_DATABASE)
            self.dictionaries = file_data.parse(sheet_name="categories")
            self.vocabulary = file_data.parse(sheet_name="vocabulary")
            self.data = pd.merge(
                self.vocabulary,
                self.dictionaries,
                left_on="category",
                right_on="category_id")
        except FileNotFoundError:
            print("Database file: tester_database.xlsx not found.")
            sys.exit()

    def __process_new_category(self):
        """ Gets category name from user,
        creates new category if vocabulary was added
        """
        try:
            new_category = self.get_user_input("\nEnter category name: ").capitalize()
            if new_category in self.dictionaries["category_name"].values:
                raise ValueError("Category already exists.")

            new_category_id, category_df = self.__create_new_category(
                new_category)
            if self.add_vocabulary(new_category_id):
                self.__update_dictionaries(category_df)
                return new_category_id, category_df
        except ValueError as error:
            message = f"\nError: {error}"
            print(TextFormatter.colorize(message, Fore.RED))
        return None

    def __create_new_category(self, new_category):
        """ Creating new category_id and
        DataFrame for new vocabulary"""
        new_category_id = int(self.dictionaries["category_id"].max() + 1)
        new_category_data_frame = pd.DataFrame(
            {
                "category_id": [new_category_id],
                "category_name": [new_category]
            }
        )
        return new_category_id, new_category_data_frame

    def __update_dictionaries(self, new_category_df):
        """ Updates category property,
        updates database file,
        reloads the database file """
        self.dictionaries = self.join_data_frames(
            self.dictionaries,
            new_category_df
        )
        self.save_to_database(self.dictionaries, "categories")
        self.__data_load()

    def __display_new_category_info(self, category_id, category_df):
        """ Displaying new category DataFrame. """
        Menu.clear_console()
        message = "New category added successfully!"
        category_name = category_df["category_name"].values[0]
        new_vocabulary = self.vocabulary[self.vocabulary["category"] == category_id]
        print(TextFormatter.colorize(message, Fore.GREEN))
        print(f"Category name: {TextFormatter.colorize(category_name, Fore.CYAN)}")
        print(new_vocabulary[["EN", "PL"]].to_string(index=False, justify="center"))
