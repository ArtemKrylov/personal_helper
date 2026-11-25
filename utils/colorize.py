from enum import StrEnum
from colorama import Fore, Style


class Color(StrEnum):
    GREEN = Fore.GREEN
    BLUE = Fore.BLUE
    RED = Fore.RED
    MAGENTA = Fore.MAGENTA


def colorize(text: str, color: Color = Color.BLUE) -> str:
    return f"{color}{text}{Style.RESET_ALL}" if text else None
 
