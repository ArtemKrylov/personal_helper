import pickle
import sys
from pathlib import Path
import colorama


from address_book import AddressBook
from phone_bot import PhoneBot
from run_with_theme import run_with_theme

if getattr(sys, "frozen", False):
    # The executable is built into the project's dist directory.
    PROJECT_DIR = Path(sys.executable).resolve().parent.parent
else:
    PROJECT_DIR = Path(__file__).resolve().parent

DATA_FILE = PROJECT_DIR / "storage" / "addressbook.pkl"


def main():
    def save_data(book):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with DATA_FILE.open("wb") as f:
            pickle.dump(book, f)

    def load_data():
        try:
            with DATA_FILE.open("rb") as f:
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
