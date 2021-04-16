"""Module for logging"""

import time


class Logger:
    """Class for logging"""
    def __init__(self):
        self.log_file = "logs.txt"
        self.gmt = 3

    def time_now(self):
        """Get time now"""
        return time.gmtime(int(time.time()) + 3600 * self.gmt)  # Время записи лога

    def log_strings(self, args):
        """Create log strings"""
        year, month, day, hour, minute, second, *_ = self.time_now()

        for arg in args:
            date = f'[{day:0>2}.{month:0>2}.{year}|{hour:0>2}:{minute:0>2}:{second:0>2}]'
            yield f'{date} {arg}'

    @staticmethod
    def __log_to_console(string: str):
        print(string, end='')

    def __log_to_file(self, string: str):
        with open(self.log_file, 'a+', encoding='utf-8') as log_file:
            log_file.write(string)

    def log_to_console(self, *args):
        all_logs = '\n'.join(self.log_strings(args)) + '\n'
        self.__log_to_console(all_logs)

    def log_to_file(self, *args):
        all_logs = '\n'.join(self.log_strings(args)) + '\n'
        self.__log_to_file(all_logs)

    def log_to_console_and_file(self, *args):
        all_logs = '\n'.join(self.log_strings(args)) + '\n'
        self.__log_to_console(all_logs)
        self.__log_to_file(all_logs)

    def wrap(self, func):
        """Logging wrapper around a function"""
        def wrapper(*args, **kwargs):
            self.log_to_console_and_file(func.__name__ + " invoked")
            return func(*args, **kwargs)
        return wrapper
