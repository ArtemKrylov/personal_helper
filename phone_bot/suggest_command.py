from difflib import get_close_matches
from typing import Callable

from phone_bot.exceptions import BreakError

PHRASE_TO_COMMAND = {
    "привіт": "hello",
    "додай-контакт": "add",
    "додай-номер-до-контакту": "add-phone-to-contact",
    "зміни-номер": "change",
    "видали-контакт": "del",
    "покажи-номер": "phones",
    "покажи-номери": "phones",
    "покажи-контакт": "show",
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
    "додай-адресу": "add-address",
    "покажи-адресу": "show-address",
    "зміни-адресу": "change-address",
    "del-address": "delete-address",
    "видали-адресу": "delete-address",
    "покажи-всі-адреси": "show-all-addresses",
    "список-адрес": "show-all-addresses",
    "додай-пошту": "add-email",
    "додай-електронну-пошту": "add-email",
    "покажи-пошту": "show-email",
    "покажи-електронну-пошту": "show-email",
    "del-email": "delete-email",
    "видали-пошту": "delete-email",
    "видали-електронну-пошту": "delete-email",
    "покажи-команди": "help",
    "допомога": "help",
    "поможи": "help",
    "закрий-програму": "close",
    "закрий": "close",
    "вийди": "exit",
    "ad": "add",
    "chane": "change",
    "chnage": "change",
    "phone": "phones",
    "phne": "phones",
    "phons": "phones",
    "phnoes": "phones",
    "shw": "show",
    "shwo": "show",
    "ad-address": "add-address",
    "add-adress": "add-address",
    "shwo-address": "show-address",
    "show-adress": "show-address",
    "chagne-address": "change-address",
    "change-adress": "change-address",
    "delte-address": "delete-address",
    "delete-adress": "delete-address",
    "shwo-all-addresses": "show-all-addresses",
    "show-all-adresses": "show-all-addresses",
    "ad-email": "add-email",
    "add-emial": "add-email",
    "shwo-email": "show-email",
    "show-emial": "show-email",
    "delte-email": "delete-email",
    "delete-emial": "delete-email",
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
