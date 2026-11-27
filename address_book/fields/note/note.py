from address_book.fields.field import Field
from address_book.fields.note.tag import Tag


class Note(Field):
    def __init__(self, text: str):
        super().__init__(text.strip())
        self.tags = []

    def add_tag(self, value: str) -> None:
        tag = Tag(value)
        self.tags.append(tag)

    def find_tag(self, value: str) -> Tag | None:
        normalized_value = value.strip().lower()

        for tag in self.tags:
            if tag.value == normalized_value:
                return tag
        
        return None

    def delete_tag(self, value: str) -> None:
        tag = self.find_tag(value)

        if tag is None:
            raise ValueError("Tag not found")

        self.tags.remove(tag)
