from collections import UserDict
from datetime import datetime, timedelta


from address_book.fields.birthday import Birthday
from address_book.constants import DATE_FORMAT, DAYS_IN_WEEK, WEEKEND_DAYS
from address_book.exceptions import (
    NoContactError,
    error_handler,
)

from address_book.fields.phone import Phone
from address_book.record import Record


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

    def search_notes(self, query: str) -> list[dict]:
        search_text = query.strip().lower()

        if not search_text:
            return[]

        results = []

        for record in self.values():
            for note in record.notes:
                if search_text in note.value.lower():
                    results.append(
                        {
                            "name": str(record.name),
                            "note": note.value,
                        }
                    )

        return results

    def sort_notes(self) -> list[dict]:
        notes = []

        for record in self.values():
            for note in record.notes:
                notes.append(
                    {
                        "name": str(record.name),
                        "note": note.value,
                    }
                )
        return sorted(
            notes,
            key=lambda item: item["note"].lower(),
        )

    def search_notes_by_tag(self, tag_value: str) -> list [dict]:
        normalized_tag = tag_value.strip().lower()
        results = []

        if not normalized_tag:
            return results

        for record in self.values():
            for note in record.notes:
                if note.find_tag(normalized_tag) is not None:
                    results.append(
                        {
                            "name": str(record.name),
                            "note": note.value,
                            "tag": normalized_tag,
                        }
                    )

        return results

    def sort_notes_by_tag(self) -> list[dict]:
        notes =[]

        for record in self.values():
            for note in record.notes:
                for tag in note.tags:
                    notes.append(
                    {
                            "name": str(record.name),
                            "note": note.value,
                            "tag": tag.value,
                        }
                    )
        
        return sorted(
            notes,
            key=lambda item: (
                item["tag"],
                item["note"].lower(),
            )
        )

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
