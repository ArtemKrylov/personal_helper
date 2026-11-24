from colorama import Fore

from address_book.fields.birthday import Birthday
from address_book.exceptions import PhoneInputError, error_handler
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
        name_column_lenght = 17

        name_column = str(self.name)[: name_column_lenght - 1] + ":"
        return f"{Fore.BLUE}{name_column:<{name_column_lenght}}{' '*7}{Fore.GREEN}Phones: {phones}{' '*3}Birthday: {birthday}{Fore.RESET}"

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
