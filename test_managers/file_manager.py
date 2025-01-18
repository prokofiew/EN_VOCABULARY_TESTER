import os
import pandas as pd

from colorama import Fore
from test_managers.text_formatter import TextFormatter


class FileManager:
    def __init__(self):
        self.text_formatter = TextFormatter()

    def results_to_file(self, test_instance):
        point_score = test_instance.get_point_score()
        percentage_score = test_instance.get_percentage_score()
        test_datetime = test_instance.get_test_datetime()
        # Convert list of categories to a comma-separated string
        category_str = (
            ', '.join(test_instance._selected_category)
            if isinstance(test_instance._selected_category, list)
            else test_instance._selected_category)

        # Create a DataFrame for the test results
        results_df = pd.DataFrame({
            "test_id": [1],
            "user_name": [test_instance._user_name],
            "test_date_time": [
                f"{test_datetime.strftime('%d-%m-%Y')}"
                f"{test_datetime.strftime('%H:%M:%S')}"
            ],
            "test_version": [
                "EN->PL"
                if test_instance._test_language_version == "EN"
                else "PL->EN"],
            "test_time_limit_sek": [
                test_instance._test_time_limit_in_seconds],
            "test_duration_sek": [f"{test_instance._test_duration:.2f}"],
            "test_result_points": [
                f"({point_score}/"
                f"{test_instance._questions_amount})"
            ],
            "test_result_percentage": [
                f"{percentage_score:.2f}%"],
            "category": [category_str]})

        # Check if the file exists
        if os.path.exists(test_instance._data_file):
            with pd.ExcelWriter(
                test_instance._data_file, mode='a', engine='openpyxl',
                if_sheet_exists='overlay'
            ) as writer:
                if "test results" in writer.book.sheetnames:
                    existing_data = pd.read_excel(
                        test_instance._data_file, sheet_name="test results")
                    next_test_id = (existing_data["test_id"].max() + 1
                                    if 'test_id' in existing_data.columns
                                    else 1)
                    results_df["test_id"] = next_test_id
                    updated_data = pd.concat([existing_data, results_df],
                                             ignore_index=True)
                    updated_data.to_excel(writer, sheet_name="test results",
                                          index=False)
                else:
                    results_df.to_excel(writer,
                                        sheet_name="test results",
                                        index=False)
        else:
            with pd.ExcelWriter(
                test_instance._data_file, engine='openpyxl'
            ) as writer:
                results_df.to_excel(writer,
                                    sheet_name="test results",
                                    index=False)
        message = "Results saved successfully"
        print(self.text_formatter.colorize(message, Fore.YELLOW))
