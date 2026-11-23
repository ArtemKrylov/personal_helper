from collections import UserDict
from datetime import datetime, timedelta
from functools import wraps

from colorama import Fore

DATE_FORMAT = "%d.%m.%Y"
WEEKEND_DAYS = (5, 6)
DAYS_IN_WEEK = 7


def error_handler(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PhoneInputError as e:
            raise PhoneInputError(str(e))
        except NoContactError as e:
            raise NoContactError(str(e))
        except DateInputError as e:
            raise DateInputError(str(e))
        except Exception as e:
            print(f"An error occurred: {e}")

    return inner


class NoContactError(Exception):
    pass


class NameInputError(Exception):
    pass


class PhoneInputError(Exception):
    pass


class DateInputError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise NameInputError("Incorrect name")

        super().__init__(value)

    def __str__(self):
        return self.value


class Phone(Field):
    def __init__(self, value: str):
        if (
            not value
            or not isinstance(value, str)
            or len(value) != 10
            or not value.isascii()
            or not value.isdigit()
        ):
            raise PhoneInputError("Phone number must contain exactly 10 digits")

        super().__init__(value)

    def __str__(self):
        return self.value


class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(parsed_date.date())
        except ValueError:
            raise DateInputError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime(DATE_FORMAT)


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


class AddressBook(UserDict):

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def add_record_phone(self, name, phone: str) -> None:
        self.data[name].add_phone(phone)

    def change_record(self, name: str, phone: str, birthday: str | None) -> None:
        record = self.data[name]
        phone and Phone(phone)
        birthday and Birthday(birthday)

        if phone:
            record.phones = []
            record.add_phone(phone)
        if birthday:
            record.birthday = Birthday(birthday)

    @error_handler
    def find(self, name: str) -> Record | None:
        if name not in self.data:
            raise NoContactError(f"Contact with name {name} does not exist")
        return self.data[name]

    @error_handler
    def delete(self, name: str) -> None:
        if name not in self.data:
            raise NoContactError(f"Contact with name {name} does not exist")
        self.data.pop(name)

    def get_upcoming_birthdays(
        self,
        date_format: str = DATE_FORMAT,
        is_workday_congrats: bool = True,
    ) -> list:
        # gets users list with name and birhday properties and return list of upcoming birthday within next 7 day (including today); if is_workday_congrats param is true and birthday is on weekend day - moves congrat to nearest workday

        curr_date = datetime.today()
        congrats = []

        # for leap year error catching
        def birthday_in_year(birthday, year):
            try:
                return birthday.replace(year=year)
            except ValueError:
                return birthday.replace(year=year, day=28)

        for record in self.values():
            if not record.birthday:
                continue

            birthday_this_year = birthday_in_year(record.birthday.value, curr_date.year)
            # for congrat in new year
            if birthday_this_year.toordinal() < curr_date.toordinal():
                birthday_this_year = birthday_in_year(
                    record.birthday.value, curr_date.year + 1
                )
            day_of_birth_this_year = birthday_this_year.weekday()

            delta_days = birthday_this_year.toordinal() - curr_date.toordinal()
            if delta_days >= 7 or delta_days < 0:
                continue

            is_weekend = day_of_birth_this_year in WEEKEND_DAYS
            if is_weekend and is_workday_congrats:
                birthday_this_year += timedelta(
                    days=DAYS_IN_WEEK - day_of_birth_this_year
                )
                delta_days = birthday_this_year.toordinal() - curr_date.toordinal()

            congrats.append(
                {
                    "name": str(record.name),
                    "congratulation_date": datetime.strftime(
                        curr_date + timedelta(days=delta_days), date_format
                    ),
                }
            )
        return congrats
