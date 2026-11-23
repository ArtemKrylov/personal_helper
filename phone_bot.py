from functools import wraps
from typing import Callable

from colorama import Fore

from address_book import (
    AddressBook,
    DateInputError,
    NoContactError,
    PhoneInputError,
    Record,
)


def input_error(func: Callable):
    @wraps(func)
    def inner(*args, **qwargs):
        try:
            return func(*args, **qwargs)
        except KeyError as error:
            contact_name = error.args[0]
            return f"Contact {Fore.BLUE}{contact_name}{Fore.RESET} does not exist."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"
        except (PhoneInputError, NoContactError, DateInputError) as e:
            return str(e)
        except (BreakError, ContinueError, ContactExist, ContactNotExist):
            raise
        except Exception as e:
            print(f"An error occurred: {e}")

    return inner


class BreakError(Exception):
    pass


class ContinueError(Exception):
    pass


class ContactExist(Exception):
    pass


class ContactNotExist(Exception):
    pass


class PhoneBot:
    def __init__(self, book: AddressBook = {}):
        self.commands = {
            "hello": self._hello,
            "add": self._add_contact,
            "add-phone-to-contact": self._add_contact_phone,
            "change": self._change_contact,
            "del": self._delete_contact,
            "phone": self._show_contact,
            "all": self._show_all_contacts,
            "add-birthday": self._add_birthday,
            "show-birthday": self._show_birthday,
            "birthdays": self._show_birthdays,
            "help": self._show_commands,
            "close": self._close,
            "exit": self._close,
        }
        self.book = book

    def start_bot(self):
        print(f"""\n{"Welcome to the assistant bot!":*^100}
    Commands list: {', '.join(self.commands)}
            """)
        while True:
            try:
                user_input = input("Enter a command: ")
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break

            if not user_input or not user_input.strip():
                continue

            command, *args = self._parse_input(user_input)

            try:
                message = self.commands[command](args)
                if message:
                    print(message)
            except KeyError:
                print("Unknown command")
            except BreakError:
                break
            except ContinueError:
                continue
            except ContactExist:
                print("Contact already exists. Rewrite it? (y/n): ")
                if input().lower() == "y":
                    print(self.commands["change"](args=args))
                else:
                    print("Contact not updated.")
            except ContactNotExist:
                print("Contact does not exist. Add it? (y/n): ")
                if input().lower() == "y":
                    print(self.commands["add"](args=args))
                else:
                    print("Contact not added.")

    def _parse_input(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    @input_error
    def _hello(self, _):
        print("How can I help you?")

    def _form_record_from_args(self, args) -> Record:
        name, phone, *rest = args
        birthday = rest[0] if rest else None
        new_record = Record(name)
        if phone:
            new_record.add_phone(phone)
        if birthday:
            new_record.add_birthday(birthday)
        return new_record

    @input_error
    def _add_contact(self, args) -> str | None:
        name = args[0]

        try:
            if name in self.book.data:
                raise ContactExist
        except NoContactError:
            pass

        new_record = self._form_record_from_args(args)
        self.book.add_record(new_record)

        return f"Contact {Fore.BLUE}{name}{Fore.RESET} added."

    @input_error
    def _add_contact_phone(self, args) -> str | None:
        name, phone = args

        if name not in self.book.data:
            raise ContactNotExist

        record = self.book.find(name)
        if record.find_phone(phone):
            return "Phone already exists"

        self.book.add_record_phone(name, phone)

        return f"Phone {Fore.GREEN}{phone}{Fore.RESET} added to contact {Fore.BLUE}{name}{Fore.RESET}."

    @input_error
    def _change_contact(self, args) -> str | None:
        name, phone, *rest = args
        birthday = rest[0] if rest else None

        if name not in self.book.data:
            raise ContactNotExist

        self.book.change_record(name, phone, birthday)

        return f"Contact {Fore.BLUE}{name}{Fore.RESET} updated."

    @input_error
    def _delete_contact(self, args) -> str:
        name = args[0]
        self.book.delete(name)

        return f"Contact {Fore.RED}{name}{Fore.RESET} deleted."

    @input_error
    def _show_contact(self, args) -> str:
        name = args[0]
        record = self.book.find(name)

        return str(record)

    @input_error
    def _show_all_contacts(self, _) -> str:
        records = self.book.values()
        if not len(records):
            return "No contacts"

        showing_contacts = "\n".join([str(record) for record in records])

        return f"{"Phonebook:":-^100}\n{showing_contacts}"

    @input_error
    def _add_birthday(self, args) -> str:
        name, birthday, *_ = args
        record = self.book.find(name)
        record.add_birthday(birthday)

        return str(record)

    @input_error
    def _show_birthday(self, args) -> str:
        name = args[0]
        record = self.book.find(name)
        birthday = record.birthday if record else None

        return (
            f"{Fore.BLUE}{name}: {Fore.GREEN}{str(birthday)}{Fore.RESET}"
            if birthday
            else "No birthday found"
        )

    @input_error
    def _show_birthdays(self, _) -> str:
        upcoming = "; ".join(
            [
                f"{congrat["name"]} : {congrat["congratulation_date"]}"
                for congrat in self.book.get_upcoming_birthdays()
            ]
        )
        if not upcoming:
            return "No upcoming birthdays"

        return f"{Fore.BLUE}Upcoming birthdays: {Fore.GREEN}{upcoming}{Fore.RESET}"

    @input_error
    def _show_commands(self, _) -> None:
        print(f"All commands: {', '.join(self.commands)}")

    @input_error
    def _close(self, _) -> None:
        print("Good bye!")
        raise BreakError
