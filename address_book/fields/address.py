from address_book.fields.field import Field
from address_book.exceptions import AddressInputError


class Address(Field):
    def __init__(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise AddressInputError("Address must be a non empty string")

        value = value.strip()

        if not any(char.isalpha() for char in value):
            raise AddressInputError("Address must contain letters")

        super().__init__(value)