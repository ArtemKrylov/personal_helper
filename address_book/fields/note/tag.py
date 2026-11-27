from address_book.fields.field import Field


class Tag(Field):
    def __init__(self, value: str):
        super().__init__(value.strip().lower())
