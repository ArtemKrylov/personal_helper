from difflib import get_close_matches
from typing import Callable

from phone_bot.exceptions import BreakError

PHRASE_TO_COMMAND = {
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
    "birth": "birthdays",
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

    candidates = {**{name: name for name in commands}, **PHRASE_TO_COMMAND}
    matches = get_close_matches(text, candidates, n=1, cutoff=0.6)

    if matches:
        suggested_command = candidates[matches[0]]
        try:
            user_input = input(f"Did you mean: {suggested_command}? Y/N ")
        except EOFError:
            return None
        except KeyboardInterrupt:
            print("\nGoodbye!")
            raise BreakError

        answer = user_input.lower().split(maxsplit=1)
        if not answer or answer[0] != "y":
            return None

        return suggested_command

    return None
