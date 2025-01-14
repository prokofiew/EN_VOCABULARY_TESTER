import os
import pandas as pd

from colorama import Fore


class FileManager:
    def results_to_file(self, test_instance):
        # Convert list of categories to a comma-separated string
        category_str = (
            ', '.join(test_instance.selected_category)
            if isinstance(test_instance.selected_category, list)
            else test_instance.selected_category)

        # Create a DataFrame for the test results
        results_df = pd.DataFrame({
            "test_id": [1],
            "user_name": [test_instance.user_name],
            "test_date_time": [
                f"{test_instance.test_datetime.strftime('%d-%m-%Y')} "
                f"{test_instance.test_datetime.strftime('%H:%M:%S')}"
            ],
            "test_version": [
                "EN->PL" if test_instance.test_language_version == "EN"
                else "PL->EN"],
            "test_time_limit_sek": [test_instance.test_time_limit_in_seconds],
            "test_duration_sek": [f"{test_instance.test_duration:.2f}"],
            "test_result_points": [
                f"({test_instance.point_score}/"
                f"{test_instance.questions_amount})"
            ],
            "test_result_percentage": [
                f"{test_instance.percentage_score:.2f}%"],
            "category": [category_str]})

        # Check if the file exists
        if os.path.exists(test_instance.data_file):
            with pd.ExcelWriter(
                test_instance.data_file, mode='a', engine='openpyxl',
                if_sheet_exists='overlay'
            ) as writer:
                if "test results" in writer.book.sheetnames:
                    existing_data = pd.read_excel(
                        test_instance.data_file, sheet_name="test results")
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
                test_instance.data_file, engine='openpyxl'
            ) as writer:
                results_df.to_excel(writer,
                                    sheet_name="test results",
                                    index=False)
        message = "Results saved successfully"
        print(test_instance.text_formatter.colorize(message, Fore.YELLOW))
