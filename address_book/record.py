from colorama import Fore

from address_book.fields.birthday import Birthday
from address_book.exceptions import PhoneInputError, error_handler
from address_book.fields.name import Name
from address_book.fields.phone import Phone
from address_book.fields.note.note import Note

from utils.colorize import Color, colorize


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None
        self.notes = []

    def __str__(self):
        phones = self.get_phones()
        birthday = str(self.birthday) if self.birthday is not None else "no data"
        name_column_lenght = 17

        name_column = str(self.name)[: name_column_lenght - 1] + ":"
        return f"{Fore.BLUE}{name_column:<{name_column_lenght}}{' '*7}{Fore.GREEN}Phones: {phones}{' '*3}Birthday: {birthday}{Fore.RESET}"
    
    def add_note(self, text: str) -> None:
        self.notes.append(Note(text))

    def find_note(self, text: str) -> Note | None:
        for note in self.notes:
            if note.value == text:
                return note

        return None

    def edit_note(self, old_text: str, new_text: str) -> None:
        note = self.find_note(old_text)

        if note is None:
            raise ValueError("Note not found")

        note.value = new_text.strip()
    
    def delete_note(self, text: str) -> None:
        note = self.find_note(text)

        if note is None:
            raise ValueError("Note not found")

        self.notes.remove(note)

    @property
    def record_table_row(self):
        name = colorize(str(getattr(self, "name", None)), Color.GREEN)
        phones = ", ".join(
            [colorize(str(phone)) for phone in getattr(self, "phones", None) or []]
        )
        birthday = colorize(str(getattr(self, "birthday", None)))
        address = colorize(str(getattr(self, "address", None)))
        email = colorize(str(getattr(self, "email", None)))
        notes = ", ".join(
            [colorize(str(note)) for note in getattr(self, "notes", None) or []]
        )
        return [
            name,
            phones,
            birthday,
            address,
            email,
            notes,  
        ]

    def get_phones(self) -> str:
        return ", ".join([str(phone) for phone in self.phones])

    def add_phone(self, phone: str) -> None:

        (
            self.phones.append(Phone(phone))
            if not self.find_phone(phone)
            else print("Phone already exists")
        )

    def remove_phone(self, phone: str) -> None:
        found_phone = self.find_phone(phone)
        if found_phone is None:
            raise PhoneInputError(f"Phone number {phone} does not exist")
        self.phones.remove(found_phone)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        found_phone = self.find_phone(old_phone)
        if found_phone is None:
            raise PhoneInputError(f"Phone number {old_phone} does not exist")
        if old_phone == new_phone:
            return
        if self.find_phone(new_phone) is not None:
            raise PhoneInputError("Phone already exists")
        self.phones[self.phones.index(found_phone)] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        return next((item for item in self.phones if item.value == phone), None)

    @error_handler
    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    @error_handler
    def change_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    @error_handler
    def del_birthday(
        self,
    ) -> None:
        self.birthday = None
