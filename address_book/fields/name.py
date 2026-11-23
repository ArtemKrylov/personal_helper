from address_book.exceptions import NameInputError
from address_book.fields.field import Field


class Name(Field):
    def __init__(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise NameInputError("Incorrect name")

        super().__init__(value)

    def __str__(self):
        return self.value
