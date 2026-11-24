from functools import wraps
from typing import Callable

from colorama import Fore

from address_book.address_book import AddressBook
from address_book.exceptions import (
    DateInputError,
    NameInputError,
    NoContactError,
    PhoneInputError,
)
from address_book.record import Record
from phone_bot.exceptions import (
    BreakError,
    ContactExist,
    ContactNotExist,
    ContinueError,
)
from phone_bot.suggest_command import suggest_command


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
        except (PhoneInputError, NoContactError, DateInputError, NameInputError) as e:
            return str(e)
        except (BreakError, ContinueError, ContactExist, ContactNotExist):
            raise
        except Exception as e:
            print(f"An error occurred: {e}")

    return inner


class PhoneBot:
    def __init__(self, book: AddressBook | None = None):
        # Add new command here (command name: executed function)
        self.commands = {
            "hello": self.__hello,
            "add": self.__add_contact,
            "add-phone-to-contact": self.__add_contact_phone,
            "change": self.__change_contact,
            "del": self.__delete_contact,
            "phone": self.__show_contact,
            "all": self.__show_all_contacts,
            "add-birthday": self.__add_birthday,
            "show-birthday": self.__show_birthday,
            "change-birthday": self.__change_birthday,
            "delete-birthday": self.__delete_birthday,
            "birthdays": self.__show_birthdays,
            "help": self.__show_commands,
            "close": self.__close,
            "exit": self.__close,
        }
        self.book = book if book is not None else AddressBook()

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
                match = suggest_command(command, self.commands)
                handler = self.commands.get(match) if match is not None else None
                if handler is None:
                    print("Unknown command")
                    continue
                message = handler(args)
                if message:
                    print(message)
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
    def __hello(self, _):
        print("How can I help you?")

    def __form_record_from_args(self, args) -> Record:
        name, phone, *rest = args
        birthday = rest[0] if rest else None
        new_record = Record(name)
        if phone:
            new_record.add_phone(phone)
        if birthday:
            new_record.add_birthday(birthday)
        return new_record

    @input_error
    def __add_contact(self, args) -> str | None:
        name = args[0]

        try:
            if name in self.book.data:
                raise ContactExist
        except NoContactError:
            pass

        new_record = self.__form_record_from_args(args)
        self.book.add_record(new_record)

        return f"Contact {Fore.BLUE}{name}{Fore.RESET} added."

    @input_error
    def __add_contact_phone(self, args) -> str | None:
        name, phone = args

        if name not in self.book.data:
            raise ContactNotExist

        record = self.book.find(name)
        if record.find_phone(phone):
            return "Phone already exists"

        self.book.add_record_phone(name, phone)

        return f"Phone {Fore.GREEN}{phone}{Fore.RESET} added to contact {Fore.BLUE}{name}{Fore.RESET}."

    @input_error
    def __change_contact(self, args) -> str | None:
        name, phone, *rest = args
        birthday = rest[0] if rest else None

        if name not in self.book.data:
            raise ContactNotExist

        self.book.change_record(name, phone, birthday)

        return f"Contact {Fore.BLUE}{name}{Fore.RESET} updated."

    @input_error
    def __delete_contact(self, args) -> str:
        name = args[0]
        self.book.delete(name)

        return f"Contact {Fore.RED}{name}{Fore.RESET} deleted."

    @input_error
    def __show_contact(self, args) -> str:
        name = args[0]
        record = self.book.find(name)

        return str(record)

    @input_error
    def __show_all_contacts(self, _) -> str:
        records = self.book.values()
        if not len(records):
            return "No contacts"

        showing_contacts = "\n".join([str(record) for record in records])

        return f"{"Phonebook:":-^100}\n{showing_contacts}"

    @input_error
    def __add_birthday(self, args) -> str:
        name, birthday, *_ = args
        record = self.book.find(name)
        record.add_birthday(birthday)

        return str(record)

    @input_error
    def __show_birthday(self, args) -> str:
        name = args[0]
        record = self.book.find(name)
        birthday = record.birthday if record else None

        return (
            f"{Fore.BLUE}{name}: {Fore.GREEN}{str(birthday)}{Fore.RESET}"
            if birthday
            else "No birthday found"
        )

    @input_error
    def __change_birthday(self, args) -> str:
        name, birthday, *_ = args
        record = self.book.find(name)
        record.change_birthday(birthday)

        return f"{Fore.BLUE}{name}: {Fore.GREEN}{str(birthday)}{Fore.RESET}"

    @input_error
    def __delete_birthday(self, args) -> str:
        name = args[0]
        record = self.book.find(name)
        record.del_birthday()

        return f"{Fore.BLUE}{name}: {Fore.GREEN}{"Birthday deleted"}{Fore.RESET}"

    @input_error
    def __show_birthdays(self, _) -> str:
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
    def __show_commands(self, _) -> None:
        print(f"All commands: {', '.join(self.commands)}")

    @input_error
    def __close(self, _) -> None:
        print("Good bye!")
        raise BreakError
