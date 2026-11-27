from functools import wraps
from typing import Callable
from phone_bot.command_help import COMMAND_HELP

from colorama import Fore
from tabulate import tabulate

from address_book.address_book import AddressBook
from address_book.exceptions import (
    DateInputError,
    EmailInputError,
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
            AddressInputError,
            EmailInputError,
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
        self.commands = {
            "hello": self.__hello,
            "help": self.__show_commands,
            "close": self.__close,
            "exit": self.__close,
            # contact
            "add": self.__add_contact,
            "show": self.__show_contact,
            "change": self.__change_contact,
            "del": self.__delete_contact,
            "all": self.__show_all_contacts,
            # phones
            "add-phone": self.__add_contact_phone,
            "change-phone": self.__change_contact_phone,
            "delete-phone": self.__delete_contact_phone,
            "phones": self.__show_contact_phones,
            # notes
            "add-note": self.__add_note,
            "edit-note": self.__edit_note,
            "del-note": self.__delete_note,
            "search-notes": self.__search_notes,
            # tags
            "add-tag": self.__add_tag,
            "search-tags": self.__search_tags,
            "del-tag": self.__delete_tag,
            "sort-tags": self.__sort_tags,
            # birthday
            "add-birthday": self.__add_birthday,
            "show-birthday": self.__show_birthday,
            "change-birthday": self.__change_birthday,
            "delete-birthday": self.__delete_birthday,
            "birthdays": self.__show_birthdays,
            # address
            "add-address": self.__add_address,
            "show-address": self.__show_address,
            "change-address": self.__change_address,
            "delete-address": self.__delete_address,
            "show-all-addresses": self.__show_all_addresses,
            # email
            "add-email": self.__add_email,
            "change-email": self.__change_email,
            "show-email": self.__show_email,
            "delete-email": self.__delete_email,
        }
        self.book = book if book is not None else AddressBook()

    def start_bot(self):
        print(
            f"\n{' Welcome to the assistant bot! ':*^100}\n"
            f"Type {Fore.GREEN}help{Fore.RESET} to see all available commands.\n"
            f"Type {Fore.GREEN}exit{Fore.RESET} to close the application.\n"
        )
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

    # Contact
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

        print(f"Contact {Fore.BLUE}{name}{Fore.RESET} added.")
        return self.__form_table([new_record])

    @input_error
    def __change_contact(self, args) -> str | None:
        name, phone, *rest = args
        birthday = rest[0] if rest else None

        if name not in self.book.data:
            raise ContactNotExist

        self.book.change_record(name, phone, birthday)
        record = self.book.find(name)

        print(f"Contact {Fore.BLUE}{name}{Fore.RESET} updated.")
        return self.__form_table([record])

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

    # Phones
    @input_error
    def __add_contact_phone(self, args) -> str | None:
        name, phone = args

        if name not in self.book.data:
            raise ContactNotExist

        record = self.book.find(name)
        if record.find_phone(phone):
            return "Phone already exists"

        self.book.add_record_phone(name, phone)

        print(
            f"Phone {Fore.GREEN}{phone}{Fore.RESET} added to contact {Fore.BLUE}{name}{Fore.RESET}."
        )
        return self.__form_table([record])

    def __show_contact_phones(self, args) -> str:
        name = args[0]
        record = self.book.find(name)

        return record.get_phones()

    @input_error
    def __change_contact_phone(self, args) -> str | None:
        name, old_phone, new_phone = args

        if name not in self.book.data:
            raise ContactNotExist

        record = self.book.find(name)
        if record.find_phone(new_phone):
            return f"Phone {new_phone} already exists"

        record.edit_phone(old_phone, new_phone)

        print(f"Phone changed: {self.__show_contact_phones([name])}")
        return self.__form_table([record])

    @input_error
    def __delete_contact_phone(self, args) -> str:
        if len(args) < 2:
            return "Usage: delete-phone <name> <phone>"
        name, phone = args
        record = self.book.find(name)
        record.remove_phone(phone)

        return f"{Fore.BLUE}{name}: {Fore.RED}{"Phone deleted"}{Fore.RESET}"

    # Birthday
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
            else:
                return "Birthday not changed"

        print(f"Birthday added: {self.__show_birthday([name])}")
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

        print(f"Birthday changed: {self.__show_birthday([name])}")
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
                for congrat in self.book.get_upcoming_birthdays(
                    days=days, is_workday_congrats=False
                )
            ]
        )

        if not upcoming:
            return f"No upcoming birthdays in the next {days} days."

        return f"{Fore.BLUE}Upcoming birthdays: {Fore.GREEN}{upcoming}{Fore.RESET}"

    # Note
    @input_error
    def __add_note(self, args) -> str:
        name, *note_parts = args

        if not note_parts:
            return "Enter contact name and note text."

        record = self.book.find(name)
        text = " ".join(note_parts)
        record.add_note(text)

        return f"Note added to {Fore.BLUE}{name}{Fore.RESET}."

    @input_error
    def __search_notes(self, args) -> str:
        query = " ".join(args)

        if not query:
            return "Enter text to search."

        notes = self.book.search_notes(query)

        if not notes:
            return "No notes found."

        result = []

        for item in notes:
            result.append(f"{item['name']}: {item['note']}")

        return "\n".join(result)

    @input_error
    def __edit_note(self, args) -> str:
        if "|" not in args:
            return "Use: edit-note <name> <old note> | <new note>."

        name = args[0]
        note_parts = args[1:]
        separator_index = note_parts.index("|")

        old_parts = note_parts[:separator_index]
        new_parts = note_parts[separator_index + 1 :]

        if not old_parts or not new_parts:
            return "Enter old and new note text."

        record = self.book.find(name)

        old_text = " ".join(old_parts)
        new_text = " ".join(new_parts)

        record.edit_note(old_text, new_text)

        return f"Note updated for {Fore.BLUE}{name}{Fore.RESET}."

    @input_error
    def __delete_note(self, args) -> str:
        if len(args) < 2:
            return "Enter contact name and note text."

        name = args[0]
        text = " ".join(args[1:])

        record = self.book.find(name)
        record.delete_note(text)

        return f"Note deleted from {Fore.BLUE}{name}{Fore.RESET}."

    # Tag
    @input_error
    def __add_tag(self, args) -> str:
        if "|" not in args:
            return "Use: add-tag <name> <note text> | <tag>."

        name = args[0]
        parts = args[1:]
        separator_index = parts.index("|")

        note_parts = parts[:separator_index]
        tag_parts = parts[separator_index + 1 :]

        if not note_parts or not tag_parts:
            return "Enter note text and tag."

        record = self.book.find(name)

        note_text = " ".join(note_parts)
        tag_value = " ".join(tag_parts)

        note = record.find_note(note_text)

        if note is None:
            return "Note not found."

        note.add_tag(tag_value)

        return f"Tag added to note for {Fore.BLUE}{name}{Fore.RESET}."

    @input_error
    def __delete_tag(self, args) -> str:
        if "|" not in args:
            return "Use: delete-tag <name> <note text> | <tag>."

        name = args[0]
        parts = args[1:]
        separator_index = parts.index("|")

        note_parts = parts[:separator_index]
        tag_parts = parts[separator_index + 1 :]

        if not note_parts or not tag_parts:
            return "Enter note text and tag."

        record = self.book.find(name)

        note_text = " ".join(note_parts)
        tag_value = " ".join(tag_parts)

        note = record.find_note(note_text)

        if note is None:
            return "Note not found."

        if note.find_tag(tag_value) is None:
            return "Tag not found."

        note.delete_tag(tag_value)

        return f"Tag deleted from note for {Fore.BLUE}{name}{Fore.RESET}."

    @input_error
    def __search_tags(self, args) -> str:
        tag_value = " ".join(args).strip()

        if not tag_value:
            return "Enter tag to search."

        notes = self.book.search_notes_by_tag(tag_value)

        if not notes:
            return "No notes found for this tag."

        result = []

        for item in notes:
            result.append(f"{item['name']}: {item['note']} " f"[{item['tag']}]")

        return "\n".join(result)

    @input_error
    def __sort_tags(self, args) -> str:
        notes = self.book.sort_notes_by_tag()

        if not notes:
            return "No tagged notes found."

        result = []

        for item in notes:
            result.append(f"{item['name']}: {item['note']}" f"[{item['tag']}]")

        return "\n".join(result)

    # Email
    @input_error
    def __add_email(self, args) -> str:
        if len(args) < 2:
            return "Usage: add-email <name> <email>"

        name, email, *_ = args
        record = self.book.find(name)
        if not record.email:
            record.add_email(email)
            print(f"Email added: {self.__show_email([name])}")
        else:
            if (
                input(
                    f"{Fore.GREEN}{name}{Fore.RESET} has email record. Change it? y/n "
                ).lower()
                == "y"
            ):
                record.change_email(email)
                print(f"Email changed: {self.__show_email([name])}")
            else:
                return "Email not changed."

        return self.__form_table([record])

    @input_error
    def __change_email(self, args) -> str:
        if len(args) < 2:
            return "Usage: change-email <name> <email>"

        name, email, *_ = args
        record = self.book.find(name)
        record.change_email(email)

        print(f"Email changed: {self.__show_email([name])}")
        return self.__form_table([record])

    @input_error
    def __show_email(self, args) -> str:
        if len(args) < 1:
            return "Usage: show-email <name>"

        name = args[0]
        record = self.book.find(name)
        email = record.email if record else None

        return (
            f"{Fore.BLUE}{name}: {Fore.GREEN}{str(email)}{Fore.RESET}"
            if email
            else "No email found"
        )

    @input_error
    def __delete_email(self, args) -> str:
        if len(args) < 1:
            return "Usage: delete-email <name>"

        name = args[0]
        record = self.book.find(name)
        record.del_email()

        return f"{Fore.BLUE}{name}: {Fore.RED}{"Email deleted"}{Fore.RESET}"

    # Address
    @input_error
    def __add_address(self, args) -> str:
        if len(args) < 2:
            return "Usage: add-address <name> <address>"

        name, *address_parts = args
        address = " ".join(address_parts)

        record = self.book.find(name)
        if not record.address:
            record.add_address(address)
            print(f"Address added: {self.__show_address([name])}")
        else:
            if (
                input(
                    f"{Fore.GREEN}{name}{Fore.RESET} has address record. Change it? y/n "
                )
                .strip()
                .lower()
                == "y"
            ):
                record.change_address(address)
                print("Address was successfully updated")
            else:
                return "Address was not updated"

        return self.__form_table([record])

    @input_error
    def __show_address(self, args) -> str:
        name = args[0]  # Index Error if empty args
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
        print(f"Address changed: {self.__show_address([name])}")
        return self.__form_table([record])

    @input_error
    def __delete_address(self, args):
        name = args[0]  # Index Error if empty args
        record = self.book.find(name)
        record.del_address()
        return f"{Fore.BLUE}{name}: " f"{Fore.GREEN}Address deleted{Fore.RESET}"

    @input_error
    def __show_all_addresses(self, _) -> str:
        # shows only records with addresses
        addresses = [
            [colorize(str(record.name), Color.BLUE), colorize(str(record.address))]
            for record in self.book.values()
            if record.address
        ]

        if not addresses:
            return "No addresses found"

        return tabulate(
            addresses,
            headers=[
                colorize(header, Color.MAGENTA) for header in ["№", "Name", "Address"]
            ],
            tablefmt="fancy_grid",
            showindex=[
                colorize(str(i), Color.MAGENTA) for i in range(1, len(addresses) + 1)
            ],
            maxcolwidths=35,
            disable_numparse=True,
        )


    @input_error
    
    def __show_commands(self, args) -> str:
        if args:
            command = args[0].lower()
    
            if command not in COMMAND_HELP:
                return f"Unknown command: {command}"
    
            usage, example, description = COMMAND_HELP[command]
    
            if len(args) == 2 and args[1].lower() == "desc":
                return f"{Fore.MAGENTA}Description:{Fore.RESET} {description}"
    
            if len(args) > 1:
                return "Usage: help [command] [desc]"
    
            return (
                f"Usage: {usage}\n"
                f"Example: {example}"
            )
    
        rows = [
            [colorize(command, Color.GREEN), usage, example]
            for command, (usage, example, _) in COMMAND_HELP.items()
        ]
    
        return tabulate(
            rows,
            headers=["Command", "Usage", "Example"],
            tablefmt="fancy_grid",
            disable_numparse=True,
        )
    

    @input_error
    def __close(self, _) -> None:
        print("Goodbye!")
        raise BreakError
