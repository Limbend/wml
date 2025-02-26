import logging
from colorama import Fore, Style
import copy


class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        record = copy.copy(record)
        if record.levelno in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelno]}" f"{record.levelname}{Style.RESET_ALL}"
            )
            record.msg = (
                f"{self.COLORS[record.levelno]}" f"{record.msg}{Style.RESET_ALL}"
            )
        return super().format(record)


class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        return not any(
            word in record.getMessage().lower()
            for word in ["password", "token", "secret"]
        )
