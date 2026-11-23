from colorama import Fore

from address_book.fields.birthday import Birthday
from address_book.exceptions import error_handler
from address_book.fields.name import Name
from address_book.fields.phone import Phone


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        phones = self.get_phones()
        birthday = str(self.birthday) if self.birthday is not None else "no data"

        return f"{Fore.BLUE}{str(self.name)}:{' '*7}{Fore.GREEN}Phones: {phones}{' '*3}Birthday: {birthday}{Fore.RESET}"

    def get_phones(self) -> str:
        return ", ".join([str(phone) for phone in self.phones])

    @error_handler
    def add_phone(self, phone: str) -> None:

        (
            self.phones.append(Phone(phone))
            if not self.find_phone(phone)
            else print("Phone already exists")
        )

    def remove_phone(self, phone: str) -> None:
        self.phones = [
            filtered_phone
            for filtered_phone in self.phones
            if filtered_phone.value != phone
        ]

    @error_handler
    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        self.phones = [
            Phone(new_phone) if phone.value == old_phone else phone
            for phone in self.phones
        ]

    def find_phone(self, phone: str) -> Phone | None:
        return next((item for item in self.phones if item.value == phone), None)

    @error_handler
    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    @error_handler
    def change_birthday(self, birthday: Birthday) -> None:
        self.birthday = Birthday(birthday)

    @error_handler
    def del_birthday(
        self,
    ) -> None:
        self.birthday = None
