from difflib import get_close_matches
from typing import Callable

from phone_bot.exceptions import BreakError

PHRASE_TO_COMMAND = {
    "hello": "hello",
    "add": "add",
    "add-phone-to-contact": "add-phone-to-contact",
    "change": "change",
    "del": "del",
    "phone": "phone",
    "all": "all",
    "add-birthday": "add-birthday",
    "show-birthday": "show-birthday",
    "change-birthday": "change-birthday",
    "delete-birthday": "delete-birthday",
    "birth": "birthdays",
    "birthdays": "birthdays",
    "help": "help",
    "close": "close",
    "exit": "exit",
    "привіт": "hello",
    "додай-контакт": "add",
    "додай-номер-до-контакту": "add-phone-to-contact",
    "зміни-номер": "change",
    "видали-контакт": "del",
    "покажи-номер": "phone",
    "покажи-всі-контакти": "all",
    "список-контактів": "all",
    "додай-день-народження": "add-birthday",
    "покажи-день-народження": "show-birthday",
    "chagne-birthday": "change-birthday",
    "зміни-день-народження": "change-birthday",
    "del-birthday": "delete-birthday",
    "видали-день-народження": "delete-birthday",
    "народж": "birthdays",
    "покажи-найближчі-дні-народження": "birthdays",
    "покажи-команди": "help",
    "допомога": "help",
    "поможи": "help",
    "закрий-програму": "close",
    "закрий": "close",
    "вийди": "exit",
    "ad": "add",
    "chane": "change",
    "chnage": "change",
    "phne": "phone",
    "al": "all",
    "exti": "exit",
}


def suggest_command(command: str, commands: dict[str, Callable]) -> str | None:

    text = " ".join(command.casefold().split())
    if text in commands:
        return text

    # returns list of the best "good enough" matches
    matches = get_close_matches(text, PHRASE_TO_COMMAND, n=1, cutoff=0.6)

    if matches:
        try:
            user_input = input(f"Did you mean: {PHRASE_TO_COMMAND[matches[0]]}? Y/N ")
        except EOFError:
            return None
        except KeyboardInterrupt:
            print("\nGoodbye!")
            raise BreakError

        answer = user_input.lower().split(maxsplit=1)
        if not answer or answer[0] != "y":
            return None

        return PHRASE_TO_COMMAND[matches[0]]

    return None
