from colorama import Fore

from address_book.fields.birthday import Birthday
from address_book.exceptions import PhoneInputError, error_handler
from address_book.fields.name import Name
from address_book.fields.phone import Phone
from address_book.fields.address import Address

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
        address = str(self.address) if self.address else "no data"
        name_column_lenght = 17

        name_column = str(self.name)[: name_column_lenght - 1] + ":"
        return f"{Fore.BLUE}{name_column:<{name_column_lenght}}{' '*7}{Fore.GREEN}Phones: {phones}{' '*3}Birthday: {birthday}{' ' * 3}Address: {address}{Fore.RESET}"

    @property
    def record_table_row(self):
        name = colorize(str(getattr(self, "name", None)), Color.BLUE)
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

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def change_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def del_birthday(
        self,
    ) -> None:
        self.birthday = None

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def change_address(self, address: str) -> None:
        self.address = Address(address)

    def del_address(self) -> None:
        self.address = None
