from difflib import get_close_matches

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
    "birth": "birthdays",
    "birthdays": "birthdays",
    "help": "help",
    "close": "close",
    "exit": "exit",
    "exti": "exit",
    "привіт": "hello",
    "додай контакт": "add",
    "додай номер до контакту": "add-phone-to-contact",
    "зміни номер": "change",
    "видали контакт": "del",
    "покажи номер": "phone",
    "покажи всі контакти": "all",
    "список контактів": "all",
    "додай день народження": "add-birthday",
    "покажи день народження": "show-birthday",
    "народж": "birthdays",
    "покажи найближчі дні народження": "birthdays",
    "покажи команди": "help",
    "допомога": "help",
    "поможи": "help",
    "закрий програму": "close",
    "закрий": "close",
    "вийди": "exit",
    "ad": "add",
    "chane": "change",
    "chnage": "change",
    "phne": "phone",
    "al": "all",
    "exti": "exit",
}


def suggest_command(user_input: str) -> str | None:
    text = " ".join(user_input.casefold().split())
    # returns list of the best "good enough" matches
    matches = get_close_matches(text, PHRASE_TO_COMMAND, n=1, cutoff=0.6)

    if matches:
        user_input = input(f"Did you mean: {PHRASE_TO_COMMAND[matches[0]]}? Y/N ")

        if user_input.split()[0].strip().lower() != "y":
            return None

        return PHRASE_TO_COMMAND[matches[0]]

    return None
