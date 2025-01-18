from test_managers.text_formatter import TextFormatter
from colorama import Fore


class ResultManager:
    def __init__(self, test_instance):
        self.__text_formatter = TextFormatter()
        self.test_instance = test_instance

    def __format_test_duration(self):
        minutes, seconds = divmod(self.test_instance._test_duration, 60)
        return f"{int(minutes)} min {int(seconds)} sec"

    def __determine_test_outcome(self):
        percentage_score = self.test_instance.get_percentage_score()
        messages = {
            1: "Test failed. Time limit exceeded!",
            2: "Test failed. Practice more!",
            3: "Test passed. Well done!",
            4: "Test passed. Great effort!",
            5: "Test passed. Excellent result!",
        }

        if (self.test_instance._test_duration
                > self.test_instance._test_time_limit_in_seconds):
            print(self.__text_formatter.colorize(messages[1], Fore.RED))
        else:
            if percentage_score < 50:
                print(self.__text_formatter.colorize(messages[2], Fore.RED))
            elif self.test_instance._percentage_score < 75:
                print(self.__text_formatter.colorize(messages[3], Fore.CYAN))
            elif self.test_instance._percentage_score < 85:
                print(self.__text_formatter.colorize(messages[4], Fore.GREEN))
            else:
                print(self.__text_formatter.colorize(messages[5], Fore.GREEN))

    def __display_table_headers(self, headers, col_widths):
        # Displaying the table header
        header_str = self.__text_formatter.format_table_row(
            headers,
            [col_widths['Questions'], col_widths['Your answers'],
             col_widths['Correct answers'], col_widths['Correct/Wrong'],
             col_widths['Points']], [Fore.YELLOW] * len(headers))
        print(header_str)

    def __calculate_column_widths(self, __test_data, headers):
        col_widths = {
            "Questions": max(__test_data[
                "Questions"].apply(len).max(), len("Question")),
            "Your answers": max(__test_data[
                "Your answers"].apply(len).max(), len("Your answers")),
            "Correct answers": max(__test_data[
                "Correct answers"].apply(len).max(), len("Correct answers")),
            "Correct/Wrong": len("Correct/Wrong"),
            "Points": len("Points")
        }
        total_width = sum(col_widths.values()) + len(headers) - 1
        return col_widths, total_width

    def __display_table_rows(self, __test_data, col_widths):
        # Print each row with appropriate color
        for _, row in __test_data.iterrows():
            correct_wrong_color = (Fore.GREEN if row[
                "Correct/Wrong"] == "Correct" else Fore.RED)
            points_color = (Fore.GREEN if row[
                "Points"] is True else Fore.RED)

            row_data = [
                str(row['Questions']),
                str(row['Your answers']),
                str(row['Correct answers']),
                str(row['Correct/Wrong']),
                str(row['Points'])]

            row_colors = [None, None, None, correct_wrong_color, points_color]
            formatted_row = self.__text_formatter.format_table_row(
                row_data,
                [col_widths['Questions'],
                 col_widths['Your answers'],
                 col_widths['Correct answers'],
                 col_widths['Correct/Wrong'],
                 col_widths['Points']],
                row_colors)
            print(formatted_row)

    def __display_summary(self, total_width):
        summary_text = self.__text_formatter.colorize(
            self.__text_formatter.center_text(
                "SUMMARY", total_width, "="), Fore.CYAN)
        print(summary_text)

    def display_results_table(self, __test_data):
        # Print headers with color
        headers = [
            "Questions",
            "Your answers",
            "Correct answers",
            "Correct/Wrong",
            "Points",]

        col_widths, total_width = self.__calculate_column_widths(
            __test_data, headers)
        self.__display_summary(total_width)
        self.__display_table_headers(headers, col_widths)
        self.__display_table_rows(__test_data, col_widths)
        print()

    def display_test_outcome(self):
        test_date_time = self.test_instance.get_test_datetime()
        points_score = self.test_instance.get_point_score()
        percentage_score = self.test_instance.get_percentage_score()
        print(f"Test date: {test_date_time.strftime('%d-%m-%Y')}")
        print(f"Test time: {test_date_time.strftime('%H:%M:%S')}")
        print(f"User: {self.test_instance._user_name}")
        print(f"Points: {points_score}/{self.test_instance.questions_amount}")
        print(f"Percentage: {percentage_score:.2f}%")
        test_duration_str = self.__format_test_duration()
        print(f"Test time limit: {
            self.test_instance._test_time_limit_in_seconds // 60} min.")
        print(f"Your time is: {test_duration_str}\n")
        self.__determine_test_outcome()
