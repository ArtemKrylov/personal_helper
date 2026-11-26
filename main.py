import pickle
from pathlib import Path
import colorama


from address_book import AddressBook
from phone_bot import PhoneBot
from run_with_theme import run_with_theme


def main():
    def save_data(book, file_path="storage/addressbook.pkl"):
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as f:
            pickle.dump(book, f)

    def load_data(file_path="storage/addressbook.pkl"):
        path = Path(file_path)
        try:
            with path.open("rb") as f:
                book = pickle.load(f)
            if not isinstance(book, AddressBook):
                raise pickle.UnpicklingError("Expected a saved address book")
            return book
        except FileNotFoundError:
            return AddressBook()
        except (
            EOFError,
            pickle.UnpicklingError,
            ValueError,
            AttributeError,
            ImportError,
            IndexError,
        ):
            print("Could not load the address book.")
            return AddressBook()

    book = load_data()
    phone_bot = PhoneBot(book)

    try:
        phone_bot.start_bot()
    finally:
        save_data(book)


if __name__ == "__main__":
    colorama.init(autoreset=True)
    # run_with_theme(main)
    try:
        main()
    except Exception as e:
        print(str(e))
