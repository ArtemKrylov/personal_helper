import re

from address_book.exceptions import EmailInputError
from address_book.fields.field import Field

EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"


class Email(Field):
    def __init__(self, value: str):
        if not value or not isinstance(value, str) or not re.fullmatch(EMAIL_PATTERN, value):
            raise EmailInputError("Invalid email. Example: name@example.com")

        super().__init__(value)