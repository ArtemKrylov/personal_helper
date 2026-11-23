from datetime import datetime

from address_book.constants import DATE_FORMAT
from address_book.exceptions import DateInputError
from address_book.fields.field import Field


class Birthday(Field):
    def __init__(self, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(parsed_date.date())
        except ValueError:
            raise DateInputError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime(DATE_FORMAT)
