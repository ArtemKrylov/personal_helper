from functools import wraps
from typing import Callable

from colorama import Fore
from tabulate import tabulate

from address_book.address_book import AddressBook
from address_book.exceptions import (
    DateInputError,
    NameInputError,
    NoContactError,
    PhoneInputError,
    AddressInputError,
)
from address_book.record import Record
from phone_bot.exceptions import (
    BreakError,
    ContactExist,
    ContactNotExist,
    ContinueError,
)
from phone_bot.suggest_command import suggest_command
from utils.colorize import Color, colorize


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
        except (
            PhoneInputError,
            NoContactError,
            DateInputError,
            NameInputError,
        ) as e:
            return str(e)
        except (BreakError, ContinueError, ContactExist, ContactNotExist):
            raise
        except Exception as e:
            print(f"An error occurred: {e}")

    return inner


class PhoneBot:
    headers = ["№", "Name", "Phones", "Birthday", "Address", "Email", "Notes"]

    def __init__(self, book: AddressBook | None = None):
        # Add new command here (command name: executed function)
        self.commands = {
            "hello": self.__hello,
            "add": self.__add_contact,
            "add-phone-to-contact": self.__add_contact_phone,
            "change": self.__change_contact,
            "del": self.__delete_contact,
            "phones": self.__show_contact_phones,
            "show": self.__show_contact,
            "all": self.__show_all_contacts,
            "add-birthday": self.__add_birthday,
            "show-birthday": self.__show_birthday,
            "change-birthday": self.__change_birthday,
            "delete-birthday": self.__delete_birthday,
            "birthdays": self.__show_birthdays,
            "add-address": self.__add_address,
            "show-address": self.__show_address,
            "change-address": self.__change_address,
            "delete-address": self.__delete_address,
            "show-all-addresses": self.__show_all_addresses,
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

    @staticmethod
    def __form_table(records: list[Record]):
        table_contacts = [record.record_table_row for record in records]
        table = tabulate(
            table_contacts,
            headers=[colorize(header, Color.MAGENTA) for header in PhoneBot.headers],
            tablefmt="fancy_grid",
            showindex=[
                colorize(str(i), Color.MAGENTA)
                for i in range(1, len(table_contacts) + 1)
            ],
            maxcolwidths=15,
            disable_numparse=True,
        )
        return table

    def __show_contact_phones(self, args) -> str:
        name = args[0]
        record = self.book.find(name)

        return record.get_phones()

    @input_error
    def __show_contact(self, args) -> str:
        name = args[0]
        record = self.book.find(name)

        return self.__form_table([record])

    def __show_all_contacts(self, _) -> str:
        records = self.book.values()
        if not len(records):
            return "No contacts"

        return self.__form_table(records)

    @input_error
    def __add_birthday(self, args) -> str:
        if len(args) < 2:
            return "Usage: add-birthday <name> <birthday>"

        name, birthday, *_ = args
        record = self.book.find(name)
        if not record.birthday:
            record.add_birthday(birthday)

        else:
            if (
                input(
                    f"{Fore.GREEN}{name}{Fore.RESET} has birthday record. Change it? y/n "
                ).lower()
                == "y"
            ):
                record.change_birthday(birthday)

        return self.__form_table([record])

    @input_error
    def __show_birthday(self, args) -> str:
        if len(args) < 1:
            return "Usage: show-birthday <name>"
        name = args[0]
        record = self.book.find(name)
        birthday = record.birthday if record else None

        return (
            f"{Fore.BLUE}{name}: {Fore.GREEN}{birthday}{Fore.RESET}"
            if birthday
            else "No birthday found"
        )

    @input_error
    def __change_birthday(self, args) -> str:
        if len(args) < 2:
            return "Usage: change-birthday <name> <birthday>"
        name, birthday, *_ = args
        record = self.book.find(name)
        record.change_birthday(birthday)

        return self.__form_table([record])

    @input_error
    def __delete_birthday(self, args) -> str:
        if len(args) < 1:
            return "Usage: show-birthday <name>"
        name = args[0]
        record = self.book.find(name)
        record.del_birthday()

        return f"{Fore.BLUE}{name}: {Fore.RED}{"Birthday deleted"}{Fore.RESET}"

    @input_error
    def __show_birthdays(self, args) -> str:
        if len(args) > 1:
            return "Usage: birthdays [number of days]"
        
        try:
            days = int(args[0]) if args else 7
        except ValueError:
            return "Please enter a valid number of days."
        
        if days <= 0:
            return "Number of days must be greater than zero."

        upcoming = "; ".join(
            [
                f"{congrat["name"]} : {congrat["congratulation_date"]}"
                for congrat in self.book.get_upcoming_birthdays(days = days, is_workday_congrats=False)
            ]
        )

        if not upcoming:
            return f"No upcoming birthdays in the next {days} days."

        return f"{Fore.BLUE}Upcoming birthdays: {Fore.GREEN}{upcoming}{Fore.RESET}"

    @input_error
    def __add_address(self, args) -> str:
        if len(args) < 2:
            return "Usage: add-address <name> <address>"

        name, *address_parts = args
        address = " ".join(address_parts)

        record = self.book.find(name)
        record.add_address(address)
        # to show an updated record in a table format
        return self.__form_table([record])

    @input_error
    def __show_address(self, args) -> str:
        name = args[0] # Index Error if empty args
        record = self.book.find(name)
        address = record.address if record else None

        return (
            f"{Fore.BLUE}{name}: {Fore.GREEN}{address}{Fore.RESET}"
            if address
            else "No address found"
        )

    @input_error
    def __change_address(self, args) -> str:
        if len(args) < 2:
            return "Usage: change-address <name> <new-address>"

        name, *address_parts = args
        address = " ".join(address_parts)
        record = self.book.find(name)
        record.change_address(address)
        # to show an updated record in a table format
        return self.__form_table([record])

    @input_error
    def __delete_address(self, args):
        name = args[0] # Index Error if empty args
        record = self.book.find(name)
        record.del_address()
        return (
            f"{Fore.BLUE}{name}: "
            f"{Fore.GREEN}Address deleted{Fore.RESET}"
        )

    @input_error
    def __show_all_addresses(self,_) -> str:
        # shows only records with addresses
        records = [
            record for record in self.book.values()
            if getattr(record, "address", None)
        ]

        if not records:
            return "No addresses found"

        return self.__form_table(records)
    
    @input_error
    def __show_commands(self, _) -> None:
        print(f"All commands: {', '.join(self.commands)}")

    @input_error
    def __close(self, _) -> None:
        print("Goodbye!")
        raise BreakError
