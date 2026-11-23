from address_book.exceptions import PhoneInputError
from address_book.fields.field import Field


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
