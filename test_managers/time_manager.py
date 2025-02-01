import time
import datetime
from functools import wraps
from colorama import Fore
from test_managers.text_formatter import TextFormatter


class TimeManager:
    def __init__(self):
        self.test_time_limit_in_seconds = None

    @staticmethod
    def measure_time(func):
        @wraps(func)
        def wrapper(instance, *args, **kwargs):
            start_time = datetime.datetime.now()
            result = func(instance, *args, **kwargs)
            end_time = datetime.datetime.now()
            instance.set_test_duration((end_time - start_time).total_seconds())
            return result
        return wrapper

    @staticmethod
    def test_delay():
        print("The test will start in: ")
        for i in range(1, 0, -1):
            print(f"\r{i} ", end="")
            time.sleep(1)
        print("\rStart!\n")

    @staticmethod
    def display_sleep(seconds: float):
        time.sleep(seconds)

    def set_test_time_limit(self):
        try:
            test_time_limit = int(input("Enter test time limit in minutes: "))
            self.test_time_limit_in_seconds = test_time_limit * 60
            return True
        except ValueError:
            message = "Invalid value. Enter a number"
            print(TextFormatter.colorize(message, Fore.RED))
            self.display_sleep(1.5)
            return self.set_test_time_limit()

    def get_test_time_limit(self):
        return self.test_time_limit_in_seconds
